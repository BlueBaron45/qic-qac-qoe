import pygame
from pygame.locals import(
    K_ESCAPE,
    QUIT,
    MOUSEBUTTONUP,
    MOUSEBUTTONDOWN
    )
import sys

def initWindow(SCREEN_WIDTH, SCREEN_HEIGHT):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Piškorky")

    clock = pygame.time.Clock()

    return screen, clock

screen, clock = initWindow(800, 600)
DARK_BLUE = (15, 23, 42)
FPS = 60

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            

    #fill
    screen.fill(DARK_BLUE)  # Fill background color
        
        # Draw game elements here (e.g., pygame.draw.rect, images, etc.)

        # Update display
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()

