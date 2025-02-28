import random

from settings import *
import pygame as pg
from utils import resource_path
import math
from pyvidplayer import Video
import json

class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = player_pos
        self.angle = PLAYER_ANGLE
        self.direction = 0
        self.lives = PLAYER_MAX_LIVES
        self.current_life_array = [1, 0, 0, 0, 0, 0, 0]
        self.rel = 0
        self.time_prev = pg.time.get_ticks()
        self.font = pg.font.Font(resource_path('resources/fonts/8bitOperatorPlusSC-Regular.ttf'), 40)
        self.score = 0
        self.highscore = self.get_highscore()
        self.is_super = False
        self.hashighscore = False
        self.first_run = True
        self.extra_life = False
        self.current_level = 1
        self.current_level_array = [0, 0, 0, 0, 0, 0, 1]
        self.points_consumed = 0
        self.powerups_consumed = 0
        self.points_left = 0
        self.points_percent = 0
        self.current_siren = ''
        self.sirenPlaying = False
        self.enemy_speed = 0.02
        self.enemy1_speed = 0.02
        self.scared_speed = 0.025
        self.eaten_speed = 0.035
        self.cons_enemy = 0
        self.bool_switch = 1
        self.scatter = True        
        self.munch = pg.mixer.Sound(resource_path('resources/sound/munch.wav'))
        self.enemy1_distance = 0
        self.enemy2_distance = 0
        self.enemy3_distance = 0
        self.enemy4_distance = 0
        self.closest_point_x = 0
        self.closest_point_y = 0
        self.closest_point_dist = 0
        self.closest_point_dir = 0
        self.freeze_player = True

        self.enemy1_scared = False
        self.enemy1_was_scared = False
        self.enemy2_scared = False
        self.enemy2_was_scared = False
        self.enemy3_scared = False
        self.enemy3_was_scared = False
        self.enemy4_scared = False
        self.enemy4_was_scared = False

        self.enemy1_scared_target = [1, 1]
        self.enemy2_scared_target = [1, 1]
        self.enemy3_scared_target = [1, 1]
        self.enemy4_scared_target = [1, 1]

        self.enemy1_scatter_target = [1, 1]
        self.enemy2_scatter_target = [1, 1]
        self.enemy3_scatter_target = [1, 1]
        self.enemy4_scatter_target = [1, 1]

        self.dist_bar_color = (0, 255, 0)

    def get_random_position(self):
        valid_index_number = random.randint(0, 319)
        random_pos = self.game.object_handler.point_positions[valid_index_number]
        return random_pos

    def get_ghost_distance(self):
        self.enemy1_distance = math.sqrt(math.pow((self.game.object_handler.npc_list[0].x - self.x), 2) +
                                         math.pow((self.game.object_handler.npc_list[0].y - self.y), 2))
        self.enemy2_distance = math.sqrt(math.pow((self.game.object_handler.npc_list[1].x - self.x), 2) +
                                        math.pow((self.game.object_handler.npc_list[1].y - self.y), 2))
        self.enemy3_distance = math.sqrt(math.pow((self.game.object_handler.npc_list[2].x - self.x), 2) +
                                       math.pow((self.game.object_handler.npc_list[2].y - self.y), 2))
        self.enemy4_distance = math.sqrt(math.pow((self.game.object_handler.npc_list[3].x - self.x), 2) +
                                        math.pow((self.game.object_handler.npc_list[3].y - self.y), 2))

    def dist_bar_coloring(self):
        if 0 <= self.closest_point_dist <= 1:
            self.dist_bar_color = (0, 255, 0)
        elif 1 < self.closest_point_dist <= 2:
            self.dist_bar_color = (28, 255, 0)
        elif 2 < self.closest_point_dist <= 3:
            self.dist_bar_color = (56, 255, 0)
        elif 3 < self.closest_point_dist <= 4:
            self.dist_bar_color = (84, 255, 0)
        elif 4 < self.closest_point_dist <= 5:
            self.dist_bar_color = (112, 255, 0)
        elif 5 < self.closest_point_dist <= 6:
            self.dist_bar_color = (140, 255, 0)
        elif 6 < self.closest_point_dist <= 7:
            self.dist_bar_color = (168, 255, 0)
        elif 7 < self.closest_point_dist <= 8:
            self.dist_bar_color = (196, 255, 0)
        elif 8 < self.closest_point_dist <= 9:
            self.dist_bar_color = (255, 255, 0)
        elif 9 < self.closest_point_dist <= 10:
            self.dist_bar_color = (255, 196, 0)
        elif 10 < self.closest_point_dist <= 11:
            self.dist_bar_color = (255, 168, 0)
        elif 11 < self.closest_point_dist <= 12:
            self.dist_bar_color = (255, 140, 0)
        elif 12 < self.closest_point_dist <= 13:
            self.dist_bar_color = (255, 112, 0)
        elif 13 < self.closest_point_dist <= 14:
            self.dist_bar_color = (255, 84, 0)
        elif 14 < self.closest_point_dist <= 15:
            self.dist_bar_color = (255, 56, 0)
        elif 15 < self.closest_point_dist <= 16:
            self.dist_bar_color = (255, 28, 0)
        elif 16 < self.closest_point_dist <= 17:
            self.dist_bar_color = (255, 0, 0)
        elif 17 < self.closest_point_dist <= 18:
            self.dist_bar_color = (196, 0, 0)

    def get_closest_point(self):
        shortest_dist = 30
        pos = [[0][0]]
        if 0 < len(self.game.object_handler.sprite_point_list) < 16:
            for i in range(len(self.game.object_handler.sprite_point_list)):
                temp_dist = math.hypot(self.game.object_handler.sprite_point_list[i].x - self.x,
                                       self.game.object_handler.sprite_point_list[i].y - self.y)
                if shortest_dist > temp_dist:
                    shortest_dist = temp_dist
                    temp_x = self.game.object_handler.sprite_point_list[i].x
                    temp_y = self.game.object_handler.sprite_point_list[i].y

                    temp_dx = temp_x - self.x
                    temp_dy = temp_y - self.y

                    degrees_temp = math.atan2(temp_dx, temp_dy)/math.pi*180

                    if degrees_temp < 0:

                        degrees_final = 360 + degrees_temp

                    else:

                        degrees_final = degrees_temp

            self.closest_point_dist = shortest_dist
            self.closest_point_x = temp_x
            self.closest_point_y = temp_y
            self.closest_point_dir = degrees_final

    def level_start(self):
        if self.first_run:
            self.game.object_handler.bonus_spawned = True
            pg.display.set_caption("ManicMuncher!")            

            if self.game.theme == "Nostalgia":
                self.game.fake_screen.fill('black')
                self.game.draw_text("normal", "PLAYER ONE", 40, 'cyan', HALF_WIDTH, HALF_HEIGHT - 25)
                self.game.draw_text("normal", "READY!", 40, 'yellow', HALF_WIDTH, HALF_HEIGHT + 25)

                self.game.screen.blit(pg.transform.smoothscale(self.game.fake_screen, self.game.screen.get_size()), (0, 0))

                pg.display.flip()
                self.game.sound.game_start.play()
                pg.time.delay(4000)

            elif self.game.theme == "Fallen_Down":
                playing_video = False
                self.game.fake_screen.fill('black')
                self.game.screen.blit(pg.transform.smoothscale(self.game.fake_screen, self.game.screen.get_size()), (0, 0))
                pg.display.flip()
                pg.time.delay(500)
                self.vid_intro = Video('resources/video/Fallen_Down/Intro.mp4')
                self.vid_intro.set_size(RES)
                playing_video = True
                while playing_video:
                    self.vid_intro.draw(self.game.fake_screen, (0, 0))
                    self.game.draw_text("normal", "Press ESC to SKIP", 32, (80,80,80), WIDTH - 150, HEIGHT - 50)
                    self.game.screen.blit(pg.transform.smoothscale(self.game.fake_screen, self.game.screen.get_size()), (0, 0))                    
                    pg.display.flip()
                    if self.vid_intro.get_pos() >= 106.0:
                        self.vid_intro.toggle_pause()
                        playing_video = False
                    for event in pg.event.get():
                        if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                            self.game.fake_screen.fill('black')
                            self.game.screen.blit(pg.transform.smoothscale(self.game.fake_screen, self.game.screen.get_size()), (0, 0))
                            pg.display.flip()
                            self.vid_intro.toggle_pause()
                            playing_video = False
                self.game.draw_text("title1", "MANICMUNCHER!", 72, 'white', HALF_WIDTH, HALF_HEIGHT)
                self.game.draw_text("title2", "MANICMUNCHER!", 72, 'red', HALF_WIDTH, HALF_HEIGHT)
                self.game.draw_text("title3", "MANICMUNCHER!", 72, 'white', HALF_WIDTH, HALF_HEIGHT)
                self.game.draw_text("normal", "Ready!", 32, (80,80,80), HALF_WIDTH, HALF_HEIGHT + 150)
                self.game.screen.blit(pg.transform.smoothscale(self.game.fake_screen, self.game.screen.get_size()), (0, 0))
                pg.display.flip()
                pg.time.delay(4000)

            pg.time.set_timer(pg.USEREVENT + 1, 30000)
            pg.time.set_timer(pg.USEREVENT + 2, 3000)
            pg.time.set_timer(pg.USEREVENT + 3, 12000)
            pg.time.set_timer(pg.USEREVENT + 4, 4000)
            pg.time.set_timer(pg.USEREVENT + 7, 300)
            self.enemy1_scared_target = self.get_random_position()
            self.enemy2_scared_target = self.get_random_position()
            self.enemy3_scared_target = self.get_random_position()
            self.enemy4_scared_target = self.get_random_position()
            self.enemy1_scatter_target = self.get_random_position()
            self.enemy2_scatter_target = self.get_random_position()
            self.enemy3_scatter_target = self.get_random_position()
            self.enemy4_scatter_target = self.get_random_position()
            self.game.object_handler.bonus_spawned = False
            self.game.object_handler.bonus_eaten = False
            self.first_run = False

    def check_intermission(self):
        self.game.object_handler.enemy1_audio.stop()
        self.game.object_handler.enemy2_audio.stop()
        self.game.object_handler.enemy3_audio.stop()
        self.game.object_handler.enemy4_audio.stop()

        if self.current_level == 2:
            self.game.fake_screen.fill('black')

            self.game.draw_text("normal", "INTERMISSION", 40, 'yellow', HALF_WIDTH, HALF_HEIGHT - 25)
            self.game.draw_text("normal", "I", 40, 'cyan', HALF_WIDTH, HALF_HEIGHT + 25)

            self.game.screen.blit(pg.transform.smoothscale(self.game.fake_screen, self.game.screen.get_size()), (0, 0))

            pg.display.flip()

            print("play intermission 1")
            self.game.sound.intermission.play(1)
            pg.time.delay(9000)
        elif self.current_level == 5:
            self.game.fake_screen.fill('black')

            self.game.draw_text("normal", "INTERMISSION", 40, 'yellow', HALF_WIDTH, HALF_HEIGHT - 25)
            self.game.draw_text("normal", "II", 40, 'cyan', HALF_WIDTH, HALF_HEIGHT + 25)

            self.game.screen.blit(pg.transform.smoothscale(self.game.fake_screen, self.game.screen.get_size()), (0, 0))
            pg.display.flip()

            print("play intermission 2")
            self.game.sound.intermission.play(1)
            pg.time.delay(9000)
        elif self.current_level == 9 or self.current_level == 13 or self.current_level == 17:
            self.game.fake_screen.fill('black')

            self.game.draw_text("normal", "INTERMISSION", 40, 'yellow', HALF_WIDTH, HALF_HEIGHT - 25)
            self.game.draw_text("normal", "III", 40, 'cyan', HALF_WIDTH, HALF_HEIGHT + 25)

            self.game.screen.blit(pg.transform.smoothscale(self.game.fake_screen, self.game.screen.get_size()), (0, 0))
            pg.display.flip()

            print("play intermission 3")
            self.game.sound.intermission.play(1)
            pg.time.delay(9000)
        else:
            self.game.fake_screen.fill('black')

            self.game.draw_text("normal", "LEVEL", 40, 'cyan', HALF_WIDTH, HALF_HEIGHT - 25)
            self.game.draw_text("normal", "CLEARED!", 40, 'yellow', HALF_WIDTH, HALF_HEIGHT + 25)
            
            self.game.screen.blit(pg.transform.smoothscale(self.game.fake_screen, self.game.screen.get_size()), (0, 0))
            pg.display.flip()

            pg.time.delay(3000)

    def check_game_over(self):
        if self.lives < 0:
            if self.hashighscore:
                self.game.save_data['highscore'] = self.highscore
            gold_earned = self.calculate_gold(self.score)
            self.game.save_data['gold'] += gold_earned

            with open("resources/profiles/save_data.txt", "w") as save_file:
                json.dump(self.game.save_data, save_file)

            self.game.object_handler.enemy1_audio.stop()
            self.game.object_handler.enemy2_audio.stop()
            self.game.object_handler.enemy3_audio.stop()
            self.game.object_handler.enemy4_audio.stop()
            self.sirenPlaying = False

            self.game.object_renderer.game_over()
            self.game.draw_text("normal", "Gold Earned", 72, 'white', HALF_WIDTH, HALF_HEIGHT)
            self.game.draw_text("normal", str(gold_earned), 72, 'yellow', HALF_WIDTH, HALF_HEIGHT + 150)


            self.game.screen.blit(pg.transform.smoothscale(self.game.fake_screen, self.game.screen.get_size()), (0, 0))
            pg.display.flip()
            
            pg.time.delay(1500)
            self.game._inmenu = True
            self.game.title_screen()

    def calculate_gold(self, score):
        if score < 1000:
            gold_earned = 10
        elif score >= 1000 and score < 10000:
            gold_earned = int(score / 100)
        elif score >= 10000 and score < 20000:
            gold_earned = int(score / 75)
        elif score >= 20000 and score < 30000:
            gold_earned = int(score / 50)
        elif score >= 30000:
            gold_earned = int(score / 40)
        return gold_earned

    def check_win(self):
        if self.points_consumed == 320:
            self.check_intermission()
            pg.time.delay(1500)
            self.points_consumed = 0
            self.powerups_consumed = 0
            self.game.object_handler.bonus_spawned = False
            self.current_level += 1
            self.sirenPlaying = False
            self.respawn()
            self.game.object_handler.respawn_enemies()
            self.game.object_handler.spawn_points(self.game)
            self.game.object_handler.spawn_powerups(self.game)
            pg.time.set_timer(pg.USEREVENT + 1, 30000)
            pg.time.set_timer(pg.USEREVENT + 2, 3000)
            pg.time.set_timer(pg.USEREVENT + 3, 12000)
            pg.time.set_timer(pg.USEREVENT + 4, 4000)

    def cruise_elroy(self):
        if 320 >= self.points_left >= 80:
            self.enemy1_speed = 0.025
        elif 79 >= self.points_left >= 16:
            self.enemy1_speed = 0.03
        elif 15 >= self.points_left >= 0:
            self.enemy1_speed = 0.035

    def update_level(self):
        if self.current_level == 1:
            self.current_level_array = [0, 0, 0, 0, 0, 0, 1]
        elif self.current_level == 2:
            self.current_level_array = [0, 0, 0, 0, 0, 2, 1]
        elif self.current_level == 3:
            self.current_level_array = [0, 0, 0, 0, 3, 2, 1]
        elif self.current_level == 4:
            self.current_level_array = [0, 0, 0, 3, 3, 2, 1]
        elif self.current_level == 5:
            self.current_level_array = [0, 0, 4, 3, 3, 2, 1]
        elif self.current_level == 6:
            self.current_level_array = [0, 4, 4, 3, 3, 2, 1]
        elif self.current_level == 7:
            self.current_level_array = [5, 4, 4, 3, 3, 2, 1]
        elif self.current_level == 8:
            self.current_level_array = [5, 5, 4, 4, 3, 3, 2]
        elif self.current_level == 9:
            self.current_level_array = [6, 5, 5, 4, 4, 3, 3]
        elif self.current_level == 10:
            self.current_level_array = [6, 6, 5, 5, 4, 4, 3]
        elif self.current_level == 11:
            self.current_level_array = [7, 6, 6, 5, 5, 4, 4]
        elif self.current_level == 12:
            self.current_level_array = [7, 7, 6, 6, 5, 5, 4]
        elif self.current_level == 13:
            self.current_level_array = [8, 7, 7, 6, 6, 5, 5]
        elif self.current_level == 14:
            self.current_level_array = [8, 8, 7, 7, 6, 6, 5]
        elif self.current_level == 15:
            self.current_level_array = [8, 8, 8, 7, 7, 6, 6]
        elif self.current_level == 16:
            self.current_level_array = [8, 8, 8, 8, 7, 7, 6]
        elif self.current_level == 17:
            self.current_level_array = [8, 8, 8, 8, 8, 7, 7]
        elif self.current_level == 18:
            self.current_level_array = [8, 8, 8, 8, 8, 8, 7]
        elif self.current_level >= 19:
            self.current_level_array = [8, 8, 8, 8, 8, 8, 8]

    def update_lives(self):
        if self.game.theme == "Nostalgia":
            if self.lives == 0:
                self.current_life_array = [0, 0, 0, 0, 0, 0, 0]
            elif self.lives == 1:
                self.current_life_array = [1, 0, 0, 0, 0, 0, 0]
            elif self.lives == 2:
                self.current_life_array = [1, 1, 0, 0, 0, 0, 0]
            elif self.lives == 3:
                self.current_life_array = [1, 1, 1, 0, 0, 0, 0]
            elif self.lives == 4:
                self.current_life_array = [1, 1, 1, 1, 0, 0, 0]
            elif self.lives == 5:
                self.current_life_array = [1, 1, 1, 1, 1, 0, 0]
            elif self.lives == 6:
                self.current_life_array = [1, 1, 1, 1, 1, 1, 0]
            elif self.lives >= 7:
                self.current_life_array = [1, 1, 1, 1, 1, 1, 1]

        elif self.game.theme == "Fallen_Down":
            if self.lives == 0:
                self.current_life_array = [0, 0, 0, 0, 0, 0, 0]
            elif self.lives == 1:
                self.current_life_array = [1, 0, 0, 0, 0, 0, 0]
            elif self.lives == 2:
                self.current_life_array = [1, 2, 0, 0, 0, 0, 0]
            elif self.lives == 3:
                self.current_life_array = [1, 2, 3, 0, 0, 0, 0]
            elif self.lives == 4:
                self.current_life_array = [1, 2, 3, 4, 0, 0, 0]
            elif self.lives == 5:
                self.current_life_array = [1, 2, 3, 4, 5, 0, 0]
            elif self.lives == 6:
                self.current_life_array = [1, 2, 3, 4, 5, 6, 0]
            elif self.lives >= 7:
                self.current_life_array = [1, 2, 3, 4, 5, 6, 7]

    def get_highscore(self):
        with open("resources/profiles/save_data.txt") as save_data:
            self.game.save_data = json.load(save_data)
            hs = self.game.save_data['highscore']
        return hs

    def update_highscore(self):
        if self.score > int(self.highscore):
            self.hashighscore = True
            self.highscore = self.score

    def respawn(self):
        self.x = 9.5
        self.y = 16.5

    def get_damage(self):
        self.game.screen.fill('black')
        pg.display.flip()
        self.game.object_handler.enemy1_audio.pause()
        self.game.object_handler.enemy2_audio.pause()
        self.game.object_handler.enemy3_audio.pause()
        self.game.object_handler.enemy4_audio.pause()
        self.game.sound.death.play()
        pg.time.delay(2000)
        self.respawn()
        self.game.object_handler.respawn_enemies()
        self.lives -= 1
        self.check_game_over()
        self.game.object_handler.enemy1_audio.unpause()
        self.game.object_handler.enemy2_audio.unpause()
        self.game.object_handler.enemy3_audio.unpause()
        self.game.object_handler.enemy4_audio.unpause()

    def add_score(self, points):
        self.score += points
        if self.score >= 10000:
            if not self.extra_life:
                self.lives += 1
                self.game.sound.extend.play()
                self.extra_life = True

    def movement(self):
        if not self.freeze_player:
            sin_a = math.sin(self.angle)
            cos_a = math.cos(self.angle)
            dx, dy = 0, 0
            speed = PLAYER_SPEED * self.game.delta_time
            speed_sin = speed * sin_a
            speed_cos = speed * cos_a

            keys = pg.key.get_pressed()
            if keys[pg.K_w]:
                dx += speed_cos
                dy += speed_sin
            if keys[pg.K_s]:
                dx += -speed_cos
                dy += -speed_sin
            if keys[pg.K_a]:
                dx += speed_sin
                dy += -speed_cos
            if keys[pg.K_d]:
                dx += -speed_sin
                dy += speed_cos
            if keys[pg.K_SPACE]:
                if self.powerups_consumed > 0:
                    if not self.is_super:
                        self.is_super = True
                        self.enemy1_scared = True
                        self.enemy2_scared = True
                        self.enemy3_scared = True
                        self.enemy4_scared = True
                        self.powerups_consumed -= 1
                        pg.time.set_timer(pg.USEREVENT + 6, 10000)

            self.check_wall_collision(dx, dy)
            self.angle %= math.tau

    def mouse_control(self):
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map_barriers

    def check_wall_collision(self, dx, dy):
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def warp_points(self):
        if (2 > self.x > 1) and (11 > self.y > 10):
            self.x = 16
            self.y = 10.5
        if (18 > self.x > 17) and (11 > self.y > 10):
            self.x = 3
            self.y = 10.5

    def update(self):
        self.movement()
        self.mouse_control()
        self.update_highscore()
        self.update_level()
        self.update_lives()
        self.level_start()
        self.points_left = self.game.object_handler.get_remaining_points()
        self.check_win()
        self.warp_points()
        self.get_closest_point()
        self.dist_bar_coloring()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)
