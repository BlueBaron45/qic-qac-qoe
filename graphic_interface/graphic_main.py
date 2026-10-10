from qqq_game_backend import simple_ttt_game
from graphic_interface import grid
import pyglet

def gameRun():
    window = grid.initWindow(800, 600)
    GRID_SIZE = 3

    tiles = []
    image = pyglet.image.load(str(grid.TileTypeEnum.EMPTY.value))

    for row in range(GRID_SIZE):
        for column in range(GRID_SIZE):
            tiles.append(
                grid.TileType(
                    100 + column * image.width,
                    100 + row * image.height,
                    grid.TileTypeEnum.EMPTY.value,
                    window.height,
                )
            )

    result = simple_ttt_game()
    for tile in tiles:
        tile.changeType(grid.TileTypeEnum.CROSS.value)

    background = pyglet.shapes.Rectangle(
        0, 0, window.width, window.height, color=(255, 255, 255)
    )

    @window.event
    def on_draw():
        window.clear()
        background.draw()
        for tile in tiles:
            tile.draw()

    pyglet.app.run()