"""Graphical representation of a delaunator triangulation.

Commands:
    ESC: quit
    ESPACE or ENTER: add a Point at mouse position
    DELETE: remove Point at mouse position
    drag&drop: on Point for move it
    a: toggle auto-adding of Point
    t: toggle random moving
    s: take a snapshot of all points positions
    ARROWS: movement of 500 px on dragged Point [NOT IMPLEMENTED]

"""


from pydelaunator    import Mesh
from random          import randint, choice
from pyglet.window   import key
from pyglet.window   import mouse
import itertools
import functools
import pyglet
import time
import math
import sys


INTERFACE_TIME_SPEED    = 0.01
SIMULATION_FPS          = 10
PROGRAM_NAME            = "Delaunator 0.1"
MOUSE_PRECISION         = 400
UNIVERSE_SIZE           = (600, 600)
VIDEO_PADDING           = 50

VIDEO_MODE_X            = UNIVERSE_SIZE[0] + VIDEO_PADDING*2
VIDEO_MODE_Y            = UNIVERSE_SIZE[1] + VIDEO_PADDING*2


# states
auto_add = False
auto_mov = False
dragged_point = None
mouse_position = None
counter = 0
dt = None

# pyglet
window = pyglet.window.Window(
    width=VIDEO_MODE_X, height=VIDEO_MODE_Y,
    caption=PROGRAM_NAME
)

# flags
PRINT_EDGES = True
class Point:
    """Objects put in the triangulation"""
    def __init__(self, color=None):
        self.color = color or tuple(randint(1, 255) for _ in range(4))


def screen_position_to_dt_position(pos:tuple) -> tuple:
    x, y = pos
    return x - VIDEO_PADDING, y - VIDEO_PADDING
def dt_position_to_screen_position(pos:tuple) -> tuple:
    x, y = pos
    return x + VIDEO_PADDING, y + VIDEO_PADDING


def start_gui(dt_object):
    """dt must be a delaunator object"""
    # first printings
    global dt
    dt = dt_object
    print("WANDA JACKSON")
    print(__doc__)

    # just for begin…
    # for i in range(4):
        # _addPointToDT()
    # UNIT TEST 0
    # _addPointToDT(300, 300)
    # UNIT TEST 1
    # _addPointToDT(200, 100)
    # _addPointToDT(100,   0)
    # _addPointToDT(  0, 100)
    # _addPointToDT(100, 200)
    # _addPointToDT(221, 249)
    # _addPointToDT(258, 305)
    # UNIT TEST 2: test the face stacking when simplifying delaunay
    #   triangulation in suppression point algorithm.
    # _addPointToDT(121, 5)
    # _addPointToDT(161, 61)
    # _addPointToDT(211, 135)
    # _addPointToDT(282, 176)
    # _addPointToDT(357, 54) # its d
    # _addPointToDT(508, 253)
    # _addPointToDT(533, 52)
    # UNIT TEST 3
    # _addPointToDT(91, 372)
    # _addPointToDT(122, 309)
    # _addPointToDT(118, 204)
    # _addPointToDT(250, 575)
    # _addPointToDT(312, 107)
    # _addPointToDT(387, 204)
    # _addPointToDT(506, 480)
    # _addPointToDT(493, 216)
    # _addPointToDT(308, 373)
    # UNIT TEST 4
    _addPointToDT(75, 381)
    _addPointToDT(133, 192)
    _addPointToDT(249, 574)
    _addPointToDT(320, 107)
    _addPointToDT(503, 488)
    _addPointToDT(528, 209)
    _addPointToDT(465, 325)

    # run pyglet printings
    pyglet.app.run()
    pyglet.app.exit()
    print("\nWANDA JACKSOFF")


@window.event
def on_key_press(symbol, modifiers):
    global auto_add, mouse_position
    if symbol == key.RETURN or symbol == key.SPACE: # add point
        if mouse_position is not None:
            _addPointToDT(*mouse_position)
    elif symbol in (key.A, key.B):
        if auto_add:
            pyglet.clock.unschedule(schedulable_addPointToDT)
        else:
            pyglet.clock.schedule_interval(
                schedulable_addPointToDT,  # dt argument is useless
                interval=INTERFACE_TIME_SPEED
            )
        auto_add = not auto_add
    elif symbol in (key.M, key.T):
        _moveAllPoints()
    elif symbol in (key.S,):
        _snapshot()
    elif symbol == key.DELETE:  # del point
        if mouse_position is not None:
            _delPoint(_getPointAt(*mouse_position))


@window.event
def on_mouse_motion(x, y, dx, dy):
    global mouse_position
    mouse_position = screen_position_to_dt_position((x, y))

@window.event
def on_mouse_press(x, y, buttons, modifiers):
    global dt, mouse_position, dragged_point
    mouse_position = screen_position_to_dt_position((x, y))
    if buttons == pyglet.window.mouse.LEFT:
        dragged_point = _getPointAt(*mouse_position)

@window.event
def on_mouse_release(x, y, buttons, modifiers):
    global mouse_position, dragged_point
    mouse_position = screen_position_to_dt_position((x, y))
    if buttons == pyglet.window.mouse.LEFT:
        dragged_point = None
    if dragged_point is not None:
        movePoint(dx, dy, dragged_point)

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    global mouse_position, dragged_point
    if dragged_point is not None:
        _movePoint(dx, dy, dragged_point)

@window.event
def on_draw():
    global dt, mouse_position, dragged_point
    window.clear()
    _draw_edges()
    # print number of objects in stdout
    print('\r', sum(1 for _ in dt), end='')
    sys.stdout.flush() # print even if line is not finish



################# DRAW METHODS #################
def _draw_edges():
    """Print current state of engine"""
    global dt, dragged_point
    def print_edge(coords, color, width=1):
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                                 ('v2f', coords),
                                 ('c4B', color),
                            ) #TODO: use width

    if not PRINT_EDGES:
        return

    color_green = (0, 255, 0, 255)
    color_red   = (255, 0, 0, 255)
    diameter = 20
    for edge in dt.edges:
        if edge in dt.outside_objects:  continue
        source, target = edge.origin_vertex, edge.target_vertex
        p1 = dt_position_to_screen_position(source.position)
        p2 = dt_position_to_screen_position(target.position)
        source_color = color_red if source is dragged_point else getattr(source.payload, 'color', color_green)
        target_color = color_red if target is dragged_point else getattr(target.payload, 'color', color_green)
        print_edge((*p1, *p2), source_color + target_color)


################# POINT FUNCTIONS #################
def schedulable_addPointToDT(dt, *args, **kwargs):
    return _addPointToDT(*args, **kwargs)

def _addPointToDT(x=None, y=None):
    """Add a random point in DT"""
    global dt
    assert x is None or isinstance(x, int)
    assert y is None or isinstance(y, int)
    coords = x or randint(1, dt.width-1), y or randint(1, dt.height-1)
    print(x, y)
    print(coords)
    print("Add point at ({};{})".format(*coords))
    dt.add(Point(), *coords)


def _delPoint(point):
    """Delete given Point"""
    global dt, dragged_point
    if point is not None:
        if dragged_point == point:
            dragged_point = None
        try:
            dt.remove(point)
        except ValueError as err:
            print(err)


def _getPointAt(x, y):
    """Return point that is at given coordinates (about MOUSE_PRECISION)"""
    global dt
    try:
        return next(iter(dt.vertices_at((x, y), MOUSE_PRECISION)))
    except StopIteration:
        return None


def _movePoint(x, y, p):
    """Add given values to (x;y) of given point"""
    global dt
    if p is not None:
        dt.move(p, x, y)


def _moveAllPoints():
    """Move all vertices by a small move"""
    global dt, dragged_point
    for v in dt.vertices:
        if v.payload:
            eps = 1
            mx = choice([-eps,eps])
            my = choice([-eps,eps])
            if v is not dragged_point:
                dt.move(v, (mx, my))


def _snapshot():
    global dt
    print('\nsnapshot:')
    for c in (o.coordinates() for o in dt.trianguledObjects()):
        print('\t_addPointToDT' + str((c.x, c.y)))


if __name__ == '__main__':
    dt = Mesh(*UNIVERSE_SIZE)
    start_gui(dt)
