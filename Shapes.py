from Block import *
from Colours import *
from Main import frames



global occupied_cells

class I:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.blocks = []
        for i in (0, 1, 2, 3,):
            block = Block(self.x, self.y - i, light_blue)
            self.blocks.append(block)
        self.pivot = self.blocks[2]
        self.stopped = False

    def rotate(self, direction):
        if direction == 'clockwise':
            for block in self.blocks:
                if block is not self.pivot:

                    #  STEP 1: subtract pivot coordinate from all blocks
                    block.x -= self.pivot.x
                    block.y -= self.pivot.y

                    # STEP 2: rotate around origin using matrix rotation
                    temp_x = block.y
                    temp_y = -1 * block.x
                    block.x = temp_x
                    block.y = temp_y

                    # STEP 3: add back pivot coordinate to all blocks
                    block.x += self.pivot.x
                    block.y += self.pivot.y

            #  STEP 4: move pivot
            if self.pivot == self.blocks[2]:
                self.pivot = self.blocks[1]
            else:
                self.pivot = self.blocks[2]

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

