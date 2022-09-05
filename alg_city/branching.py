import cairo
import os
import colorsys
import numpy as np

out_file = r'output\test1.png'

size = (1024, 1024)
size_half = (size[0]//2, size[1]//2)
origin = (0.0 , 0.0)

# create the canvas
surface = cairo.ImageSurface(cairo.FORMAT_RGB24, *size)
ctx = cairo.Context(surface)
ctx.scale(*size_half)
ctx.translate(1.0, 1.0)

def rand(low, high):
    return np.random.rand() * (high - low) + low


def branch(start, angle, length, width, hue, saturation, value, level=0):
    if level > 6:
        return
    ctx.set_line_width(width)
    rgb = colorsys.hsv_to_rgb(hue, saturation, value)
    ctx.set_source_rgb(*rgb)
    ctx.move_to(*start)
    end = start[0] + np.cos(angle) * length, start[1] + np.sin(angle) * length
    ctx.line_to(*end)
    ctx.stroke()
    branch(end, angle+0.2, length*.85, width*.8, hue*.8,
           saturation, value, level+1)
    branch(end, angle-0.2, length*.85, width*.8, hue*.8,
           saturation, value, level+1)

for ang in np.arange(0, np.pi * 2.0, 0.6):
    hue = rand(0.0, 1.0)
    length = rand(0.15, 0.2)
    branch(origin, ang, length, 0.01, hue, 0.3, 0.8)

surface.write_to_png(out_file)
os.system(out_file)

