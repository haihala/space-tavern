TILESIZE = 30
GROUND_LEVEL = 7
HELDSIZE = int(TILESIZE/2)
CONFPATH = 'conf.json'

def LERP(a, b, t):
    return (1 - t) * a + t * b

DIFFICULTY = [
        {
            "spawn_interval": 25,
            "max_enemy_count": 5,
            "boss_probability": 0,
            "space_duration": 30
        },
        {
            "spawn_interval": 22,
            "max_enemy_count": 10,
            "boss_probability": 0,
            "space_duration": 40
        },
        {
            "spawn_interval": 20,
            "max_enemy_count": 15,
            "boss_probability": 0.05,
            "space_duration": 50
        },
        {
            "spawn_interval": 17,
            "max_enemy_count": 20,
            "boss_probability": 0.1,
            "space_duration": 60
        },
        {
            "spawn_interval": 15,
            "max_enemy_count": 25,
            "boss_probability": 0.2,
            "space_duration": 80
        }
        ]
