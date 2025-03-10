# Copyright 2022 The KerasCV Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import pytest
import tensorflow as tf
import tensorflow_datasets as tfds

from keras_cv import layers
from keras_cv import models
from keras_cv.models import segmentation


class DeeplabTest(tf.test.TestCase):
    def test_deeplab_model_construction_with_preconfigured_setting(self):
        model = segmentation.DeepLabV3(classes=11, include_rescaling=True)
        input_image = tf.random.uniform(shape=[2, 256, 256, 3])
        output = model(input_image, training=True)

        self.assertEquals(output.shape, [2, 256, 256, 11])

    def test_deeplab_model_with_components(self):
        backbone = models.ResNet50V2(
            include_rescaling=True, include_top=False
        ).as_backbone(min_level=3, max_level=4)
        fpn = layers.FeaturePyramid(min_level=3, max_level=4)
        model = segmentation.DeepLabV3(
            classes=11, include_rescaling=True, backbone=backbone, decoder=fpn
        )

        input_image = tf.random.uniform(shape=[2, 256, 256, 3])
        output = model(input_image, training=True)

        self.assertEquals(output.shape, [2, 256, 256, 11])

    def test_mixed_precision(self):
        tf.keras.mixed_precision.set_global_policy("mixed_float16")
        model = segmentation.DeepLabV3(classes=11, include_rescaling=True)
        input_image = tf.random.uniform(shape=[2, 256, 256, 3])
        output = model(input_image, training=True)

        self.assertEquals(output.dtype, tf.float32)

    def test_invalid_backbone_model(self):
        with self.assertRaisesRegex(
            ValueError, "Supported premade backbones are: .*resnet50_v2"
        ):
            segmentation.DeepLabV3(
                classes=11, include_rescaling=True, backbone="resnet_v3"
            )
        with self.assertRaisesRegex(
            ValueError, "Backbone need to be a `tf.keras.layers.Layer`"
        ):
            segmentation.DeepLabV3(
                classes=11, include_rescaling=True, backbone=tf.Module()
            )

    def test_invalid_decoder(self):
        with self.assertRaisesRegex(ValueError, "Supported premade decoder are: .*fpn"):
            segmentation.DeepLabV3(classes=11, include_rescaling=True, decoder="aspp")

    @pytest.mark.skipif(
        "INTEGRATION" not in os.environ or os.environ["INTEGRATION"] != "true",
        reason="Takes a long time to run, only runs when INTEGRATION "
        "environment variable is set.  To run the test please run: \n"
        "`INTEGRATION=true pytest keras_cv/",
    )
    def test_model_train(self):
        model = segmentation.DeepLabV3(classes=1, include_rescaling=True)

        gcs_data_pattern = "gs://caltech_birds2011_mask/0.1.1/*.tfrecord*"
        features = tfds.features.FeaturesDict(
            {
                "bbox": tfds.features.BBoxFeature(),
                "image": tfds.features.Image(shape=(None, None, 3), dtype=tf.uint8),
                "image/filename": tfds.features.Text(),
                "label": tfds.features.ClassLabel(num_classes=200),
                "label_name": tfds.features.Text(),
                "segmentation_mask": tfds.features.Image(
                    shape=(None, None, 1), dtype=tf.uint8
                ),
            }
        )

        filenames = tf.io.gfile.glob(gcs_data_pattern)
        AUTO = tf.data.AUTOTUNE
        ignore_order = tf.data.Options()
        ignore_order.experimental_deterministic = False
        ds = tf.data.TFRecordDataset(filenames, num_parallel_reads=AUTO)
        ds = ds.with_options(ignore_order)
        ds = ds.map(features.deserialize_example, num_parallel_calls=AUTO)

        target_size = [384, 384]
        output_res = [96, 96]
        num_images = 11788

        image_resizing = tf.keras.layers.Resizing(target_size[1], target_size[0])
        labels_resizing = tf.keras.layers.Resizing(output_res[1], output_res[0])

        def resize_images_and_masks(data):
            image = tf.image.convert_image_dtype(data["image"], dtype=tf.float32)
            data["image"] = image_resizing(image)
            # WARNING: assumes processing unbatched
            mask = data["segmentation_mask"]
            mask = tf.image.convert_image_dtype(mask, dtype=tf.float32)
            data["segmentation_mask"] = labels_resizing(mask)
            return data

        def keep_image_and_mask_only(data):
            return data["image"], data["segmentation_mask"]

        dataset = ds
        dataset = dataset.map(resize_images_and_masks)
        dataset = dataset.map(keep_image_and_mask_only)

        batch_size = 32
        training_dataset = dataset.apply(
            tf.data.experimental.dense_to_ragged_batch(batch_size)
        )
        training_dataset = training_dataset.repeat()

        epochs = 1
        model.compile(
            optimizer="adam",
            loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
            metrics=["accuracy"],
        )

        model_history = model.fit(
            training_dataset, epochs=epochs, steps_per_epoch=num_images // batch_size
        )
        print(model_history)


if __name__ == "__main__":
    tf.test.main()
