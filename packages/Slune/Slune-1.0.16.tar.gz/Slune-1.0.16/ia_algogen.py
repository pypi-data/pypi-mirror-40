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
# It considers only 1 character at a time; see race_algogen2 for a version with 2 IA.

from __future__ import generators

RENDER = 0
PERSO  = "tux"
LEVEL  = "crashfunkel-race-1"
#LEVEL  = "crashfunkel-race-2"
#LEVEL  = "canion-race-1"
#LEVEL  = "canion-race-3"
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
    print """Optimize IA, by running 1 IA against the clock.
The resulting params are printed on stdout, and should be manually copied in race.py.

Options:
  --render         Render the 3D, so as you can see something (else no rendering is performed, for speedup).
  --perso <perso>  Choose the character IA to optimize (e.g. tux, gnu,...).
  --level <level>  Choose the level. Should be a racing level."""
    sys.exit()
    
  else:
    print "Unknown options %s !" % arg
    sys.exit(1)
    
  i += 1

IA_PARAMS = [
"slune.controler.GOTO_X_2_TURN",
"slune.controler.GOTO_X_2_SPEED",
"slune.controler.GOTO_Y_2_SPEED",
"slune.controler.GOTO_Z_2_SPEED",
"slune.controler.GOTO_NOGROUND_2_SPEED",
"slune.controler.GOTO_Y_2_JUMP",
"slune.controler.GOTO_Z_2_JUMP",
"slune.controler.GOTO_NOGROUND_2_JUMP",
  ]

import random
import soya, soya.soya3d as soya3d, soya.game.level as soya_game_level, soya.game.camera as soya_camera
import py2play.level
import slune.race as race, slune.level, slune.character, slune.player, slune.controler

class Idler(slune.level.Idler):
  def __init__(self):
    slune.level.Idler.__init__(self)
    self.next_flag_name = ""
    
  def idle(self):
    race.init_race_opponent(OPPONENT)
    
    for nb_round in range(3300):
      self.begin_round()
      self.advance_time(1.0)
      self.end_round()
      
      if self.next_round_tasks:
        for task in self.next_round_tasks: task()
        self.next_round_tasks = []
        
      self.render()
      
      if OPPONENT.best_lap != 9999.0: break
      
    return nb_round
  
  def render(self):
    if RENDER: slune.level.Idler.render(self)
    
    if hasattr(OPPONENT, "next_flag_name"):
      if self.next_flag_name != OPPONENT.next_flag_name:
        self.next_flag_name = OPPONENT.next_flag_name
        print "Next flag: ", self.next_flag_name
        
  
soya.init(width = 640, height = 480, fullscreen = 0)

idler = Idler()

import py2play.player
py2play.player.CURRENT_PLAYER = py2play.player.Player("fake") # HACK !
py2play.player.CURRENT_PLAYER.character = None

level = py2play.level.CREATE("level-" + LEVEL)
level.set_active(1)
race.init_race_game (level)
race.start_race_game(level)

for character in level.characters[:]: level.remove_character(character)

class Opponent(race.Opponent):
  def __init__(self, *args, **kargs):
    race.Opponent.__init__(self, *args, **kargs)
    
    self.value = 0
    
OPPONENT = None
def test(opponent):
  global OPPONENT
  OPPONENT = opponent
  OPPONENT.perso_name = PERSO
  
  idler.camera.add_traveling(soya_camera.ThirdPersonTraveling(OPPONENT.camera_target))
  
  OPPONENT.set_level(level, 1)
  OPPONENT.set_vehicle(1)
  
  for param in IA_PARAMS: exec """%s = %s""" % (param, OPPONENT.params[param])
  
  value = idler.idle()
  print value
  
  OPPONENT.parent.remove_character(OPPONENT)
  
  return value

def value_sorter(a, b): return cmp(a.value, b.value)

def mutate(value):
  if random.random() < 0.8: return value
  if not value: return 0.02
  return value + (random.random() - 0.5) * value

def make_love(father, mother):
  o = Opponent(chromosom = father.chromosom)
  o.params = dict(map(lambda param: (param, mutate(random.choice([father.params[param], mother.params[param]]))), IA_PARAMS))
  return o

OPPONENTS = [Opponent(chromosom = race.CHROMOSOMS[(PERSO, 2)]), Opponent(chromosom = race.CHROMOSOMS[(PERSO, 2)])]
for opponent in OPPONENTS:
  opponent.params = dict(map(lambda param: (param, eval(param)), IA_PARAMS))
  
while 1:
  for i in range(4):
    OPPONENTS.append(make_love(random.choice(OPPONENTS), random.choice(OPPONENTS)))
    
  for opponent in OPPONENTS:
    if not opponent.value: opponent.value = test(opponent)
      
  OPPONENTS.sort(value_sorter)
  OPPONENTS = OPPONENTS[:4]

  print
  for opponent in OPPONENTS:
    for k, v in opponent.params.iteritems():
      print k, "=", v
    print "=>", opponent.value
    print
