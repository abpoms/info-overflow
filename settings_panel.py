import Pyro4


class SettingsPanel():
    def __init__(self):
        pass
    def run(self):
        

def launch_settings():
    settings = SettingsPanel()
    daemon = Pyro4.Daemon()
    settings_uri = daemon.register(settings)
    ns = Pyro4.locateNS()
    ns.register("info-overflow.settings", settings_uri)
    server = Pyro4.Proxy("PYRONAME:info-overflow.server")
    daemon.requestLoop()
    