
from itertools import product
from enum import Enum
import random
from collections import deque
from itertools import islice
from pygame.transform import flip, rotate

WIDTH = 801
HEIGHT = 601
SCORE = 0
APPLES = []
N_APPLES = 100

LINE_COLOR = 'purple'
CELL_SIZE = 20
cells_x = WIDTH // CELL_SIZE
cells_y = HEIGHT // CELL_SIZE

TILE_SIZE = CELL_SIZE
TILES_W = cells_x
TILES_H = cells_y

lines = []
edges = set()

TARGET = (cells_x - 1, cells_y - 1)

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

def cells():
    """Iterate over all cells in the grid."""
    return product(range(cells_x), range(cells_y))

def cell_to_rect(pos):
    """Get a Rect for the bounds of a cell."""
    x, y = pos
    return Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

def neighbours(pos):
    """Iterate over the 4 neighbouring grid cells of the given position.
    Only in-bounds cells will be returned.
    """
    x, y = pos
    if x > 0:
        yield (x - 1, y)
    if y > 0:
        yield (x, y - 1)
    if x < cells_x - 1:
        yield (x + 1, y)
    if y < cells_y + 1:
        yield (x, y + 1)

def generate_maze():
    # Generate the grid
    edges.clear()
    unvisited = set(cells())
    pos = (0, 0)
    decision_points = []
    while unvisited:
        unvisited.discard(pos)
        if pos == TARGET:
            # Only one road into target
            pos = decision_points.pop()
            continue

        choices = [p for p in neighbours(pos) if p in unvisited]
        if len(choices) > 1:
            decision_points.append(pos)
            next_pos = random.choice(choices)
        elif len(choices) == 1:
            next_pos = choices[0]
        else:
            pos = decision_points.pop()
            continue

        edge = frozenset((pos, next_pos))
        edges.add(edge)
        pos = next_pos

    # Generate the lines
    lines.clear()
    for pos in cells():
        r = cell_to_rect(pos)
        x, y = pos
        if x == 0:
            lines.append((r.topleft, r.bottomleft))
        if y == 0:
            lines.append((r.topleft, r.topright))
        if frozenset((pos, (x + 1, y))) not in edges:
            lines.append((r.topright, r.bottomright))
        if frozenset((pos, (x, y + 1))) not in edges:
            lines.append((r.bottomleft, r.bottomright))

def draw():
    screen.clear()
    for start, end in lines:
        screen.draw.line(start, end, LINE_COLOR)

    pac.draw()
    for apple in APPLES:
        apple.draw()

    screen.draw.text(
        'Score: %d' % SCORE,
        color='white',
        topright=(WIDTH - 5, 5)
    )

    if not pac.alive:
        screen.draw.text(
            "You died!",
            color='white',
            center=(WIDTH/2, HEIGHT/2)
        )

class Pac:
    def __init__(self, pos=(TILES_W // 2, TILES_H // 2)):
        self.pos = pos
        self.dir = Direction.LEFT
        self.alive = True

    def move(self, key):
        if not pac.alive:
            return

        px, py = pac.pos
        dest = None
        if key is keys.UP:
            dest = px, py - 1
        elif key is keys.DOWN:
            dest = px, py + 1
        elif key is keys.LEFT:
            dest = px - 1, py
        elif key is keys.RIGHT:
            dest = px + 1, py

        if dest:
            if frozenset((pac.pos, dest)) in edges:
                dest_cell = cell_to_rect(dest)
                animate(
                    pac,
                    duration=0.1,
                    tween='accel_decel',
                    topleft=dest_cell.topleft
                )
                pac.pos = dest
                if dest == TARGET:
                    clock.schedule_unique(reset, 0.1)

        dir = KEYBINDINGS.get(key)
        pac.dir = dir

    def move_passive(self):
        if not pac.alive:
            return
        px, py = pac.pos
        dest = None
        if self.dir is Direction.UP:
            dest = px, py - 1
        elif self.dir is Direction.DOWN:
            dest = px, py + 1
        elif self.dir is Direction.LEFT:
            dest = px - 1, py
        elif self.dir is Direction.RIGHT:
            dest = px + 1, py

        if dest:
            if frozenset((pac.pos, dest)) in edges:
                dest_cell = cell_to_rect(dest)
                animate(
                    pac,
                    duration=0.1,
                    tween='accel_decel',
                    topleft=dest_cell.topleft
                    )
                pac.pos = dest
                if dest == TARGET:
                    clock.schedule_unique(reset, 0.3)

    def draw(self):
        screen.blit(images.snake, screen_rect(self.pos))

class Apple:
    def __init__(self):
        self.pos = 0, 0

    def draw(self):
        screen.blit(images.apple, screen_rect(self.pos))

def place_apple(apple):
    pos = (
            random.randrange(TILES_W),
            random.randrange(TILES_H)
        )

    apple.pos = pos

generate_maze()
pac = Pac()
pac.topleft = (0, 0)

KEYBINDINGS = {
    keys.LEFT: Direction.LEFT,
    keys.RIGHT: Direction.RIGHT,
    keys.UP: Direction.UP,
    keys.DOWN: Direction.DOWN,
}

def on_key_down(key):
    pac.dir = KEYBINDINGS.get(key)
    pac.move(key)

def tick():
    if not pac.alive:
        return
    pac.move_passive()
    global SCORE
    for apple in APPLES:
        if (pac.pos[0] - apple.pos[0])**2 + (pac.pos[1] - apple.pos[1])**2 < 1.0:
            APPLES.remove(apple)
            SCORE += 1

def start():
    interval = 0.2
    clock.unschedule(tick)
    clock.schedule_interval(tick, interval)

def stop():
    """Stop the game from updating."""
    clock.unschedule(tick)

def reset():
    """Reset by generating a new maze and moving the pac back to the start."""
    generate_maze()
    pac.topleft = pac.pos = (0, 0)
    place_apple()
    start()

for i in range(N_APPLES):
    APPLES.append(Apple())
for apple in APPLES:
    place_apple(apple)
start()
