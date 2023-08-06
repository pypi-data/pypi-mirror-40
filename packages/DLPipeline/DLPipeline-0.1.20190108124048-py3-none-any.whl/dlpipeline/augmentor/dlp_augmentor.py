from nisse import LazyPipeIterator


class DLPAugmentor(LazyPipeIterator):
  def __init__(self, data_iterator=None, *, C=None, **kwargs):
    super().__init__(data_iterator, C=C, **kwargs)
    self._do_augment = C.default_do_augmentation

  def apply(self, data, **kwargs):
    if self._do_augment:
      return self.func(data, **kwargs)
    return data

  @property
  def do_augment(self):
    return self._do_augment

  @do_augment.setter
  def do_augment(self, value):
    self._do_augment = value
