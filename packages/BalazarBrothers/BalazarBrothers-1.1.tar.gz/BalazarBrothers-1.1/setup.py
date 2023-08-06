#! /usr/bin/env python

# BalazarBrothers
# Copyright (C) 2003-2007 Jean-Baptiste LAMY -- jiba@tuxfamily
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

HERE        = os.path.abspath(os.path.dirname(sys.argv[0]))
HERE_PARENT = os.path.abspath(os.path.join(HERE, os.pardir))

if "--no-lang" in sys.argv:
  sys.argv.remove("--no-lang")
  no_lang = 1
else: no_lang = 0

data_files = []
def walker(dummy, dir, files):
  #print dummy, dir, files
  if "CVS" in dir: return
  dir2 = dir[len(HERE):]
  if dir2[0] == "/": dir2 = dir2[1:]
  dir2 = os.path.join("balazar_brothers", dir2)
  files = map(lambda file: os.path.join(dir, file), files)
  files = filter(lambda file: os.path.isfile(file) and (not "CVS" in file), files)
  data_files.append((dir2, files))
  #data_files.append((dir2, map(lambda file: os.path.join(dir, file), files)))
  
for path in ["images", "materials", "animated_models", "models", "worlds", "sounds", "fonts", "levels"]:
  path = os.path.abspath(os.path.join(HERE, path))
  os.path.walk(path, walker, None)
  

# data_files = [
#   (os.path.join("balazar", "images"   ), glob.glob(os.path.join(".", "images"   , "*"))),
#   (os.path.join("balazar", "materials"), glob.glob(os.path.join(".", "materials", "*"))),
#   (os.path.join("balazar", "models"   ), glob.glob(os.path.join(".", "models"   , "*"))),
#   (os.path.join("balazar", "worlds"   ), glob.glob(os.path.join(".", "worlds"   , "*"))),
#   (os.path.join("balazar", "sounds"   ), glob.glob(os.path.join(".", "sounds"   , "*"))),
#   ]
if not no_lang:
  data_files = data_files + [
    (os.path.join("balazar_brothers", os.path.dirname(mo_file)), [mo_file])
    for mo_file
    in  glob.glob(os.path.join(".", "locale", "*", "LC_MESSAGES", "*"))
    if not "CVS" in mo_file
    ]

#data_files = [file for file in data_files if not "CVS" in file]

#print data_files

distutils.core.setup(
  name         = "BalazarBrothers",
  version      = "1.1",
  license      = "GPL",
  description  = "A 3D action/puzzle game.",
  long_description  = """A 3D puzzle game featuring the Balazar Brothers.""",
  author       = "Jiba (LAMY Jean-Baptiste)",
  author_email = "jibalamy@free.fr",
  url          = "http://home.gna.org/oomadness/en/balazar_brother/index.html",
  classifiers  = [
  "Topic :: Games/Entertainment",
  "Topic :: Games/Entertainment :: Puzzle Games",
  "Topic :: Games/Entertainment :: Arcade",
  "Topic :: Multimedia :: Graphics :: 3D Rendering",
  "Natural Language :: French",
  "Natural Language :: English",
  "Programming Language :: Python",
  "Intended Audience :: End Users/Desktop",
  "License :: OSI Approved :: GNU General Public License (GPL)",
    "Programming Language :: Python :: 2.7",
  ],
  
  
  install_requires=[
    "Soya",
    "PyOpenAL",
  ],
  
  scripts      = ["balazar_brothers"],
  package_dir  = {"balazar_brothers" : ""},
  packages     = ["balazar_brothers"],
  package_data = {"balazar_brothers" : ["",
                                        "images/*.*",
                                        "materials/*.*",
                                        "animated_models/*/*.*",
                                        "models/*.*",
                                        "worlds/*.*",
                                        "sounds/*.*",
                                        "fonts/*.*",
                                        "levels/*.*",
                                        "locale/*/*/*.*",
  ]},
  
  #data_files   = data_files,
  )

