import taichi as ti
from .aliases import Color
from .parameters import *


@ti.data_oriented
class Field:

    size: int
    
    def __init__(self, cols: int, rows: int, cell_pixels: int):
        self.size = cell_pixels

        self.cells = ti.field(ti.int32, (cols, rows))
        self.cells_after = ti.field(ti.int32, (cols, rows))
        self.pixels = Color.field(shape=(cols * self.size, rows * self.size))

    
    @ti.kernel
    def compute(self):
        for x, y in self.cells:
            if self.cells[x, y] % 2 == 1:
                if self.cells[x, y] != 7 and self.cells[x, y] != 9:
                    self.edit_neighbours_after(-1, x, y)
                    self.redraw_cell(x, y, DEAD)
            elif self.cells[x, y] == 6:
                self.edit_neighbours_after(1, x, y)
                self.redraw_cell(x, y, ALIVE)

            neighbours = self.cells[x, y] // 2
            if neighbours != self.count_neighbours(x, y):
                self.redraw_cell(x, y, DEBUG_COLOR)

        for x, y in self.cells:
            self.cells[x, y] = self.cells_after[x, y]


    @ti.kernel
    def clear(self):
        for x, y in self.cells:
            self.cells[x, y] = 0
            self.cells_after[x, y] = 0
            self.redraw_cell(x, y, DEAD)


    @ti.kernel
    def randomize(self):
        self.empty()

        for x, y in self.cells:
            value = ti.random()
            if value <= PERCENTAGE:
                self.edit_neighbours_after(1, x, y)
                self.redraw_cell(x, y, ALIVE)


    @ti.kernel
    def draw_line(self, x1: int, y1: int, x2: int, y2: int, state: bool, brush: int):
        dx = 1 if x1 == x2 else x2 - x1
        dy = 1 if y1 == y2 else y2 - y1

        for x in range(min(x1, x2), max(x1, x2) + 1):
            y = y1 + (y2 - y1) * (x - x1) / dx
            self.paint_brush(x, y, state, brush)
        for y in range(min(y1, y2), max(y1, y2) + 1):
            x = x1 + (x2 - x1) * (y - y1) / dy
            self.paint_brush(x, y, state, brush)


    @ti.kernel
    def highlight_brush(self, x: int, y: int, brush: int):
        cols, rows = self.cells.shape
        side = 2 * brush - 1

        for n in range(side * side):
            i, j = (x - brush + 1 + n%side) % cols, (y - brush + 1 + n//side) % rows
            if self.cells_after[i, j] % 2 == 0:
                self.redraw_cell(i, j, HIGHLIGHT)


    @ti.kernel
    def restore_brush(self, x: int, y: int, brush: int):
        cols, rows = self.cells.shape
        side = 2 * brush - 1

        for n in range(side * side):
            i, j = (x - brush + 1 + n%side) % cols, (y - brush + 1 + n//side) % rows
            color = ALIVE if self.cells_after[i, j] % 2 == 1 else DEAD
            self.redraw_cell(i, j, color)


    @ti.func
    def paint_cell(self, x: int, y: int, state: bool):
        if bool(self.cells[x, y] % 2) != state:
            if state:
                self.edit_neighbours(1, x, y)
                self.edit_neighbours_after(1, x, y)
                self.redraw_cell(x, y, ALIVE)
            elif not state:
                self.edit_neighbours(-1, x, y)
                self.edit_neighbours_after(-1, x, y)
                self.redraw_cell(x, y, DEAD)


    @ti.func
    def paint_brush(self, x: int, y: int, state: bool, brush: int):
        cols, rows = self.cells.shape
        side = 2 * brush - 1

        for n in range(side * side):
            self.paint_cell((x - brush + 1 + n%side) % cols, (y - brush + 1 + n//side) % rows, state)


    @ti.func
    def redraw_cell(self, x: int, y: int, color: Color): # type: ignore
        for i in range(x * self.size, x * self.size + self.size):
            for j in range(y * self.size, y * self.size + self.size):
                self.pixels[i, j] = color


    @ti.func
    def empty(self):
        for x, y in self.cells:
            self.cells[x, y] = 0
            self.cells_after[x, y] = 0
            self.redraw_cell(x, y, DEAD)


    @ti.func
    def edit_neighbours_after(self, difference: ti.int32, x: int, y: int): # type: ignore
        self.cells_after[x, y] += difference
        cols, rows = self.cells_after.shape
        for n in range(9):
            self.cells_after[(x - 1 + n%3) % cols, (y - 1 + n//3) % rows] += 2 * difference

            
    @ti.func
    def edit_neighbours(self, difference: ti.int32, x: int, y: int): # type: ignore
        self.cells[x, y] += difference
        cols, rows = self.cells.shape
        for n in range(9):
            self.cells[(x - 1 + n%3) % cols, (y - 1 + n//3) % rows] += 2 * difference


    @ti.func
    def count_neighbours(self, x: int, y: int) -> int:
        count = 0
        cols, rows = self.cells.shape

        for n in range(9):
            count += self.cells[(x - 1 + n%3) % cols, (y - 1 + n//3) % rows] % 2

        return count
