from nisse import LazyPipeIterator


class DLPEmbedder(LazyPipeIterator):
  def __init__(self, *args, cache_embeddings=True, **kwargs):
    super().__init__(*args, **kwargs)
    self._do_cache_embeddings = cache_embeddings

  @property
  def do_cache_embeddings(self) -> bool:
    return self._do_cache_embeddings

  @do_cache_embeddings.setter
  def do_cache_embeddings(self, value: bool):
    self._do_cache_embeddings = value
