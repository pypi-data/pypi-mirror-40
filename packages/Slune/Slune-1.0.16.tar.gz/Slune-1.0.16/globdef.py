# Slune
# Copyright (C) 2002-2003 Jean-Baptiste LAMY
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

import soya
APPDIR = os.path.dirname(__file__)

soya.path.insert(0, APPDIR)

soya.AUTO_EXPORTERS_ENABLED = 0 #os.path.exists(os.path.join(APPDIR, "CVS"))

LOCALEDIR = os.path.join(APPDIR, "locale")
try: gettext.translation("slune", LOCALEDIR).install(1)
except IOError:
  
  LOCALEDIR = os.path.join(APPDIR, "..", "locale")
  try: gettext.translation("slune", LOCALEDIR).install(1)
  except IOError:
    
    LOCALEDIR = os.path.join("/", "usr", "share", "locale")
    try: gettext.translation("slune", LOCALEDIR).install(1)
    except IOError:
      
      # Non-supported language, defaults to english
      LOCALEDIR = os.path.join(APPDIR, "locale")
      try: gettext.translation("slune", LOCALEDIR, ("en",)).install(1)
      except IOError:
        
        LOCALEDIR = os.path.join(APPDIR, "..", "locale")
        try: gettext.translation("slune", LOCALEDIR, ("en",)).install(1)
        except IOError:
          
          LOCALEDIR = os.path.join("/", "usr", "share", "locale")
          gettext.translation("slune", LOCALEDIR, ("en",)).install(1)
      


VERIFICATION_SERVER = ""

DIFFICULTY = 0

CHARACTER = "Tux"

VEHICLE = 1

FULLSCREEN    = 0
SCREEN_WIDTH  = 1024
SCREEN_HEIGHT = 600

QUALITY    = 1
MAX_VISION = 1.0

PORT = 36079

PARRAIN_HOST = ""
PARRAIN_PORT = 36079

MUSIC = 1
SOUND = 1
SOUND_VOLUME = 1.0

SPEED             = 1.0
RACE_NB_LAPS      = 1
RACE_NB_OPPONENTS = 3

NEXT_MISSION = 1

# Check for "dot slune" config file
CONFIG_FILE = os.path.expanduser(os.path.join("~", ".slune"))
if CONFIG_FILE[0] == "~":
  # Fucking winedaube OS !!!
  CONFIG_FILE = "C:\\.slune" # Random name...
  
try:
  import getpass
  NAME = getpass.getuser().title()
except:
  NAME = "jiba"
  
if os.path.exists(CONFIG_FILE):
  try:
    execfile(CONFIG_FILE)
  except:
    import sys
    sys.excepthook(*sys.exc_info())
    print """* Slune * Error in config file ~/.slune !
Please reconfigure Slune !
Config file ignored.
"""

    
def generate_dot_slune():
  open(CONFIG_FILE, "w").write("""
FULLSCREEN        = %(FULLSCREEN)s
SCREEN_WIDTH      = %(SCREEN_WIDTH)s
SCREEN_HEIGHT     = %(SCREEN_HEIGHT)s
QUALITY           = %(QUALITY)s
MAX_VISION        = %(MAX_VISION)s


CHARACTER    = '%(CHARACTER)s'
VEHICLE      = %(VEHICLE)s
NEXT_MISSION = %(NEXT_MISSION)s

SPEED             = %(SPEED)s
DIFFICULTY        = %(DIFFICULTY)s
RACE_NB_LAPS      = %(RACE_NB_LAPS)s
RACE_NB_OPPONENTS = %(RACE_NB_OPPONENTS)s

NAME = '%(NAME)s'
PORT = %(PORT)s

PARRAIN_HOST = '%(PARRAIN_HOST)s'
PARRAIN_PORT = %(PARRAIN_PORT)s

SOUND_VOLUME = %(SOUND_VOLUME)s

""" % globals())

VERSION = "1.0.15"

GUI = 0

DIFFICULTY_NEWBIE = 0
DIFFICULTY_HACKER = 1
DIFFICULTY_GURU   = 2
DIFFICULTIES = {
  _("Newbie") : 0,
  _("Hacker") : 1,
  _("Guru"  ) : 2,
  }

CHARACTERS = "Tux", "Gnu", "Shark", "Python"

VEHICLES = {
  _("Biplan" ) : 0,
  _("Car"    ) : 1,
  _("Truck"  ) : 2,
  _("Scooter") : 3,
  _("Tanker" ) : 4,
  }



