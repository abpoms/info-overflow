import Pyro4
import pygame
from pygame.locals import (QUIT,
                           MOUSEMOTION,
                           MOUSEBUTTONUP,
                           MOUSEBUTTONDOWN)
import multiprocessing
import sys

SCALE = 8
WIDTH = 3840 / SCALE
HEIGHT = 2160 / SCALE


class ParallelCoordGraph():
    def __init__(self):
        pass

    def draw(self):
        pass


class ParallelCoordPanel():
    def __init__(self):
        self.windowSurface = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Parallel Coordinates Panel')
        self._clock = pygame.time.Clock()

    def add_tags(self, tags):
        pass

    def _event_check(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                pass
            elif event.type == MOUSEBUTTONDOWN:
                pass

    def _run(self):
        self.windowSurface.fill((50, 50, 50))
        self._event_check()
        pygame.draw.line(self.windowSurface,
                         pygame.Color(100, 50, 50),
                         (0, 0),
                         (100, 100))
        pygame.display.update()
        self._clock.tick(30)

    def update(self):
        self._run()
        # thread = threading.Thread(target=self._run)
        # thread.setDaemon(True)
        # thread.start()


def launch_parallel_coords():
    pygame.init()
    parallel = ParallelCoordPanel()
    daemon = Pyro4.Daemon()
    parallel_uri = daemon.register(parallel)
    ns = Pyro4.locateNS()
    ns.register("info-overflow.parallel_coords", parallel_uri)
    thread = .Thread(target=daemon.requestLoop)
    thread.setDaemon(True)
    thread.start()
    while True:
        parallel.update()
    