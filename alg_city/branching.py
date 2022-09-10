import cairo
import os
import colorsys
import numpy as np

import geopandas as gpd


out_file = r'output\test1.png'

size = (2048, 2048)
size_half = (size[0]//2, size[1]//2)
origin = (0.0 , 0.0)

# create the canvas
surface = cairo.ImageSurface(cairo.FORMAT_RGB24, *size)
ctx = cairo.Context(surface)
ctx.scale(*size_half)
ctx.translate(1.0, 1.0)

def rand(low, high):
    return np.random.rand() * (high - low) + low


def branch(start, angle, angle_off, length, length_off, width, hue, saturation, value,
           level=0):
    if level > rand(4.9, 9.1):
        return
    ctx.set_line_width(width)
    rgb = colorsys.hsv_to_rgb(hue, saturation, value)
    ctx.set_source_rgb(*rgb)
    ctx.move_to(*start)
    local_length = length + rand(-length_off, length_off)
    end = start[0] + np.cos(angle) * local_length, start[1] + np.sin(angle) * local_length
    ctx.line_to(*end)
    ctx.stroke()

    num_branches = np.random.choice([2,3], p=[0.75, 0.25])
    if num_branches == 2:
        ang_inc = 0.4
    else:
        ang_inc = 0.2


    for angle_loc in np.arange(-0.2, 0.21, ang_inc):
        angle_ran = rand(-angle_off, angle_off)
        branch(end, angle+angle_loc + angle_ran, 0.15, local_length*.85,
               local_length*.38, width*.8, hue*.8,
           saturation, value, level+1)

start_angle = rand(0.0, 0.5)
for ang in np.arange(0, np.pi * 2.0, 0.6):
    hue = rand(0.0, 1.0)
    length = rand(0.10, 0.14)
    branch(origin, ang + rand(-0.1, 0.1),
           ang/8.0, length, length * 0.38, 0.01, hue, 0.3, 0.8)

surface.write_to_png(out_file)


