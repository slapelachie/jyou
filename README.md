# JYOU
Simple lockscreen manager for tiling window managers.
Generates a lockscreen for multiscreened i3lock.

## How to use
If you ever get stuck on the syntax of this command, execute: `jyou -h` for the list of avaliable arguments.

### Arguments
The arguments are the following:

| Argument  | Usage |
|-----------|-----------------------------------------------------|
| -h, --help| Shows the help message for the wallpaper subcommand |
| -g        | Switch for generating the lockscreen |
| -i        | The input file |
| -v        | Allows verbose logging |
| -q        | Allows for just error logging |
| -b        | The radius to blur |
| -d        | The darkness (darker < 1.0 < lighter) |
| --clear   | Clears the cache |

## Installation

### Dependencies

#### Python
 - [tqdm](https://pypi.org/project/tqdm/)
 - [Pillow](https://pypi.org/project/Pillow/)

#### Additional Programs
 - [xrandr](https://www.archlinux.org/packages/extra/x86_64/xorg-xrandr/)

#### System Wide Install
To install system wide, run `$ pip install jyou` or if from source `$ pip install .`

#### User Install
To install for just the user, un `$pip install --user jyou` or if from source `$ pip install --user .`

This method assumes that `~/.local/bin/` is set in the `$PATH` environmental variable.

## Postscripts
Post scripts are executables that are run after one of the sub commands are completed.
To create a postscript, do the following:
1. Create a file with the following naming convention: `##-name`.

	 - Where `##` is a number from 00-99 (The files are loaded in numerical order)
 	 - Where `name` is the name of it

2. Add this file under `~/.local/share/jyou/postscripts`
3. Make it executable (`chmod +x filename`)

For examples of postscripts look under `examples/postscripts`
