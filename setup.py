from setuptools import setup

LONG_DESC = open('README.md').read()

setup(name='JYOU',
	version='1.0a2',
	description='Simple lockscreen manager for tiling window managers. Generates a lockscreen for multiscreened i3locks',
	long_description_content_type="text/markdown",
	long_description=LONG_DESC,
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Environment :: X11 Applications',
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Natural Language :: English',
		'Operating System :: POSIX :: Linux',
		'Programming Language :: Python :: 3.8',
	],
	url='http://github.com/slapelachie/jyou',
	author='slapelachie',
	author_email='slapelachie@gmail.com',
	license='GPLv3',
	packages=['jyou'],
	entry_points={"console_scripts": ["jyou=jyou.__main__:main"]},
	install_requires = [
		'Pillow',
		'tqdm',
	],
	zip_safe=False)
