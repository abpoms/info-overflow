def launch_server():
    pass

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
        pass
