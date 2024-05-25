import taichi as ti
from aliases import *


COLS = 1024
ROWS = 512
ARCH = ti.gpu

ALIVE = Color(255, 255, 255)
DEAD = Color(0, 0, 0)
CORRELATION = 0.1
