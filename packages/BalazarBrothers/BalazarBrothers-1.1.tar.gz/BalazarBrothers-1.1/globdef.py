# Balazar Brothers
# Copyright (C) 2006-2007 Jean-Baptiste LAMY
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

import os, os.path, gettext

import soya, soya.tofu as tofu
APPDIR = os.path.dirname(__file__)

soya.path.insert(0, APPDIR)


soya.AUTO_EXPORTERS_ENABLED = 0 #os.path.exists(os.path.join(APPDIR, ".svn"))


translator = None
LOCALEDIR = os.path.join(APPDIR, "locale")
try: translator = gettext.translation("balazar_brothers", LOCALEDIR)
except IOError:
  
  LOCALEDIR = os.path.join(APPDIR, "..", "locale")
  try: translator = gettext.translation("balazar_brothers", LOCALEDIR)
  except IOError:
    
    LOCALEDIR = os.path.join("/", "usr", "share", "locale")
    try: translator = gettext.translation("balazar_brothers", LOCALEDIR)
    except IOError:
      
      # Non-supported language, defaults to english
      LOCALEDIR = os.path.join(APPDIR, "locale")
      try: translator = gettext.translation("balazar_brothers", LOCALEDIR, ("en",))
      except IOError:
        
        LOCALEDIR = os.path.join(APPDIR, "..", "locale")
        try: translator = gettext.translation("balazar_brothers", LOCALEDIR, ("en",))
        except IOError:
          
          LOCALEDIR = os.path.join("/", "usr", "share", "locale")
          translator = gettext.translation("balazar_brothers", LOCALEDIR, ("en",))
      
translator.install(1)
#open(os.path.join(LOCALEDIR, "fr", "LC_MESSAGES", "balazar_brothers.po")).read()


VERIFICATION_SERVER = ""

DIFFICULTY = 0

FULLSCREEN    = 0
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600
MIN_FRAME_DURATION = 0.025

QUALITY    = 1

SERVER_HOST = "localhost"
SERVER_PORT = 6901

START_LEVEL = "tutorial"

SOUND = 1
SOUND_VOLUME = 1.0
WAIT_FOR_SOUND = 1

FPS_LABEL = 1

# Check for "dot balazar" config file
CONFIG_FILE = os.path.expanduser(os.path.join("~", ".balazar_brothers/config"))
if CONFIG_FILE[0] == "~": # Fucking winedaube OS !!!
  CONFIG_FILE = "C:\\.balazar_brothers/config" # Random name...
  


try:
  import getpass
  LOGIN = getpass.getuser()
except:
  LOGIN = "your_name"

tofu.HOST           = ""
tofu.PORT           = 6919
tofu.SAVED_GAME_DIR = os.path.expanduser(os.path.join("~", ".balazar_brothers"))
if tofu.SAVED_GAME_DIR[0] == "~": # Fucking winedaube OS !!!
  tofu.SAVED_GAME_DIR = "C:\\balazar_brothers" # Random name...

if os.path.exists(CONFIG_FILE):
  try:
    execfile(CONFIG_FILE)
  except:
    import sys
    sys.excepthook(*sys.exc_info())
    print """* BalazarBrothers * Error in config file %s !
Please reconfigure Balazar !
Config file ignored.
""" % CONFIG_FILE


SAVE_REPLAY = 0


def generate_config_file():
  f = open(CONFIG_FILE, "w")
  f.write("""
FULLSCREEN        = %(FULLSCREEN)s
SCREEN_WIDTH      = %(SCREEN_WIDTH)s
SCREEN_HEIGHT     = %(SCREEN_HEIGHT)s
QUALITY           = %(QUALITY)s

DIFFICULTY        = %(DIFFICULTY)s

SOUND_VOLUME      = %(SOUND_VOLUME)s
WAIT_FOR_SOUND    = %(WAIT_FOR_SOUND)s

LOGIN             = '%(LOGIN)s'
""" % globals())
  f.write("""
tofu.HOST           = '%s'
tofu.PORT           = %s
tofu.SAVED_GAME_DIR = '%s'
""" % (tofu.HOST, tofu.PORT, tofu.SAVED_GAME_DIR))
  

VERSION = "1.0"




