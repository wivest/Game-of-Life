import taichi
from application import Application


COLS = 1400
ROWS = 700

taichi.init(arch=taichi.gpu)
app = Application(COLS, ROWS)

app.run()
