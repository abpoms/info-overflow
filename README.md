InfoOverflow
============

##Run:
open 4 tabs in the env
cd /Users/bryanmaass/Dropbox/\!Winter13/163/info-overflow;source .env/bin/activate

-----
1:
python -Wignore -m Pyro4.naming
----
2:
python graph_plot
-----
3:
python info-overflow
-----
4:
python qa_plotter
-----
click on: qa_plotter
-----
3:
close info-overflow
-----
4:
open info

An interactive visualization of StackOverflow.

## Dependencies

 - hdf5-1.8.10
 
To install on mac using brew, run

    brew install hdf5

 - pygame
 
    brew install hg
    brew tap homebrew/headonly
    brew install --HEAD smpeg

    brew tap homebrew/science
    
    sudo pip install nose
    brew install gfortran

    brew install sdl sdl_image sdl_mixer sdl_ttf smpeg portmidi
    sudo pip install hg+https://bitbucket.org/pygame/pygame

## Building
Run

    virtualenv --no-site-packages --distribute .env && source .env/bin/activate && pip install -r requirements.txt
    
to install a virtualenv, activate it, and install the package requirements required to build.

## Installing New Packages
If you need to add more packages to the project, install them using pip in the virtualenv and then run

    pip freeze > requirements.txt

This will make sure that dependencies are preserved in the repo.

