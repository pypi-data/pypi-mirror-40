Installation Instructions for macapi
====================================

### Python

Currently macapi only supports Python 2.7.x. Other versions of Python are not supported.

You can verify your version of Python from the command line by typing:
`python --version`

### Git

You also need Git installed. You can veiriy that git is installed by typing:

`git --version`

If git is not installed then you can follow this [documentation](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git). For windows you can just run this [installer](http://git-scm.com/download/win).

### macapi Installation


To install macapi you need a copy of the source code on your local machine. You can do this by cloning the [macapi repository](https://bitbucket.org/dmcna005/macap):

      git clone git@bitbucket.org:dmcna005/macapi.git

 Once you have a copy of the repo on your local machine, you can `cd` into the macapi directory and type the following:
    `sudo python setup.py install`
    
The installer should now run and install macapi into your Python's site-packages folder and create all the necessary symlinks to setup the tool in your path so you can use from the command line as you would any other tools.



#### More Installation Options to come




