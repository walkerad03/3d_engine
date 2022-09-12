import numpy as np
import math

class Point:
    """A point object used to help store data for other 3d objects."""
    def __init__(self, pos):
        self.pos = pos

class Box:
    """A 3d box object."""
    def __init__(self, pos, rotation, scale):
        """Constructor for the box object."""
        self.pos = -pos
        self.rotation = -rotation
        self.scale = -scale

        self.points = []
        self.points.append(Point(np.array([0.5, -0.5, -0.5])))   
        self.points.append(Point(np.array([0.5, 0.5, -0.5])))
        self.points.append(Point(np.array([0.5, 0.5, 0.5])))
        self.points.append(Point(np.array([0.5, -0.5, 0.5])))
        self.points.append(Point(np.array([-0.5, -0.5, -0.5])))
        self.points.append(Point(np.array([-0.5, 0.5, -0.5])))
        self.points.append(Point(np.array([-0.5, 0.5, 0.5])))
        self.points.append(Point(np.array([-0.5, -0.5, 0.5])))

        self.connections = [
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0),
            (4, 5),
            (5, 6),
            (6, 7),
            (7, 4),
            (0, 4),
            (1, 5),
            (2, 6),
            (3, 7)
        ]

        self.world_space_points = []

class Plane:
    """A simple plan object."""
    def __init__(self, pos, rotation, scale):
        self.pos = -pos
        self.rotation = -rotation
        self.scale = -scale

        self.points = []
        self.points.append(Point(np.array([-0.5, 0.0, -0.5])))   
        self.points.append(Point(np.array([0.5, 0.0, -0.5])))
        self.points.append(Point(np.array([-0.5, 0.0, 0.5])))
        self.points.append(Point(np.array([0.5, 0.0, 0.5])))

        self.connections = [
            (0, 1),
            (0, 2),
            (2, 3),
            (3, 1)
        ]

        self.world_space_points = []

class Sphere:
    """A WIP 'Sphere'."""
    def __init__(self, pos, rotation, scale):
        self.pos = pos
        self.rotation = rotation
        self.scale = scale

        self.points = []
        self.points.append(Point(np.array([0, 1, 0])))
        self.points.append(Point(np.array([math.cos(2*math.pi/3), 0, math.sin(2*math.pi/3)])))
        self.points.append(Point(np.array([math.cos(4*math.pi/3), 0, math.sin(4*math.pi/3)])))
        self.points.append(Point(np.array([math.cos(6*math.pi/3), 0, math.sin(6*math.pi/3)])))
        self.points.append(Point(np.array([0, -1, 0])))

        self.connections = [
            (0, 1),
            (0, 2),
            (0, 3),
            (1, 2),
            (1, 3),
            (3, 2),
            (4, 1),
            (4, 2),
            (4, 3)
        ]

        self.world_space_points = []

class Camera:
    """A camera class, used to calculate the view matrix for other objects."""
    def __init__(self, pos, rotation, ortho_zoom):
        self.pos = pos
        self.rotation = rotation
        self.ortho_zoom = ortho_zoom
        self.z_near = 0.1
        self.z_far = 100