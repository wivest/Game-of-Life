import json
import taichi as ti
from .aliases import Color


PATH = "parameters.json"


with open(PATH) as f:
	data = json.load(f)


COLS = data["columns"]
ROWS = data["rows"]
SIZE = data["size"]
ARCH = getattr(ti, data["arch"])
PROFILING = data["profiling"]

ALIVE = Color(*data["alive"])
DEAD = Color(*data["dead"])
HIGHLIGHT = Color(*data["highlight"])
PERCENTAGE = data["percentage"]
