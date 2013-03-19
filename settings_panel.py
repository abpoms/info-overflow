import Pyro4
import pygame

SCALE = 4
WIDTH = 3840 / SCALE
HEIGHT = 2160 / SCALE

class SettingsPanel():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display_set_mode((WIDTH, HEIGHT))
        

    def run(self):
        for event in pygame.event.get()
        pass


def launch_settings():
    settings = SettingsPanel()
    server = Pyro4.Proxy("PYRONAME:info-overflow.server")


def _launch_daemon(q):
    daemon = Pyro4.Daemon()
    graph_endpoint = GraphPlotEndpoint(q)
    graph_plot_uri = daemon.register(graph_endpoint)
    ns = Pyro4.locateNS()
    ns.register("info-overflow.graph_plot", graph_plot_uri)
    daemon.requestLoop()


class SettingsEndpoint():
    def __init__(self, q):
        self.q = q

    def 