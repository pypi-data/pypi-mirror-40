from abc import abstractmethod


class DLPBase(object):

  def __call__(self, data, **kwargs):
    return self.apply(data, **kwargs)

  def apply(self,data, **kwargs):
    return self.pipeline_function(data, **kwargs)

  @abstractmethod
  def pipeline_function(self, data, **kwargs):
    pass

  @abstractmethod
  def build(self, **kwargs):
    pass


