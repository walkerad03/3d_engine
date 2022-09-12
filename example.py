"""An example file showing how to use the Renderer class."""

from objects import Box, Camera, Plane
import numpy as np
import renderer

def deg2rad(val):
    return val / 180.0 * np.pi

camera_translation = np.array([0.0, 0.0, 0.0], dtype="float64")
camera_rotation = np.array([0.0, 0.0, 0.0], dtype="float64")
camera = Camera(camera_translation, camera_rotation, 5)

box_translation = np.array([0.0, 0.0, 0.0])
box_rotation = deg2rad(np.array([15.0, 0.0, 0.0]))
box_scale = np.array([1.0, 1.0, 1.0])
box = Box(box_translation, box_rotation, box_scale)

plane_translation = np.array([0.0, -0.5, 0.0])
plane_rotation = deg2rad(np.array([15.0, 0.0, 0.0]))
plane_scale = np.array([3.0, 1.0, 3.0])
plane = Plane(plane_translation, plane_rotation, plane_scale)

r = renderer.Renderer()

r.add_object(box)
r.add_object(plane)

while True:
    try:
        r.render_frame(camera)

        camera.rotation[1] += 0.01

    except KeyboardInterrupt:
        break