import taichi as ti
from field import Field


class Application:

    def __init__(self, cols: int, rows: int):
        self.display = ti.GUI("Game of Life", (cols, rows), fast_gui=True)
        self.display.fps_limit = 1000
        self.field = Field(cols, rows)


    def run(self):
        while self.display.running:
            self.handle_events()
            self.field.compute()
            self.render()


    def render(self):
        self.field.update_pixels()
        self.display.set_image(self.field.pixels)
        self.display.show()


    def handle_events(self):
        for event in self.display.get_events():
            if event.type == ti.GUI.PRESS:
                if event.key == "r":
                    self.field.randomize()
                elif event.key == "c":
                    self.field.clear()
