# space-tavern

# Setup

0. install python3 and pip
1. `pip install -r requirements.txt`
2. python3 src

# Feature list

* Turn-based
* Single inventory slot
* Use or throw held item
* Only one use items
* Evil aliens
* Transport Beer from planet to planet for money
* Use money to buy:
  * Planet's Beer
  * Information
    * enemy types
    * spawn areas
  * Gadgets
* Background space panorama\*

# Gadget List

* Plasma gun
  * Shoots projectile dealing 1 damage
  * 4 ticks to reload
* Jump pad block
  * Stepping on the pad will launch you up in the air
* Turret
  * Shoots enemy when in sight
* Za Warudo
  * Stops time for 8 ticks

# Alien List

* Basic Alien
  * Move 4 ticks
  * Move 1 tile
  * 1 Max Health
  * Jump 3 tile
  * Gravity 1 tile
  * Projectile:
    * No Gravity
    * 1 damage

* Flying Alien
  * Move 6 ticks
  * Move 1 tile - Omnidirectional
  * 1 Max Health
  * Gravity 0
  * Projectile:
    * Gravity 2 tile
    * 1 damage

* Brain Alien
  * Move 10 ticks
  * Move 0 tiles
  * Gravity 5 tiles
  * 1 Max Health
  * Jump 0 tiles
  * Projectile: None
  * Passive:
    * Other aliens get +1 HP

* Turret Alien
  * Move 2 ticks
  * Move 0 tiles
  * 2 Max Health
  * Jump 4 tiles
  * Gravity 2 tiles
  * Projectile:
    * Gravity 1 tile
    * 1 damage

* Kamikaze Alien
  * Move 3 ticks
  * Move 2 tiles
  * 1 Max Health
  * Jump 2 tiles
  * Gravity 1 tile
  * AI:
    * Explode when next to player

* Runner Alien
  * Move 1 tick
  * Move 1 tile
  * 1 Max Health
  * Jump 3 tiles
  * Gravity 1 tile
  * Type: Melee

* Road roller alien
  * Move 6 tick
  * Move 1 tile
  * 4 Max Health
  * Jump 0 tile
  * Gravity 2 tiles
