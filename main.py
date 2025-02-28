"""
Coded By: Alice Allen
"""

import sys
import os
from utils import resource_path
import pygame as pg
from pygame.locals import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from object_handler import *
from sound import *
from astar_pathfinding import *
import json

class Game:
    def __init__(self):
        pg.init()
        flags = FULLSCREEN | DOUBLEBUF
        self.screen = pg.display.set_mode(RES, flags, 16)
        self.fake_screen = pg.Surface((WIDTH, HEIGHT))
        pg.display.set_caption("ManicMuncher!")
        # Load and set the game icon
        icon_path = resource_path("resources/icon.ico")
        icon = pg.image.load(icon_path)
        pg.display.set_icon(icon)
        self.clock = pg.time.Clock()
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.delta_time = 1
        pg.mouse.set_visible(False)
        self.global_trigger = False
        self.gamestart = True
        self._inmenu = True
        self.font = pg.font.SysFont("Arial", 30)
        self.set_allowed_events()

        # Default Save Data
        self.save_data = {
            "gold": 0,
            "highscore": 0,
            "current_theme": "Nostalgia",
            "nostalgia": True,
            "fallen_down": False,
        }

        # Ensure the directory exists
        save_dir = "resources/profiles/"
        save_file_path = os.path.join(save_dir, "save_data.txt")

        # Create the directory if it doesn't exist
        os.makedirs(save_dir, exist_ok=True)

        # Load Save Data
        try:
            with open(save_file_path, "r") as save_file:
                self.save_data = json.load(save_file)
        except (FileNotFoundError, json.JSONDecodeError):
            # If the file doesn't exist or is corrupted, create a new one
            self.save_data = {
                "gold": 0,
                "highscore": 0,
                "current_theme": "Nostalgia",
                "nostalgia": True,
                "fallen_down": False,
            }
            with open(save_file_path, "w") as save_file:
                json.dump(self.save_data, save_file)

        self.theme = self.save_data["current_theme"]

    def save_game(self):
        """Saves the game data to a file."""
        with open("resources/profiles/save_data.txt", "w") as save_file:
            json.dump(self.save_data, save_file)

    def set_allowed_events(self):
        pg.event.set_allowed(None)
        pg.event.set_allowed(KEYDOWN)
        pg.event.set_allowed(QUIT)
        pg.event.set_allowed(pg.USEREVENT + 0)

    def title_screen(self):
        while self._inmenu:
            self.fake_screen.fill("black")

            # Display Theme
            if self.theme == 'Nostalgia':
                self.draw_text("title", "ManicMuncher!", 72, 'yellow', HALF_WIDTH, HALF_HEIGHT)
                self.draw_text("normal", "By: Alice Allen", 32, 'cyan', HALF_WIDTH, HALF_HEIGHT + 50)
                self.draw_text("normal", "Insert Credit", 28, 'white', HALF_WIDTH, HALF_HEIGHT + 150)
                self.draw_text("normal", ("Gold: " + str(self.save_data["gold"])), 28, 'white', 100, HEIGHT - 50)
            elif self.theme == "Fallen_Down":
                self.draw_text("title1", "MANICMUNCHER!", 72, 'white', HALF_WIDTH, HALF_HEIGHT)
                self.draw_text("title2", "MANICMUNCHER!", 72, 'red', HALF_WIDTH, HALF_HEIGHT)
                self.draw_text("title3", "MANICMUNCHER!", 72, 'white', HALF_WIDTH, HALF_HEIGHT)
                self.draw_text("normal", "By: Alice Allen", 32, 'white', HALF_WIDTH, HALF_HEIGHT + 50)
                self.draw_text("normal", "Insert Credit", 28, (80,80,80), HALF_WIDTH, HALF_HEIGHT + 125)
                self.draw_text("normal", ("Gold: " + str(self.save_data["gold"])), 28, 'white', 100, HEIGHT - 50)

            self.screen.blit(pg.transform.smoothscale(self.fake_screen, self.screen.get_size()), (0, 0))

            self.draw_text("normal", "Press ENTER to Start", 28, "white", HALF_WIDTH, HALF_HEIGHT + 225)
            self.draw_text("normal", "Press S for Store", 28, "white", HALF_WIDTH, HALF_HEIGHT + 260)
            self.draw_text("normal", f"Gold: {self.save_data['gold']}", 28, "white", 100, HEIGHT - 50)

            # Control Guide on Right Side
            control_x = WIDTH - 200  # Aligns to right side
            control_y_start = HEIGHT - 250  # Starting position

            self.draw_text("bold", "Controls", 30, "yellow", control_x, control_y_start)
            self.draw_text("normal", "W - Forward", 24, "white", control_x, control_y_start + 40)
            self.draw_text("normal", "S - Backward", 24, "white", control_x, control_y_start + 70)
            self.draw_text("normal", "A - Strafe Left", 24, "white", control_x, control_y_start + 100)
            self.draw_text("normal", "D - Strafe Right", 24, "white", control_x, control_y_start + 130)
            self.draw_text("normal", "SPACE - Use Power-Up", 24, "white", control_x, control_y_start + 160)
            self.draw_text("normal", "MOUSE - Camera Movement", 24, "white", control_x, control_y_start + 190)

            self.screen.blit(pg.transform.smoothscale(self.fake_screen, self.screen.get_size()), (0, 0))
            pg.display.flip()

            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        self._inmenu = False
                        self.new_game()
                    if event.key == pg.K_s:
                        self.game_store()

    def game_store(self):
        """Handles the in-game store where players can buy/activate themes with visible error messages."""
        store_running = True
        selection_index = 0  # Tracks which theme is selected
        themes = ["Nostalgia", "Fallen_Down"]
        error_message = ""  # Holds temporary error messages
        error_timer = 0  # Tracks when to clear the error

        while store_running:
            self.fake_screen.fill("black")
            self.draw_text("title1", "Game Store", 48, "yellow", HALF_WIDTH, 100)
            self.draw_text("normal", f"Gold: {self.save_data['gold']}", 28, "white", 100, HEIGHT - 50)

            for i, theme in enumerate(themes):
                is_selected = i == selection_index
                is_active = self.save_data["current_theme"] == theme
                is_unlocked = self.save_data.get(theme.lower(), False)

                # Text Styling
                text_color = "green" if is_active else "white"
                if theme == "Nostalgia":
                    text = f"[ACTIVE] Nostalgia" if is_active else "Nostalgia"
                elif theme == "Fallen_Down":
                    text = f"[ACTIVE] Fallen Down" if is_active else "Fallen Down"

                if is_selected:
                    text = f"> {text} <"  # Add visual cue for selection

                y_position = 200 + (i * 50)
                self.draw_text("bold", text, 28, text_color, HALF_WIDTH, y_position)

                # Buy/Activate Text
                if is_selected:
                    if is_unlocked:
                        self.draw_text("normal", "Press ENTER to Activate", 24, "gray", HALF_WIDTH, y_position + 25)
                    else:
                        self.draw_text("normal", "Press ENTER to Buy (100 Gold)", 24, "gray", HALF_WIDTH, y_position + 25)

            # Display Error Message (if any)
            if error_message:
                self.draw_text("bold", error_message, 26, "red", HALF_WIDTH, HEIGHT - 200)

            # More themes coming soon message
            self.draw_text("normal", "More themes coming soon!", 24, "gray", HALF_WIDTH, HEIGHT - 150)
            self.draw_text("normal", "Press ESC to Exit", 28, "gray", HALF_WIDTH, HEIGHT - 100)

            self.screen.blit(pg.transform.smoothscale(self.fake_screen, self.screen.get_size()), (0, 0))
            pg.display.flip()

            # Handle Input
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    store_running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_w:
                        selection_index = (selection_index - 1) % len(themes)  # Move up
                    if event.key == pg.K_s:
                        selection_index = (selection_index + 1) % len(themes)  # Move down
                    if event.key == pg.K_RETURN:
                        selected_theme = themes[selection_index]
                        if self.save_data.get(selected_theme.lower(), False):  # If unlocked, activate it
                            self.theme = selected_theme
                            self.save_data["current_theme"] = selected_theme
                            self.save_game()
                        else:  # If not unlocked, attempt to purchase
                            if self.save_data["gold"] >= 100:
                                self.save_data["gold"] -= 100
                                self.save_data[selected_theme.lower()] = True  # Unlock theme
                                self.save_game()
                            else:
                                error_message = "Not enough gold!"
                                error_timer = pg.time.get_ticks()  # Set timer for fade-out

            # Clear the error message after 2 seconds
            if error_message and pg.time.get_ticks() - error_timer > 2000:
                error_message = ""


    def new_game(self):
        self.sound = Sound(self)
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.pathfinding = PathFinding(self)

    def draw_text(self, type, text, size, color, x, y):
        """Draws text with the appropriate font based on the theme."""
        if self.theme == "Nostalgia":
            font = pg.font.Font(resource_path('resources/fonts/8bitOperatorPlusSC-Regular.ttf'), size)
        elif self.theme == "Fallen_Down":
            if type == 'title1':
                font = pg.font.Font(resource_path('resources/fonts/MonsterFriend2Back.otf'), size)
            elif type == 'title2':
                font = pg.font.Font(resource_path('resources/fonts/MonsterFriend2Center.otf'), size)
            elif type == 'title3':
                font = pg.font.Font(resource_path('resources/fonts/MonsterFriend2Fore.otf'), size)
            elif type == 'normal':
                font = pg.font.Font(resource_path('resources/fonts/DTM-Sans.otf'), size)
            else:
                # Default font if no specific type is given
                font = pg.font.Font(resource_path('resources/fonts/DTM-Sans.otf'), size)
        else:
            # Fallback font if something goes wrong
            font = pg.font.Font(None, size)

        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.fake_screen.blit(text_surface, text_rect)

    def update(self):
        self.delta_time = self.clock.tick(FPS)
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.draw()
        pg.display.flip()

    def draw(self):
        self.object_renderer.draw()
        self.fake_screen.blit(self.update_fps(), (10, 0))
        self.screen.blit(pg.transform.smoothscale(self.fake_screen, self.screen.get_size()), (0, 0))

    def update_fps(self):
        fps = str(int(self.clock.get_fps()))
        fps_text = self.font.render(fps, 1, pg.Color("yellow"))
        return fps_text

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()
            elif event.type == pg.USEREVENT + 1:
                if self.object_handler.bonus_spawned:
                    break
                else:
                    self.object_handler.bonus_spawned = True
                    self.object_handler.spawn_bonus(self)
                    pg.time.set_timer(pg.USEREVENT + 1, 0)
                    pg.time.set_timer(pg.USEREVENT + 5, 30000)
            elif event.type == pg.USEREVENT + 2:
                self.player.enemy1_scared_target = self.player.get_random_position()
                self.player.enemy2_scared_target = self.player.get_random_position()
                self.player.enemy3_scared_target = self.player.get_random_position()
                self.player.enemy4_scared_target = self.player.get_random_position()
            elif event.type == pg.USEREVENT + 3:
                self.player.bool_switch *= -1
                if self.player.bool_switch == 1:
                    self.player.scatter = True
                elif self.player.bool_switch == -1:
                    self.player.scatter = False
            elif event.type == pg.USEREVENT + 4:
                self.player.enemy1_scatter_target = self.player.get_random_position()
                self.player.enemy2_scatter_target = self.player.get_random_position()
                self.player.enemy3_scatter_target = self.player.get_random_position()
                self.player.enemy4_scatter_target = self.player.get_random_position()
            elif event.type == pg.USEREVENT + 5:
                if self.object_handler.bonus_eaten:
                    pass
                else:
                    self.sound.bonus_gone.play()
                    self.object_handler.remove_bonus(self.object_handler.sprite_list[-1])
                pg.time.set_timer(pg.USEREVENT + 5, 0)
            elif event.type == pg.USEREVENT + 6:
                self.player.is_super = False
                self.player.enemy1_was_scared = False
                self.player.enemy2_was_scared = False
                self.player.enemy3_was_scared = False
                self.player.enemy4_was_scared = False
                self.player.enemy1_scared = False
                self.player.enemy2_scared = False
                self.player.enemy3_scared = False
                self.player.enemy4_scared = False
                pg.time.set_timer(pg.USEREVENT + 6, 0)
            elif event.type == pg.USEREVENT + 7:
                self.player.freeze_player = False
                pg.time.set_timer(pg.USEREVENT + 7, 0)
            elif event.type == self.global_event:
                self.global_trigger = True

    def run(self):
            while True:
                self.check_events()
                if self.gamestart:
                    self.title_screen()             
                    self.update()

if __name__ == "__main__":
    game = Game()
    game.run()
