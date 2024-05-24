import taichi as ti


@ti.data_oriented
class Field:

    alive = ti.Vector((255, 255, 255), ti.u8)
    dead = ti.Vector((10, 10, 10), ti.u8)
    grid = ti.Vector((30, 30, 30), ti.u8)

    spawn_chance = 0.3
    grid_size = 0
    
    def __init__(self, cols: int, rows: int, size: int):
        self.size = size
        self.field = ti.field(ti.int32, (cols, rows))
        self.field_update = ti.field(ti.int32, (cols, rows))
        self.pixels: ti.Field = ti.Vector.field(3, ti.u8, shape=(cols*size, rows*size))

    
    @ti.kernel
    def compute(self):
        for x, y in self.field:
            state = self.field[x, y]
            if state != 0:
            
                life = state % 2
                neighbours = state // 2

                if life and (neighbours != 3 and neighbours != 4):
                    self._edit_neighbours_update(-1, x, y)
                elif not life and neighbours == 3:
                    self._edit_neighbours_update(1, x, y)

        self.apply()

    
    @ti.func
    def apply(self):
        for x, y in self.field:
            self.field[x, y] = self.field_update[x, y]


    @ti.kernel
    def update_pixels(self):
        for x, y in self.pixels:
            col = x // self.size
            row = y // self.size

            if self.field[col, row] % 2:
                self.pixels[x, y] = self.alive
            elif x % self.size < self.grid_size or y % self.size < self.grid_size:
                self.pixels[x, y] = self.grid
            else:
                self.pixels[x, y] = self.dead


    @ti.kernel
    def clear(self):
        self._clear()


    @ti.kernel
    def randomize(self):
        self._clear()

        for x, y in self.field:
            value: ti.float32 = ti.random(ti.float32)
            if value <= self.spawn_chance:
                self._edit_neighbours(1, x, y)
                self._edit_neighbours_update(1, x, y)


    @ti.func
    def _edit_neighbours(self, difference: ti.int32, x: ti.int32, y: ti.int32):
        self.field[x, y] += 1 * difference
        cols, rows = self.field.shape
        for n in range(9):
            self.field[(x - 1 + n%3) % cols, (y - 1 + n//3) % rows] += 2 * difference


    @ti.func
    def _edit_neighbours_update(self, difference: ti.int32, x: ti.int32, y: ti.int32):
        self.field_update[x, y] += 1 * difference
        cols, rows = self.field_update.shape
        for n in range(9):
            self.field_update[(x - 1 + n%3) % cols, (y - 1 + n//3) % rows] += 2 * difference


    @ti.func
    def _clear(self):
        for x, y in self.field:
            self.field[x, y] = 0
            self.field_update[x, y] = 0
