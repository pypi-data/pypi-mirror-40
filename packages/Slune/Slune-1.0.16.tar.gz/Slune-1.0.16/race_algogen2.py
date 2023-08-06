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

# This script is used for genetically optimizing racing IA.
# It considers 2 character at a time; see race_algogen for a version with a single IA.

from __future__ import generators

RENDER = 0
PERSO  = "tux"
LEVEL  = "crashfunkel-race-2"
import sys

i = 1
while i < len(sys.argv):
  arg = sys.argv[i]
  if   arg == "--render": RENDER = 1
  
  elif arg == "--perso":
    i += 1
    PERSO = sys.argv[i]
  
  elif arg == "--level":
    i += 1
    LEVEL = sys.argv[i]
  
  elif arg == "--help":
    print """Optimize racing IA, by running 2 IAs against each other.
The resulting chromosoms are printed on stdout, and should be manually copied in race.py.

Options:
  --render         Render the 3D, so as you can see something (else no rendering is performed, for speedup).
  --perso <perso>  Choose the character IA to optimize (e.g. tux, gnu,...).
  --level <level>  Choose the level. Should be a racing level."""
    sys.exit()
    
  else:
    print "Unknown options %s !" % arg
    sys.exit(1)
    
  i += 1


import random
import soya, soya.soya3d as soya3d, soya.game.level as soya_game_level, soya.game.camera as soya_camera
import py2play.level
import slune.race as race, slune.level, slune.character, slune.player

MAX_DURATION = 1500

class Idler(slune.level.Idler):
  def __init__(self):
    slune.level.Idler.__init__(self)
    self.next_flag_name1 = ""
    self.next_flag_name2 = ""
    
  def idle(self):
    value1 = value2 = MAX_DURATION
    OPPONENT1.best_lap = OPPONENT2.best_lap = 9999.0
    race.init_race_opponent(OPPONENT1)
    race.init_race_opponent(OPPONENT2)
    
    for nb_round in range(MAX_DURATION):
      self.begin_round()
      self.advance_time(1.0)
      self.end_round()
      
      if self.next_round_tasks:
        for task in self.next_round_tasks: task()
        self.next_round_tasks = []
        
      self.render()

      if OPPONENT1.best_lap != 9999.0:
        if value1 == MAX_DURATION: value1 = nb_round
      else:
        if OPPONENT1.life < 0: value1 = MAX_DURATION + 1
        
      if OPPONENT2.best_lap != 9999.0:
        if value2 == MAX_DURATION: value2 = nb_round
      else:
        if OPPONENT2.life < 0: value2 = MAX_DURATION + 1
        
      if (value1 != MAX_DURATION) and (value2 != MAX_DURATION): break
      
    return value1, value2
  
  def render(self):
    if RENDER: slune.level.Idler.render(self)
    
    if hasattr(OPPONENT1, "next_flag_name"):
      if self.next_flag_name1 != OPPONENT1.next_flag_name:
        self.next_flag_name1 = OPPONENT1.next_flag_name
        print "Opponent 1: Next flag: ", self.next_flag_name1
        
    if hasattr(OPPONENT2, "next_flag_name"):
      if self.next_flag_name2 != OPPONENT2.next_flag_name:
        self.next_flag_name2 = OPPONENT2.next_flag_name
        print "Opponent 2: Next flag: ", self.next_flag_name2
        
  
soya.init(width = 640, height = 480, fullscreen = 0)

idler = Idler()

import py2play.player
py2play.player.CURRENT_PLAYER = 1 # HACK !

level = py2play.level.CREATE("level-" + LEVEL)
level.set_active(1)
level.max_laps = 999
for character in level.characters: level.remove_character(character)

class Opponent(race.Opponent):
  def __init__(self, *args, **kargs):
    race.Opponent.__init__(self, *args, **kargs)
    
    self.value = 0
    
OPPONENT1 = None
OPPONENT2 = None
def test(opponent1, opponent2):
  global OPPONENT1, OPPONENT2
  OPPONENT1 = opponent1
  OPPONENT2 = opponent2
  
  OPPONENT1.perso_name = PERSO
  OPPONENT2.perso_name = PERSO
  
  idler.camera.add_traveling(soya_camera.ThirdPersonTraveling(OPPONENT2.camera_target))
  
  OPPONENT1.set_level(level, 1)
  OPPONENT2.set_level(level, 1)
  
  value1, value2 = idler.idle()

  # If they are not dead !
  if OPPONENT1.parent: OPPONENT1.parent.remove_character(OPPONENT1)
  if OPPONENT2.parent: OPPONENT2.parent.remove_character(OPPONENT2)
  
  OPPONENT1.level = None
  OPPONENT2.level = None
  
  return value1, value2

def value_sorter(a, b): return cmp(a.value, b.value)

def mutate(value):
  if random.random < 0.6: return value
  if not value: return 0.02
  return value + (random.random() - 0.5) * value

def make_love(father, mother):
  chromosom = map(random.choice, zip(father.chromosom, mother.chromosom))
  chromosom = map(mutate, chromosom)
  return Opponent(chromosom = chromosom)



OPPONENTS = [Opponent(chromosom = race.CHROMOSOMS[(PERSO, 2)]), Opponent(chromosom = race.CHROMOSOMS[(PERSO, 2)])]

while 1:
  for i in range(4):
    OPPONENTS.append(make_love(random.choice(OPPONENTS), random.choice(OPPONENTS)))
    
  for i in range(0, len(OPPONENTS), 2):
    opponent1 = OPPONENTS[i]
    opponent2 = OPPONENTS[i + 1]
    opponent1.value, opponent2.value = test(opponent1, opponent2)
    
  OPPONENTS.sort(value_sorter)
  OPPONENTS = OPPONENTS[:4]
  
  for opponent in OPPONENTS:
    print opponent.chromosom, "=>", opponent.value
