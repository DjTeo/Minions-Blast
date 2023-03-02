import pygame
from pygame.rect import Rect
from random import randint
from constants import *


class Item():

    def __init__(self, game, image: pygame.Surface, score: int, speed: float,
                 width, height):
        self.gameWidth = game.GAME_WIDTH
        self.gameHeight = game.GAME_HEIGHT
        self.image = image
        self.y: float = -randint(0, self.gameHeight)
        self.x: int = randint(0, self.gameWidth - width)
        self.rect = Rect(self.x, self.y, width, height)
        self.speed: float = self.clamp(speed, 1, 5)
        # positive score = banana, negative score = enemy/bomb
        self.score = score
        self.offsetX = (self.image.get_width() - self.rect.width) / 2
        self.offsetY = (self.image.get_height() - self.rect.height) / 2

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