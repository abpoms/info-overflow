InfoOverflow
============

Stack Overflow DataVis


Building
============
Run

    virtualenv --no-site-packages --distribute .env && source .env/bin/activate && pip install -r requirements.txt
    
to install a virtualenv, activate it, and install the package requirements required to build.g

Installing New Packages
===========
If you need to add more packages to the project, install them using pip in the virtualenv and then run

    pip freeze > requirements.txt

This will make sure that dependencies are preserved in the repo.

