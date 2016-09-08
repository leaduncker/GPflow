from six.moves import configparser
import os
import collections
import tensorflow as tf

c = configparser.ConfigParser()

# first look in the current directory, then in the user's home directory, then in the same directory as this file.
locations = map(os.path.abspath, [os.curdir, os.path.expanduser('~'), os.path.dirname(os.path.realpath(__file__))])

for loc in locations:
    # try both with and without preceeding 'dot' for hidden files (prefer non-hidden)
    if c.read(os.path.join(loc, 'gpflowrc')):
        break
    if c.read(os.path.join(loc, '.gpflowrc')):
        break


# a very simple parser
def parse(string):
    if type(string) is not str:
        raise ValueError
    if string in ['true', 'True']:
        return True
    elif string in ['false', 'False']:
        return False
    elif string in ['float64', 'float32', 'float16', 'int64', 'int32', 'int16']:
        return getattr(tf, string)
    else:
        try:
            return float(string)
        except:
            return string


# make the dictionary into a nested series of named tuples. This is what allows
# accessing by attribute: settings.numerics.jitter
def namedtuplify(mapping):  # thank you https://gist.github.com/hangtwenty/5960435
    if isinstance(mapping, collections.Mapping):
        for key, value in list(mapping.items()):
            mapping[key] = namedtuplify(value)
        try:
            mapping.pop('__name__')
        except:
            pass
        return collections.namedtuple('settings', dict(**mapping))(**mapping)
    return parse(mapping)

settings = namedtuplify(c._sections)