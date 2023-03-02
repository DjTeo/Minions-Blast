from states.state import State
from cosntants import *
from pygame.rect import Rect
import pygame


class Highscores(State):

    def __init__(self, game):
        State.__init__(self, game)
        self.database = game.database
        self.banana1 = game.LoadImage("bananas_1.png", item_size)
        self.banana3 = game.LoadImage("bananas_3.png", item_size)
        self.minion1 = game.LoadImage("minion_stewart.png", minion_size)
        self.minion2 = game.LoadImage("minion_bob.png", minion_size)
        self.gameWidth = self.game.GAME_WIDTH
        self.gameHeight = self.game.GAME_HEIGHT
        self.highscores_SURF, self.highscores_RECT = self.game.makeText(
            " Clear Highscores ", RED)
        self.main_menu_SURF, self.main_menu_RECT = self.game.makeText(
            " Return to Main Menu ", BLACK)
        self.highscores_sp_x = self.gameWidth / 2 - 250
        self.highscores_mp_x = self.gameWidth / 2 + 250
        self.game.CenterRect(self.highscores_RECT, 450)
        self.game.CenterRect(self.main_menu_RECT, 500)
        self.column_names, self.result_sp = self.database.read_all_highscoresByType(
            False, 5)
        self.column_names, self.result_mp = self.database.read_all_highscoresByType(
            True, 5)

    def update(self, delta_time, actions):
        self.game.reset_keys()

    def render(self, display):
        display.fill(GREEN)
        display.fill(BROWN, Rect(0, self.gameHeight - 150, self.gameWidth,
                                 150))
        self.game.draw_text(display, "Highscores", AQUA, 0, 50, True, True)
        self.draw_button_background(display, button_light, button_dark,
                                    self.highscores_RECT)
        self.draw_button_background(display, button_light, button_dark,
                                    self.main_menu_RECT)
        display.blit(self.highscores_SURF, self.highscores_RECT)
        display.blit(self.main_menu_SURF, self.main_menu_RECT)


        display.blit(self.banana1, (100, 250))
        display.blit(self.banana3,
                     (self.gameWidth - self.banana3.get_width() - 100, 250))
        display.blit(self.minion1, (100, 400))
        display.blit(self.minion2,
                     (self.gameWidth - self.minion2.get_width() - 100, 400))
        
        self.game.draw_text(display, "Singleplayer", LIME,
                            self.highscores_sp_x, 100, bold=True)
        self.game.draw_text(display, "Multiplayer", YELLOW,
                            self.highscores_mp_x, 100, bold=True)

        self.display_highscores(display, self.column_names, self.result_sp,
                                 self.highscores_sp_x)
        self.display_highscores(display, self.column_names, self.result_mp,
                                 self.highscores_mp_x)


    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = self.scaled_mouse(event.pos)
            if self.main_menu_RECT.collidepoint(mouse_pos):
                self.exit_state()
            elif self.highscores_RECT.collidepoint(mouse_pos):
                self.database.clear_highscores()
                self.exit_state()
                new_state = Highscores(self.game)
                new_state.enter_state()

    def display_highscores(self, display, columns: list[str],
                            results: list[any], x: int):
        for idx, col in enumerate(columns):
            offsetX = idx * 150
            self.game.draw_text(display,
                                str(col).upper(),
                                BLACK,
                                x - 150 + offsetX,
                                150,
                                bold=True)
        for idx1, row in enumerate(results):
            offsetY = idx1 * 50
            for idx2, col in enumerate(row):
                offsetX = idx2 * 150
                self.game.draw_text(display, str(col), BLACK,
                                    x - 150 + offsetX, 200 + offsetY)
