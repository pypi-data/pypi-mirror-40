#! /usr/bin/env python

# Slune
# Copyright (C) 2006 Jean-Baptiste LAMY -- jiba@tuxfamily
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import os, os.path, sys, glob, distutils.core, distutils.sysconfig
from distutils.core import setup


if "--no-lang" in sys.argv:
  sys.argv.remove("--no-lang")
  no_lang = 1
else: no_lang = 0


data_files = [
  (os.path.join("slune", "images"   ), glob.glob(os.path.join(".", "images"   , "*"))),
  (os.path.join("slune", "materials"), glob.glob(os.path.join(".", "materials", "*"))),
  (os.path.join("slune", "shapes"   ), glob.glob(os.path.join(".", "shapes"   , "*"))),
  (os.path.join("slune", "worlds"   ), glob.glob(os.path.join(".", "worlds"   , "*"))),
  (os.path.join("slune", "sounds"   ), glob.glob(os.path.join(".", "sounds"   , "*"))),
  ]
if not no_lang:
  data_files = data_files + [
    (os.path.join("slune", os.path.dirname(mo_file)), [mo_file])
    for mo_file
    in  glob.glob(os.path.join(".", "locale", "*", "LC_MESSAGES", "*"))
    if not "CVS" in mo_file
    ]

distutils.core.setup(
  name         = "Slune",
  version      = "1.0.16",
  license      = "GPL",
  description  = "A 3D racing and car-crashing game in Python, with multiplayer mode.",
  long_description  = """A 3D racing and car-crashing game in Python.
In this game, Gnu and Tux must provide AIDS medicine for Africa.
Includes a multiplayer mode.""",
  author       = "Jiba (LAMY Jean-Baptiste), Blam (LAMY Bertrand)",
  author_email = "jiba@tuxfamily.org",
  url          = "http://slune.nekeme.net",
  classifiers  = [
  "Topic :: Games/Entertainment :: Arcade",
  "Topic :: Multimedia :: Graphics :: 3D Rendering",
  "Natural Language :: French",
  "Natural Language :: English",
  "Programming Language :: Python",
  "Intended Audience :: End Users/Desktop",
  "Development Status :: 5 - Production/Stable",
  "License :: OSI Approved :: GNU General Public License (GPL)",
  "Programming Language :: Python :: 2.7", 
  ],
  
  install_requires=[
    "Soya",
    "PyOpenAL",
    "Py2Play",
  ],
  
  scripts      = ["slune"],
  package_dir  = {"slune" : ""},
  packages     = ["slune"],
  package_data = {"slune" : ["",
                             "images/*.*",
                             "materials/*.*",
                             "shapes/*.*",
                             "worlds/*.*",
                             "sounds/*.*",
                             "locale/*/*/*.*",
  ]},
  
  #data_files = data_files,
  )


if "install" in sys.argv:
  # Post install stuff
  
  pass
