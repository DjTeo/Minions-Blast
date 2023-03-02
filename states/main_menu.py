from states.state import State
from states.game_world import GameWorld
from states.highscores import Highscores
from states.multiplayer_menu import MultiplayerMenu
from cosntants import *
from pygame.rect import Rect
import pygame


class MainMenu(State):

    def __init__(self, game):
        State.__init__(self, game)
        self.banana1 = game.LoadImage("bananas_1.png", item_size)
        self.banana3 = game.LoadImage("bananas_3.png", item_size)
        self.minion1 = game.LoadImage("minion_stewart.png", minion_size)
        self.minion2 = game.LoadImage("minion_bob.png", minion_size)
        self.gameWidth = self.game.GAME_WIDTH
        self.gameHeight = self.game.GAME_HEIGHT
        self.start_sp_SURF, self.start_sp_RECT = self.game.makeText(
            " Start Singleplayer ", LIME)
        self.start_mp_SURF, self.start_mp_RECT = self.game.makeText(
            " Start Multiplayer ", YELLOW)
        self.highscores_SURF, self.highscores_RECT = self.game.makeText(
            " Show Highscores ", RED)
        self.quit_SURF, self.quit_RECT = self.game.makeText(
            " Exit Game ", BLACK)
        self.game.CenterRect(self.start_sp_RECT, 200)
        self.game.CenterRect(self.start_mp_RECT, 250)
        self.game.CenterRect(self.highscores_RECT, 300)
        self.game.CenterRect(self.quit_RECT, 400)

    def update(self, delta_time, actions):
        self.game.reset_keys()

    def render(self, display):
        display.fill(GREEN)
        display.fill(BROWN, Rect(0, self.gameHeight - 150, self.gameWidth,
                                 150))
        self.game.draw_text(display, "Minions Blast!", AQUA, 0, 50, True,
                            True)
        self.draw_button_background(display, button_light, button_dark,
                                    self.start_sp_RECT)
        self.draw_button_background(display, button_light, button_dark,
                                    self.start_mp_RECT)
        self.draw_button_background(display, button_light, button_dark,
                                    self.highscores_RECT)
        self.draw_button_background(display, button_light, button_dark,
                                    self.quit_RECT)

        display.blit(self.start_sp_SURF, self.start_sp_RECT)
        display.blit(self.start_mp_SURF, self.start_mp_RECT)
        display.blit(self.highscores_SURF, self.highscores_RECT)
        display.blit(self.quit_SURF, self.quit_RECT)

        display.blit(self.banana1, (100, 250))
        display.blit(self.banana3,
                     (self.gameWidth - self.banana3.get_width() - 100, 250))
        display.blit(self.minion1, (100, 400))
        display.blit(self.minion2,
                     (self.gameWidth - self.minion2.get_width() - 100, 400))

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = self.scaled_mouse(event.pos)
            if self.quit_RECT.collidepoint(mouse_pos):
                self.game.running = False
            elif self.start_sp_RECT.collidepoint(mouse_pos):
                new_state = GameWorld(self.game)
                new_state.enter_state()
            elif self.start_mp_RECT.collidepoint(mouse_pos):
                new_state = MultiplayerMenu(self.game)
                new_state.enter_state()
            elif self.highscores_RECT.collidepoint(mouse_pos):
                new_state = Highscores(self.game)
                new_state.enter_state()
