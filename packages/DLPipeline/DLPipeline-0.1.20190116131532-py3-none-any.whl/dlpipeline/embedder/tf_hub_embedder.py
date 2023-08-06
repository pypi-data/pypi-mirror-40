#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

import numpy as np
import tensorflow as tf
from warg import NOD

from dlpipeline.embedder.dlp_embedder import DLPEmbedder
from dlpipeline.utilities.path_utilities.directory_exists import ensure_directory_exists

__author__ = 'cnheider'

import tensorflow_hub as hub

# A module is understood as instrumented for quantization with TF-Lite
# if it contains any of these ops.
FAKE_QUANT_OPS = ('FakeQuantWithMinMaxVars',
                  'FakeQuantWithMinMaxVarsPerChannel')


class TFHubEmbedder(DLPEmbedder):

  def pipeline_function(self,
                        data,
                        *,
                        sess,
                        **kwargs):
    embedding = self.get_embedding(sess,
                                   data,
                                   **kwargs).data
    return embedding

  def __init__(self, data: iter = None, trainable=False, *, C, **kwargs):
    super().__init__(data, **kwargs)

    self._C = C

    self.module_specification = hub.load_module_spec(C.embedding_module)
    self.input_size = hub.get_expected_image_size(self.module_specification)

    self.height, self.width = self.input_size
    self.depth = hub.get_num_image_channels(self.module_specification)

    self.augmented_jpeg_str_placeholder = tf.placeholder(tf.string, name='augmented_jpeg_str_placeholder')
    decoded_image = tf.image.decode_jpeg(self.augmented_jpeg_str_placeholder, channels=self.depth)

    self.decoded_image_as_float = tf.image.convert_image_dtype(decoded_image, tf.float32)

    self.embedder_input_node = tf.placeholder(tf.float32,
                                              [None, self.height, self.width, self.depth],
                                              name='embedding_input')
    module = hub.Module(self.module_specification, trainable=trainable)
    # tf.get_collection(tf.GraphKeys.REGULARIZATION_LOSSES)
    self.embedder_loss = tf.losses.get_regularization_loss()
    self.embedding_output_node = module(self.embedder_input_node)
    quantize = any(node.op in FAKE_QUANT_OPS for node in tf.get_default_graph().as_graph_def().node)

    self.quantize = quantize

    self.batch_size, self.embedding_size = self.embedding_output_node.get_shape().as_list()

  def create_embedding_file(self,
                            sess,
                            data,
                            data_path,
                            *,
                            embedding_path,
                            ):
    '''
    Create a single embedding file.
    '''

    print('Creating embedding at ' + embedding_path)

    try:
      embedding_values = self.compute_embedding(sess,
                                                [data])
    except Exception as e:
      raise RuntimeError(f'Error during processing file {data_path} ({e})')

    embedding_string = ','.join(str(x) for x in embedding_values)

    with open(embedding_path, 'w') as embedding_file:
      embedding_file.write(embedding_string)

  def get_or_create_cached_embedding(self,
                                     sess,
                                     *,
                                     data_path,
                                     data,
                                     label_name,
                                     ):
    '''
    Retrieves or calculates embedding values for an image.

    If a cached version of the embedding data exists on-disk, return that,
    otherwise calculate the data and save it to disk for future use.

    Args:
      sess: The current active TensorFlow Session.
      dataset: OrderedDict of training images for each label.
      label_name: Label string we want to get an image for.
      index: Integer offset of the image we want. This will be modulo-ed by the
      available number of images for the label, so it can be arbitrarily large.
      category: Name string of which set to pull images from - training, testing,
      or validation.
      embedding_directory: Folder string holding cached files of embedding values.
      image_data_node: The tensor to feed loaded jpeg data into.
      resized_image_node: The output of decoding and resizing the image.
      resized_input_tensor: The input node of the recognition graph.
      embedding_output_node: The output tensor for the embedding values.
      embedding_module: The name of the image module being used.

    Returns:
      Numpy array of values produced by the embedding layer for the image.
    '''

    sub_directory_path = os.path.join(self._C.embedding_directory,
                                      label_name)
    ensure_directory_exists(sub_directory_path)
    embedding_path = self.get_embedding_path(label_name,
                                             data_path)

    if embedding_path is None:
      return None

    if not os.path.exists(embedding_path):
      self.create_embedding_file(sess,
                                 data=data,
                                 data_path=data_path,
                                 embedding_path=embedding_path)

    with open(embedding_path, 'r') as embedding_file:
      embedding_string = embedding_file.read()

    did_hit_error = False
    data = None

    try:
      data = [float(x) for x in embedding_string.split(',')]
    except ValueError:
      tf.logging.warning('Invalid float found, recreating embedding')
      did_hit_error = True

    if did_hit_error:
      self.create_embedding_file(sess,
                                 data=data,
                                 data_path=data_path,
                                 embedding_path=embedding_path)

      with open(embedding_path, 'r') as embedding_file:
        embedding_string = embedding_file.read()

      data = [float(x) for x in embedding_string.split(',')]

    return NOD.dict_of(data, embedding_path)

  def compute_embedding(self,
                        sess,
                        data):
    '''Runs inference on an image to extract the 'embedding' summary layer.

    Args:
      sess: Current active TensorFlow Session.
      data: String of raw JPEG data.
      image_data_node: Input data layer in the graph.
      resized_image_node: Output of initial image resizing and preprocessing.

    Returns:
      Numpy array of embedding values.
    '''
    # First decode the JPEG image, resize it, and rescale the pixel values.

    embedding_values = sess.run(self.embedding_output_node,
                                feed_dict={self.embedder_input_node:data})

    embedding_values = np.squeeze(embedding_values)

    return embedding_values

  def cache_embeddings(self,
                       sess,
                       data,
                       data_path
                       ):
    '''Ensures all the training, testing, and validation embeddings are cached.

    Because we're likely to read the same image multiple times (if there are no
    distortions applied during training) it can speed things up a lot if we
    calculate the embedding layer values once for each image during
    preprocessing, and then just read those cached values repeatedly during
    training. Here we go through all the images we've found, calculate those
    values, and save them off.

    Args:
      sess: The current active TensorFlow Session.
      dataset: OrderedDict of training images for each label.
      image_directory: Root folder string of the subfolders containing the training
      images.
      embedding_directory: Folder string holding cached files of embedding values.
      image_data_node: Input tensor for jpeg data from file.
      resized_image_node: The output of decoding and resizing the image.
      resized_input_tensor: The input node of the recognition graph.
      embedding_output_node: The penultimate output layer of the graph.
      embedding_module: The name of the image module being used.

    Returns:
      Nothing.
    '''

    how_many_embeddings = 0
    ensure_directory_exists(self._C.embedding_directory)

    for label_name, label_lists in self._parent.items():
      for category in ['training', 'testing', 'validation']:
        category_list = label_lists[category]

        for index, unused_base_name in enumerate(category_list):
          ret = self.get_or_create_cached_embedding(sess,
                                                    data=data,
                                                    data_path=data_path,
                                                    label_name=label_name
                                                    )
          if ret is None:
            return None

          how_many_embeddings += 1
          if how_many_embeddings % 100 == 0:
            tf.logging.info(f'{str(how_many_embeddings)} embedding files created.')

  def get_embedding(self,
                    sess,
                    data_in,
                    *,
                    label_name,
                    data_path,
                    **kwargs
                    ):
    '''Retrieves embedding values for cached images.

    If no distortions are being applied, this function can retrieve the cached
    embedding values directly from disk for images. It picks a random set of
    images from the specified category.

    Args:
      sess: Current TensorFlow Session.
      dataset: OrderedDict of training images for each label.
      batch_size: If positive, a random sample of this size will be chosen.
      If negative, all embeddings will be retrieved.
      category: Name string of which set to pull from - training, testing, or
      validation.
      embedding_directory: Folder string holding cached files of embedding values.
      image_directory: Root folder string of the subfolders containing the training
      images.
      image_data_placeholder: The layer to feed jpeg image data into.
      resized_image_node: The output of decoding and resizing the image.
      resized_input_tensor: The input node of the recognition graph.
      embedding_output_node: The embedding output layer of the CNN graph.
      embedding_module: The name of the image module being used.

    Returns:
      List of embedding arrays, their corresponding ground truths, and the
      relevant filenames.
    '''
    data = []
    embedding_path = []

    if self._do_cache_embeddings:
      for d, l, p in zip(data_in, label_name, data_path):
        ret = self.get_or_create_cached_embedding(sess,
                                                  data=d,
                                                  data_path=p,
                                                  label_name=l)
        data.append(ret.data)
        embedding_path.append(ret.embedding_path)
    else:
      data = self.compute_embedding(sess, data=data_in)

    return NOD.dict_of(data, embedding_path)

  def get_embedding_path(self,
                         label_name,
                         data_path
                         ):
    '''
    Returns a path to a embedding file for a label at the given index.

    Args:
      dataset: OrderedDict of training images for each label.
      label_name: Label string we want to get an image for.
      index: Integer offset of the image we want. This will be moduloed by the
      available number of images for the label, so it can be arbitrarily large.
      embedding_directory: Folder string holding cached files of embedding values.
      category: Name string of set to pull images from - training, testing, or
      validation.

    Returns:
      File system path string to an image that meets the requested parameters.
    '''
    module_name = (self._C.embedding_module.replace('://', '~')  # URL scheme.
                   .replace('/', '~')  # URL and Unix paths.
                   .replace(':', '~').replace('\\', '~'))  # Windows paths.

    name = os.path.split(data_path)[1]

    e_path = f'{self._C.embedding_directory}/{label_name}/{name}'

    return e_path + '_' + module_name + '.txt'
