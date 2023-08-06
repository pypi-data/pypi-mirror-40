from dlpipeline.utilities.dlp_base import DLPBase


class DLPAugmentor(DLPBase):
  def __init__(self, *, do_augment=True, **kwargs):
    self._do_augment = do_augment

  def apply(self, data, **kwargs):
    if self._do_augment:
      return self.pipeline_function(data, **kwargs)
    return data

  def build(self, **kwargs):
    pass

  @property
  def do_augment(self):
    return self._do_augment

  @do_augment.setter
  def do_augment(self, value):
    self._do_augment = value
