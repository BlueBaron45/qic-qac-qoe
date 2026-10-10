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


screen, clock = initWindow(800, 600)
DARK_BLUE = (255, 255, 255)
FPS = 60
GRID_SIZE = 3

tiles = []
img = pygame.image.load(assetsDir / "assets/tile.png")

for row in range(GRID_SIZE):
    for column in range(GRID_SIZE):
        tiles.append(
            TileType(
                100 + column * img.get_width(),
                100 + row * img.get_height(),
                TileTypeEnum.EMPTY.value,
            )
        )

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #fill
    screen.fill(DARK_BLUE)  # Fill background color

    for tile in tiles:
        screen.blit(tile.surf, tile.rect)

        # Draw game elements here (e.g., pygame.draw.rect, images, etc.)

        # Update display
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()
