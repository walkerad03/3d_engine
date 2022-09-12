from objects import Point
import math
import numpy as np

def _objectToWorld(point, translation, rotation, scale):
    """Converts a given point from object to world space, and applies translation, rotation, and scale."""
    transformation_matrix = np.array([
        [1, 0, 0, translation[0]],
        [0, 1, 0, translation[1]],
        [0, 0, 1, translation[2]],
        [0, 0, 0, 1]
    ], dtype="float64")

    x_rotation_matrix = np.array([
        [1, 0, 0, 0],
        [0, math.cos(rotation[0]), -math.sin(rotation[0]), 0],
        [0, math.sin(rotation[0]), math.cos(rotation[0]), 0],
        [0, 0, 0, 1]
    ], dtype="float64")

    y_rotation_matrix = np.array([
        [math.cos(rotation[1]), 0, math.sin(rotation[1]), 0],
        [0, 1, 0, 0],
        [-math.sin(rotation[1]), 0, math.cos(rotation[1]), 0],
        [0, 0, 0, 1]
    ], dtype="float64")

    z_rotation_matrix = np.array([
        [math.cos(rotation[2]), -math.sin(rotation[2]), 0, 0],
        [math.sin(rotation[2]), math.cos(rotation[2]), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ], dtype="float64")

    scale_matrix = np.array([
        [scale[0], 0, 0, 0],
        [0, scale[1], 0, 0],
        [0, 0, scale[2], 0],
        [0, 0, 0, 1]
    ], dtype="float64")

    vertex_vector = np.array([
        [point.pos[0]],
        [point.pos[1]],
        [point.pos[2]],
        [1],
    ], dtype="float64")

    translation_matrix = np.matmul(np.matmul(np.matmul(np.matmul(transformation_matrix, x_rotation_matrix), y_rotation_matrix), z_rotation_matrix), scale_matrix)
    world_vertex = np.matmul(translation_matrix, vertex_vector)
    return Point(np.array([world_vertex[0], world_vertex[1], world_vertex[2]], dtype="float64"))

def _worldToView(point, camera):
    """Uses camera position and rotation to convert world space to view space for ease of calculations."""
    view_transformation_matrix = np.array([
        [1, 0, 0, camera.pos[0]],
        [0, 1, 0, camera.pos[1]],
        [0, 0, 1, camera.pos[2]],
        [0, 0, 0, 1]
    ], dtype="float64")

    view_x_rotation_matrix = np.array([
        [1, 0, 0, 0],
        [0, math.cos(camera.rotation[0]), -math.sin(camera.rotation[0]), 0],
        [0, math.sin(camera.rotation[0]), math.cos(camera.rotation[0]), 0],
        [0, 0, 0, 1]
    ], dtype="float64")

    view_y_rotation_matrix = np.array([
        [math.cos(camera.rotation[1]), 0, math.sin(camera.rotation[1]), 0],
        [0, 1, 0, 0],
        [-math.sin(camera.rotation[1]), 0, math.cos(camera.rotation[1]), 0],
        [0, 0, 0, 1]
    ], dtype="float64")

    view_z_rotation_matrix = np.array([
        [math.cos(camera.rotation[2]), -math.sin(camera.rotation[2]), 0, 0],
        [math.sin(camera.rotation[2]), math.cos(camera.rotation[2]), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ], dtype="float64")

    vertex_vector = np.array([
        [point.pos[0]],
        [point.pos[1]],
        [point.pos[2]],
        [1],
    ], dtype="float64")

    view_matrix = np.linalg.inv(np.matmul(np.matmul(np.matmul(view_transformation_matrix, view_x_rotation_matrix), view_y_rotation_matrix), view_z_rotation_matrix))
    view_vertex = np.matmul(view_matrix, vertex_vector)
    return Point(np.array([view_vertex[0], view_vertex[1], view_vertex[2]], dtype="float64"))

def _viewToProjection(point, camera): 
    """Converts point from view space to 2d projection space."""
    
    projection_matrix = np.array([
        [1 / camera.ortho_zoom, 0, 0, 0],
        [0, 1 / camera.ortho_zoom, 0, 0],
        [0, 0, -2 * (1 / camera.z_far - camera.z_near), -1 * (camera.z_far + camera.z_near) / (camera.z_far - camera.z_near)],
        [0, 0, 0, 1]
    ], dtype="float64")
    
    vertex_vector = np.array([
        [point.pos[0]],
        [point.pos[1]],
        [point.pos[2]],
        [1],
    ], dtype="float64")

    projection_vertex = np.matmul(projection_matrix, vertex_vector)
    return Point(np.array([projection_vertex[0], projection_vertex[1], projection_vertex[2]], dtype="float64"))

def objectToProjection(point, translation, rotation, scale, camera):
    """Condensed function which automatically converts from object space to projection space."""
    return _viewToProjection(_worldToView(_objectToWorld(point, translation, rotation, scale), camera), camera)

def rescale(point, window_w, window_h):
    """Simple function which normalizes vector data to be between the window bounds."""
    remapped_x = (point.pos[0] + 1) / 2
    remapped_y = (point.pos[1] + 1) / 2

    return (int(remapped_x * window_w), int(remapped_y * window_h))