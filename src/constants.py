TILESIZE = 30
HELDSIZE = int(TILESIZE/2)
CONFPATH = 'conf.json'
def LERP(a, b, t):
    return (1 - t) * a + t * b
