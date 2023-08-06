# PYSILICO: Prosilica AVT camera controller for Plico

| [![Build Status][travis]][travislink] | [![Coverage Status][coveralls]][coverallslink] | 

pysilico is an application to control [Allied AVT/Prosilica][allied] cameras (and possibly other GigE cameras) under the [plico][plico] environment.



[plico]: https://github.com/lbusoni/plico
[allied]: https://www.alliedvision.com
[travis]: https://travis-ci.com/lbusoni/pysilico.svg?branch=master "go to travis"
[travislink]: https://travis-ci.com/lbusoni/pysilico
[coveralls]: https://coveralls.io/repos/github/lbusoni/pysilico/badge.svg?branch=master "go to coveralls"
[coverallslink]: https://coveralls.io/github/lbusoni/pysilico


## Installation

On the client 

```
pip install pysilico
```


On the server 

First install Vimba (that comes with the camera, or download Vimba SDK from 
```
pip install pysilico-server
```

The pysilico-server package installs also the client package.




## Usage

### Starting Servers

Starts the 2 servers that control one device each.

```
pysilico_start
```

### Using the GUI

Run `pysilico_gui`
  

### Using the client module 

In a python terminal on the client computer:

```
In [1]: import pysilico

In [2]: cam1= pysilico.camera('192.168.1.18', 7100)

In [3]: cam2= pysilico.camera('192.168.1.18', 7110)

In [4]: frames= cam1.getFutureFrames(10)
```

### Stopping pysilico

To kill the servers run

```
pysilico_stop
```

More hard:

```
pysilico_kill_all
```




## Administration Tool

For developers.


### Testing
Never commit before tests are OK!
To run the unittest and integration test suite cd in pysilico source dir

```
python setup.py test
```


### Creating a Conda environment
Use the Anaconda GUI or in terminal

```
conda create --name pysilico
```

To create an environment with a specific python version

```
conda create --name pysilico python=2.6
```


It is better to install available packages from conda instead of pip. 

```
conda install --name pysilico matplotlib scipy ipython numpy
```

### Packaging and distributing

See https://packaging.python.org/tutorials/distributing-packages/#

To make a source distribution

```
python setup.py sdist
```

and the tar.gz is created in ../dist


You can make a universal wheel 

```
python setup.py bdist_wheel 
```

The wheels are created in ../dist. I suppose one can delete 
pysilico/build now and distribute the files in ../dist


To upload on pip (but do you really want to make it public?)

```
twine upload ../dist/*
```