import pygame as py

occupied_cells = []


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

    def can_move(self):
        return self.y != 19 and (self.x, self.y + 1) not in occupied_cells

