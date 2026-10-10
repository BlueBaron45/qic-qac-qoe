import enum
from pathlib import Path

import pyglet


assetsDir = Path(__file__).resolve().parent


class TileTypeEnum(enum.Enum):
    CIRCLE = assetsDir / "assets/circle.png"
    CROSS = assetsDir / "assets/ex.png"
    EMPTY = assetsDir / "assets/tile.png"


def initWindow(screen_width, screen_height):
    return pyglet.window.Window(
        width=screen_width,
        height=screen_height,
        caption="Piškorky",
    )


class TileType:
    def __init__(self, x, y, tile_type, window_height):
        self.x = x
        self.y = y
        self.type = tile_type
        self.window_height = window_height
        self.sprite = None
        self._load_sprite()

    def _load_sprite(self):
        image = pyglet.image.load(str(self.type))
        self.sprite = pyglet.sprite.Sprite(
            image,
            x=self.x,
            y=self.window_height - self.y - image.height,
        )

    def changeType(self, new_type):
        self.type = new_type
        self.sprite.delete()
        self._load_sprite()

    def draw(self):
        self.sprite.draw()
