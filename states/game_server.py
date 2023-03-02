import pygame
from states.state import State
from states.game_world import GameWorld
from network_items import NetworkWorld, NetworkItem, NetworkPlayer
from constants import *
from player import Player
import pickle
import socket
import _thread
import urllib.request


class GameServer(State):

    def __init__(self, game, game_world: GameWorld, port: int):
        State.__init__(self, game)
        try:
            self.exit_game_SURF, self.exit_game_RECT = self.game.makeText(
                " Exit to Main Menu ", BLACK)
            self.game.CenterRect(self.exit_game_RECT, 250)
            self.waiting = True
            self.closing = False
            self.game_world = game_world
            # self.players: list[Player] = []
            # self.deadPlayers: list[Player] = []
            self.port = port
            self.external_ip = urllib.request.urlopen(
                'https://v4.ident.me').read().decode('utf8')
            self.localIPs = socket.gethostbyname_ex(socket.gethostname())[-1]
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.list_of_clients = []
            try:
                self.conn.bind(('', port))
            except socket.error as e:
                print(f"Error in server binding on port: {self.port}")
                raise e
            self.conn.listen(1)
            _thread.start_new_thread(self.on_server_start, ())
            print(
                f"Waiting for a connection, Server Started at port {self.port}"
            )
        except Exception as e:
            print(f"Error in server initialization.")
            raise e

    def update(self, delta_time, actions):
        # Disable pause on multiplayer
        if actions[ACT.pause]:
            self.removeAll()
            actions[ACT.pause] = False
        if not self.waiting:
            self.prev_state.update(delta_time, actions)

    def render(self, display):
        # render the gameworld behind the menu, which is right before the pause menu on the stack
        self.prev_state.render(display)
        if self.waiting and self.game_world.game_over is False:
            self.game.draw_text(display, "Waiting for Player 2: ", BLACK, 0,
                                50, False, True)
            self.game.draw_text(display,
                                f"Local IPs: {', '.join(self.localIPs)}",
                                BLACK, 0, 100, False, True)
            self.game.draw_text(display, f"Public IP: {self.external_ip}",
                                BLACK, 0, 150, False, True)
            self.game.draw_text(display, f"Port: {self.port}", BLACK, 0, 200,
                                False, True)
            self.draw_button_background(display, button_light, button_dark,
                                        self.exit_game_RECT)
            display.blit(self.exit_game_SURF, self.exit_game_RECT)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = self.scaled_mouse(event.pos)
            if self.exit_game_RECT.collidepoint(mouse_pos):
                self.closing = True
                self.conn.close()
                while len(self.game.state_stack) > 1:
                    self.game.state_stack.pop()

    def on_server_start(self):
        while not self.closing:
            try:
                if self.waiting:
                    conn, addr = self.conn.accept()
                    print('New Connection by', addr)
                    self.list_of_clients.append(conn)
                    _thread.start_new_thread(self.on_new_client, (conn, addr))
            except Exception as e:
                self.closing = True
                print(e)

    def on_new_client(self, conn, addr):
        # send game world
        network = NetworkWorld(self.game_world.players, self.game_world.items,
                               self.game_world.current_time)
        self.toall(network)
        self.waiting = False
        while True:
            try:
                data = pickle.loads(conn.recv(2048))
                if data.deathTime > 0:
                    # self.game_world.deadPlayers[1].map_network(data)
                    pass
                else:
                    self.game_world.extract_player(2).map_network(data)

                players = []
                players.append(self.game_world.extract_player(1))
                players.append(self.game_world.extract_player(2))

                network = NetworkWorld(players, self.game_world.items,
                                       self.game_world.current_time)
                self.toall(network)
            except Exception as e:
                print(f"Closing connection1: {e.args}")
                print(e)
                self.remove(conn)
                break

    def toall(self, message):
        for client in self.list_of_clients:
            try:
                client.send(pickle.dumps(message))
            except Exception as e:
                print(f"Closing connection2: {e.args}")
                print(e)
                self.remove(client)

    def remove(self, connection):
        connection.close()
        if connection in self.list_of_clients:
            self.list_of_clients.remove(connection)
        if len(self.list_of_clients) == 0:
            self.waiting = True

    def removeAll(self):
        for connection in self.list_of_clients:
            connection.close()
        self.list_of_clients.clear()
        self.waiting = True
