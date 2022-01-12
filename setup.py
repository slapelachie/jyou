from setuptools import setup
from jyou.__init__ import __author__, __email__, __version__

LONG_DESC = open("README.md").read()

setup(
    name="JYOU",
    version=__version__,
    description="Simple lockscreen manager for tiling window managers. Generates a lockscreen for multiscreened i3locks",
    long_description_content_type="text/markdown",
    long_description=LONG_DESC,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: X11 Applications",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.10",
    ],
    url="http://github.com/slapelachie/jyou",
    author=__author__,
    author_email=__email__,
    license="GPLv3",
    packages=["jyou"],
    entry_points={"console_scripts": ["jyou=jyou.__main__:main"]},
    install_requires=[
        "Pillow",
        "tqdm",
    ],
    zip_safe=False,
)
