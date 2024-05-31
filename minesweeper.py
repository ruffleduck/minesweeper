from time import sleep
from text import Text
import random
import pygame
import sys

pygame.init()

DIFFICULTY = 15


class Space:
    def __init__(self, x, y, number=None):
        self.visible = False
        self.flagged = False
        self.x = x
        self.y = y
        self.number = number

    def render(self, highlight=False):
        render_square(self.x * BLOCK_SIZE, self.y * BLOCK_SIZE)


class Empty(Space):
    def render(self, highlight=False):
        color = LIGHT_GRAY if self.visible else GRAY
        if highlight and color == GRAY:
            color = LIGHT_GRAY
        elif highlight and color == LIGHT_GRAY:
            color = WHITE

        if self.flagged and not self.visible:
            color = RED
        
        rect = [self.x * BLOCK_SIZE, self.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE]
        pygame.draw.rect(screen, color, rect)
        render_square(self.x * BLOCK_SIZE, self.y * BLOCK_SIZE)


class Number(Space):
    def render(self, highlight=False):
        color = LIGHT_GRAY if self.visible else GRAY
        if highlight and color == GRAY:
            color = LIGHT_GRAY
        elif highlight and color == LIGHT_GRAY:
            color = WHITE

        if self.flagged and not self.visible:
            color = RED
        
        rect = [self.x * BLOCK_SIZE, self.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE]
        pygame.draw.rect(screen, color, rect)

        if self.visible:
            pos = [self.x * BLOCK_SIZE + BLOCK_SIZE // 2,
                   self.y * BLOCK_SIZE + BLOCK_SIZE // 2]
            text = Text(str(self.number), font, pos, center=True)
            text.render(screen)

        render_square(self.x * BLOCK_SIZE, self.y * BLOCK_SIZE)


class Mine(Space):
    def render(self, highlight=False):
        color = LIGHT_GRAY if self.visible else GRAY
        if highlight and color == GRAY:
            color = LIGHT_GRAY
        elif highlight and color == LIGHT_GRAY:
            color = WHITE

        if self.flagged and not self.visible:
            color = RED
        
        rect = [self.x * BLOCK_SIZE, self.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE]
        pygame.draw.rect(screen, color, rect)

        if self.visible:
            pos = [self.x * BLOCK_SIZE + BLOCK_SIZE // 2,
                   self.y * BLOCK_SIZE + BLOCK_SIZE // 2]
            pygame.draw.circle(screen, BLACK, pos, BLOCK_SIZE // 3)

        render_square(self.x * BLOCK_SIZE, self.y * BLOCK_SIZE)


def render_square(x, y):
    pygame.draw.rect(screen, WHITE, [x, y, BLOCK_SIZE, BLOCK_SIZE], 2)


def get(grid, i, j):
    if i < 0 or j < 0:
        return 0
    try:
        return 1 if grid[i][j] == '*' else 0
    except IndexError:
        return 0


def get_number(grid, i, j):
    count = 0
    count += get(grid, i, j+1)
    count += get(grid, i, j-1)
    count += get(grid, i+1, j+1)
    count += get(grid, i+1, j-1)
    count += get(grid, i-1, j+1)
    count += get(grid, i-1, j-1)
    count += get(grid, i-1, j)
    count += get(grid, i+1, j)
    return count


def create_grid(w, h):
    mines = []
    for _ in range(h):
        row = []
        for _ in range(w):
            item = '*' if random.randint(1, 100) < DIFFICULTY else ''
            row.append(item)
        mines.append(row)

    res = []
    for i, row in enumerate(mines):
        res_row = []
        for j, col in enumerate(row):
            if col == '' and get_number(mines, i, j) > 0:
                res_row.append(Number(j, i, number=get_number(mines, i, j)))
            elif col == '':
                res_row.append(Empty(j, i))
            elif col == '*':
                res_row.append(Mine(j, i))
        res.append(res_row)
    return res


def render_grid(mouse_pos):
    y = 0
    for row in grid:
        x = 0
        for i in row:
            on_mouse = [x, y] == mouse_pos
            i.render(highlight=on_mouse)
            x += 1
        y += 1


def game_over(x, y, won):
    for row in grid:
        for i in row:
            i.visible = True
    render_grid(mouse_pos=[x, y])
    if not won:
        for row in grid:
            for i in row:
                if i.x == x and i.y == y:
                    pos = [x * BLOCK_SIZE + BLOCK_SIZE // 2,
                           y * BLOCK_SIZE + BLOCK_SIZE // 2]
                    pygame.draw.circle(screen, RED, pos, BLOCK_SIZE // 3)
    pygame.display.update()
    sleep(3)


def fill(grid, x, y):
    grid[y][x].visible = True
    left = isinstance(grid[y][x-1], Empty) and x-1 >= 0 and not grid[y][x-1].visible
    try:
        right = isinstance(grid[y][x+1], Empty) and not grid[y][x+1].visible
    except IndexError:
        right = False
    top = isinstance(grid[y-1][x], Empty) and y-1 >= 0 and not grid[y-1][x].visible
    try:
        bottom = isinstance(grid[y+1][x], Empty) and not grid[y+1][x].visible
    except IndexError:
        bottom = False

    if isinstance(grid[y][x-1], Number) and x-1 >= 0:
        grid[y][x-1].visible = True
    try:
        if isinstance(grid[y][x+1], Number):
            grid[y][x+1].visible = True
    except IndexError:
        pass
    if isinstance(grid[y-1][x], Number) and y-1 >= 0:
        grid[y-1][x].visble = True
    try:
        if isinstance(grid[y+1][x], Number):
            grid[y+1][x].visible = True
    except IndexError:
        pass

    if isinstance(grid[y-1][x-1], Number) and x-1 >= 0 and y-1 >= 0:
        grid[y-1][x-1].visible = True
    try:
        if isinstance(grid[y+1][x+1], Number):
            grid[y+1][x+1].visible = True
    except IndexError:
        pass
    try:
        if isinstance(grid[y-1][x+1], Number) and y-1 >= 0:
            grid[y-1][x+1].visible = True
    except IndexError:
        pass
    try:
        if isinstance(grid[y+1][x-1], Number) and x-1 >= 0:
            grid[y+1][x-1].visible = True
    except IndexError:
        pass

    res = grid[:]
    if left:
        res[y][x-1].visible = True
        res = fill(res, x-1, y)
    if right:
        res[y][x+1].visible = True
        res = fill(res, x+1, y)
    if top:
        res[y-1][x].visible = True
        res = fill(res, x, y-1)
    if bottom:
        res[y+1][x].visible = True
        res = fill(res, x, y+1)
    return res


def won():
    for row in grid:
        for i in row:
            if not i.visible and not isinstance(i, Mine):
                return False
    return True


def handle_click(x, y):
    if isinstance(grid[y][x], Mine):
        game_over(x, y, won=won())
        return True
    elif isinstance(grid[y][x], Number):
        grid[y][x].visible = True
    elif isinstance(grid[y][x], Empty):
        fill(grid, x, y)
    return False


def place_flag(x, y):
    grid[y][x].flagged = not grid[y][x].flagged


WIDTH = 1800
HEIGHT = 900
BLOCK_SIZE = 60

pygame.display.set_caption('Minesweeper')
screen = pygame.display.set_mode([WIDTH, HEIGHT])

font = pygame.font.SysFont('Helvetica', 32)

WHITE = (255, 255, 255)
LIGHT_GRAY = (210, 210, 210)
GRAY = (180, 180, 180)
BLACK = (0, 0, 0)
RED = (230, 0, 0)

grid = create_grid(WIDTH // BLOCK_SIZE, HEIGHT // BLOCK_SIZE)

done = False
while not done:
    x, y = pygame.mouse.get_pos()
    mousex = (x - x % BLOCK_SIZE) // BLOCK_SIZE
    mousey = (y - y % BLOCK_SIZE) // BLOCK_SIZE
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            for row in grid:
                for i in row:
                    i.visible = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if handle_click(mousex, mousey):
                    grid = create_grid(WIDTH // BLOCK_SIZE, HEIGHT // BLOCK_SIZE)
            elif event.button == 3:
                place_flag(mousex, mousey)

    screen.fill(WHITE)

    render_grid(mouse_pos=[mousex, mousey])

    if won():
        game_over(0, 0, won=True)
        grid = create_grid(WIDTH // BLOCK_SIZE, HEIGHT // BLOCK_SIZE)
    
    pygame.display.update()

pygame.quit()
