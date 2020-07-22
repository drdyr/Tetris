import pygame as py
import sys
from Block import *
from Colours import *
from Grid import *

py.init()
global occupied_cells
clock = py.time.Clock()
cell_size = 40
screen_width, screen_height = 10 * cell_size, 20 * cell_size
screen = py.display.set_mode((screen_width, screen_height))

grid = Grid(10, 20)
shapes = []



class I:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.blocks = []
        for i in (0, 1, 2, 3,):
            block = Block(self.x, self.y - i, light_blue)
            self.blocks.append(block)
        self.clockwise_pivot = self.blocks[2]
        self.anti_clockwise_pivot = self.blocks[1]

        self.stopped = False

    def rotate(self, direction):
        i = 1
        j = 1

        if direction == 'clockwise':
            j = -1
            pivot = self.clockwise_pivot
        if direction == 'anticlockwise':
            i = -1
            pivot = self.anti_clockwise_pivot

        if not self.stopped:
            for block in self.blocks:
                if block is not pivot:

                    #  STEP 1: subtract pivot coordinate from all blocks
                    block.x -= pivot.x
                    block.y -= pivot.y

                    # STEP 2: rotate around origin using matrix rotation
                    temp_x = i * block.y
                    temp_y = j * block.x
                    block.x = temp_x
                    block.y = temp_y

                    # STEP 3: add back pivot coordinate to all blocks
                    block.x += pivot.x
                    block.y += pivot.y

            #  STEP 4: move pivot
            self.clockwise_pivot, self.anti_clockwise_pivot = self.anti_clockwise_pivot, self.clockwise_pivot

    def move_shape(self):
        for block in self.blocks:
            if not block.can_move():
                if not self.stopped:
                    occupied_cells.append((block.x, block.y))
                    self.stopped = True
                return
        for block in self.blocks:
            block.move()

    def draw(self, screen):
        if frames % 20 == 0:
            self.move_shape()

        for block in self.blocks:
            block.draw(screen)


exampleShape = I(3, 5)
shapes.append(exampleShape)

frames = 0

while True:
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            sys.exit()
        if event.type == py.KEYDOWN:
            if event.key == py.K_LEFT:
                exampleShape.rotate('anticlockwise')
            if event.key == py.K_RIGHT:
                exampleShape.rotate('clockwise')

    screen.fill((0, 0, 0))
    grid.draw(screen)

    for shape in shapes:
        shape.draw(screen)

    py.display.flip()
    frames += 1
    clock.tick(60)
