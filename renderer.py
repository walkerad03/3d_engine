import pygame
import transform

WIDTH = 500
HEIGHT = 500
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Renderer:
    def __init__(self):
        """Constructor for Renderer class"""
        pygame.init()
        pygame.font.init()

        self.WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.fps = pygame.font.SysFont("freesanbold.tff", 20)

        self.objects: list = []

    def add_object(self, object):
        """Adds a 3d object to the set of rendered objects."""
        self.objects.append(object)

    def render_frame(self, camera):
        """Renders all objects to a frame."""
        self.WINDOW.fill(BLACK)

        for obj in self.objects:
            obj.world_space_points = []
            for each in obj.points:
                obj.world_space_points.append(transform.objectToProjection(each, obj.pos, obj.rotation, obj.scale, camera))

        for obj in self.objects:
            for connection in obj.connections:
                pygame.draw.line(
                    self.WINDOW,
                    WHITE,
                    transform.rescale(obj.world_space_points[connection[0]], WIDTH, HEIGHT),
                    transform.rescale(obj.world_space_points[connection[1]], WIDTH, HEIGHT))

        fps_text = self.fps.render(f'FPS: {round(self.clock.get_fps(), 2)}', True, (255, 255, 255))

        self.WINDOW.blit(fps_text, (5, 5))
        pygame.display.update()
        self.clock.tick(FPS)