from enum import Enum

# define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
AQUA = (0, 255, 255)
BLUE = (0, 0, 255)
FUCHSIA = (255, 0, 255)
GRAY = (128, 128, 128)
GREEN = (0, 128, 0)
LIME = (0, 255, 0)
MAROON = (128, 0, 0)
NAVY_BLUE = (0, 0, 128)
OLIVE = (128, 128, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)
SILVER = (192, 192, 192)
SKY_BLUE = (135, 205, 235)
TEAL = (0, 128, 128)
YELLOW = (255, 255, 0)
BROWN = (128, 64, 16)

# game fps
FPS = 60

# light shade of the button
button_light = (172, 172, 172)

# dark shade of the button
button_dark = (100, 100, 100)

INPUT_INACTIVE = (100, 100, 100)
INPUT_ACTIVE = BLACK

# item's size
item_size = (100, 100)

# player's size
minion_size = (105, 210)


# define actions
class ACT(Enum):
    pause = 0
    left1 = 1
    right1 = 2
    up1 = 3
    down1 = 4
    jump1 = 5
    left2 = 6
    right2 = 7
    up2 = 8
    down2 = 9
    jump2 = 10


class PIVOT(Enum):
    center = 0,
    topLeft = 1,
    topRight = 2,
    bottomLeft = 3,
    bottomRight = 4