#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math

from warg import NOD

from dlpipeline.augmentor.dlp_augmentor import DLPAugmentor

__author__ = 'cnheider'

import tensorflow as tf


class TFAugmentor(DLPAugmentor):

  def pipeline_function(self,
                        data,
                        *,
                        tf_session,
                        **kwargs):
    return tf_session.run(self._augmentation_nodes.augmented_image_node,
                       feed_dict={self._augmentation_nodes.augmented_image_placeholder:data})

  def build(self,
            *,
            height,
            width,
            depth,
            batch_size=None,
            **kwargs):
    self._augmentation_nodes = self.add_input_augmentation(height,
                                                           width,
                                                           depth,
                                                           batch_size=batch_size,
                                                           **kwargs)

  @staticmethod
  def add_input_augmentation(input_height,
                             input_width,
                             input_depth,
                             *,
                             batch_size=None,
                             flip_left_right=0,
                             random_crop=0,
                             random_scale=0,
                             random_brightness=0,
                             random_rotation_degrees=0,
                             **kwargs):
    '''Creates the operations to apply the specified distortions.

    During training it can help to improve the results if we run the images
    through simple distortions like crops, scales, and flips. These reflect the
    kind of variations we expect in the real world, and so can help train the
    classifier to cope with natural data more effectively. Here we take the supplied
    parameters and construct a network of operations to apply them to an image.

    Cropping
    ~~~~~~~~

    Cropping is done by placing a bounding box at a random position in the full
    image. The cropping parameter controls the size of that box relative to the
    input image. If it's zero, then the box is the same size as the input and no
    cropping is performed. If the value is 50%, then the crop box will be half the
    width and height of the input. In a diagram it looks like this:

    <       width         >
    +---------------------+
    |                     |
    |   width - crop%     |
    |    <      >         |
    |    +------+         |
    |    |      |         |
    |    |      |         |
    |    |      |         |
    |    +------+         |
    |                     |
    |                     |
    +---------------------+

    Scaling
    ~~~~~~~

    Scaling is a lot like cropping, except that the bounding box is always
    centered and its size varies randomly within the given range. For example if
    the scale percentage is zero, then the bounding box is the same size as the
    input and no scaling is applied. If it's 50%, then the bounding box will be in
    a random range between half the width and height and full size.

    Args:
      flip_left_right: Boolean whether to randomly mirror images horizontally.
      random_crop: Integer percentage setting the total margin used around the
      crop box.
      random_scale: Integer percentage of how much to vary the scale by.
      random_brightness: Integer range to randomly multiply the pixel values by.
      graph.
      input_size: The hub.ModuleSpec for the image module being used.

    Returns:
      The jpeg input layer and the distorted result tensor.
    '''

    augmented_image_placeholder = tf.placeholder(tf.float32, name='augmented_image_placeholder')

    # decoded_image_4d = tf.expand_dims(augmented_image_placeholder, 0)
    decoded_image_4d = augmented_image_placeholder
    margin_scale = 1.0 + (random_crop / 100.0)
    resize_scale = 1.0 + (random_scale / 100.0)
    margin_scale_value = tf.constant(margin_scale)
    resize_scale_value = tf.random_uniform(shape=[],
                                           minval=1.0,
                                           maxval=resize_scale)

    scale_value = tf.multiply(margin_scale_value, resize_scale_value)
    precrop_width = tf.multiply(scale_value, input_width)
    precrop_height = tf.multiply(scale_value, input_height)
    precrop_shape = tf.stack([precrop_height, precrop_width])
    precrop_shape_as_int = tf.cast(precrop_shape, dtype=tf.int32)
    precropped_image = tf.image.resize_bilinear(decoded_image_4d,
                                                precrop_shape_as_int)

    rotation_degrees = tf.random_uniform(shape=[],
                                         minval=-random_rotation_degrees,
                                         maxval=random_rotation_degrees)

    rotation_rads = rotation_degrees * math.pi / 180
    # rotation_rads = math.radians(rotation_degrees)

    rotated_image = tf.contrib.image.rotate(precropped_image,
                                            rotation_rads,
                                            interpolation='NEAREST',
                                            name='rotated_image')

    # precropped_image_3d = tf.squeeze(rotated_image, axis=[0])
    precropped_image_3d = rotated_image
    cropped_image = tf.random_crop(precropped_image_3d,
                                   [batch_size,
                                    input_height,
                                    input_width,
                                    input_depth])
    if flip_left_right:
      flipped_image = tf.image.random_flip_left_right(cropped_image)
    else:
      flipped_image = cropped_image

    brightness_min = 1.0 - (random_brightness / 100.0)
    brightness_max = 1.0 + (random_brightness / 100.0)
    brightness_value = tf.random_uniform(shape=[],
                                         minval=brightness_min,
                                         maxval=brightness_max)
    brightened_image = tf.multiply(flipped_image,
                                   brightness_value,
                                   name='augmented_image_node')
    augmented_image_node = brightened_image
    # augmented_image_node = tf.expand_dims(brightened_image, 0, name='augmented_image_node')

    return NOD.dict_of(augmented_image_placeholder, augmented_image_node)
