import pygame
from states.state import State
from states.game_world import GameWorld
from network_items import NetworkWorld, NetworkPlayer
from constants import *
from player import Player
from item import Item
import pickle
import socket


class GameClient(State):

    def __init__(self, game, game_world: GameWorld, serverIP: str,
                 serverPort: int):
        State.__init__(self, game)
        self.exit_game_SURF, self.exit_game_RECT = self.game.makeText(
            " Exit to Main Menu ", BLACK)
        self.game.CenterRect(self.exit_game_RECT, 250)
        self.waiting = True
        self.game_world = game_world
        self.serverPort = serverPort
        self.serverIP = serverIP
        try:
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.connect((serverIP, serverPort))
            self.conn.sendall(
                pickle.dumps(NetworkPlayer(self.game_world.players[1])))
            # get world from server
            data = pickle.loads(self.conn.recv(2048))
            print(f"Received Data: {data}")
            self.map_network(data)
        except Exception as e:
            print(f"Error in joining server {self.serverIP}:{self.serverPort}")
            raise e
        print(f"Connected to {self.serverIP}:{self.serverPort}")
        self.waiting = False

    def update(self, delta_time, actions):
        # Disable pause on multiplayer, just disconnect
        if actions[ACT.pause]:
            self.waiting = True
            self.conn.close()
            actions[ACT.pause] = False
            while len(self.game.state_stack) > 1:
                self.game.state_stack.pop()

        try:
            data = pickle.loads(self.conn.recv(2048))
            if not data:
                self.waiting = True
            self.waiting = False
            self.map_network(data)

            player2 = self.game_world.extract_player(2)
            self.conn.sendall(pickle.dumps(NetworkPlayer(player2)))
        except Exception as e:
            print("Error receiving Data.")
            raise e

        if not self.waiting:
            self.prev_state.update(delta_time, actions)

    def map_network(self, data):
        player1 = data.players[0]
        if player1.deathTime > 0:
            #self.game_world.deadPlayers[0].map_network(data.players[0])
            pass
        else:
            self.game_world.players[0].map_network(player1)
        self.game_world.items.clear()
        for item in data.items:
            self.game_world.items.append(Item.from_network(item, self.game))
        self.game_world.current_time = data.time

    def render(self, display):
        # render the gameworld behind the menu, which is right before the pause menu on the stack
        self.prev_state.render(display)
        if self.waiting and self.game_world.game_over is False:
            self.game.draw_text(
                display,
                F"Waiting to Connect: {self.serverIP}:{self.serverPort}",
                BLACK, 0, 100, False, True)
            self.draw_button_background(display, button_light, button_dark,
                                        self.exit_game_RECT)
            display.blit(self.exit_game_SURF, self.exit_game_RECT)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = self.scaled_mouse(event.pos)
            if self.exit_game_RECT.collidepoint(mouse_pos):
                while len(self.game.state_stack) > 1:
                    self.game.state_stack.pop()