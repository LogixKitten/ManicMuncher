import time
from utils import resource_path

from sprite_object import *


class NPC(AnimatedSprite):
    def __init__(self, game, path=resource_path('resources/textures/Nostalgia/Enemies/enemy1/0.png'), pos=(10, 6),
                 scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.eaten_images = self.get_images(self.path + '/eaten')
        self.scared_images = self.get_images(self.path + '/scared')
        self.walk_images = self.get_images(self.path + '/walk')

        self.name = "enemy1"
        self.attack_dist = 0.5
        self.size = 20
        self.alive = True
        self.enemy1_scared = False
        self.enemy2_scared = False
        self.enemy3_scared = False
        self.enemy4_scared = False

        self.enemy1_siren1 = False
        self.enemy1_siren2 = False
        self.enemy1_siren3 = False

        self.enemy2_siren1 = False
        self.enemy2_siren2 = False
        self.enemy2_siren3 = False

        self.enemy3_siren1 = False
        self.enemy3_siren2 = False
        self.enemy3_siren3 = False

        self.enemy4_siren1 = False
        self.enemy4_siren2 = False
        self.enemy4_siren3 = False

        self.enemy1_scared_sound = False
        self.enemy2_scared_sound = False
        self.enemy3_scared_sound = False
        self.enemy4_scared_sound = False

        self.enemy1_eaten_sound = False
        self.enemy2_eaten_sound = False
        self.enemy3_eaten_sound = False
        self.enemy4_eaten_sound = False

    def attack(self):
        self.game.player.get_damage()

    def check_if_scared(self):
        if self.name == "enemy1":
            if not self.game.player.enemy1_was_scared:
                self.enemy1_scared = self.game.player.enemy1_scared
        elif self.name == "enemy2":
            if not self.game.player.enemy2_was_scared:
                self.enemy2_scared = self.game.player.enemy2_scared
        elif self.name == "enemy3":
            if not self.game.player.enemy3_was_scared:
                self.enemy3_scared = self.game.player.enemy3_scared
        elif self.name == "enemy4":
            if not self.game.player.enemy4_was_scared:
                self.enemy4_scared = self.game.player.enemy4_scared

    def get_eaten(self):
        self.alive = False
        if self.name == "enemy1":
            self.game.player.enemy1_scared = False
        elif self.name == "enemy2":
            self.game.player.enemy2_scared = False
        elif self.name == "enemy3":
            self.game.player.enemy3_scared = False
        elif self.name == "enemy4":
            self.game.player.enemy4_scared = False
        self.player.cons_enemy += 1
        self.game.sound.eat_enemy.play()
        if self.player.cons_enemy == 1:
            self.player.add_score(SCORE_ENEMY1)
        elif self.player.cons_enemy == 2:
            self.player.add_score(SCORE_ENEMY2)
        elif self.player.cons_enemy == 3:
            self.player.add_score(SCORE_ENEMY3)
        elif self.player.cons_enemy == 4:
            self.player.add_score(SCORE_ENEMY4)

    def play_sound(self):
        if self.alive:
            if self.name == "enemy1":
                if not self.player.enemy1_was_scared:
                    if self.enemy1_scared:
                        if not self.enemy1_scared_sound:
                            self.game.object_handler.enemy1_audio.stop()
                            self.game.object_handler.enemy1_audio.play(self.game.sound.enemy_scared, loops=-1)
                            self.enemy1_scared_sound = True
                            self.enemy1_eaten_sound = False
                            self.enemy1_siren1 = False
                            self.enemy1_siren2 = False
                            self.enemy1_siren3 = False
            elif self.name == "enemy2":
                if not self.player.enemy2_was_scared:
                    if self.enemy2_scared:
                        if not self.enemy2_scared_sound:
                            self.game.object_handler.enemy2_audio.stop()
                            self.game.object_handler.enemy2_audio.play(self.game.sound.enemy_scared, loops=-1)
                            self.enemy2_scared_sound = True
                            self.enemy2_eaten_sound = False
                            self.enemy2_siren1 = False
                            self.enemy2_siren2 = False
                            self.enemy2_siren3 = False
            elif self.name == "enemy3":
                if not self.player.enemy3_was_scared:
                    if self.enemy3_scared:
                        if not self.enemy3_scared_sound:
                            self.game.object_handler.enemy3_audio.stop()
                            self.game.object_handler.enemy3_audio.play(self.game.sound.enemy_scared, loops=-1)
                            self.enemy3_scared_sound = True
                            self.enemy3_eaten_sound = False
                            self.enemy3_siren1 = False
                            self.enemy3_siren2 = False
                            self.enemy3_siren3 = False
            elif self.name == "enemy4":
                if not self.player.enemy4_was_scared:
                    if self.enemy4_scared:
                        if not self.enemy4_scared_sound:
                            self.game.object_handler.enemy4_audio.stop()
                            self.game.object_handler.enemy4_audio.play(self.game.sound.enemy_scared, loops=-1)
                            self.enemy4_scared_sound = True
                            self.enemy4_eaten_sound = False
                            self.enemy4_siren1 = False
                            self.enemy4_siren2 = False
                            self.enemy4_siren3 = False

            if 320 >= self.player.points_left >= 80:
                if self.name == "enemy1":
                    if not self.enemy1_scared:
                        if not self.enemy1_siren1:
                            self.game.object_handler.enemy1_audio.stop()
                            self.game.object_handler.enemy1_audio.play(self.game.sound.siren_1, loops=-1)
                            self.enemy1_scared_sound = False
                            self.enemy1_eaten_sound = False
                            self.enemy1_siren1 = True
                            self.enemy1_siren2 = False
                            self.enemy1_siren3 = False
                if self.name == "enemy2":
                    if not self.enemy2_scared:
                        if not self.enemy2_siren1:
                            self.game.object_handler.enemy2_audio.stop()
                            self.game.object_handler.enemy2_audio.play(self.game.sound.siren_1, loops=-1)
                            self.enemy2_scared_sound = False
                            self.enemy2_eaten_sound = False
                            self.enemy2_siren1 = True
                            self.enemy2_siren2 = False
                            self.enemy2_siren3 = False
                if self.name == "enemy3":
                    if not self.enemy3_scared:
                        if not self.enemy3_siren1:
                            self.game.object_handler.enemy3_audio.stop()
                            self.game.object_handler.enemy3_audio.play(self.game.sound.siren_1, loops=-1)
                            self.enemy3_scared_sound = False
                            self.enemy3_eaten_sound = False
                            self.enemy3_siren1 = True
                            self.enemy3_siren2 = False
                            self.enemy3_siren3 = False
                if self.name == "enemy4":
                    if not self.enemy4_scared:
                        if not self.enemy4_siren1:
                            self.game.object_handler.enemy4_audio.stop()
                            self.game.object_handler.enemy4_audio.play(self.game.sound.siren_1, loops=-1)
                            self.enemy4_scared_sound = False
                            self.enemy4_eaten_sound = False
                            self.enemy4_siren1 = True
                            self.enemy4_siren2 = False
                            self.enemy4_siren3 = False
            elif 79 >= self.player.points_left >= 16:
                if self.name == "enemy1":
                    if not self.enemy1_scared:
                        if not self.enemy1_siren2:
                            self.game.object_handler.enemy1_audio.stop()
                            self.game.object_handler.enemy1_audio.play(self.game.sound.siren_2, loops=-1)
                            self.enemy1_scared_sound = False
                            self.enemy1_eaten_sound = False
                            self.enemy1_siren1 = False
                            self.enemy1_siren2 = True
                            self.enemy1_siren3 = False
                if self.name == "enemy2":
                    if not self.enemy2_scared:
                        if not self.enemy2_siren2:
                            self.game.object_handler.enemy2_audio.stop()
                            self.game.object_handler.enemy2_audio.play(self.game.sound.siren_2, loops=-1)
                            self.enemy2_scared_sound = False
                            self.enemy2_eaten_sound = False
                            self.enemy2_siren1 = False
                            self.enemy2_siren2 = True
                            self.enemy2_siren3 = False
                if self.name == "enemy3":
                    if not self.enemy3_scared:
                        if not self.enemy3_siren2:
                            self.game.object_handler.enemy3_audio.stop()
                            self.game.object_handler.enemy3_audio.play(self.game.sound.siren_2, loops=-1)
                            self.enemy3_scared_sound = False
                            self.enemy3_eaten_sound = False
                            self.enemy3_siren1 = False
                            self.enemy3_siren2 = True
                            self.enemy3_siren3 = False
                if self.name == "enemy4":
                    if not self.enemy4_scared:
                        if not self.enemy4_siren2:
                            self.game.object_handler.enemy4_audio.stop()
                            self.game.object_handler.enemy4_audio.play(self.game.sound.siren_2, loops=-1)
                            self.enemy4_scared_sound = False
                            self.enemy4_eaten_sound = False
                            self.enemy4_siren1 = False
                            self.enemy4_siren2 = True
                            self.enemy4_siren3 = False
            elif 15 >= self.player.points_left >= 0:
                if self.name == "enemy1":
                    if not self.enemy1_scared:
                        if not self.enemy1_siren3:
                            self.game.object_handler.enemy1_audio.stop()
                            self.game.object_handler.enemy1_audio.play(self.game.sound.siren_3, loops=-1)
                            self.enemy1_scared_sound = False
                            self.enemy1_eaten_sound = False
                            self.enemy1_siren1 = False
                            self.enemy1_siren2 = False
                            self.enemy1_siren3 = True
                if self.name == "enemy2":
                    if not self.enemy2_scared:
                        if not self.enemy2_siren3:
                            self.game.object_handler.enemy2_audio.stop()
                            self.game.object_handler.enemy2_audio.play(self.game.sound.siren_3, loops=-1)
                            self.enemy2_scared_sound = False
                            self.enemy2_eaten_sound = False
                            self.enemy2_siren1 = False
                            self.enemy2_siren2 = False
                            self.enemy2_siren3 = True
                if self.name == "enemy3":
                    if not self.enemy3_scared:
                        if not self.enemy3_siren3:
                            self.game.object_handler.enemy3_audio.stop()
                            self.game.object_handler.enemy3_audio.play(self.game.sound.siren_3, loops=-1)
                            self.enemy3_scared_sound = False
                            self.enemy3_eaten_sound = False
                            self.enemy3_siren1 = False
                            self.enemy3_siren2 = False
                            self.enemy3_siren3 = True
                if self.name == "enemy4":
                    if not self.enemy4_scared:
                        if not self.enemy4_siren3:
                            self.game.object_handler.enemy4_audio.stop()
                            self.game.object_handler.enemy4_audio.play(self.game.sound.siren_3, loops=-1)
                            self.enemy4_scared_sound = False
                            self.enemy4_eaten_sound = False
                            self.enemy4_siren1 = False
                            self.enemy4_siren2 = False
                            self.enemy4_siren3 = True
        else:
            if self.name == "enemy1":
                if not self.enemy1_eaten_sound:
                    self.game.object_handler.enemy1_audio.stop()
                    self.game.object_handler.enemy1_audio.play(self.game.sound.retreating, loops=-1)
                    self.enemy1_scared_sound = False
                    self.enemy1_eaten_sound = True
                    self.enemy1_siren1 = False
                    self.enemy1_siren2 = False
                    self.enemy1_siren3 = False
            if self.name == "enemy2":
                if not self.enemy2_eaten_sound:
                    self.game.object_handler.enemy2_audio.stop()
                    self.game.object_handler.enemy2_audio.play(self.game.sound.retreating, loops=-1)
                    self.enemy2_scared_sound = False
                    self.enemy2_eaten_sound = True
                    self.enemy2_siren1 = False
                    self.enemy2_siren2 = False
                    self.enemy2_siren3 = False
            if self.name == "enemy3":
                if not self.enemy3_eaten_sound:
                    self.game.object_handler.enemy3_audio.stop()
                    self.game.object_handler.enemy3_audio.play(self.game.sound.retreating, loops=-1)
                    self.enemy3_scared_sound = False
                    self.enemy3_eaten_sound = True
                    self.enemy3_siren1 = False
                    self.enemy3_siren2 = False
                    self.enemy3_siren3 = False
            if self.name == "enemy4":
                if not self.enemy4_eaten_sound:
                    self.game.object_handler.enemy4_audio.stop()
                    self.game.object_handler.enemy4_audio.play(self.game.sound.retreating, loops=-1)
                    self.enemy4_scared_sound = False
                    self.enemy4_eaten_sound = True
                    self.enemy4_siren1 = False
                    self.enemy4_siren2 = False
                    self.enemy4_siren3 = False

    def get_player_distance(self):
        player_dist = math.hypot(self.x - self.game.player.x, self.y - self.game.player.y)

        if self.name == "enemy1":
            self.game.player.enemy1_distance = player_dist
        elif self.name == "enemy2":
            self.game.player.enemy2_distance = player_dist
        elif self.name == "enemy3":
            self.game.player.enemy4_distance = player_dist
        elif self.name == "enemy4":
            self.game.player.enemy4_distance = player_dist

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map_barriers

    def check_wall_collision(self, dx, dy):
        if self.check_wall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy

    def move_chase(self):
        next_pos = self.game.pathfinding.get_path(self.map_pos, self.game.player.map_pos)
        center_x, center_y = (next_pos[0] + 0.5), (next_pos[1] + 0.5)
        next_x = center_x
        next_y = center_y

        if not self.name == "enemy1":
            angle = math.atan2(next_y - self.y, next_x - self.x)
            dx = math.cos(angle) * self.game.player.enemy_speed
            dy = math.sin(angle) * self.game.player.enemy_speed
        else:
            angle = math.atan2(next_y - self.y, next_x - self.x)
            dx = math.cos(angle) * self.game.player.enemy1_speed
            dy = math.sin(angle) * self.game.player.enemy1_speed
        self.check_wall_collision(dx, dy)

    def move_scatter(self):
        if self.name == "enemy1":
            enemy1_scatter_pos = (int(self.game.player.enemy1_scatter_target[0]), int(self.game.player.enemy1_scatter_target[1]))
            next_pos = self.game.pathfinding.get_path(self.map_pos, enemy1_scatter_pos)
            center_x, center_y = (next_pos[0] + 0.5), (next_pos[1] + 0.5)
            next_x = center_x
            next_y = center_y

            angle = math.atan2(next_y - self.y, next_x - self.x)
            dx = math.cos(angle) * self.game.player.enemy_speed
            dy = math.sin(angle) * self.game.player.enemy_speed

        elif self.name == "enemy2":
            enemy2_scatter_pos = (int(self.game.player.enemy2_scatter_target[0]), int(self.game.player.enemy2_scatter_target[1]))
            next_pos = self.game.pathfinding.get_path(self.map_pos, enemy2_scatter_pos)
            center_x, center_y = (next_pos[0] + 0.5), (next_pos[1] + 0.5)
            next_x = center_x
            next_y = center_y

            angle = math.atan2(next_y - self.y, next_x - self.x)
            dx = math.cos(angle) * self.game.player.enemy_speed
            dy = math.sin(angle) * self.game.player.enemy_speed

        elif self.name == "enemy3":
            enemy3_scatter_pos = (int(self.game.player.enemy3_scatter_target[0]), int(self.game.player.enemy3_scatter_target[1]))
            next_pos = self.game.pathfinding.get_path(self.map_pos, enemy3_scatter_pos)
            center_x, center_y = (next_pos[0] + 0.5), (next_pos[1] + 0.5)
            next_x = center_x
            next_y = center_y

            angle = math.atan2(next_y - self.y, next_x - self.x)
            dx = math.cos(angle) * self.game.player.enemy_speed
            dy = math.sin(angle) * self.game.player.enemy_speed

        elif self.name == "enemy4":
            enemy4_scatter_pos = (int(self.game.player.enemy4_scatter_target[0]), int(self.game.player.enemy4_scatter_target[1]))
            next_pos = self.game.pathfinding.get_path(self.map_pos, enemy4_scatter_pos)
            center_x, center_y = (next_pos[0] + 0.5), (next_pos[1] + 0.5)
            next_x = center_x
            next_y = center_y

            angle = math.atan2(next_y - self.y, next_x - self.x)
            dx = math.cos(angle) * self.game.player.enemy_speed
            dy = math.sin(angle) * self.game.player.enemy_speed

        self.check_wall_collision(dx, dy)

    def move_scared(self):
        if self.name == "enemy1":
            enemy1_scared_pos = (int(self.game.player.enemy1_scared_target[0]), int(self.game.player.enemy1_scared_target[1]))
            next_pos = self.game.pathfinding.get_path(self.map_pos, enemy1_scared_pos)
            center_x, center_y = (next_pos[0] + 0.5), (next_pos[1] + 0.5)
            next_x = center_x
            next_y = center_y

            angle = math.atan2(next_y - self.y, next_x - self.x)
            dx = math.cos(angle) * self.game.player.scared_speed
            dy = math.sin(angle) * self.game.player.scared_speed

        elif self.name == "enemy2":
            enemy2_scared_pos = (int(self.game.player.enemy2_scared_target[0]), int(self.game.player.enemy2_scared_target[1]))
            next_pos = self.game.pathfinding.get_path(self.map_pos, enemy2_scared_pos)
            center_x, center_y = (next_pos[0] + 0.5), (next_pos[1] + 0.5)
            next_x = center_x
            next_y = center_y

            angle = math.atan2(next_y - self.y, next_x - self.x)
            dx = math.cos(angle) * self.game.player.scared_speed
            dy = math.sin(angle) * self.game.player.scared_speed

        elif self.name == "enemy3":
            enemy3_scared_pos = (int(self.game.player.enemy3_scared_target[0]), int(self.game.player.enemy3_scared_target[1]))
            next_pos = self.game.pathfinding.get_path(self.map_pos, enemy3_scared_pos)
            center_x, center_y = (next_pos[0] + 0.5), (next_pos[1] + 0.5)
            next_x = center_x
            next_y = center_y

            angle = math.atan2(next_y - self.y, next_x - self.x)
            dx = math.cos(angle) * self.game.player.scared_speed
            dy = math.sin(angle) * self.game.player.scared_speed

        elif self.name == "enemy4":
            enemy4_scared_pos = (int(self.game.player.enemy4_scared_target[0]), int(self.game.player.enemy4_scared_target[1]))
            next_pos = self.game.pathfinding.get_path(self.map_pos, enemy4_scared_pos)
            center_x, center_y = (next_pos[0] + 0.5), (next_pos[1] + 0.5)
            next_x = center_x
            next_y = center_y

            angle = math.atan2(next_y - self.y, next_x - self.x)
            dx = math.cos(angle) * self.game.player.scared_speed
            dy = math.sin(angle) * self.game.player.scared_speed

        self.check_wall_collision(dx, dy)

    def move_eaten(self):
        respawn_point = (9, 10)
        next_pos = self.game.pathfinding.get_path(self.map_pos, respawn_point)
        center_x, center_y = (next_pos[0] + 0.5), (next_pos[1] + 0.5)
        next_x = center_x
        next_y = center_y

        angle = math.atan2(next_y - self.y, next_x - self.x)
        dx = math.cos(angle) * self.game.player.eaten_speed
        dy = math.sin(angle) * self.game.player.eaten_speed

        self.check_wall_collision(dx, dy)

        if self.map_pos == respawn_point:
            self.alive = True
            if self.name == "enemy1":
                self.game.player.enemy1_scared = False
            elif self.name == "enemy2":
                self.game.player.enemy2_scared = False
            elif self.name == "enemy3":
                self.game.player.enemy3_scared = False
            elif self.name == "enemy4":
                self.game.player.enemy4_scared = False

    def update(self):
        self.check_animation_time()
        self.get_sprite()
        self.run_logic()

    def run_logic(self):
        self.play_sound()
        if self.alive:
            self.get_player_distance()

            if self.name == "enemy1":
                if self.enemy1_scared:
                    self.animate(self.scared_images)
                    self.move_scared()
                    self.check_if_scared()
                    if self.dist < self.attack_dist:
                        self.get_eaten()
                else:
                    self.animate(self.walk_images)
                    if self.game.player.scatter:
                        self.move_scatter()
                    else:
                        self.move_chase()
                    self.player.cruise_elroy()
                    self.check_if_scared()
                    if self.dist < self.attack_dist:
                        self.attack()
            elif self.name == "enemy2":
                if self.enemy2_scared:
                    self.animate(self.scared_images)
                    self.move_scared()
                    self.check_if_scared()
                    if self.dist < self.attack_dist:
                        self.get_eaten()
                else:
                    self.animate(self.walk_images)
                    if self.game.player.scatter:
                        self.move_scatter()
                    else:
                        self.move_chase()
                    self.player.cruise_elroy()
                    self.check_if_scared()
                    if self.dist < self.attack_dist:
                        self.attack()
            elif self.name == "enemy3":
                if self.enemy3_scared:
                    self.animate(self.scared_images)
                    self.move_scared()
                    self.check_if_scared()
                    if self.dist < self.attack_dist:
                        self.get_eaten()
                else:
                    self.animate(self.walk_images)
                    if self.game.player.scatter:
                        self.move_scatter()
                    else:
                        self.move_chase()
                    self.player.cruise_elroy()
                    self.check_if_scared()
                    if self.dist < self.attack_dist:
                        self.attack()
            elif self.name == "enemy4":
                if self.enemy4_scared:
                    self.animate(self.scared_images)
                    self.move_scared()
                    self.check_if_scared()
                    if self.dist < self.attack_dist:
                        self.get_eaten()
                else:
                    self.animate(self.walk_images)
                    if self.game.player.scatter:
                        self.move_scatter()
                    else:
                        self.move_chase()
                    self.player.cruise_elroy()
                    self.check_if_scared()
                    if self.dist < self.attack_dist:
                        self.attack()
        else:
            self.animate(self.eaten_images)
            self.move_eaten()

    @property
    def map_pos(self):
        return int(self.x), int(self.y)


class Enemy1NPC(NPC):
    def __init__(self, game, path='resources/textures/Nostalgia/Enemies/enemy1/0.png', pos=(10.5, 6.5),
                 scale=0.7, shift=0.27, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.name = "enemy1"


class Enemy2NPC(NPC):
    def __init__(self, game, path=resource_path('resources/textures/Nostalgia/Enemies/enemy2/0.png'), pos=(10.5, 6.5),
                 scale=0.7, shift=0.27, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.name = "enemy2"


class Enemy3NPC(NPC):
    def __init__(self, game, path=resource_path('resources/textures/Nostalgia/Enemies/enemy3/0.png'), pos=(10.5, 6.5),
                 scale=0.7, shift=0.27, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.name = "enemy3"


class Enemy4NPC(NPC):
    def __init__(self, game, path=resource_path('resources/textures/Nostalgia/Enemies/enemy4/0.png'), pos=(10.5, 6.5),
                 scale=0.7, shift=0.27, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.name = "enemy4"
