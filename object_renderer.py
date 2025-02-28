import pygame as pg
from settings import *
from utils import resource_path

class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.fake_screen
        self.wall_textures = self.load_wall_textures()
        self.sky_offset = 0        
        self.icon_size = 32
        self.ui_scale = []

        if self.game.theme == "Nostalgia":
            self.sky_image = self.get_texture(resource_path('resources/textures/Nostalgia/Sky/sky.png'), (WIDTH, HALF_HEIGHT))

            self.game_over_image = self.get_texture(resource_path('resources/textures/Nostalgia/Screens/game_over.png'), RES)

            self.life_icons = [self.get_texture(resource_path(f'resources/textures/Nostalgia/Lives/{i}.png'), [self.icon_size * 1.5] * 2) for i in range(2)]
            self.life_images = dict(zip(map(str, range(2)), self.life_icons))

            self.level_icons = [self.get_texture(resource_path(f'resources/textures/Nostalgia/BonusItems/{i}.png'), [self.icon_size * 1.5] * 2) for i in range(9)]
            self.level_images = dict(zip(map(str, range(9)), self.level_icons))

            self.powerup_image = self.get_texture(resource_path('resources/textures/Nostalgia/Powerup/powerup.png'), (64, 64))

        elif self.game.theme == "Fallen_Down":
            self.sky_image = self.get_texture(resource_path('resources/textures/Fallen_Down/Sky/sky.png'), (WIDTH, HALF_HEIGHT))

            self.game_over_image = self.get_texture(resource_path('resources/textures/Fallen_Down/Screens/game_over.png'), RES)

            self.life_icons = [self.get_texture(resource_path(f'resources/textures/Fallen_Down/Lives/{i}.png'), [self.icon_size * 1.5] * 2) for i in range(8)]
            self.life_images = dict(zip(map(str, range(8)), self.life_icons))

            self.level_icons = [self.get_texture(resource_path(f'resources/textures/Fallen_Down/BonusItems/{i}.png'), [self.icon_size * 1.5] * 2) for i in range(9)]
            self.level_images = dict(zip(map(str, range(9)), self.level_icons))

            self.powerup_image = self.get_texture(resource_path('resources/textures/Fallen_Down/Powerup/powerup.png'), (128, 128))



    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_ui()

    def draw_ui(self):
        self.game.draw_text("normal", ("Score: " + str(self.game.player.score)), 35, 'white', 400, 20)
        self.game.draw_text("normal", ("Pellets Remaining: " + str(self.game.player.points_left)), 35, 'white', HALF_WIDTH, 20)
        self.game.draw_text("normal", ("High Score: " + str(self.game.player.highscore)), 35, 'white', WIDTH - 400, 20)

        if self.game.theme == "Nostalgia":
            self.game.draw_text("normal", ("Power-Ups"), 32, 'white', 115, HALF_HEIGHT - 235)
            self.game.draw_text("normal", ("[  ]"), 72, 'white', 100, HALF_HEIGHT - 185)
            self.game.draw_text("normal", ("x" + str(self.game.player.powerups_consumed)), 32, 'white', 185, HALF_HEIGHT - 185)

            if self.game.player.powerups_consumed > 0:            
                powerup_rect = self.powerup_image.get_rect()
                powerup_rect.center = (100, HALF_HEIGHT - 185)
                self.screen.blit(self.powerup_image, powerup_rect)

        elif self.game.theme == "Fallen_Down":
            self.game.draw_text("normal", ("Power-Ups"), 32, 'white', 115, HALF_HEIGHT - 225)
            self.game.draw_text("normal", ("[    ]"), 72, 'white', 100, HALF_HEIGHT - 185)
            self.game.draw_text("normal", ("x" + str(self.game.player.powerups_consumed)), 32, 'white', 185, HALF_HEIGHT - 185)

            if self.game.player.powerups_consumed > 0:  
                powerup_rect = self.powerup_image.get_rect()
                powerup_rect.center = (100, HALF_HEIGHT - 200)
                self.screen.blit(self.powerup_image, powerup_rect)

        for i in range(0, 7):
            lives_rect = self.life_icons[self.game.player.current_life_array[i]].get_rect()
            lives_rect.bottomleft = ((HALF_WIDTH - (HALF_WIDTH * 0.97)) + i * (self.icon_size + 20), HEIGHT - 30)
            self.screen.blit(self.life_icons[self.game.player.current_life_array[i]], lives_rect)

        for i in range(0, 7):
            levels_rect = self.level_icons[self.game.player.current_level_array[i]].get_rect()
            levels_rect.bottomright = ((HALF_WIDTH + (HALF_WIDTH * 0.67)) + i * (self.icon_size + 10), HEIGHT - 30)
            self.screen.blit(self.level_icons[self.game.player.current_level_array[i]], levels_rect)

        if 15 >= self.game.player.points_left >= 0:
            self.game.draw_text("normal", ("Closest"), 35, 'white', WIDTH - 100, HALF_HEIGHT - 200)
            self.game.draw_text("normal", ("Pellet"), 35, 'white', WIDTH - 100, HALF_HEIGHT - 168)

            pg.draw.rect(self.screen, self.game.player.dist_bar_color,
                         pg.Rect(WIDTH - 82, HALF_HEIGHT - 100, 5, 200))
            pg.draw.rect(self.screen, self.game.player.dist_bar_color,
                         pg.Rect(WIDTH - 100, ((HALF_HEIGHT - 100) + (self.game.player.closest_point_dist / DIST_BAR_RATIO)), 40, 10))

    def game_over(self):
        self.screen.blit(self.game_over_image, (0, 0))

    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        # floor
        if self.game.theme == "Nostalgia":
            pg.draw.rect(self.screen, (0, 0, 0), (0, HALF_HEIGHT, WIDTH, HEIGHT))
        elif self.game.theme == "Fallen_Down":
            pg.draw.rect(self.screen, (187, 84, 213), (0, HALF_HEIGHT, WIDTH, HEIGHT))    

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        if self.game.theme == "Nostalgia":
            return {
            
                99: self.get_texture(resource_path('resources/textures/Nostalgia/Walls/wall1.png')),
                98: self.get_texture(resource_path('resources/textures/Nostalgia/Walls/EnemyEnclosure.png')),
                97: self.get_texture(resource_path('resources/textures/Nostalgia/Walls/portal.png')),
                96: self.get_texture(resource_path('resources/textures/Nostalgia/Walls/wall2.png')),
                95: self.get_texture(resource_path('resources/textures/Nostalgia/Walls/wall3.png'))
            }
        elif self.game.theme == "Fallen_Down":
            return {
            
                99: self.get_texture(resource_path('resources/textures/Fallen_Down/Walls/wall1.png')),
                98: self.get_texture(resource_path('resources/textures/Fallen_Down/Walls/EnemyEnclosure.png')),
                97: self.get_texture(resource_path('resources/textures/Fallen_Down/Walls/portal.png')),
                96: self.get_texture(resource_path('resources/textures/Fallen_Down/Walls/wall2.png')),
                95: self.get_texture(resource_path('resources/textures/Fallen_Down/Walls/wall3.png'))
            }
