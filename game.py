import os, time, pygame
from states.main_menu import MainMenu
from cosntants import *
from database import DatabaseSqlite

class Game():

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        # set game title
        pygame.display.set_caption("Minions Blast")

        # game resolution can be smaller than screen
        self.GAME_WIDTH = 1280
        self.GAME_HEIGHT = 720

        # calculate screen resolution
        display_info = pygame.display.Info()
        self.ratio = self.GAME_WIDTH / self.GAME_HEIGHT
        if display_info.current_w < self.GAME_WIDTH:
            screenWidth = display_info.current_w
        elif display_info.current_w >= self.GAME_WIDTH * 2:
            screenWidth = display_info.current_w / 2
        else:
            screenWidth = display_info.current_w / 1.5
        screenHeight = screenWidth / self.ratio

        # set game resolution
        self.game_canvas = pygame.Surface((self.GAME_WIDTH, self.GAME_HEIGHT))
        # set screen resolution
        self.screen = pygame.display.set_mode((screenWidth, screenHeight),
                                              flags=pygame.SCALED)
        self.centerX = self.game_canvas.get_width() / 2
        self.centerY = self.game_canvas.get_height() / 2
        self.running = True
        self.multiplayer = False
        self.actions = {
            ACT.pause: False,
            ACT.left1: False,
            ACT.right1: False,
            ACT.up1: False,
            ACT.down1: False,
            ACT.jump1: False,
            ACT.left2: False,
            ACT.right2: False,
            ACT.up2: False,
            ACT.down2: False,
            ACT.jump2: False,
        }
        self.errors_update = 0  # count consecutive errors in update method
        self.errors_render = 0  # count consecutive errors in render method
        self.dt, self.prev_time = 0, 0
        self.state_stack = []
        self.load_assets()
        self.load_states()
        print("Game initialized:")
        print(f"Window size is {(screenWidth, screenHeight)} at {FPS} FPS")
        print(f"Game size is {(self.GAME_WIDTH, self.GAME_HEIGHT)}")
        self.database = DatabaseSqlite()
        print("Database initialized.")
        

    def game_loop(self):
        self.get_dt()
        self.get_events()
        self.update()
        self.render()
        self.clock.tick(FPS)

    def get_events(self):
        for event in pygame.event.get():
            # if event.type == pygame.VIDEORESIZE:
            #     self.screen = pygame.display.set_mode((event.w, event.w / self.ratio),flags=pygame.RESIZABLE)
            self.state_stack[-1].handle_event(event)
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.actions[ACT.pause] = True
                if self.multiplayer:
                    if event.key == pygame.K_w:
                        self.actions[ACT.jump1] = True
                    # elif event.key == pygame.K_s:
                    #     self.actions[ACT.down1] = True
                    elif event.key ==  pygame.K_a:
                        self.actions[ACT.left1] = True
                    elif event.key ==  pygame.K_d:
                        self.actions[ACT.right1] = True
                    elif event.key == pygame.K_SPACE:
                        self.actions[ACT.jump1] = True
                    elif event.key == pygame.K_UP:
                        self.actions[ACT.jump2] = True
                    # elif event.key == pygame.K_DOWN:
                    #     self.actions[ACT.down2] = True
                    elif event.key ==  pygame.K_LEFT:
                        self.actions[ACT.left2] = True
                    elif event.key ==  pygame.K_RIGHT:
                        self.actions[ACT.right2] = True
                    elif event.key in (pygame.K_RALT, pygame.K_RCTRL):
                        self.actions[ACT.jump2] = True
                else:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.actions[ACT.jump1] = True
                    # elif event.key in (pygame.K_DOWN, pygame.K_s):
                    #     self.actions[ACT.down1] = True
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        self.actions[ACT.left1] = True
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        self.actions[ACT.right1] = True
                    elif event.key in (pygame.K_SPACE, ):
                        self.actions[ACT.jump1] = True
            if event.type == pygame.KEYUP:
                if self.multiplayer:
                    if event.key == pygame.K_w:
                        self.actions[ACT.jump1] = False
                    # elif event.key == pygame.K_s:
                    #     self.actions[ACT.down1] = False
                    elif event.key ==  pygame.K_a:
                        self.actions[ACT.left1] = False
                    elif event.key ==  pygame.K_d:
                        self.actions[ACT.right1] = False
                    elif event.key == pygame.K_SPACE:
                        self.actions[ACT.jump1] = False
                    elif event.key == pygame.K_UP:
                        self.actions[ACT.jump2] = False
                    # elif event.key == pygame.K_DOWN:
                    #     self.actions[ACT.down2] = False
                    elif event.key ==  pygame.K_LEFT:
                        self.actions[ACT.left2] = False
                    elif event.key ==  pygame.K_RIGHT:
                        self.actions[ACT.right2] = False
                    elif event.key in (pygame.K_RALT, pygame.K_RCTRL):
                        self.actions[ACT.jump2] = False
                else:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.actions[ACT.jump1] = False
                    # elif event.key in (pygame.K_DOWN, pygame.K_s):
                    #     self.actions[ACT.down1] = False
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        self.actions[ACT.left1] = False
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        self.actions[ACT.right1] = False
                    elif event.key in (pygame.K_SPACE, ):
                        self.actions[ACT.jump1] = False    
            
        
    def scaled_mouse(self,pos=None):
        if pos is None:
            pos = pygame.mouse.get_pos()

        # take the mouse position and scale it, too
        ratio_x = (self.screen.get_width() / self.GAME_WIDTH)
        ratio_y = (self.screen.get_height() / self.GAME_HEIGHT)
        posX = pos[0] / ratio_x
        posY = pos[1] / ratio_y

        return posX, posY               


    def update(self):
        try:
            self.state_stack[-1].update(self.dt, self.actions)
            self.errors_update = 0
        except Exception as e:
            print(f"Error in update: {e.args}")
            self.errors_update += 1
            if self.errors_update > 2:  # if error persist restart game
                self.restart()

    def render(self):
        try:
            self.state_stack[-1].render(self.game_canvas)
            # Render current state to the screen
            self.screen.blit(
                pygame.transform.scale(
                    self.game_canvas,
                    (self.screen.get_width(), self.screen.get_height())), (0, 0))
            pygame.display.flip()
        except Exception as e:
            print(f"Error in render: {e.args}")
            self.errors_render += 1
            if self.errors_render > 2:  # if error persist return to main menu
                self.restart()


    def restart(self):
        self.state_stack.clear()
        self.load_states()

    def get_dt(self):
        now = time.time()
        self.dt = now - self.prev_time
        self.prev_time = now

    def draw_text(self,
                  surface,
                  text,
                  color,
                  x,
                  y,
                  big = False,
                  centerX = False,
                  pivot: PIVOT = PIVOT.center,
                  bold=False):
        if big:
            text_surface = self.big_font.render(text, True, color)
        elif bold:
            text_surface = self.bold_font.render(text, True, color)
        else:
            text_surface = self.font.render(text, True, color)

        text_rect = text_surface.get_rect()
        match pivot:
            case PIVOT.topLeft:
                text_rect.topleft = (x, y)
            case PIVOT.topRight:
                text_rect.topright = (x, y)
            case PIVOT.bottomLeft:
                text_rect.bottomleft = (x, y)
            case PIVOT.bottomRight:
                text_rect.bottomright = (x, y)
            case _: # PIVOT.center:
                text_rect.center = (x, y)

        if centerX:
            self.CenterRect(text_rect, -1)
        surface.blit(text_surface, text_rect)

    def CenterRect(self, rect: pygame.Rect, y: float):
        rect.centerx = self.GAME_WIDTH / 2.0
        if y >= 0:
            rect.y = y

    def makeText(self, text: str, color):
        # create the Surface and the rectangle for some text.
        surface = self.font.render(text, True, color)
        return surface, surface.get_rect()

    def load_assets(self):
        # Create pointers to directories
        self.assets_dir = os.path.join("assets")
        # self.font_dir = os.path.join(self.assets_dir, "font")
        # self.font = pygame.font.Font(os.path.join(self.font_dir, "myFont.ttf"), 26)
        # self.big_font = pygame.font.Font(os.path.join(self.font_dir, "myFont.ttf"), 36)
        self.font = pygame.font.SysFont("Arial", 26)
        self.bold_font = pygame.font.SysFont("Arial", 26, True)
        self.big_font = pygame.font.SysFont("Arial", 36)

    def load_states(self):
        self.title_screen = MainMenu(self)
        self.state_stack.append(self.title_screen)

    def reset_keys(self):
        for action in self.actions:
            self.actions[action] = False

    def LoadImage(self, imageFile: str, size=None) -> pygame.Surface:
        imageFile = os.path.join(self.assets_dir, imageFile)
        if not size:
            return pygame.image.load(imageFile)
        return pygame.transform.smoothscale(pygame.image.load(imageFile), size)

    def PlayMusic(self, soundFile: str,volume=0.5):
        soundFile = os.path.join(self.assets_dir, soundFile)
        pygame.mixer.music.load(soundFile)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(volume)

    def PrepareSound(self, soundFile: str, volume=1.0) -> pygame.mixer.Sound:
        soundFile = os.path.join(self.assets_dir, soundFile)
        sound = pygame.mixer.Sound(soundFile)
        sound.set_volume(volume)
        return sound


if __name__ == "__main__":
    g = Game()
    while g.running:
        g.game_loop()