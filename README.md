# JYOU
Simple lockscreen manager for tiling window managers.
Generates a lockscreen for multiscreened i3locks

## How to use
If you ever get stuck on the syntax of this command, execute: `jyou -h` for the list of avaliable arguments.

### Arguments
The arguments are the following:

| Argument  | Usage |
|-----------|-----------------------------------------------------|
| -h, --help| Shows the help message for the wallpaper subcommand |
| -g        | Switch for generating the lockscreen |
| -i        | The input file |
| --clear   | Clears the cache |

## Installation

### Dependencies

#### Python
 - [tqdm](https://pypi.org/project/tqdm/)

#### Additional Programs
 - [xrandr](https://www.archlinux.org/packages/extra/x86_64/xorg-xrandr/)
 - [ImageMagick](https://www.archlinux.org/packages/extra/x86_64/imagemagick/)

### Process
To install this, go to the project root (where this README is) and run the command `$ make && make install && make clean`

## Postscripts
Post scripts are executables that are run after one of the sub commands are completed.
To create a postscript, do the following:
1. Create a file with the following naming convention: `##-name`.

	 - Where `##` is a number from 00-99 (The files are loaded in numerical order)
 	 - Where `name` is the name of it

2. Add this file under ~/.local/share/jyou/postscripts
3. Make it executable (under linux `chmod +x filename` works)

For examples of postscripts look under `examples/postscripts`
