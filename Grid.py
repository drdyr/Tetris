import pygame as py


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        rect = py.Rect(40 * self.x, 40 * self.y, 40, 40)
        py.draw.rect(screen, (255, 255, 255), rect, 1)


class Grid:
    def __init__(self, width, height):
        self.cells = []
        for x in range(width):
            for y in range(height):
                cell = Cell(x, y)
                self.cells.append(cell)

    def draw(self, screen):
        for cell in self.cells:
            cell.draw(screen)
