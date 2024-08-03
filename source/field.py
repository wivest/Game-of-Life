import taichi as ti
from .aliases import Color
from .parameters import *


@ti.data_oriented
class Field:
    
    def __init__(self, cols: int, rows: int):
        self.cells = ti.field(ti.int32, (cols, rows))
        self.cells_after = ti.field(ti.int32, (cols, rows))
        self.pixels = Color.field(shape=(cols, rows))

    
    @ti.kernel
    def compute(self):
        for x, y in self.cells:
            if self.cells[x, y] % 2 == 1:
                if self.cells[x, y] != 7 and self.cells[x, y] != 9:
                    self.edit_neighbours_after(-1, x, y)
                    self.redraw_pixel(x, y, DEAD)
            elif self.cells[x, y] == 6:
                self.edit_neighbours_after(1, x, y)
                self.redraw_pixel(x, y, ALIVE)

        for x, y in self.cells:
            self.cells[x, y] = self.cells_after[x, y]


    @ti.kernel
    def randomize(self):
        self.clear()

        for x, y in self.cells:
            value = ti.random()
            if value <= PERCENTAGE:
                self.edit_neighbours_after(1, x, y)
                self.redraw_pixel(x, y, ALIVE)


    @ti.kernel
    def paint_cell(self, x: int, y: int):
        if self.cells[x, y] % 2 == 0:
            self.edit_neighbours(1, x, y)
            self.edit_neighbours_after(1, x, y)
            self.redraw_pixel(x, y, ALIVE)


    @ti.func
    def redraw_pixel(self, x: int, y: int, color: Color): # type: ignore
        self.pixels[x, y] = color


    @ti.func
    def clear(self):
        for x, y in self.cells:
            self.cells[x, y] = 0
            self.cells_after[x, y] = 0
            self.redraw_pixel(x, y, DEAD)


    @ti.func
    def edit_neighbours_after(self, difference: ti.int32, x: int, y: int):
        self.cells_after[x, y] += difference
        cols, rows = self.cells_after.shape
        for n in range(9):
            self.cells_after[(x - 1 + n%3) % cols, (y - 1 + n//3) % rows] += 2 * difference

            
    @ti.func
    def edit_neighbours(self, difference: ti.int32, x: int, y: int):
        self.cells[x, y] += difference
        cols, rows = self.cells.shape
        for n in range(9):
            self.cells[(x - 1 + n%3) % cols, (y - 1 + n//3) % rows] += 2 * difference
