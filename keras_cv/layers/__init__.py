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

from tensorflow.keras.layers import CenterCrop
from tensorflow.keras.layers import RandomBrightness
from tensorflow.keras.layers import RandomContrast
from tensorflow.keras.layers import RandomCrop
from tensorflow.keras.layers import RandomHeight
from tensorflow.keras.layers import RandomRotation
from tensorflow.keras.layers import RandomTranslation
from tensorflow.keras.layers import RandomWidth
from tensorflow.keras.layers import RandomZoom
from tensorflow.keras.layers import Rescaling
from tensorflow.keras.layers import Resizing

from keras_cv.layers.feature_pyramid import FeaturePyramid
from keras_cv.layers.object_detection.anchor_generator import AnchorGenerator
from keras_cv.layers.object_detection.nms_prediction_decoder import NmsPredictionDecoder
from keras_cv.layers.object_detection.non_max_suppression import NonMaxSuppression
from keras_cv.layers.object_detection.retina_net_label_encoder import (
    RetinaNetLabelEncoder,
)
from keras_cv.layers.preprocessing.aug_mix import AugMix
from keras_cv.layers.preprocessing.augmenter import Augmenter
from keras_cv.layers.preprocessing.auto_contrast import AutoContrast
from keras_cv.layers.preprocessing.base_image_augmentation_layer import (
    BaseImageAugmentationLayer,
)
from keras_cv.layers.preprocessing.channel_shuffle import ChannelShuffle
from keras_cv.layers.preprocessing.cut_mix import CutMix
from keras_cv.layers.preprocessing.equalization import Equalization
from keras_cv.layers.preprocessing.fourier_mix import FourierMix
from keras_cv.layers.preprocessing.grayscale import Grayscale
from keras_cv.layers.preprocessing.grid_mask import GridMask
from keras_cv.layers.preprocessing.maybe_apply import MaybeApply
from keras_cv.layers.preprocessing.mix_up import MixUp
from keras_cv.layers.preprocessing.mosaic import Mosaic
from keras_cv.layers.preprocessing.posterization import Posterization
from keras_cv.layers.preprocessing.rand_augment import RandAugment
from keras_cv.layers.preprocessing.random_augmentation_pipeline import (
    RandomAugmentationPipeline,
)
from keras_cv.layers.preprocessing.random_channel_shift import RandomChannelShift
from keras_cv.layers.preprocessing.random_choice import RandomChoice
from keras_cv.layers.preprocessing.random_color_degeneration import (
    RandomColorDegeneration,
)
from keras_cv.layers.preprocessing.random_color_jitter import RandomColorJitter
from keras_cv.layers.preprocessing.random_crop_and_resize import RandomCropAndResize
from keras_cv.layers.preprocessing.random_cutout import RandomCutout
from keras_cv.layers.preprocessing.random_flip import RandomFlip
from keras_cv.layers.preprocessing.random_gaussian_blur import RandomGaussianBlur
from keras_cv.layers.preprocessing.random_hue import RandomHue
from keras_cv.layers.preprocessing.random_jpeg_quality import RandomJpegQuality
from keras_cv.layers.preprocessing.random_saturation import RandomSaturation
from keras_cv.layers.preprocessing.random_sharpness import RandomSharpness
from keras_cv.layers.preprocessing.random_shear import RandomShear
from keras_cv.layers.preprocessing.randomly_zoomed_crop import RandomlyZoomedCrop
from keras_cv.layers.preprocessing.solarization import Solarization
from keras_cv.layers.regularization.drop_path import DropPath
from keras_cv.layers.regularization.dropblock_2d import DropBlock2D
from keras_cv.layers.regularization.squeeze_excite import SqueezeAndExcite2D
from keras_cv.layers.regularization.stochastic_depth import StochasticDepth
from keras_cv.layers.spatial_pyramid import SpatialPyramidPooling
