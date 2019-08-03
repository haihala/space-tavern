from engine import Engine

def filesystem_setup():
    # Check that all files that should exist, do. Create ones that don't
    pass

def load_config():
    # Returns configs in object form
    pass

def main():
    filesystem_setup()
    engine = Engine(load_config())
    engine.run()

if __name__=="__main__":
    main()
