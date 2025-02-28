import pygame as pg
from utils import resource_path


class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.pre_init(44100, 16, 2, 4096)
        pg.mixer.init()
        pg.mixer.set_num_channels(20)        
        self.credit = pg.mixer.Sound(resource_path('resources/sound/credit.wav'))
        self.death = pg.mixer.Sound(resource_path('resources/sound/death.wav'))
        self.eat_bonus = pg.mixer.Sound(resource_path('resources/sound/eat_bonus.wav'))
        self.eat_enemy = pg.mixer.Sound(resource_path('resources/sound/eat_enemy.wav'))
        self.extend = pg.mixer.Sound(resource_path('resources/sound/extend.wav'))
        self.game_start = pg.mixer.Sound(resource_path('resources/sound/game_start.wav'))
        self.intermission = pg.mixer.Sound(resource_path('resources/sound/intermission.wav'))
        self.enemy_scared = pg.mixer.Sound(resource_path('resources/sound/enemy_scared.wav'))
        self.retreating = pg.mixer.Sound(resource_path('resources/sound/retreating.wav'))
        self.siren_1 = pg.mixer.Sound(resource_path('resources/sound/siren_1.wav'))
        self.siren_2 = pg.mixer.Sound(resource_path('resources/sound/siren_2.wav'))
        self.siren_3 = pg.mixer.Sound(resource_path('resources/sound/siren_3.wav'))
        self.bonus_gone = pg.mixer.Sound(resource_path('resources/sound/bonus_gone.wav'))
        self.collect_powerup = pg.mixer.Sound(resource_path('resources/sound/collect_powerup.wav'))
