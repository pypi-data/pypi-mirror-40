#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import tensorflow as tf
from warg import NamedOrderedDictionary as NOD

from dlpipeline.data_loader.dlp_data_loader import DLPDataLoader

__author__ = 'cnheider'


class TFDataLoader(DLPDataLoader):

  def pipeline_function(self,
                        data,
                        *,
                        sess,
                        **kwargs):
    data = sess.run(self._handles.resized_image_node,
                    feed_dict={
                      self._handles.jpeg_str_placeholder:data
                      })

    return data

  def build(self,
             height,
             width,
             depth,
             **kwargs):
    self._handles = self.add_jpeg_decoding_resize(height,
                                                  width,
                                                  depth)

  @staticmethod
  def add_jpeg_decoding_resize(input_height, input_width, input_depth, ratio=2, size_limit=(10e3, 10e3)):
    '''
    Adds operations that perform JPEG decoding and resizing to the graph..

    Args:
      module_spec: The hub.ModuleSpec for the image module being used.

    Returns:
      Tensors for the node to feed JPEG data into, and the output of the
        preprocessing steps.
    '''

    jpeg_str_placeholder = tf.placeholder(tf.string, name='jpeg_str_placeholder')
    decoded_image = tf.image.decode_jpeg(jpeg_str_placeholder, channels=input_depth, ratio=ratio)

    original_shape = decoded_image.shape
    if original_shape[0] > size_limit[0] or original_shape[1] > size_limit[1]:
      decoded_image = tf.image.resize_images(decoded_image,size_limit,preserve_aspect_ratio=True)
      tf.log(f'Warning large input, of size {original_shape}, resized to {decoded_image.shape}')


    decoded_image_as_float = tf.image.convert_image_dtype(decoded_image, tf.float32)
    # Convert from full range of uint8 to range [0,1] of float32.

    # decoded_image_4d = decoded_image_as_float
    decoded_image_4d = tf.expand_dims(decoded_image_as_float, 0)
    resize_shape = tf.stack([input_height, input_width])
    resize_shape_as_int = tf.cast(resize_shape, dtype=tf.int32)
    resized_image_node = tf.image.resize_bilinear(decoded_image_4d, resize_shape_as_int)
    resized_image_node = tf.squeeze(resized_image_node)

    return NOD.dict_of(jpeg_str_placeholder, resized_image_node)
