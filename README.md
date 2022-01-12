# JYOU
![Run Tests](https://github.com/slapelachie/jyou/workflows/Run%20Tests/badge.svg)

[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/L3L726D8I)

Simple lockscreen manager for tiling window managers.
Generates a lockscreen for multi-screened i3lock.

## How to use
If you ever get stuck on the syntax of this command, execute: `jyou -h` for the list of available arguments.

### Arguments
The arguments are the following:

|Argument  |Usage|
|----------|---------------------------------------------------|
|-h, --help|Shows the help message for the wallpaper subcommand|
|-v        |Allows verbose logging|
|-g        |Switch for generating the lockscreen|
|-i        |The input file|
|-b        |The radius to blur|
|-d        |The darkness (darker < 1.0 < lighter)|
|--override|Override existing lockscreen file|
|--clear   |Clears the cache|
|--progress|Displays the progress|

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
To install for just the user, run `$ pip install --user jyou` or if from source `$ pip install --user .`

This method assumes that `~/.local/bin/` is set in the `$PATH` environmental variable.

## Hooks
Hooks are executables that run after one of the sub commands are completed.
To create a hook, do the following:
1. Create a file with the following naming convention: `##-name`.
	 - Where `##` is a number from 00-99 (The files are loaded in numerical order)
 	 - Where `name` is the name of it

2. Add this file under `~/.local/share/jyou/hooks`
3. Make it executable (`chmod +x filename`)

For examples of postscripts look under `examples/hooks`
