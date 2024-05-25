import taichi as ti
from application import Application
from parameters import *


ti.init(arch=ARCH, kernel_profiler=True)
app = Application(COLS, ROWS)
app.run()
