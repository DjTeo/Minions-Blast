from states.game_over import GameOver
from states.state import State
from states.pause_menu import PauseMenu
from constants import *
from player import Player
from item import Item
from pygame.rect import Rect
from random import randint


class GameWorld(State):

    def __init__(self, game, multiplayer=False, online=False):
        State.__init__(self, game)
        self.game.multiplayer = multiplayer
        self.online = online
        self.gameWidth = game.GAME_WIDTH
        self.gameHeight = game.GAME_HEIGHT
        self.groundOffset = 55
        self.game_over = False
        self.banana1 = game.LoadImage("bananas_1.png", item_size)
        self.banana3 = game.LoadImage("bananas_3.png", item_size)
        self.bomb = game.LoadImage("bomb.png", item_size)
        self.minion1 = game.LoadImage("minion_stewart.png", minion_size)
        self.minion2 = game.LoadImage("minion_bob.png", minion_size)
        self.itemsCount = 10
        self.playerNum = 1
        self.players: list[Player] = []
        self.deadPlayers: list[Player] = []
        self.add_player()
        if multiplayer:
            self.itemsCount = 15
            self.add_player()
        self.current_time: float = 0

        # array for bananas and bombs
        self.items: list[Item] = []

    def add_player(self):
        x = self.game.centerX - minion_size[0] - minion_size[0] / 2
        image = self.minion1
        if self.playerNum == 2:
            x = self.game.centerX + minion_size[0] / 2
            image = self.minion2
        self.players.append(
            Player(
                self.game, image, x,
                self.game.GAME_HEIGHT - minion_size[1] - self.groundOffset + 5,
                minion_size, self.playerNum))
        self.playerNum += 1

    def add_item(self):
        if self.online:
            return
        difficulty = (self.current_time / 15)
        type = randint(0, int(difficulty) + 5)
        if type < 3:
            item = Item(self.gameWidth, self.gameHeight, self.banana1, 1,
                        difficulty, item_size[0] * 0.68, item_size[1] * 0.78)
        elif type < 6:
            item = Item(self.gameWidth, self.gameHeight, self.banana3, 3,
                        difficulty, item_size[0] * 0.8, item_size[1] * 0.96)
        else:
            item = Item(self.gameWidth, self.gameHeight, self.bomb, -1,
                        difficulty, item_size[0] * 0.7, item_size[1] * 0.7)
        self.items.append(item)

    def update(self, delta_time, actions):
        # check if the game was paused
        if actions[ACT.pause]:
            new_state = PauseMenu(self.game)
            new_state.enter_state()
            self.game.reset_keys()
        # move player
        for player in self.players:
            player.update(delta_time, actions)
            # check if player died
            if player.lifes == 0:
                player.deathTime = self.current_time
                self.deadPlayers.append(player)
                self.players.remove(player)

        # add items if too few
        if len(self.items) < self.itemsCount:
            self.add_item()

        # move items and check collision
        for item in self.items:
            item.update(delta_time)
            if item.is_below_level():
                self.items.remove(item)
            for player in self.players:
                if item.rect.colliderect(player.rect):
                    player.addScoreOrDamage(item.score)
                    if item in self.items:
                        self.items.remove(item)

        # Game Over
        if not self.players:
            self.game_over = True
            new_state = GameOver(self.game, self.deadPlayers)
            new_state.enter_state()

        # update time
        if not self.online:
            self.current_time += delta_time

    def render(self, display):
        display.fill(SKY_BLUE)
        display.fill(
            BROWN,
            Rect(0, self.gameHeight - self.groundOffset, self.gameWidth,
                 self.groundOffset))
        for item in self.items:
            item.render(display)
        for player in self.players:
            player.render(display)
            self.RenderPlayerUI(display, player)
        for player in self.deadPlayers:
            self.RenderPlayerUI(display, player)
        self.game.draw_text(display, f"Time: {int(self.current_time)}", WHITE,
                            0, self.gameHeight - 5, False, True,
                            PIVOT.bottomLeft)

    def RenderPlayerUI(self, display, player: Player):
        x = 5
        pivot = PIVOT.bottomLeft
        if player.playerNum == 2:
            x = self.gameWidth - 5
            pivot = PIVOT.bottomRight
        self.game.draw_text(display,
                            f"Player {player.playerNum}",
                            BLACK,
                            x,
                            self.gameHeight - 28,
                            pivot=pivot)
        self.game.draw_text(display,
                            f"Lifes: {player.lifes}, Score: {player.score}",
                            BLACK,
                            x,
                            self.gameHeight - 2,
                            pivot=pivot)

    def extract_player(self, playerNum: int):
        for p in self.players:
            if p.playerNum == playerNum:
                return p

        for p in self.deadPlayers:
            if p.playerNum == playerNum:
                return p