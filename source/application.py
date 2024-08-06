from enum import Enum
import taichi as ti
from .field import Field


class Mode(Enum):
    VIEW = 0
    DRAWING = 1
    ERASING = 2


class Application:

    processing: bool = True
    mode: Mode = Mode.VIEW

    cursor: tuple[int, int] = (0, 0)
    brush: int = 1

    def __init__(self, cols: int, rows: int, size: int):
        self.window = ti.ui.Window("Game of Life", (cols * size, rows * size))
        self.display = self.window.get_canvas()
        self.field = Field(cols, rows, size)
        self.field.randomize()


    def run(self):
        while self.window.running:
            self.handle_events()
            cursor_new: tuple[int, int] = self.get_cursor_coordinates()

            match self.mode:
                case Mode.VIEW:
                    if self.processing:
                        self.field.compute()
                    self.field.restore_brush(*self.cursor, self.brush + 1)
                    self.field.highlight_brush(*cursor_new, self.brush)
                case Mode.DRAWING:
                    self.field.draw_line(*self.cursor, *cursor_new, True, self.brush)
                case Mode.ERASING:
                    self.field.draw_line(*self.cursor, *cursor_new, False, self.brush)
            
            self.cursor = cursor_new
            self.render()


    def render(self):
        self.display.set_image(self.field.pixels)
        self.window.show()


    def handle_events(self):
        for event in self.window.get_events(ti.ui.PRESS):
            match event.key:
                case "r":
                    self.field.randomize()
                case "c":
                    self.field.clear()
                case ti.ui.UP:
                    self.brush += 1
                case ti.ui.DOWN:
                    self.brush = max(1, self.brush - 1)
                case ti.ui.SPACE:
                    self.processing = not self.processing
                case ti.ui.LMB:
                    self.mode = Mode.DRAWING
                case ti.ui.RMB:
                    self.mode = Mode.ERASING
                    self.field.restore_brush(*self.cursor, self.brush)

        for event in self.window.get_events(ti.ui.RELEASE):
            match event.key:
                case ti.ui.LMB:
                    self.mode = Mode.VIEW
                case ti.ui.RMB:
                    self.mode = Mode.VIEW

    
    def get_cursor_coordinates(self) -> tuple[int, int]:
        clip = lambda value : max(0, min(value, 1))

        cursor_pos = self.window.get_cursor_pos()
        cursor_pos = (clip(cursor_pos[0]), clip(cursor_pos[1]))
        window_size = self.window.get_window_shape()

        x = int(cursor_pos[0] * (window_size[0] - 1) // self.field.size)
        y = int(cursor_pos[1] * (window_size[1] - 1) // self.field.size)
        return (x, y)
