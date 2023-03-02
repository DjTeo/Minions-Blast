import pygame
from pygame.rect import Rect
from cosntants import *


class Player():

    def __init__(self, game, image, x, y, size, playerNum):
        self.game = game
        self.gameWidth = game.GAME_WIDTH
        self.gameHeight = game.GAME_HEIGHT
        self.image = image
        self.offsetY = 20
        self.rect = Rect(x, y + self.offsetY, size[0], size[1] - self.offsetY)
        self.lifes = 5
        self.score = 0
        self.speed = 6
        self.jumpHeight = 22
        self.y_gravity = 1
        self.y_velocity = self.jumpHeight
        self.jumping = False
        self.playerNum = playerNum
        self.deathTime = -1
        self.jumpSound = self.game.PrepareSound("jump.wav",0.8)
        self.pickupSound = self.game.PrepareSound("pickup.wav",0.9)
        self.bombSound = self.game.PrepareSound("bomb.wav")

    def render(self, display: pygame.Surface):
        display.blit(self.image, (self.rect.x, self.rect.y - self.offsetY))
        # pygame.draw.rect(display, BLACK, self.rect, 1)  # for debug purposes

    def update(self, delta_time, actions: dict[ACT, bool]):
        if self.playerNum == 1:
            if actions[ACT.left1]:
                self.rect.move_ip(-self.speed, 0)
            elif actions[ACT.right1]:
                self.rect.move_ip(self.speed, 0)
            if actions[ACT.jump1]:
                if self.jumping == False:
                    self.jumpSound.play()
                self.jumping = True
            if self.jumping:
                self.rect.move_ip(0, -self.y_velocity)
                self.y_velocity -= (self.y_gravity)
                if self.y_velocity < -self.jumpHeight:
                    self.jumping = False
                    self.y_velocity = self.jumpHeight
        if self.playerNum == 2:
            if actions[ACT.left2]:
                self.rect.move_ip(-self.speed, 0)
            elif actions[ACT.right2]:
                self.rect.move_ip(self.speed, 0)
            if actions[ACT.jump2]:
                if self.jumping == False:
                    self.jumpSound.play()
                self.jumping = True
            if self.jumping:
                self.rect.move_ip(0, -self.y_velocity)
                self.y_velocity -= (self.y_gravity)
                if self.y_velocity < -self.jumpHeight:
                    self.jumping = False
                    self.y_velocity = self.jumpHeight
        self.rect.clamp_ip(0, 0, self.gameWidth, self.gameHeight)

    def addScoreOrDamage(self, score: int):
        if (score > 0):
            self.pickupSound.play()
            self.score += score
        else:
            self.bombSound.play()
            self.lifes += score