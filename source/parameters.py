import taichi as ti
from .aliases import Color


COLS = 1024
ROWS = 512
ARCH = ti.gpu
PROFILING = False

ALIVE = Color(255, 255, 255)
DEAD = Color(0, 0, 0)
PERCENTAGE = 0.1
