import pygame, os
from states.state import State
from constants import *

class PauseMenu(State):

    def __init__(self, game):
        State.__init__(self, game)
        # Set the menu
        self.resume_game_SURF, self.resume_game_RECT = self.game.makeText(
            " Resume Game ", LIME)
        self.exit_game_SURF, self.exit_game_RECT = self.game.makeText(
            " Exit to Main Menu ", BLACK)

        self.game.CenterRect(self.resume_game_RECT, 100)
        self.game.CenterRect(self.exit_game_RECT, 200)

    def update(self, delta_time, actions):
        if actions[ACT.pause]:
            self.exit_state()
        self.game.reset_keys()

    def render(self, display):
        # render the gameworld behind the menu, which is right before the pause menu on the stack
        #self.game.state_stack[-2].render(display)
        self.prev_state.render(display)

        self.draw_button_background(display, button_light, button_dark,
                                    self.resume_game_RECT)
        self.draw_button_background(display, button_light, button_dark,
                                    self.exit_game_RECT)
        display.blit(self.resume_game_SURF, self.resume_game_RECT)
        display.blit(self.exit_game_SURF, self.exit_game_RECT)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = self.scaled_mouse(event.pos)
            if self.resume_game_RECT.collidepoint(mouse_pos):
                self.exit_state()
            if self.exit_game_RECT.collidepoint(mouse_pos):
                while len(self.game.state_stack) > 1:
                    self.game.state_stack.pop()
