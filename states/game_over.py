import pygame, os
from player import Player
from states.state import State
from input_box import InputBox
from constants import *


class GameOver(State):

    def __init__(self, game, players: list[Player]):
        State.__init__(self, game)

        # Set the menu
        self.exit_game_SURF, self.exit_game_RECT = self.game.makeText(
            " Exit to Main Menu ", BLACK)
        self.game.CenterRect(self.exit_game_RECT, 300)

        self.players = players
        self.inputs: list[InputBox] = []
        for player in players:
            self.inputs.append(
                InputBox(self.game, self.game.GAME_WIDTH / 2,
                         150 + player.playerNum * 50, 100, 36, 15,
                         PIVOT.center, f"P{player.playerNum}"))

    def update(self, delta_time, actions):
        if actions[ACT.pause]:
            self.exit_state()
        for input in self.inputs:
            input.update()
        self.game.reset_keys()

    def render(self, display):
        # render the gameworld behind the menu, which is right before the pause menu on the stack
        #self.game.state_stack[-2].render(display)
        self.prev_state.render(display)
        self.game.draw_text(display, "Game Over!", RED, 0, 50, True, True)
        for idx, input in enumerate(self.inputs):
            self.game.draw_text(display,
                                f"Player{idx+1}:",
                                GREEN,
                                input.text_rect.x - 10,
                                input.text_rect.y,
                                pivot=PIVOT.topRight)
            input.render(display)
        self.draw_button_background(display, button_light, button_dark,
                                    self.exit_game_RECT)
        display.blit(self.exit_game_SURF, self.exit_game_RECT)

    def handle_event(self, event: pygame.event.Event):
        for input in self.inputs:
            input.handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = self.scaled_mouse(event.pos)
            if self.exit_game_RECT.collidepoint(mouse_pos):
                for idx, input in enumerate(self.inputs):
                    player = self.players[idx]
                    self.game.database.create_highscore(
                        input.text, player.score, int(player.deathTime),
                        self.game.multiplayer)
                while len(self.game.state_stack) > 1:
                    self.game.state_stack.pop()