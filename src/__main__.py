from constants import CONFPATH
from engine import Engine

from json import load, dump
from os import mkdir
import sys
from os.path import isdir, isfile, dirname

def load_config():
    with open(CONFPATH) as f:
        return load(f)

def main(resolution):
    engine = Engine(load_config(), resolution)
    engine.run()

if __name__=="__main__":
    main([int(i) for i in sys.argv[1:3]])
