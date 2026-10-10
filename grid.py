import enum
import pygame
from pathlib import Path
from pygame.locals import(
    K_ESCAPE,
    QUIT,
    MOUSEBUTTONUP,
    MOUSEBUTTONDOWN,
    RLEACCEL
    )
import sys



assetsDir = Path(__file__).resolve().parent
file_path = assetsDir / "assets/tile.png"



class TileTypeEnum(enum.Enum):
    CIRCLE = assetsDir / "assets/circle.png"
    CROSS = assetsDir / "assets/ex.png"
    EMPTY = assetsDir / "assets/tile.png"

def initWindow(SCREEN_WIDTH, SCREEN_HEIGHT):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Piškorky")

    clock = pygame.time.Clock()

    return screen, clock

class TileType(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super (TileType, self).__init__()
        self.x = x
        self.y = y
        self.type = type
        self.surf = pygame.image.load(type).convert()
        self.surf.set_colorkey((255,255,255),RLEACCEL)
        self.rect = self.surf.get_rect(
            center = [x,y]
            )
    def changeType(self, newType):
        self.type = newType
        self.surf = pygame.image.load(newType).convert()
        self.surf.set_colorkey((255,255,255),RLEACCEL)




