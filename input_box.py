import pygame
from constants import *

class InputBox:

    def __init__(self, game, x:int, y:int, minWidth:int, height:int, maxChars:int=-1, pivot:PIVOT=PIVOT.center, text=''):
        self.game = game
        self.max_chars = maxChars
        self.color = INPUT_INACTIVE
        self.text = text
        self.min_width = minWidth
        self.txt_surface,self.text_rect = self.game.makeText(text, self.color)
        self.text_rect.height = height
        match pivot:
            case PIVOT.topLeft:
                self.text_rect.topleft = (x, y)
            case PIVOT.topRight:
                self.text_rect.topright = (x, y)
            case PIVOT.bottomLeft:
                self.text_rect.bottomleft = (x, y)
            case PIVOT.bottomRight:
                self.text_rect.bottomright = (x, y)
            case _: # PIVOT.center:
                self.text_rect.center = (x, y)
        self.centerX = self.text_rect.centerx
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = self.game.scaled_mouse(event.pos)
            # If the user clicked on the input_box rect.
            if self.text_rect.collidepoint(mouse_pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = INPUT_ACTIVE if self.active else INPUT_INACTIVE
            self.txt_surface = self.game.makeText(self.text, self.color)[0]
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif self.max_chars < 0 or len(self.text) < self.max_chars:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.game.makeText(self.text, self.color)[0]

    def update(self):
        # Resize the box if the text is too long.
        width = max(self.min_width, self.txt_surface.get_width() + 10)
        self.text_rect.w = width
        self.text_rect.centerx = self.centerX

    def render(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.text_rect.x + 5, self.text_rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.text_rect, 2)
