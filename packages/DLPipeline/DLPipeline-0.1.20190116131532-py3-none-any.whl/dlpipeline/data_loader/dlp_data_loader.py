#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
from typing import Iterable, Iterator

import tensorflow as tf
from warg import NamedOrderedDictionary as NOD

from dlpipeline.data_loader.image_sets import build_deep_level_image_list, sys
from dlpipeline.data_loader.image_sets.first_level_label import build_first_level_image_list
from dlpipeline.utilities.dlp_base import DLPBase

__author__ = 'cnheider'


class DLPDataLoader(DLPBase,Iterable):

  def __init__(self,
               C=None):

    self._first_level = C.first_level_categories

    if C:
      self.load(C.image_directory, C)

  def load(self, image_directory='', C=None):
    if not image_directory:
      tf.logging.error('Must set flag --image_directory.')
      return -1

    if self._first_level:
      self._input = build_first_level_image_list(**vars(C))
    else:
      self._input = build_deep_level_image_list(**vars(C))

    if not self._input:
      raise EnvironmentError

    self.class_count = len(self._input.keys())
    if self.class_count == 0:
      tf.logging.error(f'No valid folders of images found at {image_directory}')
      return -1
    if self.class_count == 1:
      tf.logging.error(
          f'Only one valid folder of images found at {image_directory} - multiple classes are '
          f'needed for classification.')
      return -1

    for label, sets in self._input.items():
      for set, instances in sets.items():
        print(f'Class {label}, {set} has {len(instances)} instances')

  @property
  def image_list(self):
    return self._input.items()

  @property
  def class_count(self):
    return self._class_count

  @class_count.setter
  def class_count(self,value):
    self._class_count =value

  def keys(self):
    return self._input.keys()

  def items(self):
    return self._input.items()

  def __getitem__(self, item):
    return self._input.get(item)

  def __len__(self):
    return len(self.items())


  def __iter__(self) -> Iterator:
    return self.sampler(set_name='training')

  def __contains__(self, item):
    return item in self._input

  def sampler(self, *, set_name, batch_size=16, **kwargs):
    batch = []
    while True:
      label_index = random.randrange(self.class_count)
      label_name = list(self.keys())[label_index]
      data_index = random.randrange(sys.maxsize + 1)
      data_path = get_image_path(data_collection=self._input,
                                 label_name=label_name,
                                 image_index=data_index,
                                 set_name=set_name)

      data = self.pipeline_function(tf.gfile.GFile(data_path, 'rb').read(), **kwargs)

      instance = (data,
                  data_path,
                  data_index,
                  label_index,
                  label_name)
      batch.append(instance)

      if len(batch) == batch_size:
        (data,
         data_path,
         data_index,
         label_index,
         label_name) = zip(*batch)

        batch = []
        yield NOD.dict_of(data,
                          data_path,
                          data_index,
                          label_index,
                          label_name)

  def iterator(self, set_name, **kwargs):
    while True:
      for label_index, label_name in enumerate(self.root.keys()):
        for image_index, image_path in enumerate(self.root[label_name][set_name]):
          image_path = get_image_path(data_collection=self.root,
                                      label_name=label_name,
                                      image_index=image_index,
                                      set_name=set_name)

          data = self.pipeline_function(tf.gfile.GFile(image_path, 'rb').read(), **kwargs)

          info = NOD.dict_of(image_path,
                             image_index,
                             label_name)
          yield NOD.dict_of(data, label_index, info)

def get_image_path(*,
                   data_collection,
                   label_name,
                   image_index,
                   set_name):
  '''
  Returns a path to an image for a label at the given index.

  Args:
    data_collection: OrderedDict of images for each label.
    label_name: Label string we want to get an image for.
    image_index: Int offset of the image we want. This will be moduloed by the
    available number of images for the label, so it can be arbitrarily large.
    image_directory: Root folder string of the subfolders containing the training
    images.
    set_name: Name string of set to pull images from - training, testing, or
    validation.

  Returns:
    File system path string to an image that meets the requested parameters.

  '''
  if label_name not in data_collection:
    tf.logging.fatal(f'Label does not exist {label_name}.')
  label_lists = data_collection[label_name]

  if set_name not in label_lists:
    tf.logging.fatal(f'Set does not exist {set_name}')
  the_set = label_lists[set_name]

  set_len = len(the_set)

  if not the_set or set_len == 0:
    tf.logging.fatal(f'Label {label_name} has no images in the category {set_name}.')
    return None

  mod_index = image_index % set_len
  image_path = the_set[mod_index]

  if not tf.gfile.Exists(image_path):
    tf.logging.fatal(f'File does not exist {image_path}')

  return image_path
