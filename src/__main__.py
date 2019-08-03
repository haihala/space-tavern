from constants import CONFPATH
from engine import Engine

from json import load, dump
from os import mkdir
from os.path import isdir, isfile, dirname


def load_config():
    with open(CONFPATH) as f:
        return load(f)

def main():
    engine = Engine(load_config())
    engine.run()

if __name__=="__main__":
    main()
