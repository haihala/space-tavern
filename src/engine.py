from entity import Entity
from enemy import Enemy
from item import Item
from player import Player
from tile import Tile
from enemy_collection import ENEMIES
from item_collection import ITEMS

from constants import HELDSIZE, TILESIZE, LERP, GROUND_LEVEL, DIFFICULTY

import pygame
import math

from random import randint, random, uniform
from copy import copy
from time import sleep, time

class Engine():
    def __init__(self, conf, resolution):
        flags = (pygame.FULLSCREEN * int(conf["fullscreen"]))
        self.display = pygame.display.set_mode(resolution, flags)
        self.null_entity = Entity()

        self.money = 50
        self.in_space = False

        self.tick_count = 0
        self.planet = 0

        self.ship_width = 10
        self.ship_height = 6
        self.ship_gap = 4

        self.player = Player(conf["binds"])
        self.console = ITEMS["item_console"]([-7, -1])
        self.console.sprite_offset = 1
        self.console_available = 0
        self.entities = [
                self.player,
                self.console,
                ITEMS["item_gun"]((-3, -1))
                ]
        self.tiles = []
        self.background = []
        self.particles = {}
        self.panorama = [
                Tile([0,0], "panorama_stars"),
                Tile([-self.display.get_width(), 0], "panorama_stars"),
                Tile([0,self.display.get_height()/TILESIZE], "panorama_planet")
                ]
        self.color = (0, 0, 0)

        self.tick_target_duration = 1
        self.cam = [0,0]
        self.target_cam = [0,0]
        self.running = False

        from pygame_objects import SOUNDS
        SOUNDS["music_peace"].set_volume(0.5)
        SOUNDS["music_space"].set_volume(0.5)
        #SOUNDS["music_peace"].play(-1, 0, 2)

        self.basic_font = pygame.font.SysFont("comicsansms", 30)

        for x in range(-self.ship_width, self.ship_width+1):
            for y in range(-self.ship_height, self.ship_height+1):
                if abs(x) <= 6 and abs(y) >= 2 and abs(y) <= 4:
                    if abs(x) < 6 and (y == 2 or y == -4):
                        self.background.append(Tile([x,y], "window_top"))
                    elif abs(x) < 6 and (y == 4 or y == -2):
                        self.background.append(Tile([x,y], "window_bottom"))
                    elif x == -6 and abs(y) == 3:
                        self.background.append(Tile([x,y], "window_left"))
                    elif x == 6 and abs(y) == 3:
                        self.background.append(Tile([x,y], "window_right"))
                    elif x == -6 and (y == -4 or y == 2):
                        self.background.append(Tile([x,y], "window_top_left"))
                    elif x == 6 and (y == -4 or y == 2):
                        self.background.append(Tile([x,y], "window_top_right"))
                    elif x == -6 and (y == 4 or y == -2):
                        self.background.append(Tile([x,y], "window_bottom_left"))
                    elif x == 6 and (y == 4 or y == -2):
                        self.background.append(Tile([x,y], "window_bottom_right"))
                elif math.sin(x) > 0 and abs(math.sin(y)) < (0.2 + abs(math.cos(x)/1.23)):
                    self.background.append(Tile([x,y], "wall_middle"))
                else:
                    self.background.append(Tile([x,y], "wall"))

        for x in range(-self.ship_width, self.ship_width+1):
            for y in range(-self.ship_height, self.ship_height+1):
                if ((x == -self.ship_width or x == self.ship_width) or (y == -self.ship_height or y == self.ship_height or y == 0) and (not (y == 0 and abs(x) < 3))) and not (y <= 5 and y >= 3):
                    self.tiles.append(Tile([x,y], "floor"))
                elif (y <= 5 and y >= 3) and (x == -self.ship_width or x == self.ship_width):
                    self.tiles.append(Tile([x,y], "door"))
                elif y == self.ship_height-1 and abs(x) == 0:
                    self.entities.append(ITEMS["item_jump_pad"]([x,y]))

                if y == self.ship_height or y == -self.ship_height or (y == 0 and abs(x) > 2) or (y == 2 and (x == -self.ship_width or x == self.ship_width)):
                    self.background.append(Tile([x,y+1], "floor_bottom"))
                if y == -self.ship_height or y == self.ship_height or (y == 0 and abs(x) > 2):
                    self.background.append(Tile([x,y-1], "floor_top"))
                if (x == -self.ship_width or x == self.ship_width or (y == 0 and x == -3)) and not (y <= 5 and y >= 3):
                    self.background.append(Tile([x+1,y], "floor_right"))
                if (x == -self.ship_width or x == self.ship_width or (y == 0 and x == 3)) and not (y <= 5 and y >= 3):
                    self.background.append(Tile([x-1,y], "floor_left"))
                if ((x == -self.ship_width and y == -self.ship_height) or (y == 0 and x == 3)) or (y == self.ship_height and x == -self.ship_width):
                    self.background.append(Tile([x-1,y-1], "floor_top_left"))
                if ((x == -self.ship_width and y == self.ship_height) or (y == 0 and x == 3)) or (y == 2 and (x == -self.ship_width or x == self.ship_width)):
                    self.background.append(Tile([x-1,y+1], "floor_bottom_left"))
                if ((x == self.ship_width and y == -self.ship_height) or (y == 0 and x == -3)) or (y == self.ship_height and x == self.ship_width):
                    self.background.append(Tile([x+1,y-1], "floor_top_right"))
                if ((x == self.ship_width and y == self.ship_height) or (y == 0 and x == -3)) or (y == 2 and (x == -self.ship_width or x == self.ship_width)):
                    self.background.append(Tile([x+1,y+1], "floor_bottom_right"))
        self.update_surroundings(self.in_space)

        self.pause(True)
        self.pause()        # Info for players


    @property
    def enemies(self):
        return [i for i in self.entities if type(i) is Enemy]

    def add_particles(self, position, kind):
        self.particles.append((position, kind))

    def liftoff(self):
        self.console.data["console"] = self.in_space
        self.console.sprite_offset = self.in_space
        self.console_available = self.tick_count + DIFFICULTY[self.planet]["space_duration"]
        self.update_surroundings(not self.in_space)

    def update_surroundings(self, state):
        from pygame_objects import SPRITES, SOUNDS
        self.in_space = state

        if self.in_space:
            SOUNDS["ship_space"].play()
            SOUNDS["music_peace"].fadeout(2)
            SOUNDS["music_space"].play(-1, 0, 2)
            for x in range(-self.ship_width, self.ship_width+1):
                for y in range(-self.ship_height, self.ship_height+1):
                    if (y <= 5 and y >= 3) and (x == -self.ship_width or x == self.ship_width):
                        self.tiles.append(Tile([x,y],"door"))
            self.background = [background for background in self.background if background._sprite != SPRITES["ground_top"]]
            self.entities = [entity for entity in self.entities if not (entity._sprite in [SPRITES["item_sell"], SPRITES["item_shop"]])]

        else:
            self.planet += 1
            SOUNDS["ship_land"].play()
            SOUNDS["music_space"].fadeout(2)
            SOUNDS["music_peace"].play(-1, 0, 2)
            self.tiles = [tile for tile in self.tiles if tile._sprite != SPRITES["door"]]
            self.entities = [entity for entity in self.entities if type(entity) is not Enemy]
            for x in range(-self.ship_width*3, self.ship_width*3+1):
                self.background.append(Tile([x,GROUND_LEVEL], "ground_top"))

            self.entities.append(ITEMS["item_sell"]([self.ship_width+3, GROUND_LEVEL-1]))

            self.entities.append(ITEMS["item_shop"]([-self.ship_width-3, GROUND_LEVEL-1], "box"))
            for i in range(3):
                self.entities.append(ITEMS["item_shop"]([-self.ship_width-6 - 3*i, GROUND_LEVEL-1]))


    def collides(self, entity=None, point=None, target="collider", exclude=[]):
        if target in ["collider", "*"]:
            if entity:
                if entity.position[1] == GROUND_LEVEL:
                    return [self.null_entity]
        spaces = {
                "*": self.entities + self.tiles,
                "collider": self.tiles + [i for i in self.entities if i.collider],
                "enemy": self.enemies,
                "player": [self.player],
                "tile": self.tiles,
                "entity": self.entities,
                "trigger_item": [i for i in self.entities if type(i) is Item and i.on_collision],
                "pickup": [i for i in self.entities if type(i) is Item and i.can_pickup]
                }
        search_space = spaces[target]

        if entity:
            return [i for i in search_space if i not in exclude and (abs(i.position[0]-entity.position[0]) + abs(i.position[1]-entity.position[1]))<=3 and any(p in i.colliders for p in entity.colliders)]
        if point:
            return [i for i in search_space if i not in exclude and abs(i.position[0]-point[0]) + abs(i.position[1]-point[1])<=2 and point in i.colliders]

    def project_collides(self, entity, shift, target="collider", exclude=[]):
        cp = copy(entity)
        cp.position = [cp.position[i]+shift[i] for i in range(2)]
        exclude.append(cp)
        return self.collides(cp, target=target, exclude=exclude)

    def place(self, item, exclude=[], target="*"):
        if not self.collides(entity=item, target=target, exclude=exclude):
            self.entities.append(item)
            return True

    def camera_shake(self, amount):
        self.cam = [self.cam[i] + uniform(-amount, amount) for i in range(2)]

    def run(self):
        self.running = True
        while self.running:
            self.particles = []
            if self.tick_count >= self.console_available:
                self.console.data["console"] = True
                self.console.sprite_offset = 1
            for dead in self.entities:
                if dead.dead and dead.on_death:
                    self.add_particles(dead.position, "particle_explosion")
                    dead.on_death(dead, self, self.player)
            self.entities = [entity for entity in self.entities if not entity.dead]
            for entity in self.entities:
                for item in self.collides(entity, target="trigger_item", exclude=[entity]):
                    if item.on_collision:
                        item.on_collision(item, self, entity)
                if entity == self.player:
                    self.player_tick(self.tick_target_duration)
                    if self.in_space:
                        start_time = time()
                        while time()-start_time < 0.25:
                            self.render(0)
                else:
                    entity.tick(self)

            for entity in self.entities:
                entity.grounded = self.project_collides(entity, [0,1], exclude=[entity])

            if self.tick_count % DIFFICULTY[self.planet]["spawn_interval"]== 0 and len(self.enemies) < DIFFICULTY[self.planet]["max_enemy_count"] and self.in_space:
                boss = int(random() < DIFFICULTY[self.planet]["boss_probability"])
                while True:
                    rand_coords = [randint(-self.ship_width+1, self.ship_width-1), randint(-self.ship_height+1, self.ship_height-1)]
                    if self.place(ENEMIES[["alien_spawner", "alien_spawner_big"][boss]](rand_coords)):
                        break
            self.tick_count += 1

    def quit(self, hard=False):
        if not hard:
            self.pause(False, True)
        exit(0)

    def player_tick(self, slot):
        buffered = None
        start_time = time()
        true_slot = (slot/2 if self.player.fatigue else slot) if self.in_space else 0.1
        while time()-start_time < true_slot and not buffered:
            self.render(((time()-start_time)/true_slot) if self.in_space else 1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit(True)
                if not self.player.fatigue:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            btn = 'up'
                        elif event.key == pygame.K_DOWN:
                            btn = 'down'
                        elif event.key == pygame.K_LEFT:
                            btn = 'left'
                        elif event.key == pygame.K_RIGHT:
                            btn = 'right'
                        elif event.key == pygame.K_ESCAPE:
                            btn = 'esc'
                        elif event.key == pygame.K_SPACE:
                            btn = 'space'
                        else:
                            btn = event.unicode

                        if btn in self.player.binds:
                            buffered = self.player.binds[btn]

                        if buffered == "pause":
                            self.pause()

        self.player.tick(self, buffered)

    def pause(self, title=False, end=False):
        paused = True
        while paused:
            if title:
                self.draw_title_screen()
            elif end:
                self.draw_end_screen()
                sleep(2)
            else:
                self.draw_help()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit(True)
                elif event.type == pygame.KEYDOWN:
                    paused = False
                    break

    def draw_help(self):
        self.display.fill((0, 0, 0))
        text_height = 30
        offset = 0
        self.display.blit(self.text_surface("HUD(bottom right):", (255, 255, 255)), (10, int(10+offset*text_height*1.1)))
        offset += 1
        self.display.blit(self.text_surface("Blue is current planet", (0, 0, 255)), (10, int(10+offset*text_height*1.1)))
        offset += 1
        self.display.blit(self.text_surface("Green is money", (0, 255, 0)), (10, int(10+offset*text_height*1.1)))
        offset += 1
        self.display.blit(self.text_surface("Red is health", (255, 0, 0)), (10, int(10+offset*text_height*1.1)))
        offset += 2

        self.display.blit(self.text_surface("Keys:", (255, 255, 255)), (10, int(10+offset*text_height*1.1)))
        offset += 1
        self.display.blit(self.text_surface("x - Use/pickup/buy/throw something in the same square or the one in front", (255, 255, 255)), (10, int(10+offset*text_height*1.1)))
        offset += 1
        self.display.blit(self.text_surface("Arrow keys - Move", (255, 255, 255)), (10, int(10+offset*text_height*1.1)))
        offset += 1
        self.display.blit(self.text_surface("z - Use held item", (255, 255, 255)), (10, int(10+offset*text_height*1.1)))
        offset += 1
        self.display.blit(self.text_surface("up arrow or space - Jump", (255, 255, 255)), (10, int(10+offset*text_height*1.1)))
        offset += 1
        self.display.blit(self.text_surface("down arrow - Skip turn", (255, 255, 255)), (10, int(10+offset*text_height*1.1)))
        offset += 1
        self.display.blit(self.text_surface("esc - Open this pause menu.", (255, 255, 255)), (10, int(10+offset*text_height*1.1)))
        offset += 2

        self.display.blit(self.text_surface("Use console to take off", (255, 255, 255)), (10, int(10+offset*text_height*1.1)))
        offset += 1
        self.display.blit(self.text_surface("Throw beer into dollar sign when on a planet to sell", (255, 255, 255)), (10, int(10+offset*text_height*1.1)))
        offset += 1
        self.display.blit(self.text_surface("Holding onto beer raises value", (255, 255, 255)), (10, int(10+offset*100*1.1)))
        offset += 1
        self.display.blit(self.text_surface("Use items to survive. 5 planets max, each one harder than the last.", (255, 255, 255)), (10, int(10+offset*100*1.1)))
        offset += 2

        cont_txt = self.text_surface("Press any key to continue", (255, 255, 255))
        self.display.blit(cont_txt, (
            self.display.get_width()/2-cont_txt.get_width()/2, self.display.get_height()*0.8-cont_txt.get_height()/2))
        pygame.display.flip()

    def draw_title_screen(self):
        from pygame_objects import SPRITES
        self.display.fill((0, 0, 0))
        self.display.blit(pygame.transform.scale(SPRITES["panorama_stars"][0], self.display.get_size()), (0,0))
        cont_txt = self.text_surface("Press any key to continue", (255, 255, 255))
        self.display.blit(cont_txt, (
            self.display.get_width()/2-cont_txt.get_width()/2, self.display.get_height()*0.8-cont_txt.get_height()/2))
        pygame.display.flip()

    def draw_end_screen (self):
        from pygame_objects import SPRITES
        self.display.fill((0, 0, 0))
        sarcasm = self.text_surface("Red is health", (255, 0, 0))
        self.display.blit(sarcasm,
                [self.display.get_size()[i]/2-sarcasm.get_size()[i]/2 for i in range(2)])

        cont_txt = self.text_surface("Press any key to exit", (255, 255, 255))
        self.display.blit(cont_txt, (
            self.display.get_width()/2-cont_txt.get_width()/2, self.display.get_height()*0.8-cont_txt.get_height()/2))
        pygame.display.flip()

    def render(self, tick_time_left):
        # Draw the world
        self.cam = [LERP(self.cam[i], self.target_cam[i], 0.1) for i in range(2)]
        self.draw_panorama()
        self.draw_background()
        self.draw_world()
        self.draw_hud(tick_time_left)
        pygame.display.flip()

    def draw_panorama(self):
        from pygame_objects import SPRITES
        targets = []
        for p in self.panorama:
            if p._sprite == SPRITES["panorama_stars"]:
                p.position = [p.position[0]+(1 if self.in_space else 0), p.position[1]]
                p.old_position = [LERP(p.old_position[i], p.position[i], 0.1) for i in range(2)]
                if p.position[0] > self.display.get_width():
                    p.position = [-self.display.get_width(), 0]
                    p.old_position = p.position[:]
                if randint(0,100) > 99:
                    p.sprite_offset = p.sprite_offset + 1
                sprite, position = p.get_surf(self.display, self.cam)
                targets.append((pygame.transform.scale(sprite, (self.display.get_width(), self.display.get_height())), p.old_position))
            elif p._sprite == SPRITES["panorama_planet"]:
                p.position = [0,self.display.get_height()] if self.in_space else [0, 0]
                p.old_position = [LERP(p.old_position[i], p.position[i], 0.1) for i in range(2)]
                sprite, position = p.get_surf(self.display, self.cam)
                targets.append((pygame.transform.scale(sprite, (self.display.get_width(), self.display.get_height())), p.old_position))

        self.display.fill(self.color)
        self.display.blits(targets)

    def draw_background(self):
        targets= []
        for bg in self.background:
            targets.append(bg.get_surf(self.display, self.cam))
        for fg in self.tiles:
            targets.append(fg.get_surf(self.display, self.cam))

        self.display.blits(targets)

    def text_surface(self, content, color):
        return self.basic_font.render(content, True, color)

    def draw_world(self):
        targets = []
        for entity in self.entities:
            sprite, position = entity.get_surf(self.display, self.cam)
            entity.old_position = [LERP(entity.old_position[i], entity.position[i], (0.1 if self.in_space else 0.5)) for i in range(2)]
            targets.append((sprite, position))
            if type(entity) is Player and entity.inventory:
                inventory_sprite, inventory_position = entity.inventory.get_surf(self.display, self.cam)
                offset = [HELDSIZE if entity.facing_right else -HELDSIZE, 0]

                targets.append((
                    pygame.transform.scale(
                        pygame.transform.flip(
                            inventory_sprite, True, False)
                        if entity.facing_right else inventory_sprite, (HELDSIZE, HELDSIZE)), [position[i] + offset[i] + TILESIZE/2 - HELDSIZE/2 for i in range(2)]))

            if type(entity) is Item and entity.data and "item" in entity.data and entity.data["itemcount"] != 0:
                inventory_sprite, inventory_position = ITEMS[entity.data["item"]](entity.position).get_surf(self.display, self.cam)
                targets.append((
                    pygame.transform.scale(
                        inventory_sprite,
                        (HELDSIZE, HELDSIZE)
                        ), [position[i] + TILESIZE/2 - HELDSIZE/2 for i in range(2)]))

                col = (133, 187, 101)
                if entity.data["cost"] > self.money:
                    col = (255, 0, 0)

                cost_txt = pygame.transform.scale(self.text_surface(str(entity.data["cost"]), col), (TILESIZE, TILESIZE))
                targets.append([cost_txt, [position[i] + [0, -TILESIZE][i] for i in range(2)]])

        from pygame_objects import SPRITES
        for part in self.particles:
            relpos, kind = part
            abspos = [(relpos[i]-self.cam[i]-0.5)*TILESIZE + self.display.get_size()[i]/2 for i in range(2)]
            targets.append((SPRITES[kind], abspos))

        self.display.blits(targets)


    def draw_hud(self, tick_portion_left):
        # Fatigue bar
        if self.player.fatigue:
            color = [255, 0, 0]
        else:
            color = [0, 255, 0]
        pygame.draw.rect(self.display, color, (0, 0, self.display.get_width()*(1-tick_portion_left), 50))

        # Health
        base = [self.display.get_size()[i]-TILESIZE for i in range(2)]
        heart = pygame.Surface((TILESIZE, TILESIZE))
        heart.fill((255, 0, 0))
        for i in range(self.player.health):
            self.display.blit(heart, (int(base[0]-i*TILESIZE*1.1), base[1]))

        # Money
        money_text = pygame.transform.scale(self.text_surface("$ {}".format(self.money), (133, 187, 101)), (int(self.display.get_width()/6), int(self.display.get_height()/10)))
        self.display.blit(money_text, (
            int(self.display.get_width()-money_text.get_width()-10),
            int(self.display.get_height()-money_text.get_height()-10-TILESIZE)))

        # Planet
        planet_text = pygame.transform.scale(self.text_surface("Planet {}".format(self.planet), (30, 100, 255)), (int(self.display.get_width()/5), int(self.display.get_height()/10)))
        self.display.blit(planet_text, (
            int(self.display.get_width()-planet_text.get_width()-10),
            int(self.display.get_height()-planet_text.get_height()-100)))

        # Ticks left
        if self.in_space:
            time_text = pygame.transform.scale(self.text_surface("Turns remaining {}".format(max(0, self.console_available-self.tick_count)), (255, 255, 255)), (int(self.display.get_width()/5), int(self.display.get_height()/10)))
            self.display.blit(time_text, (
                int(self.display.get_width()-time_text.get_width()-10),
                int(self.display.get_height()-time_text.get_height()-200)))

