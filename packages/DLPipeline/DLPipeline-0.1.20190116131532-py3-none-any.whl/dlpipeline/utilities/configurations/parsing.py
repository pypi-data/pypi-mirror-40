from pathlib import Path, PosixPath

from warg import NOD


def get_upper_case_vars_or_protected_of(module):
  v = vars(module)
  if v:
    return {
      key:value
      for key, value in module.__dict__.items()
      if key.isupper() or (key.startswith('_') and not key.endswith('_'))
      }
  return {}


def to_dict(C, only_upper_case=True):
  if only_upper_case:
    return get_upper_case_vars_or_protected_of(C)
  else:
    return vars(C)


class ConfigObject(NOD):

  def __setattr__(self, item,value):
    self.__dict__[item.lower()]=value

  def __getattr__(self, item):
    return self.__dict__[item.lower()]


def to_config_object(C_dict):
  if not type(C_dict) is dict:
    C_dict = to_dict(C_dict)

  a = ConfigObject()

  for (k, v) in C_dict.items():
    assert type(k) is str
    lowered = k.lower()
    if isinstance(v, Path):
      setattr(a, lowered, str(v))
    else:
      setattr(a, lowered, v)

  return a


def print_kws(**kwargs):
  for (k, v) in kwargs.items():
    print(f'{k}:{v} is not used')
