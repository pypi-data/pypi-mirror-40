from dlpipeline.utilities.dlp_base import DLPBase

class DLPEmbedder(DLPBase):
  def __init__(self, *args, cache_embeddings=True, **kwargs):
    self._do_cache_embeddings = cache_embeddings

  @property
  def do_cache_embeddings(self) -> bool:
    return self._do_cache_embeddings

  @do_cache_embeddings.setter
  def do_cache_embeddings(self, value: bool):
    self._do_cache_embeddings = value
