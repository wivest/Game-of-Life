import pygame as pg
import sys
from field import Field


class Application:

    def __init__(self, cols: int, rows: int, size: int):
        self.display = pg.display.set_mode((cols*size, rows*size), pg.DOUBLEBUF)
        pg.display.set_caption("Loading...")
        self.clock = pg.time.Clock()

        self.field = Field(cols, rows, size)


    def run(self):
        while True:
            self.handle_events()
            self.field.compute()
            self.render()
            
            self.clock.tick(0)
            pg.display.set_caption(f"FPS: {round(self.clock.get_fps(), 2)}")


    def render(self):
        self.field.update_pixels()
        pixels_array = self.field.pixels.to_numpy()
        pg.surfarray.blit_array(self.display, pixels_array)
        pg.display.flip()


    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit(0)
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    self.field.randomize()
                elif event.key == pg.K_c:
                    self.field.clear()
