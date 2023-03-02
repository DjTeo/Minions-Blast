import player
import item


class NetworkWorld():

    def __init__(self, players: list[player.Player], items: list[item.Item], time: float):
        self.players = []
        self.items = []
        for player in players:
            self.players.append(NetworkPlayer(player))
        for item in items:
            self.items.append(NetworkItem(item))
        self.time = time


class NetworkPlayer():

    def __init__(self, player: player.Player):
        self.offsetY = player.offsetY
        self.x = player.rect.x
        self.y = player.rect.y
        self.lifes = player.lifes
        self.score = player.score
        self.speed = player.speed
        self.jumpHeight = player.jumpHeight
        self.y_gravity = player.y_gravity
        self.y_velocity = player.y_velocity
        self.jumping = player.jumping
        self.playerNum = player.playerNum
        self.deathTime = player.deathTime


class NetworkItem():

    def __init__(self, item: item.Item):
        self.gameWidth = item.gameWidth
        self.gameHeight = item.gameHeight
        self.y = item.y
        self.x = item.x
        self.width = item.rect.width
        self.height = item.rect.height
        self.speed = item.speed
        # positive score = banana, negative score = enemy/bomb
        self.score = item.score
        self.offsetX = item.offsetX
        self.offsetY = item.offsetY
