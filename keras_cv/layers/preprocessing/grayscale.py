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

import tensorflow as tf

from keras_cv.layers.preprocessing.base_image_augmentation_layer import (
    BaseImageAugmentationLayer,
)


@tf.keras.utils.register_keras_serializable(package="keras_cv")
class Grayscale(BaseImageAugmentationLayer):
    """Grayscale is a preprocessing layer that transforms RGB images to Grayscale images.
    Input images should have values in the range of [0, 255].

    Input shape:
        3D (unbatched) or 4D (batched) tensor with shape:
        `(..., height, width, channels)`, in `"channels_last"` format
    Output shape:
        3D (unbatched) or 4D (batched) tensor with shape:
        `(..., height, width, channels)`, in `"channels_last"` format
    Args:
        output_channels.
            Number color channels present in the output image.
            The output_channels can be 1 or 3. RGB image with shape
            (..., height, width, 3) will have the following shapes
            after the `Grayscale` operation:
                 a. (..., height, width, 1) if output_channels = 1
                 b. (..., height, width, 3) if output_channels = 3.

    Usage:
    ```python
    (images, labels), _ = tf.keras.datasets.cifar10.load_data()
    to_grayscale = keras_cv.layers.preprocessing.Grayscale()
    augmented_images = to_grayscale(images)
    ```
    """

    def __init__(self, output_channels=1, **kwargs):
        super().__init__(**kwargs)
        self.output_channels = output_channels
        # This layer may raise an error when running on GPU using auto_vectorize
        self.auto_vectorize = False

    def _check_input_params(self, output_channels):
        if output_channels not in [1, 3]:
            raise ValueError(
                "Received invalid argument output_channels. "
                f"output_channels must be in 1 or 3. Got {output_channels}"
            )
        self.output_channels = output_channels

    def augment_image(self, image, transformation=None, **kwargs):
        grayscale = tf.image.rgb_to_grayscale(image)
        if self.output_channels == 1:
            return grayscale
        elif self.output_channels == 3:
            return tf.image.grayscale_to_rgb(grayscale)
        else:
            raise ValueError("Unsupported value for `output_channels`.")

    def augment_bounding_boxes(self, bounding_boxes, **kwargs):
        return bounding_boxes

    def augment_label(self, label, transformation=None, **kwargs):
        return label

    def augment_segmentation_mask(self, segmentation_mask, transformation, **kwargs):
        return segmentation_mask

    def get_config(self):
        config = {
            "output_channels": self.output_channels,
        }
        base_config = super().get_config()
        return dict(list(base_config.items()) + list(config.items()))
