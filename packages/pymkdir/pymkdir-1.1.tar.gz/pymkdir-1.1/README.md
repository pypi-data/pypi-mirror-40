# pymkdir

A command line utility to create python folders (folders with ```__init__.py```) to quickly create Python packages
without the burden of manually creating new folders and then an ```__init__.py``` file in it.

## Python Packages

Python treats folders with an ```__init__.py``` as packages which can be used to hold python code. Also,
in the init file may contain initialization code for the package.

However... after some time coding in Python, one realizes that creating folders and then creating
 a file name ```__init__.py``` becomes a burden!

But... worry no more! By using pymkdir, the old unix OS function ```mkdir``` will be improved to ALSO
create automagically the ```__init__.py``` file! Yes, no more worries!

## Usage

To create a local pyfolder, use the -f/--folder to create a pyfolder with the desired name:

```bash
pymkdir -f <folder_name>
```

To create a pyfolder at a given directory, use the -p/--path flag (defaults to ```./```):

```bash
pymkdir -f <folder_name> -p <path_name>
```

And... just in case one becomes SO addicted to pymkdir (which is normal) and wants to start using it to create
even normal folders (without the ```__init__.py```), just use the -e/--empty flag!

```bash
pymkdir -f <folder_name> -p <path_name> -e
```

Then, just enjoy the nice output (hopefully one has an UTF-8 based terminal):

```bash
_ . * . 📂  Pymkdir 📂 . * . _
Creating the folder name...
Creating the __init__.py file...
Done!
```