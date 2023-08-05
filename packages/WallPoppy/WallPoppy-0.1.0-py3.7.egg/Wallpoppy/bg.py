#!/usr/bin/env python3
## Public Domain


import os
import pydbus
import random
import argparse
from gi.repository import GLib

parser = argparse.ArgumentParser(description="Set X11 root window BG using a file or folder and feh.")
parser.add_argument('src', metavar='path',
		    help="Source file or folder.")
parser.add_argument('-r', '--random', action='store_true',
		    help="Randomize image order.")
parser.add_argument('-t', '--time', metavar='SECONDS', type=int, default=3600,
		    help="Time between changes.")
parser.add_argument('-s','--style', choices=['center', 'fill', 'max', 'scale', 'tile'], default='fill',
		    help="In which style fill the background.\n" +
		         "Preserved ratio:\n" +
		         "* center: Keep the image in the center using the image resolution.\n" +
		         "* fill  : Zoom the image until no corner is left untouched.\n" +
		         "* max   : Zoom the image until it touches a corner.\n" +
		         "* tile  : Repeat the image over the background.\n"+
		         "By ratio:\n" +
		         "* scale : Stretch and/or shrink the image until it fits.")

class controlBus(object):
	"""
		<node>
			<interface name='moe.hattshire.bg.control'>
				<signal name='BackgroundChanged'>
					<arg type='s' name='file' direction='out' />
				</signal>

				<method name='next'>
					<arg type='b' name='response' direction='out' />
				</method>
				<method name='previous'>
					<arg type='b' name='response' direction='out' />
				</method>

				<method name='addFile'>
					<arg type='s' name='file' direction='in' />
					<arg type='b' name='response' direction='out' />
				</method>
				<method name='addFileNext'>
					<arg type='s' name='file' direction='in' />
					<arg type='b' name='response' direction='out' />
				</method>

				<method name='removeFile'>
					<arg type='s' name='file' direction='in' />
					<arg type='b' name='response' direction='out' />
				</method>

				<property name='currentBackgroundFile' type='s' access='read'>
					<annotation name='org.freedesktop.DBus.Property.EmitsChangedSignal' value='true' />
				</property>
				<property name='previousBackgroundFile' type='s' access='read'>
					<annotation name='org.freedesktop.DBus.Property.EmitsChangedSignal' value='true' />
				</property>
				<property name='nextBackgroundFile' type='s' access='read'>
					<annotation name='org.freedesktop.DBus.Property.EmitsChangedSignal' value='true' />
				</property>

				<property name='fileList' type='s' access='read'>
					<annotation name='org.freedesktop.DBus.Property.EmitsChangedSignal' value='true' />
				</property>

				<property name='imageAvailable' type='b' access='read'>
					<annotation name='org.freedesktop.DBus.Property.EmitsChangedSignal' value='true' />
				</property>

				<property name='random' type='b' access='readwrite'>
					<annotation name='org.freedesktop.DBus.Property.EmitsChangedSignal' value='true' />
				</property>

				<property name='delay' type='i' access='readwrite'>
					<annotation name='org.freedesktop.DBus.Property.EmitsChangedSignal' value='true' />
				</property>
			</interface>
		</node>
	"""
	PropertiesChanged = pydbus.generic.signal()
	BackgroundChanged = pydbus.generic.signal()

	ext_list = ['gif', 'png', 'tiff', 'jpeg', 'jpg']

	def __init__(self):
		args = parser.parse_args()

		self.__random     = args.random
		source_name       = os.path.expanduser(args.src)
		self.__image_list = []
		self.__delay      = args.time
		self.__style      = "--bg-%s" % args.style

		self.addFile(source_name)
		self.next()
		self.__timeout_handle = GLib.timeout_add(self.__delay*1000, self.next)

	# Methods

	def next(self):
		if self.imageAvailable:
			image = self.__getImage(position=0)
			self.__setBackground(image)

			if self.random and len(self.__image_list) > 1:
				self.__randomNext()
			return True
		return False

	def previous(self):
		self.__swap(-1, 0)
		self.__setBackground(self.__image_list[-1])
		return True

	def addFile(self, file):
		if os.path.isdir(file):
			file_list = os.listdir(file)
			for folder_file in file_list:
				file_ext = folder_file.split(os.extsep)[-1]
				if file_ext not in self.ext_list:
					continue
				self.__image_list.append(os.path.join(file, folder_file))
		elif os.path.exists(file):
			self.__image_list.append(file)
		else:
			return False
		return True

	def addFileNext(self, file):
		if os.path.isdir(file):
			file_list = os.listdir(file)
			for folder_file in file_list:
				file_ext = folder_file.split(os.extsep)[-1]
				if file_ext not in self.ext_list:
					continue
				self.__image_list.insert(0, os.path.join(file, folder_file))
		elif os.path.exists(file):
			self.__image_list.append(0, file)
		else:
			return False
		return True

	def removeFile(self, file):
		if file in self.__image_list:
			self.__image_list.remove(file)
			return True
		return False

	# Properties

	@property
	def currentBackgroundFile(self):
		return self.__image_list[-1]

	@property
	def nextBackgroundFile(self):
		return self.__image_list[0]

	@property
	def previousBackgroundFile(self):
		return self.__image_list[-2]

	@property
	def imageAvailable(self, value=None):
		return len(self.__image_list) > 1

	@property
	def fileList(self):
		return str(self.__image_list)

	# TODO Setter for random and delay
	@property
	def random(self):
		return self.__random

	@property
	def delay(self):
		return self.__delay

	# Utils

	def __getImage(self, position):
		return self.__swap(position, -1)

	def __setBackground(self, image):
		# TODO send BackgroundChanged signal
		os.system("feh %s '%s'" % (self.__style, image))

	def __randomNext(self):
		pos = random.randint(0, len(self.__image_list) - 2)
		self.__swap(pos, 0)

	def __swap(self, fromPosition, toPosition):
		image = self.__image_list.pop(fromPosition)
		if toPosition < 0:
			if toPosition == -1:
				self.__image_list.append(image)
			else:
				self.__image_list.insert(toPosition+1, image)
		else:
			self.__image_list.insert(toPosition, image)
		return image
