"""An assortment of utilities to aid this project"""
import hashlib
import os
import re
import subprocess

from typing import List

from .settings import CONFIG_PATH


def md5(string: str) -> str:
    """
    Generates a md5 hash based on the parsed string

    Arguments:
        string (str): a string to be encoded

    Returns:
        (str): md5 encoding of the given string
    """
    hash_md5 = hashlib.md5(str(string).encode())
    return hash_md5.hexdigest()


def md5_file(file_path: str) -> str:
    """
    Generates a md5 hash based on the file parsed

    Arguments:
        file_path (str): location of the file ('/home/bob/pic.png')

    Returns:
        (str): md5 encoding of the given file
    """
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def get_absolute_image_path(image_path: str) -> str:
    """
    Get the absolute path of a parsed file (image)

    Arguments:
        image_path (str): location of the file

    Returns:
        (str): the absolute path of the parsed file
    """
    if os.path.isfile(image_path):
        return os.path.abspath(image_path)

    return None


def get_directory_image_paths(image_directory: str) -> List[str]:
    """
    Get a list of all image paths in a directory

    Arguments:
        img_dir (str): the directory where the images are stored

    Returns:
        (List[str]): list of all file paths in a directory
    """
    file_types = ("png", "jpg", "jpeg")
    return [
        img.name
        for img in os.scandir(image_directory)
        if img.name.lower().endswith(file_types)
    ]


def run_hooks():
    """Run all scripts within the hooks folder"""
    hooks_dir = os.path.join(CONFIG_PATH, "hooks")
    os.makedirs(hooks_dir, exist_ok=True)

    scripts = [
        f
        for f in os.listdir(hooks_dir)
        if re.match(r"^([0-9]{2}-\w+)", f)
        and os.access(os.path.join(hooks_dir, f), os.X_OK)
    ]
    scripts.sort()

    for script in scripts:
        script = os.path.join(hooks_dir, script)

        with open(os.devnull, "w", encoding="UTF-8") as devnull:
            subprocess.run(script, stdout=devnull, stderr=subprocess.STDOUT, check=True)
