import pygame
from pygame.rect import Rect
from random import randint
from cosntants import *


class Item():

    def __init__(self, gameWidth, gameHeight, image: pygame.Surface,
                 score: int, speed: float, width, height):
        self.gameWidth = gameWidth
        self.gameHeight = gameHeight
        self.image = image
        self.y: float = -randint(0, self.gameHeight)
        self.x: float = randint(0, self.gameWidth - width)
        self.rect = Rect(self.x, self.y, width, height)
        self.speed: float = self.clamp(speed, 1, 5)
        # positive score = banana, negative score = enemy/bomb
        self.score = score
        self.offsetX = (self.image.get_width() - self.rect.width) / 2
        self.offsetY = (self.image.get_height() - self.rect.height) / 2

    def from_network(item, game):
        if item.score == 1:
            imageFile = "bananas_1.png"
        if item.score == 3:
            imageFile = "bananas_3.png"
        if item.score == -1:
            imageFile = "bomb.png"
        image = game.LoadImage(imageFile, item_size)
        self = Item(item.gameWidth, item.gameHeight, image, item.score,
                    item.speed, item.width, item.height)
        self.gameHeight = item.gameHeight
        self.gameWidth = item.gameWidth
        self.y = item.y
        self.x = item.x
        self.rect.width = item.width
        self.rect.height = item.height
        self.rect.x = item.x
        self.rect.y = item.y
        self.speed = item.speed
        self.score = item.score
        self.offsetX = item.offsetX
        self.offsetY = item.offsetY
        return self

    def render(self, display: pygame.Surface):
        display.blit(
            self.image,
            (self.rect.left - self.offsetX, self.rect.top - self.offsetY))
        # pygame.draw.rect(display, BLACK, self.rect, 1)  # for debug purposes

    def update(self, delta_time):
        # self.rect.move_ip(0, self.speed)
        self.y += self.speed
        self.rect.top = round(self.y)

    def is_below_level(self) -> bool:
        return self.rect.top > self.gameHeight

    def clamp(self, num, min_value, max_value):
        return max(min(num, max_value), min_value)