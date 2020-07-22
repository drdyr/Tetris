from Block import *
from Colours import *

global occupied_cells

class I:
    def __init__(self, x , y):
        self.x = x
        self.y = y
        self.blocks = []
        self.main = Block(self.x, self.y, light_blue)
        self.blocks.append(self.main)
        for i in (1, 2, 3):
            block = Block(self.x, self.y - i, light_blue)
            self.blocks.append(block)

    def draw(self, screen):
        if self.main.can_move():
            for block in self.blocks:
                block.move()

        elif not self.main.stopped:
            for block in self.blocks:
                occupied_cells.append((block.x, block.y))
                block.stopped = True

        for block in self.blocks:
            block.draw(screen)

