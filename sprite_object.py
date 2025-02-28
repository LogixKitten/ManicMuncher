import pygame as pg
from utils import resource_path
from settings import *
import os
from collections import deque


class SpriteObject:
    def __init__(self, game, path=resource_path('resources/textures/Nostalgia/Points/pellet.png'),
                 pos=(10.5, 3.5), scale=0.7, shift=0.27):
        self.game = game
        self.player = game.player
        self.x, self.y = pos
        self.image = pg.image.load(path).convert_alpha()
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.image.get_width() // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
        self.sprite_half_width = 0
        self.SPRITE_SCALE = scale
        self.SPRITE_HEIGHT_SHIFT = shift

        self.alive = True
        self.name = "pellet"
        self.ray_cast_value = False
        self.collect_dist = 0.65
        self.player_search_trigger = False
        self.munch_audio = pg.mixer.Channel(10)

    def collect_item(self):
        if self.name == "pellet":
            self.alive = False
            if not self.munch_audio.get_busy():
                self.munch_audio.play(self.player.munch)
            index = self.game.object_handler.sprite_point_list.index(self)
            self.game.object_handler.remove_point(self.game.object_handler.sprite_point_list[index])
            self.player.points_consumed += 1
            self.player.add_score(SCORE_POINT)
        elif self.name == "powerup":
            self.alive = False
            self.game.sound.collect_powerup.play()
            index2 = self.game.object_handler.sprite_powerup_list.index(self)
            self.game.object_handler.remove_powerup(self.game.object_handler.sprite_powerup_list[index2])
            self.player.powerups_consumed += 1
            self.player.add_score(SCORE_POWERUP)
        elif self.name == "bonus1":
            self.game.object_handler.remove_bonus(self.game.object_handler.sprite_list[-1])
            self.game.sound.eat_bonus.play()
            self.game.object_handler.bonus_eaten = True
            self.player.add_score(SCORE_BONUS1)
        elif self.name == "bonus2":
            self.game.object_handler.remove_bonus(self.game.object_handler.sprite_list[-1])
            self.game.sound.eat_bonus.play()
            self.game.object_handler.bonus_eaten = True
            self.player.add_score(SCORE_BONUS2)
        elif self.name == "bonus3":
            self.game.object_handler.remove_bonus(self.game.object_handler.sprite_list[-1])
            self.game.sound.eat_bonus.play()
            self.game.object_handler.bonus_eaten = True
            self.player.add_score(SCORE_BONUS3)
        elif self.name == "bonus4":
            self.game.object_handler.remove_bonus(self.game.object_handler.sprite_list[-1])
            self.game.sound.eat_bonus.play()
            self.game.object_handler.bonus_eaten = True
            self.player.add_score(SCORE_BONUS4)
        elif self.name == "bonus5":
            self.game.object_handler.remove_bonus(self.game.object_handler.sprite_list[-1])
            self.game.sound.eat_bonus.play()
            self.game.object_handler.bonus_eaten = True
            self.player.add_score(SCORE_BONUS5)
        elif self.name == "bonus6":
            self.game.object_handler.remove_bonus(self.game.object_handler.sprite_list[-1])
            self.game.sound.eat_bonus.play()
            self.game.object_handler.bonus_eaten = True
            self.player.add_score(SCORE_BONUS6)
        elif self.name == "bonus7":
            self.game.object_handler.remove_bonus(self.game.object_handler.sprite_list[-1])
            self.game.sound.eat_bonus.play()
            self.game.object_handler.bonus_eaten = True
            self.player.add_score(SCORE_BONUS7)
        elif self.name == "bonus8":
            self.game.object_handler.remove_bonus(self.game.object_handler.sprite_list[-1])
            self.game.sound.eat_bonus.play()
            self.game.object_handler.bonus_eaten = True
            self.player.add_score(SCORE_BONUS8)

    def run_logic(self):
        if self.alive:
            self.ray_cast_value = self.ray_cast_player_item()
            if self.ray_cast_value:
                if self.dist < self.collect_dist:
                    self.collect_item()

    @property
    def map_pos(self):
        return int(self.x), int(self.y)

    def ray_cast_player_item(self):
        if self.game.player.map_pos == self.map_pos:
            return True

        player_dist_v, player_dist_h = 0, 0

        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.theta

        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        # horizontals
        y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

        depth_hor = ((y_hor - oy) + 0.00001) / (sin_a + 0.00001)
        x_hor = ox + depth_hor * (cos_a + 0.00001)

        delta_depth = dy / (sin_a + 0.00001)
        dx = delta_depth * (cos_a + 0.00001)

        for i in range(MAX_DEPTH):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor == self.map_pos:
                player_dist_h = depth_hor
                break

            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        # verticals
        x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

        depth_vert = (x_vert - ox) / cos_a
        y_vert = oy + depth_vert * sin_a

        delta_depth = dx / cos_a
        dy = delta_depth * sin_a

        for i in range(MAX_DEPTH):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert == self.map_pos:
                player_dist_v = depth_vert
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        player_dist = max(player_dist_v, player_dist_h)

        if 0 < player_dist:
            return True
        return False

    def get_sprite_projection(self):
        proj = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE
        proj_width, proj_height = proj * self.IMAGE_RATIO, proj

        image = pg.transform.scale(self.image, (proj_width, proj_height))

        self.sprite_half_width = proj_width // 2
        height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT
        pos = self.screen_x - self.sprite_half_width, HALF_HEIGHT - proj_height // 2 + height_shift

        self.game.raycasting.objects_to_render.append((self.norm_dist, image, pos))

    def get_sprite(self):
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.dx, self.dy = dx, dy
        self.theta = math.atan2(dy, dx)

        delta = self.theta - self.player.angle
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau

        delta_rays = delta / DELTA_ANGLE
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE

        self.dist = math.hypot(dx, dy)
        self.norm_dist = self.dist * math.cos(delta)
        if -self.IMAGE_HALF_WIDTH < self.screen_x < (WIDTH + self.IMAGE_HALF_WIDTH) and self.norm_dist > 0.5:
            self.get_sprite_projection()

    def update(self):
        self.get_sprite()
        self.run_logic()


class PointSprite(SpriteObject):
    def __init__(self, game, path=resource_path('resources/textures/Nostalgia/Points/pellet.png'),
                 pos=(10.5, 6.5), scale=0.7, shift=0.27):
        super().__init__(game, path, pos, scale, shift)
        self.name = "pellet"


class PowerupSprite(SpriteObject):
    def __init__(self, game, path=resource_path('resources/textures/Nostalgia/Powerup/powerup.png'),
                 pos=(10.5, 6.5), scale=0.7, shift=0.27):
        super().__init__(game, path, pos, scale, shift)
        self.name = "powerup"


class Bonus1Sprite(SpriteObject):
    def __init__(self, game, path=resource_path('resources/textures/Nostalgia/BonusItems/1.png'),
                 pos=(10.5, 6.5), scale=0.7, shift=0.27):
        super().__init__(game, path, pos, scale, shift)
        self.name = "bonus1"


class Bonus2Sprite(SpriteObject):
    def __init__(self, game, path=resource_path('resources/textures/Nostalgia/BonusItems/2.png'),
                 pos=(10.5, 6.5), scale=0.7, shift=0.27):
        super().__init__(game, path, pos, scale, shift)
        self.name = "bonus2"


class Bonus3Sprite(SpriteObject):
    def __init__(self, game, path=resource_path('resources/textures/Nostalgia/BonusItems/3.png'),
                 pos=(10.5, 6.5), scale=0.7, shift=0.27):
        super().__init__(game, path, pos, scale, shift)
        self.name = "bonus3"


class Bonus4Sprite(SpriteObject):
    def __init__(self, game, path=resource_path('resources/textures/Nostalgia/BonusItems/4.png'),
                 pos=(10.5, 6.5), scale=0.7, shift=0.27):
        super().__init__(game, path, pos, scale, shift)
        self.name = "bonus4"


class Bonus5Sprite(SpriteObject):
    def __init__(self, game, path=resource_path('resources/textures/Nostalgia/BonusItems/5.png'),
                 pos=(10.5, 6.5), scale=0.7, shift=0.27):
        super().__init__(game, path, pos, scale, shift)
        self.name = "bonus5"


class Bonus6Sprite(SpriteObject):
    def __init__(self, game, path=resource_path('resources/textures/Nostalgia/BonusItems/6.png'),
                 pos=(10.5, 6.5), scale=0.7, shift=0.27):
        super().__init__(game, path, pos, scale, shift)
        self.name = "bonus6"


class Bonus7Sprite(SpriteObject):
    def __init__(self, game, path=resource_path('resources/textures/Nostalgia/BonusItems/7.png'),
                 pos=(10.5, 6.5), scale=0.7, shift=0.27):
        super().__init__(game, path, pos, scale, shift)
        self.name = "bonus7"


class Bonus8Sprite(SpriteObject):
    def __init__(self, game, path=resource_path('resources/textures/Nostalgia/BonusItems/8.png'),
                 pos=(10.5, 6.5), scale=0.7, shift=0.27):
        super().__init__(game, path, pos, scale, shift)
        self.name = "bonus8"


class AnimatedSprite(SpriteObject):
    def __init__(self, game, path=resource_path('resources/sprites/animated_sprites/placeholder/0.png'),
                 pos=(11.5, 3.5), scale=0.8, shift=0.16, animation_time=120):
        super().__init__(game, path, pos, scale, shift)
        self.animation_time = animation_time
        self.path = path.rsplit('/', 1)[0]
        self.images = self.get_images(self.path)
        self.animation_time_prev = pg.time.get_ticks()
        self.animation_trigger = False

    def update(self):
        super().update()
        self.check_animation_time()
        self.animate(self.images)

    def animate(self, images):
        if self.animation_trigger:
            images.rotate(-1)
            self.image = images[0]

    def check_animation_time(self):
        self.animation_trigger = False
        time_now = pg.time.get_ticks()
        if time_now - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = time_now
            self.animation_trigger = True

    def get_images(self, path):
        images = deque()
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):
                img = pg.image.load(path + '/' + file_name).convert_alpha()
                images.append(img)
        return images
