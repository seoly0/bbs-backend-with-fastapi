from os.path import abspath, dirname

from .const import Const
from .environment import Environment

ENV = Environment()
CONST = Const()
ROOT = dirname(dirname(abspath(__file__)))
