#!/usr/bin/env python3

from setuptools import setup, find_packages

with open('README.md') as f:
	readme = f.read()


setup(
	name = "WallPoppy",
	version = "0.1.0",
	description = "Simple wallpaper daemon using feh",
	long_description = readme,
	author = "Oliver Hattshire",
	author_email = "Ohattsh@hashbang.sh",
	url = "https://github.com/hattshire/wallpoppy",
	keywords = "dbus wallpaper daemon pictures desktop",
	license = "Unlicense",

	packages = find_packages(),
	package_data = {
		'': ["*.rst"]
	},
	install_requires = [
		"pydbus", "pygobject"
	],
	entry_points = {
		'console_scripts': [
			'wallpoppyd=Wallpoppy:run',
		],
	},
	zip_safe = True,
	classifiers = [
		'Development Status :: 2 - Pre-Alpha',
		'Intended Audience :: End Users/Desktop',
		'Intended Audience :: System Administrators',
		'Environment :: No Input/Output (Daemon)',
		'Natural Language :: English',
		'Operating System :: POSIX',
		'License :: Public Domain',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Topic :: Desktop Environment',
		'Topic :: Utilities',
	],
)
