import taichi as ti
from .field import Field


class Application:

    processing: bool = True
    drawing: bool = False

    def __init__(self, cols: int, rows: int):
        self.window = ti.ui.Window("Game of Life", (cols, rows))
        self.display = self.window.get_canvas()
        self.field = Field(cols, rows)
        self.field.randomize()


    def run(self):
        while self.window.running:
            self.handle_events()
            if not self.drawing:
                if self.processing:
                    self.field.compute()
            else:
                pass
            self.render()


    def render(self):
        self.display.set_image(self.field.pixels)
        self.window.show()


    def handle_events(self):
        for event in self.window.get_events(ti.ui.PRESS):
            if event.key == "r":
                self.field.randomize()
            if event.key == ti.ui.SPACE:
                self.processing = not self.processing
            if event.key == ti.ui.LMB:
                self.drawing = True

        for event in self.window.get_events(ti.ui.RELEASE):
            if event.key == ti.ui.LMB:
                self.drawing = False

    
    def get_cursor_coordinates(self) -> tuple[int, int]:
        clip = lambda value : max(0, min(value, 1))

        cursor_pos = self.window.get_cursor_pos()
        cursor_pos = (clip(cursor_pos[0]), clip(cursor_pos[1]))
        window_size = self.window.get_window_shape()

        x = int(cursor_pos[0] * window_size[0])
        y = int(cursor_pos[1] * window_size[1])
        return (x, y)
