import taichi
from application import Application


COLS = 1400
ROWS = 700
SIZE = 1

taichi.init(arch=taichi.gpu)
app = Application(COLS, ROWS, SIZE)

app.run()
