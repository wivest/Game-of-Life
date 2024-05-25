import taichi as ti
from source.application import Application
from source.parameters import *


if __name__ == "__main__":
	ti.init(arch=ARCH, kernel_profiler=True)
	app = Application(COLS, ROWS)
	app.run()
	
	if PROFILING:
		ti.sync()
		ti.profiler.print_kernel_profiler_info()
