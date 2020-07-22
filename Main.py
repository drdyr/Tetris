import pygame as py
import sys
from Block import Block
from Colours import *
from Grid import *
from Shapes import *

py.init()
clock = py.time.Clock()
cell_size = 40
screen_width, screen_height = 10 * cell_size, 20 * cell_size
screen = py.display.set_mode((screen_width, screen_height))

grid = Grid(10, 20)
shapes = []

exampleShape = I(2, 3)
shapes.append(exampleShape)

while True:
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            sys.exit()
        if event.type == py.KEYDOWN:
            if event.key == py.K_SPACE:
                new_shape = I(2, 0)
                shapes.append(new_shape)

    screen.fill((0, 0, 0))
    grid.draw(screen)

    for shape in shapes:
        shape.draw(screen)

    py.display.flip()
    clock.tick(3)
