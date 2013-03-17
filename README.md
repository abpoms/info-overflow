InfoOverflow
============

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
    
    pip install nose
    brew install gfortran

    brew install sdl sdl_image sdl_mixer sdl_ttf smpeg portmidi
    pip install hg+http://bitbucket.com/pygame/pygame

## Building
Run

    virtualenv --no-site-packages --distribute .env && source .env/bin/activate && pip install -r requirements.txt
    
to install a virtualenv, activate it, and install the package requirements required to build.

## Installing New Packages
If you need to add more packages to the project, install them using pip in the virtualenv and then run

    pip freeze > requirements.txt

This will make sure that dependencies are preserved in the repo.

