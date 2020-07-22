from Block import *
from Colours import *

global occupied_cells


class I:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.blocks = []
        for i in (0, 1, 2, 3,):
            block = Block(self.x, self.y - i, light_blue)
            self.blocks.append(block)
        self.stopped = False

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
        self.move_shape()

        for block in self.blocks:
            block.draw(screen)

