import cairo
import os
import colorsys
import numpy as np

out_file = r'output\test1.png'

size = (1024, 1024)
size_half = (size[0]//2, size[1]//2)
origin = (0.0 , 0.0)
surface = cairo.ImageSurface(cairo.FORMAT_RGB24, *size)
ctx = cairo.Context(surface)

ctx.scale(*size_half)
ctx.translate(1.0, 1.0)


ctx.set_line_width(0.005)

for ang in np.arange(0, np.pi * 2.0, 0.1):
    hue = np.random.rand()
    radius = np.random.rand() * .5 + .5
    rgb = colorsys.hsv_to_rgb(hue, 0.3, 0.75)
    ctx.set_source_rgb(*rgb)
    target = np.cos(ang) * radius, np.sin(ang) * radius
    ctx.move_to(*origin)
    ctx.line_to(*target)
    ctx.stroke()

surface.write_to_png(out_file)
os.system(out_file)

