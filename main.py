import pygame, taichi
from application import Application


COLS = 1400
ROWS = 700
SIZE = 1

taichi.init(arch=taichi.gpu)
pygame.init()
app = Application(COLS, ROWS, SIZE)

app.run()
