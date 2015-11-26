from tkinter import *

def x(pt,canvas_width):
    # canvas_width ignored
    return pt[0] + 10
def y(pt,canvas_height):
    return (canvas_height - (pt[1] + 10))

def draw_point(canvas, pt, canvas_height, canvas_width, fill="blue"):
    canvas.create_rectangle(x(pt,canvas_width),
                            y(pt,canvas_height),
                            x(pt,canvas_width),
                            y(pt,canvas_height),
                            fill=fill)
    
def draw_line(canvas, start, end, canvas_height, canvas_width, fill="red"):
    canvas.create_line(x(start,canvas_width),
                       y(start,canvas_height),
                       x(end,canvas_width),
                       y(end,canvas_height),
                       fill=fill)

def draw(canvas, pts, lns, scale, canvas_height, canvas_width):
    canvas.delete(ALL)
    def scale_point(pt):
        return [scale*pt[0], scale*pt[1]]
    scaled_pts = [scale_point(pt) for pt in pts]
    scaled_lines = [[scale_point(p1),scale_point(p2)] for [p1,p2] in lns]
    for st, en in scaled_lines:
        draw_line(canvas, st, en, canvas_height, canvas_width)
    for pt in scaled_pts:
        draw_point(canvas, pt, canvas_height, canvas_width)

def run(point_data, line_data, max_x_val, max_y_val):
    root = Tk()
    canvas_height = 1020
    canvas_width = 1020
    canvas = Canvas(root,
                    width = canvas_width,
                    height = canvas_height)
    canvas.pack()
    root.canvas = canvas.canvas = canvas
    canvas.data = { }
    # available y and x room
    # subtracting 10 to deal with the offsets built into functions
    # `x' and `y'
    #
    # subtracting another 10 to leave room on other side
    canvas_y_avail = canvas_height - 10 - 10
    canvas_x_avail = canvas_width - 10 - 10
    # at 1 this will attempt to fill the canvas
    # higher values fill less
    scale_factor = 1
    # scale according to most restrictive dimension
    # this code is circuituous to be more legible
    if max_y_val/canvas_y_avail > max_x_val/canvas_x_avail:
        limiting_side = "y"
    else:
        limiting_side = "x"
    # scaling factor found
    if limiting_side == "y":
        scale = canvas_y_avail/(scale_factor*max_y_val)
    else:
        scale = canvas_x_avail/(scale_factor*max_x_val)
    draw(canvas, point_data, line_data, scale, canvas_height, canvas_width)
    root.mainloop()

def draw_hull(point_data, hull_points):
    line_data = []
    prev = hull_points[0]
    for pt in hull_points[1:] + [prev]:
        line_data.append((prev, pt,))
        prev = pt
    max_x_val = max(p[0] for p in hull_points)
    max_y_val = max(p[1] for p in hull_points)
    run(point_data, line_data, max_x_val, max_y_val)
    

def draw_hull_indexes(point_data, hull_data):
    """
    Call this function!
    point_data is a list of tuples containing xy values: [(x, y), (x, y) ...]
    hull_data is a list of indexes of xy values: [0, 4, 7...]
    There will be a 10px padding around where the points are drawn.
    The points draw in a 
    """
    draw_hull(point_data, list(map(lambda i: point_data[i], hull_data)))
