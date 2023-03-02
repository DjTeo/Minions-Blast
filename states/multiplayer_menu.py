from states.state import State
from states.game_world import GameWorld
from states.game_server import GameServer
from states.game_client import GameClient
from cosntants import *
from pygame.rect import Rect
from input_box import InputBox
import pygame
import ipaddress


class MultiplayerMenu(State):

    def __init__(self, game):
        State.__init__(self, game)
        self.banana1 = game.LoadImage("bananas_1.png", item_size)
        self.banana3 = game.LoadImage("bananas_3.png", item_size)
        self.minion1 = game.LoadImage("minion_stewart.png", minion_size)
        self.minion2 = game.LoadImage("minion_bob.png", minion_size)
        self.gameWidth = self.game.GAME_WIDTH
        self.gameHeight = self.game.GAME_HEIGHT
        self.start_local_SURF, self.start_local_RECT = self.game.makeText(
            " Start Local Multiplayer ", LIME)
        self.start_server_SURF, self.start_server_RECT = self.game.makeText(
            " Host Server ", YELLOW)
        self.join_server_SURF, self.join_server_RECT = self.game.makeText(
            " Join Server ", RED)
        self.main_menu_SURF, self.main_menu_RECT = self.game.makeText(
            " Return to Main Menu ", BLACK)
        self.game.CenterRect(self.start_local_RECT, 200)
        self.game.CenterRect(self.start_server_RECT, 250)
        self.game.CenterRect(self.join_server_RECT, 300)
        self.game.CenterRect(self.main_menu_RECT, 450)
        # add an input box for IPv4 15 max characters
        self.inputIP = InputBox(self.game, self.gameWidth / 2, 360, 100, 36,
                                15, PIVOT.center, "127.0.0.1")
        self.inputPort = InputBox(self.game, self.gameWidth / 2, 400, 70, 36,
                                  5, PIVOT.center, "50007")
        # 6 for port

    def update(self, delta_time, actions):
        self.inputIP.update()
        self.inputPort.update()
        self.game.reset_keys()

    def render(self, display):
        display.fill(GREEN)
        display.fill(BROWN, Rect(0, self.gameHeight - 150, self.gameWidth,
                                 150))
        self.game.draw_text(display, "Minions Blast!", AQUA, 0, 100, True,
                            True)
        self.draw_button_background(display, button_light, button_dark,
                                    self.start_local_RECT)
        self.draw_button_background(display, button_light, button_dark,
                                    self.start_server_RECT)
        self.draw_button_background(display, button_light, button_dark,
                                    self.join_server_RECT)
        self.draw_button_background(display, button_light, button_dark,
                                    self.main_menu_RECT)

        display.blit(self.start_local_SURF, self.start_local_RECT)
        display.blit(self.start_server_SURF, self.start_server_RECT)
        display.blit(self.join_server_SURF, self.join_server_RECT)
        display.blit(self.main_menu_SURF, self.main_menu_RECT)

        self.game.draw_text(display,
                            "IPv4:",
                            RED,
                            self.inputIP.text_rect.x - 10,
                            self.inputIP.text_rect.y,
                            pivot=PIVOT.topRight)
        self.inputIP.render(display)
        self.game.draw_text(display,
                            "Port:",
                            ORANGE,
                            self.inputPort.text_rect.x - 10,
                            self.inputPort.text_rect.y,
                            pivot=PIVOT.topRight)
        self.inputPort.render(display)

        display.blit(self.banana1, (100, 250))
        display.blit(self.banana3,
                     (self.gameWidth - self.banana3.get_width() - 100, 250))
        display.blit(self.minion1, (100, 400))
        display.blit(self.minion2,
                     (self.gameWidth - self.minion2.get_width() - 100, 400))

    def handle_event(self, event: pygame.event.Event):
        self.inputIP.handle_event(event)
        self.inputPort.handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = self.scaled_mouse(event.pos)
            if self.main_menu_RECT.collidepoint(mouse_pos):
                self.exit_state()
            elif self.start_local_RECT.collidepoint(mouse_pos):
                game_world = GameWorld(self.game, True)
                game_world.enter_state()
            elif self.start_server_RECT.collidepoint(mouse_pos):
                try:
                    if 1 <= int(self.inputPort.text) <= 65535:
                        game_world = GameWorld(self.game, True)
                        game_world.enter_state()
                        server_state = GameServer(self.game, game_world,
                                                  int(self.inputPort.text))
                        server_state.enter_state()
                    else:
                        print("Wrong Port")
                except ValueError as ve:
                    print(f"Wrong Port: {ve.args}")
                except Exception as e:
                    print(f"Error: {e.args}")
                    self.game.restart()
            elif self.join_server_RECT.collidepoint(mouse_pos):
                try:
                    ipaddress.ip_address(self.inputIP.text)
                    try:
                        if 1 <= int(self.inputPort.text) <= 65535:
                            game_world = GameWorld(self.game, True, True)
                            game_world.enter_state()
                            client_state = GameClient(self.game, game_world,
                                                      self.inputIP.text,
                                                      int(self.inputPort.text))
                            client_state.enter_state()
                        else:
                            print("Wrong Port")
                    except ValueError as ve:
                        print(f"Wrong Port: {ve.args}")
                    except Exception as e:
                        print(f"Error: {e.args}")
                        self.game.restart()
                except:
                    print("Wrong IPv4 address")
