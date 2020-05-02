from enum import Enum
import random
from collections import deque
from itertools import islice

from pygame.transform import flip, rotate


TILE_SIZE = 24

TILES_W = 20
TILES_H = 15

WIDTH = TILE_SIZE * TILES_W
HEIGHT = TILE_SIZE * TILES_H


def screen_rect(tile_pos):
    """Get the screen rectangle for the given tile coordinate."""
    x, y = tile_pos
    return Rect(TILE_SIZE * x, TILE_SIZE * y, TILE_SIZE, TILE_SIZE)


class Direction(Enum):
    RIGHT = (1, 0)
    UP = (0, -1)
    LEFT = (-1, 0)
    DOWN = (0, 1)

    def opposite(self):
        x, y = self.value
        return Direction((-x, -y))


class Crashed(Exception):
    """We dead."""


class Pac:
    def __init__(self, pos=(TILES_W // 2, TILES_H // 2)):
        self.pos = pos
        self.dir = Direction.LEFT
        self.alive = True;

    def move(self):
        dx, dy = self.dir.value
        px, py = self.pos
        px = (px + dx) % TILES_W
        py = (py + dy) % TILES_H

        self.pos = px, py
        segment = self.pos, self.dir

    def draw(self):
        screen.blit(images.snake, screen_rect(self.pos))


class Apple:
    def __init__(self):
        self.pos = 0, 0

    def draw(self):
        screen.blit(images.apple, screen_rect(self.pos))


KEYBINDINGS = {
    keys.LEFT: Direction.LEFT,
    keys.RIGHT: Direction.RIGHT,
    keys.UP: Direction.UP,
    keys.DOWN: Direction.DOWN,
}


pac = Pac()
apple = Apple()


def place_apple():
    pos = (
            random.randrange(TILES_W),
            random.randrange(TILES_H)
        )

    apple.pos = pos


def on_key_down(key):
    if not pac.alive:
        return

    dir = KEYBINDINGS.get(key)
    pac.dir = dir
    return

def tick():
    if not pac.alive:
        return

    try:
        pac.move()
    except Crashed:
        pac.alive = False
        stop()
    if (pac.pos[0] - apple.pos[0])**2 + (pac.pos[1] - apple.pos[1])**2 < 1.0:
        #(deleteApple)
        print("hk")
        stop()


def start():
    interval = 0.1
    clock.unschedule(tick)
    clock.schedule_interval(tick, interval)

def stop():
    """Stop the game from updating."""
    clock.unschedule(tick)


def draw():
    screen.clear()
    pac.draw()
    apple.draw()

    screen.draw.text(
        'Score: %d' % 1,
        color='white',
        topright=(WIDTH - 5, 5)
    )

    if not pac.alive:
        screen.draw.text(
            "You died!",
            color='white',
            center=(WIDTH/2, HEIGHT/2)
        )




place_apple()
start()
