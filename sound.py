import pygame as pg


class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.pre_init(44100, 16, 2, 4096)
        pg.mixer.init()
        pg.mixer.set_num_channels(20)
        self.path = 'resources/sound/'
        self.credit = pg.mixer.Sound(self.path + 'credit.wav')
        self.death = pg.mixer.Sound(self.path + 'death.wav')
        self.eat_bonus = pg.mixer.Sound(self.path + 'eat_bonus.wav')
        self.eat_enemy = pg.mixer.Sound(self.path + 'eat_enemy.wav')
        self.extend = pg.mixer.Sound(self.path + 'extend.wav')
        self.game_start = pg.mixer.Sound(self.path + 'game_start.wav')
        self.intermission = pg.mixer.Sound(self.path + 'intermission.wav')
        self.enemy_scared = pg.mixer.Sound(self.path + 'enemy_scared.wav')
        self.retreating = pg.mixer.Sound(self.path + 'retreating.wav')
        self.siren_1 = pg.mixer.Sound(self.path + 'siren_1.wav')
        self.siren_2 = pg.mixer.Sound(self.path + 'siren_2.wav')
        self.siren_3 = pg.mixer.Sound(self.path + 'siren_3.wav')
        self.bonus_gone = pg.mixer.Sound(self.path + 'bonus_gone.wav')
        self.collect_powerup = pg.mixer.Sound(self.path + 'collect_powerup.wav')
