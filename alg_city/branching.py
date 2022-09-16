import cairo
import os
import colorsys
import numpy as np

np.random.seed(44444)



# TODO create street lights along line segments
# TODO create street lights in discs

# parameters
size = (2048, 2048)
inner_disc_radius = 0.13
twist_angle = 0.19
disc_mult = 0.07
zoom = 0.5
depth_low = 2.9
depth_high = 6.1


out_file = r'output\test1.png'
pi2 = np.pi * 2.0

size_half = (size[0] // 2, size[1] // 2)
origin = (0.0, 0.0)


line_list = []
disc_list = []

# create the canvas
surface = cairo.ImageSurface(cairo.FORMAT_RGB24, *size)
ctx = cairo.Context(surface)
ctx.scale(size_half[0] * zoom, size_half[1] * zoom)
ctx.translate(1.0 / zoom, 1.0 / zoom)


def rand(low, high):
    return np.random.rand() * (high - low) + low


def branch(start, angle, angle_off, length, length_off, start_offset,  width,
           hue, saturation, value, twist, level=0):
    if level > rand(depth_low, depth_high):
        return
    ctx.set_line_width(width)
    rgb = colorsys.hsv_to_rgb(hue, saturation, value)
    ctx.set_source_rgb(*rgb)
    line_start = start[0] + np.cos(angle) * start_offset, \
        start[1] + np.sin(angle) * start_offset

    local_length = length + rand(0, length_off)
    end = start[0] + np.cos(angle) * local_length, \
          start[1] + np.sin(angle) * local_length

    num_branches = np.random.choice([1, 3, 5], p=[0.7, 0.2, 0.1])

    if num_branches > 3:
        end_radius = np.sqrt(end[0]**2 + end[1]**2)
        end_offset = disc_mult/(end_radius**0.3)
        ctx.arc(*end, end_offset, 0.0, pi2)
        disc_list.append((end, end_offset))
    else:
        end_offset = 0.0

    ctx.move_to(*line_start)


    line_end = start[0] + np.cos(angle) * (local_length - end_offset), \
        start[1] + np.sin(angle) * (local_length - end_offset)
    ctx.line_to(*line_end)
    ctx.stroke()

    line_list.append((line_start, line_end, level))

    ang_inc = 0.25

    ang_start = ((num_branches - 1.0)/2.0) * ang_inc


    for angle_loc in np.arange(-ang_start, ang_start + 0.1, ang_inc):
        angle_ran = rand(-angle_off, angle_off)
        branch(end, angle + angle_loc + angle_ran + twist, 0.15, local_length * .85,
               local_length * .38, end_offset, width * .6, hue * .8,
               saturation, value, twist, level + 1)


start_angle = rand(0.0, 0.3)
ctx.arc(*origin, inner_disc_radius, 0.0, pi2)
for ang in np.arange(start_angle, pi2, 0.5):
    hue = rand(0.0, 1.0)
    length = rand(0.20, 0.24)
    twist_factor = np.random.choice([-1.0, 1.0])
    branch(origin, ang + rand(-0.1, 0.1),
           ang / 8.0, length, length * 0.38, inner_disc_radius, 0.01,
           hue, 0.3, 0.8, twist_angle * twist_factor)


# street lights
for line in line_list:
    start, end, level = line
    start = np.array(start)
    end = np.array(end)
    diff = end - start
    perp_dist_factor = 0.014 - (level * 0.0018)

    perpen = (-diff[1], diff[0]) / np.linalg.norm(diff)

    ctx.set_line_width(0.003)
    inc = 0.035 * (level + 1.2)
    inc = max(0.13, inc)
    for l in np.arange(0, 1, inc):
        coord = start * (1.0-l) + end * l
        coordl = coord - perpen * perp_dist_factor
        coordr = coord + perpen * perp_dist_factor

        ctx.set_source_rgb(float(level) * .25, 0.1, 0.0)


        ctx.arc(*coordl, 0.003, 0.0, pi2)
        ctx.stroke()

        ctx.arc(*coordr, 0.003, 0.0, pi2)
        ctx.stroke()






surface.write_to_png(out_file)
