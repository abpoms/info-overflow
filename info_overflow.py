import Pyro4


def log(output):
    print "Server: " + output


class OverflowServer():
    def __init__(self):
        self.current_time = 0
        self.tags = set()

    def get_time(self):
        log("get_time")
        return self.current_time

    def set_time(self, time):
        log("set_time - " + time)
        self.current_time = time

    def select_tag(self, tag):
        log("select_tag - " + tag)
        self.tags.add(tag)

    def deselect_tag(self, tag):
        log("deselect_tag - " + tag)
        self.tags.remove(tag)

    def run(self):
        pass


def launch_server():
    server = OverflowServer()
    daemon = Pyro4.Daemon()
    server_uri = daemon.register(server)
    ns = Pyro4.locateNS()
    ns.register("info-overflow.server", server_uri)
    server.run()
    print "Server running"
    daemon.requestLoop()


if __name__ == "__main__":
    import sys
    import preprocess as pre
    # Perform preproccessing on supplied directory
    if (len(sys.argv) > 1):
        if (sys.argv[1] == "-p"):
            pre.preprocess_to_hdf5(sys.argv[2])
    # Launch Viz server
    else:
        launch_server()
