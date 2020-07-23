import pygame as py
import sys
from Block import *
from Colours import *
from Grid import *
import random

py.init()

occupied_cells = [

]


clock = py.time.Clock()
cell_size = 40
screen_width, screen_height = 10 * cell_size, 20 * cell_size
screen = py.display.set_mode((screen_width, screen_height))

grid = Grid(10, 20)


shapes = {
    'I': {'colour': light_blue, 'block_positions': [(0, 0), (0, -1), (0, -2), (0, -3)], 'pivots': [1, 2]},
    'O': {'colour': yellow, 'block_positions': [(0, 0), (0, -1), (-1, -1), (-1, 0)], 'pivots': [1, 2]},
    'T': {'colour': purple, 'block_positions': [(-1, 0), (0, 0), (0, 1), (1, 0)], 'pivots': [1, 1]},
    'J': {'colour': blue, 'block_positions': [(0, 0), (1, 0), (1, -1), (1, -2)], 'pivots': [1, 2]},
    'L': {'colour': orange, 'block_positions': [(0, 0), (-1, 0), (-1, -1), (-1, -2)], 'pivots': [1, 2]},
    'S': {'colour': green, 'block_positions': [(-1, 0), (0, 0), (0, -1), (1, -1)], 'pivots': [1, 2]},
    'Z': {'colour': red, 'block_positions': [(1, 0), (0, 0), (0, -1), (-1, -1)], 'pivots': [1, 2]},
}

shape_types = ['I', 'O', 'T', 'J', 'L', 'S', 'Z']

class Block:
    def __init__(self, x, y, colour):
        self.x = x
        self.y = y
        self.colour = colour


    def draw(self, screen):
        rect = py.Rect(self.x * 40 + 1, self.y * 40 + 1, 38, 38)
        py.draw.rect(screen, self.colour, rect, 0)

    def move(self):
        self.y += 1

    def can_move_down(self):
        return self.y != 19 and (self.x, self.y + 1) not in occupied_cells

class Shape:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.blocks = []
        self.colour = shapes[self.shape]['colour']
        self.pivots = shapes[self.shape]['pivots']

        for coordinate in shapes[self.shape]['block_positions']:
            block = Block(self.x + coordinate[0], self.y + coordinate[1], self.colour)
            self.blocks.append(block)

        self.clockwise_pivot = self.blocks[self.pivots[0]]
        self.anti_clockwise_pivot = self.blocks[self.pivots[1]]

        self.stopped = False
        self.left = False
        self.right = False
        self.insta_move = False

    def check_left(self):
        for block in self.blocks:
            if block.x == 0 or (block.x - 1, block.y) in occupied_cells:
                return False
        return True

    def check_right(self):
        for block in self.blocks:
            if block.x == 9 or (block.x + 1, block.y) in occupied_cells:
                return False
        return True

    def move_horizontally(self):
        if not self.stopped and frames % 3 == 0 and not self.insta_move:
            if self.right and self.check_right():
                for block in self.blocks:
                    block.x += 1
            if self.left and self.check_left():
                for block in self.blocks:
                    block.x -= 1

    def rotate(self, direction):
        i = 1
        j = 1
        if direction == 'clockwise':
            j = -1
            pivot = self.clockwise_pivot
        if direction == 'anticlockwise':
            i = -1
            pivot = self.anti_clockwise_pivot
        if not self.stopped and not self.insta_move:
            trial_coordinates = []
            for block in self.blocks:
                if block is not pivot:
                    temp_x = block.x
                    temp_y = block.y
                    #  STEP 1: subtract pivot coordinate from all blocks
                    temp_x -= pivot.x
                    temp_y -= pivot.y

                    # STEP 2: rotate around origin using matrix rotation
                    temp_x_2 = i * temp_y
                    temp_y_2 = j * temp_x
                    temp_x = temp_x_2
                    temp_y = temp_y_2

                    # STEP 3: add back pivot coordinate to all blocks
                    temp_x += pivot.x
                    temp_y += pivot.y

                    if temp_y > 19 or temp_x < 0 or temp_x > 9:
                        return

                    trial_coordinates.append((temp_x, temp_y))
                else:
                    trial_coordinates.append((block.x, block.y))

            count = 0
            for block in self.blocks:
                block.x, block.y = trial_coordinates[count]
                count += 1

            #  STEP 4: move pivot
            self.clockwise_pivot, self.anti_clockwise_pivot = self.anti_clockwise_pivot, self.clockwise_pivot

    def move_down(self):
        for block in self.blocks:
            if not block.can_move_down():
                if not self.stopped:
                    for block in self.blocks:
                        occupied_cells.append((block.x, block.y))
                        stoppedBlocks.append(block)
                    self.stopped = True

        if not self.stopped:
            for block in self.blocks:
                block.move()

    def drop(self):
        if self.insta_move:
            self.move_down()

    def draw(self, screen):
        self.drop()

        if frames % 30 == 0 and not self.insta_move:
            self.move_down()

        for block in self.blocks:
            block.draw(screen)


rand_shape = random.choice(shape_types)

currentShape = Shape(5, 0, rand_shape)
stoppedBlocks = []


def create_new():
    global currentShape
    if currentShape.stopped:

        print("Shape stopped----------------------------")
        print(len(stoppedBlocks))
        print(len(occupied_cells))

        rand_shape = random.choice(shape_types)
        currentShape = Shape(5, 0, rand_shape)



def line_check():
    global occupied_cells
    global stoppedBlocks

    rows_to_be_deleted = []
    for y in range(20):
        for x in range(10):
            if (x, y) not in occupied_cells:
                break
            if x == 9:
                rows_to_be_deleted.append(y)

    if len(rows_to_be_deleted) >= 1:
        before_coordinates = []
        for block in stoppedBlocks:
            before_coordinates.append((block.x, block.y))
        print("Just before deletion----------------------------------------")
        print(before_coordinates)
        print(occupied_cells)
        print(len(before_coordinates))
        print(len(occupied_cells))
        print(rows_to_be_deleted)

        for block in stoppedBlocks:
            if block.y in rows_to_be_deleted:
                stoppedBlocks.remove(block)
                occupied_cells.remove((block.x, block.y))
                continue


        print("After deletion---------")
        print("occupied cells", occupied_cells)
        print("no occupied cells", len(occupied_cells))
frames = 0
py.time.delay(500)

while True:

    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            sys.exit()
        if event.type == py.MOUSEBUTTONDOWN:
            currentShape.rotate('clockwise')
        if event.type == py.KEYDOWN:
            if event.key == py.K_w:
                currentShape.rotate('anticlockwise')
            if event.key == py.K_s:
                currentShape.rotate('clockwise')
            if event.key == py.K_a:
                currentShape.left = True
            if event.key == py.K_d:
                currentShape.right = True
            if event.key == py.K_SPACE:
                currentShape.insta_move = True
        if event.type == py.KEYUP:
            if event.key == py.K_a:
                currentShape.left = False
            if event.key == py.K_d:
                currentShape.right = False

    screen.fill((0, 0, 0))
    grid.draw(screen)

    currentShape.move_horizontally()
    currentShape.draw(screen)

    create_new()
    line_check()


    for block in stoppedBlocks:
        block.draw(screen)


    py.display.flip()
    frames += 1
    clock.tick(60)
