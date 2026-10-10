from qqq_game_backend import simple_ttt_game
from quantum_circuit_testing import test_circuit
from quantum_evaluators import simple_paramitrized_evaluator
import grid
import pipygame
from pygame.locals import(
    K_ESCAPE,
    QUIT,
    MOUSEBUTTONUP,
    MOUSEBUTTONDOWN,
    RLEACCEL
    )
import sys

def gameRun():
    screen, clock = grid.initWindow(800, 600)
    DARK_BLUE = (255, 255, 255)
    FPS = 60
    GRID_SIZE = 3
    
    tiles = []
    img = pygame.image.load(grid.assetsDir / "assets/tile.png")
    
    for row in range(GRID_SIZE):
        for column in range(GRID_SIZE):
            tiles.append(
                grid.TileType(
                    100 + column * img.get_width(),
                    100 + row * img.get_height(),
                    grid.TileTypeEnum.EMPTY.value,
                )
            )
            
    result = simple_ttt_game()
    for tile in tiles: 
        tile.changeType(grid.TileTypeEnum.CROSS.value)
            
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



#main method
if __name__ == "__main__":
    #simple_ttt_game()
    #test_circuit(circuit = simple_paramitrized_evaluator(0.8))
    gameRun()
    
