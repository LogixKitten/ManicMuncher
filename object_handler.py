import pygame as pg
from npc import *
from utils import resource_path


class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.sprite_point_list = []
        self.sprite_powerup_list = []
        self.npc_list = []
        self.npc_sprite_path = resource_path('resources/sprites/npc/')
        self.static_sprite_path = resource_path('resources/sprites/static_sprites/')
        self.anim_sprite_path = resource_path('resources/sprites/animated_sprites/')
        self.npc_positions = {}
        self.point_positions = [[1.5, 1.5], [2, 1.5], [2.5, 1.5], [3, 1.5], [3.5, 1.5], [4, 1.5], [4.5, 1.5], [5, 1.5],
                                 [5.5, 1.5], [6, 1.5], [6.5, 1.5], [7, 1.5], [7.5, 1.5], [8, 1.5], [8.5, 1.5],
                                 [10.5, 1.5], [11, 1.5], [11.5, 1.5], [12, 1.5], [12.5, 1.5], [13, 1.5], [13.5, 1.5],
                                 [14, 1.5], [14.5, 1.5], [15, 1.5], [15.5, 1.5], [16, 1.5], [16.5, 1.5], [17, 1.5],
                                 [17.5, 1.5], [1.5, 2], [4.5, 2], [8.5, 2], [10.5, 2], [14.5, 2], [17.5, 2], [4.5, 2.5],
                                 [8.5, 2.5], [10.5, 2.5], [14.5, 2.5], [1.5, 3], [4.5, 3], [8.5, 3], [10.5, 3],
                                 [14.5, 3], [17.5, 3], [1.5, 3.5], [4.5, 3.5], [8.5, 3.5], [10.5, 3.5], [14.5, 3.5],
                                 [17.5, 3.5], [1.5, 4], [4.5, 4], [8.5, 4], [10.5, 4], [14.5, 4], [17.5, 4], [1.5, 4.5],
                                 [2, 4.5], [2.5, 4.5], [3, 4.5], [3.5, 4.5], [4, 4.5], [4.5, 4.5], [5, 4.5], [5.5, 4.5],
                                 [6, 4.5], [6.5, 4.5], [7, 4.5], [7.5, 4.5], [8, 4.5], [8.5, 4.5], [9, 4.5], [9.5, 4.5],
                                 [10, 4.5], [10.5, 4.5], [11, 4.5], [11.5, 4.5], [12, 4.5], [12.5, 4.5], [13, 4.5],
                                 [13.5, 4.5], [14, 4.5], [14.5, 4.5], [15, 4.5], [15.5, 4.5], [16, 4.5], [16.5, 4.5],
                                 [17, 4.5], [17.5, 4.5], [1.5, 5], [4.5, 5], [6.5, 5], [12.5, 5], [14.5, 5], [17.5, 5],
                                 [1.5, 5.5], [4.5, 5.5], [6.5, 5.5], [12.5, 5.5], [14.5, 5.5], [17.5, 5.5], [1.5, 6],
                                 [4.5, 6], [6.5, 6], [12.5, 6], [14.5, 6], [17.5, 6], [1.5, 6.5], [2, 6.5], [2.5, 6.5],
                                 [3, 6.5], [3.5, 6.5], [4, 6.5], [4.5, 6.5], [6.5, 6.5], [7, 6.5], [7.5, 6.5], [8, 6.5],
                                 [8.5, 6.5], [10.5, 6.5], [11, 6.5], [11.5, 6.5], [12, 6.5], [12.5, 6.5], [14.5, 6.5],
                                 [15, 6.5], [15.5, 6.5], [16, 6.5], [16.5, 6.5], [17, 6.5], [17.5, 6.5], [4.5, 7],
                                 [14.5, 7], [4.5, 7.5], [14.5, 7.5], [4.5, 8], [14.5, 8], [4.5, 8.5], [14.5, 8.5],
                                 [4.5, 9], [14.5, 9], [4.5, 9.5], [14.5, 9.5], [4.5, 10], [14.5, 10], [4.5, 10.5],
                                 [14.5, 10.5], [4.5, 11], [14.5, 11], [4.5, 11.5], [14.5, 11.5], [4.5, 12], [14.5, 12],
                                 [4.5, 12.5], [14.5, 12.5], [4.5, 13], [14.5, 13], [4.5, 13.5], [14.5, 13.5], [4.5, 14],
                                 [14.5, 14], [1.5, 14.5], [2, 14.5], [2.5, 14.5], [3, 14.5], [3.5, 14.5], [4, 14.5],
                                 [4.5, 14.5], [5, 14.5], [5.5, 14.5], [6, 14.5], [6.5, 14.5], [7, 14.5], [7.5, 14.5],
                                 [8, 14.5], [8.5, 14.5], [10.5, 14.5], [11, 14.5], [11.5, 14.5], [12, 14.5],
                                 [12.5, 14.5], [13, 14.5], [13.5, 14.5], [14, 14.5], [14.5, 14.5], [15, 14.5],
                                 [15.5, 14.5], [16, 14.5], [16.5, 14.5], [17, 14.5], [17.5, 14.5], [1.5, 15], [4.5, 15],
                                 [8.5, 15], [10.5, 15], [14.5, 15], [17.5, 15], [1.5, 15.5], [4.5, 15.5], [8.5, 15.5],
                                 [10.5, 15.5], [14.5, 15.5], [17.5, 15.5], [1.5, 16], [4.5, 16], [8.5, 16], [10.5, 16],
                                 [14.5, 16], [17.5, 16], [2, 16.5], [2.5, 16.5], [4.5, 16.5], [5, 16.5], [5.5, 16.5],
                                 [6, 16.5], [6.5, 16.5], [7, 16.5], [7.5, 16.5], [8, 16.5], [8.5, 16.5], [10.5, 16.5],
                                 [11, 16.5], [11.5, 16.5], [12, 16.5], [12.5, 16.5], [13, 16.5], [13.5, 16.5],
                                 [14, 16.5], [14.5, 16.5], [16.5, 16.5], [17, 16.5], [2.5, 17], [4.5, 17], [6.5, 17],
                                 [12.5, 17], [14.5, 17], [16.5, 17], [2.5, 17.5], [4.5, 17.5], [6.5, 17.5],
                                 [12.5, 17.5], [14.5, 17.5], [16.5, 17.5], [2.5, 18], [4.5, 18], [6.5, 18], [12.5, 18],
                                 [14.5, 18], [16.5, 18], [1.5, 18.5], [2, 18.5], [2.5, 18.5], [3, 18.5], [3.5, 18.5],
                                 [4, 18.5], [4.5, 18.5], [6.5, 18.5], [7, 18.5], [7.5, 18.5], [8, 18.5], [8.5, 18.5],
                                 [10.5, 18.5], [11, 18.5], [11.5, 18.5], [12, 18.5], [12.5, 18.5], [14.5, 18.5],
                                 [15, 18.5], [15.5, 18.5], [16, 18.5], [16.5, 18.5], [17, 18.5], [17.5, 18.5],
                                 [1.5, 19], [8.5, 19], [10.5, 19], [17.5, 19], [1.5, 19.5], [8.5, 19.5], [10.5, 19.5],
                                 [17.5, 19.5], [1.5, 20], [8.5, 20], [10.5, 20], [17.5, 20], [1.5, 20.5], [2, 20.5],
                                 [2.5, 20.5], [3, 20.5], [3.5, 20.5], [4, 20.5], [4.5, 20.5], [5, 20.5], [5.5, 20.5],
                                 [6, 20.5], [6.5, 20.5], [7, 20.5], [7.5, 20.5], [8, 20.5], [8.5, 20.5], [9, 20.5],
                                 [9.5, 20.5], [10, 20.5], [10.5, 20.5], [11, 20.5], [11.5, 20.5], [12, 20.5],
                                 [12.5, 20.5], [13, 20.5], [13.5, 20.5], [14, 20.5], [14.5, 20.5], [15, 20.5],
                                 [15.5, 20.5], [16, 20.5], [16.5, 20.5], [17, 20.5], [17.5, 20.5]]
        self.points_remaining = 0
        self.spawn_points(game)
        self.powerups_pos = [[1.5, 2.5], [17.5, 2.6], [17.5, 16.5], [1.5, 16.5]]
        self.spawn_powerups(game)
        self.bonus_spawn_pos = [9.5, 12.5]
        self.bonus_spawned = True
        self.bonus_eaten = False
        self.enemy1_audio = pg.mixer.Channel(11)
        self.enemy2_audio = pg.mixer.Channel(12)
        self.enemy3_audio = pg.mixer.Channel(13)
        self.enemy4_audio = pg.mixer.Channel(14)

        # spawn npc
        if self.game.theme == "Nostalgia":
            self.add_npc(Enemy1NPC(self.game, path = resource_path('resources/textures/Nostalgia/Enemies/enemy1/0.png'), pos=(9.5, 8.5)))
            self.add_npc(Enemy2NPC(self.game, path = resource_path('resources/textures/Nostalgia/Enemies/enemy2/0.png'), pos=(8.5, 10.5)))
            self.add_npc(Enemy3NPC(self.game, path = resource_path('resources/textures/Nostalgia/Enemies/enemy3/0.png'), pos=(9.5, 10.5)))
            self.add_npc(Enemy4NPC(self.game, path = resource_path('resources/textures/Nostalgia/Enemies/enemy4/0.png'), pos=(10.5, 10.5)))
        elif self.game.theme == "Fallen_Down":
            self.add_npc(Enemy1NPC(self.game, path = resource_path('resources/textures/Fallen_Down/Enemies/enemy1/0.png'), pos=(9.5, 8.5)))
            self.add_npc(Enemy2NPC(self.game, path = resource_path('resources/textures/Fallen_Down/Enemies/enemy2/0.png'), pos=(8.5, 10.5)))
            self.add_npc(Enemy3NPC(self.game, path = resource_path('resources/textures/Fallen_Down/Enemies/enemy3/0.png'), pos=(9.5, 10.5)))
            self.add_npc(Enemy4NPC(self.game, path = resource_path('resources/textures/Fallen_Down/Enemies/enemy4/0.png'), pos=(10.5, 10.5)))

    def get_remaining_points(self):
        return len(self.sprite_point_list)

    def enemy_audio_positioner(self):
        enemy1_vol = abs((((self.game.player.enemy1_distance - 0.5) * 4) / 100) - 1)
        self.enemy1_audio.set_volume(enemy1_vol)
        enemy2_vol = abs((((self.game.player.enemy2_distance - 0.5) * 4) / 100) - 1)
        self.enemy2_audio.set_volume(enemy2_vol)
        enemy3_vol = abs((((self.game.player.enemy3_distance - 0.5) * 4) / 100) - 1)
        self.enemy3_audio.set_volume(enemy3_vol)
        enemy4_vol = abs((((self.game.player.enemy4_distance - 0.5) * 4) / 100) - 1)
        self.enemy4_audio.set_volume(enemy4_vol)

    def spawn_bonus(self, game):
        x_coor = self.bonus_spawn_pos[0]
        y_coor = self.bonus_spawn_pos[1]
        if self.game.theme == "Nostalgia":
            if self.game.player.current_level == 1:
                self.add_bonus(Bonus1Sprite(game, path = resource_path('resources/textures/Nostalgia/BonusItems/1.png'), pos=(x_coor, y_coor), scale=0.5, shift=0.75))
            elif self.game.player.current_level == 2:
                self.add_bonus(Bonus2Sprite(game, path = resource_path('resources/textures/Nostalgia/BonusItems/2.png'), pos=(x_coor, y_coor), scale=0.5, shift=0.75))
            elif self.game.player.current_level == 3 or self.game.player.current_level == 4:
                self.add_bonus(Bonus3Sprite(game, path = resource_path('resources/textures/Nostalgia/BonusItems/3.png'), pos=(x_coor, y_coor), scale=0.5, shift=0.75))
            elif self.game.player.current_level == 5 or self.game.player.current_level == 6:
                self.add_bonus(Bonus4Sprite(game, path = resource_path('resources/textures/Nostalgia/BonusItems/4.png'), pos=(x_coor, y_coor), scale=0.5, shift=0.75))
            elif self.game.player.current_level == 7 or self.game.player.current_level == 8:
                self.add_bonus(Bonus5Sprite(game, path = resource_path('resources/textures/Nostalgia/BonusItems/5.png'), pos=(x_coor, y_coor), scale=0.5, shift=0.75))
            elif self.game.player.current_level == 9 or self.game.player.current_level == 10:
                self.add_bonus(Bonus6Sprite(game, path = resource_path('resources/textures/Nostalgia/BonusItems/6.png'), pos=(x_coor, y_coor), scale=0.5, shift=0.75))
            elif self.game.player.current_level == 11 or self.game.player.current_level == 12:
                self.add_bonus(Bonus7Sprite(game, path = resource_path('resources/textures/Nostalgia/BonusItems/7.png'), pos=(x_coor, y_coor), scale=0.5, shift=0.75))
            elif self.game.player.current_level >= 13:
                self.add_bonus(Bonus8Sprite(game, path = resource_path('resources/textures/Nostalgia/BonusItems/8.png'), pos=(x_coor, y_coor), scale=0.5, shift=0.75))
            self.game.sound.credit.play(3)
        elif self.game.theme == "Fallen_Down":
            if self.game.player.current_level == 1:
                self.add_bonus(Bonus1Sprite(game, path = resource_path('resources/textures/Fallen_Down/BonusItems/1.png'), pos=(x_coor, y_coor), scale=0.5, shift=0.75))
            elif self.game.player.current_level == 2:
                self.add_bonus(Bonus2Sprite(game, path = resource_path('resources/textures/Fallen_Down/BonusItems/2.png'), pos=(x_coor, y_coor), scale=0.5, shift=0.75))
            elif self.game.player.current_level == 3 or self.game.player.current_level == 4:
                self.add_bonus(Bonus3Sprite(game, path = resource_path('resources/textures/Fallen_Down/BonusItems/3.png'), pos=(x_coor, y_coor), scale=0.5, shift=0.75))
            elif self.game.player.current_level == 5 or self.game.player.current_level == 6:
                self.add_bonus(Bonus4Sprite(game, path = resource_path('resources/textures/Fallen_Down/BonusItems/4.png'), pos=(x_coor, y_coor), scale=0.5, shift=0.75))
            elif self.game.player.current_level == 7 or self.game.player.current_level == 8:
                self.add_bonus(Bonus5Sprite(game, path = resource_path('resources/textures/Fallen_Down/BonusItems/5.png'), pos=(x_coor, y_coor), scale=0.5, shift=0.75))
            elif self.game.player.current_level == 9 or self.game.player.current_level == 10:
                self.add_bonus(Bonus6Sprite(game, path = resource_path('resources/textures/Fallen_Down/BonusItems/6.png'), pos=(x_coor, y_coor), scale=0.5, shift=0.75))
            elif self.game.player.current_level == 11 or self.game.player.current_level == 12:
                self.add_bonus(Bonus7Sprite(game, path = resource_path('resources/textures/Fallen_Down/BonusItems/7.png'), pos=(x_coor, y_coor), scale=0.5, shift=0.75))
            elif self.game.player.current_level >= 13:
                self.add_bonus(Bonus8Sprite(game, path = resource_path('resources/textures/Fallen_Down/BonusItems/8.png'), pos=(x_coor, y_coor), scale=0.5, shift=0.75))
            self.game.sound.credit.play(3)

    def respawn_enemies(self):
        # enemy1
        self.npc_list[0].x = 9.5
        self.npc_list[0].y = 8.5

        # enemy2
        self.npc_list[1].x = 8.5
        self.npc_list[1].y = 10.5

        # enemy3
        self.npc_list[2].x = 9.5
        self.npc_list[2].y = 10.5

        # enemy4
        self.npc_list[3].x = 10.5
        self.npc_list[3].y = 10.5

    def spawn_points(self, game):
        for i in self.point_positions:
            x_coor = i[0]
            y_coor = i[1]
            if self.game.theme == "Nostalgia":
                self.add_point(PointSprite(game, path = resource_path('resources/textures/Nostalgia/Points/pellet.png'), pos=(x_coor, y_coor), scale=0.3, shift=0.75))            
            elif self.game.theme == "Fallen_Down":
                self.add_point(PointSprite(game, path = resource_path('resources/textures/Fallen_Down/Points/candy.png'), pos=(x_coor, y_coor), scale=0.3, shift=0.75))

    def spawn_powerups(self, game):
        for i in self.powerups_pos:
            x_coor = i[0]
            y_coor = i[1]
            if self.game.theme == "Nostalgia":
                self.add_powerups(PowerupSprite(game, path = resource_path('resources/textures/Nostalgia/Powerup/powerup.png'), pos=(x_coor, y_coor), scale=0.69, shift=0.1))
            if self.game.theme == "Fallen_Down":
                self.add_powerups(PowerupSprite(game, path = resource_path('resources/textures/Fallen_Down/Powerup/powerup.png'), pos=(x_coor, y_coor), scale=0.69, shift=0.1))

    def update(self):
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}
        [sprite.update() for sprite in self.sprite_list]
        [sprite.update() for sprite in self.sprite_point_list]
        [sprite.update() for sprite in self.sprite_powerup_list]
        [npc.update() for npc in self.npc_list]
        self.enemy_audio_positioner()

    def add_npc(self, npc):
        self.npc_list.append(npc)

    def add_bonus(self, sprite):
        self.sprite_list.append(sprite)

    def add_point(self, sprite):
        self.sprite_point_list.append(sprite)

    def add_powerups(self, sprite):
        self.sprite_powerup_list.append(sprite)

    def remove_powerup(self, sprite):
        self.sprite_powerup_list.remove(sprite)

    def remove_bonus(self, sprite):
        self.sprite_list.remove(sprite)

    def remove_point(self, sprite):
        self.sprite_point_list.remove(sprite)
