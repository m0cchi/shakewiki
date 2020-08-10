
import os

def str2bool(s):
  if str(s).lower() in [
      't',
      'true',
      '1',
  ]:
    return True
  return False

def get_env(key, default=None, encoder=None):
  value = os.environ.get(key, default)
  if encoder:
    value = encoder(value)
  return value

