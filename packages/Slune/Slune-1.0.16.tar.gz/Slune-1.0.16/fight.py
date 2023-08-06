# -*- coding: utf-8 -*-

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

from __future__ import generators

import time, random, math

import soya, soya.widget as widget, soya.ray as ray
import py2play.level as py2p_level, py2play.action as action, py2play.character as character
from soya import Point, Vector
import slune.character as slune_character, slune.globdef as globdef
import slune.controler


def init_fight_game(level):
  pass

def start_fight_game(level):
  CheckEveryoneIsKilled(level)
  
def end_fight_game(level):
  pass

class CheckEveryoneIsKilled(soya.Volume):
  def begin_round(self):
    from py2play.player import CURRENT_PLAYER
    
    if (len(self.parent.characters) == 1) and (self.parent.characters[0] is CURRENT_PLAYER.character):
      from py2play.idler import IDLER
      
      IDLER.level_completed(CURRENT_PLAYER.character, 1)
      
      self.parent.remove(self)
      

STRATEGY_RUN      = 0
STRATEGY_FLEE     = 1
STRATEGY_BACKSTAB = 2
STRATEGY_DODGE    = 3
STRATEGY_FRONTRUN = 4
STRATEGY_SIDERUN  = 5
STRATEGY_WANDER   = 6

class FightChromosom:
  def __init__(self, max_speed, will, turbosity, autododge, run, dodge, flee, frontrun, siderun, wander):
    self.max_speed   = max_speed
    self.will        = will
    self.turbosity   = turbosity
    self.autododge   = autododge
    self.run         = run
    self.dodge       = dodge
    self.flee        = flee
    self.frontrun    = frontrun
    self.siderun     = siderun
    self.wander      = wander
    
  def mutate(self, random):
    for attr, value in self.__dict__.iteritems():
      if attr != "max_speed":
        if random.random() < 0.4: 
          setattr(self, attr, value * (0.5 + random.random()))
          
CHROMOSOMS = {
  
  ("tux", 0):    FightChromosom(0.65, 100.0, -7.0, 0.0, 0.8, 1.0, 0.1, 1.7, 1.0, 1.3),
  ("tux", 1):    FightChromosom(0.8,  100.0, -1.0, 0.0, 1.0, 1.1, 0.6, 1.1, 1.3, 1.0),
  ("tux", 2):    FightChromosom(0.9,  100.0,  0.5, 2.5, 1.0, 1.5, 1.1, 1.0, 1.5, 0.5),
  
  ("gnu", 0):    FightChromosom(0.6,  150.0, -2.0, 0.0, 1.2, 1.0, 0.1, 2.0, 0.6, 1.5),
  ("gnu", 1):    FightChromosom(0.75, 150.0,  0.7, 0.0, 1.8, 0.6, 0.3, 1.2, 0.7, 1.1),
  ("gnu", 2):    FightChromosom(0.9,  150.0,  1.0, 1.5, 2.0, 0.5, 0.4, 0.5, 1.0, 0.5),
  
  ("shark", 0):  FightChromosom(0.6,   80.0, -9.0, 0.0, 0.9, 1.0, 0.2, 1.6, 0.5, 1.5),
  ("shark", 1):  FightChromosom(0.7,   80.0, -4.0, 1.0, 1.0, 1.4, 0.5, 1.0, 0.5, 1.2),
  ("shark", 2):  FightChromosom(0.9,   70.0,  0.0, 1.5, 1.0, 1.5, 0.6, 0.2, 0.5, 0.9),

  ("python", 0): FightChromosom(0.6,  100.0,  0.0, 0.0, 1.2, 1.0, 0.1, 2.0, 0.6, 1.5),
  ("python", 1): FightChromosom(0.8,  100.0,  1.3, 0.5, 1.8, 0.6, 0.3, 1.2, 0.7, 1.1),
  ("python", 2): FightChromosom(0.9,  100.0,  2.0, 2.5, 2.0, 0.5, 0.4, 0.5, 1.0, 0.5),
  
  
#   ("tux", 0): [0.23161940934461928, 0.0, 0.0, 0.54152636319441949, 0.057433463934462713, 1.5669823329989161, 15.877046130951882, 0.18908021610553249, 0.066441050148349098, 3.0216818334258322, 2.0, 0.0, 0.8, 1.0, 0.1, 1.7, 1.0, 1.3, 0.65, 20.0],
#   ("tux", 1): [0.23161940934461928, 0.0, 0.0, 0.54152636319441949, 0.057433463934462713, 1.5669823329989161, 15.877046130951882, 0.18908021610553249, 0.066441050148349098, 3.0216818334258322, 3.0, 0.0, 1.0, 1.1, 0.6, 1.1, 1.3, 1.0, 0.8 , 10.0],
#   ("tux", 2): [0.23161940934461928, 0.0, 0.0, 0.54152636319441949, 0.057433463934462713, 1.5669823329989161, 15.877046130951882, 0.18908021610553249, 0.066441050148349098, 3.0216818334258322, 4.0, 2.5, 1.0, 1.5, 1.1, 1.0, 1.5, 0.5, 0.9 ,  1.0],
  
#   ("gnu", 0): [0.27955060118474129, 0.0, 0.0, 0.94713263528551006, 0.0076398049940541654, 0.46242007806615826, 22.758284696585228, 0.07628649333395944, 0.0051247277708940846, 5.6391784712330182, 2.0, 0.0, 1.2, 1.0, 0.1, 2.0, 0.6, 1.5, 0.6 , 30.0],
#   ("gnu", 1): [0.27955060118474129, 0.0, 0.0, 0.94713263528551006, 0.0076398049940541654, 0.46242007806615826, 22.758284696585228, 0.07628649333395944, 0.0051247277708940846, 5.6391784712330182, 3.0, 0.0, 1.8, 0.6, 0.3, 1.2, 0.7, 1.1, 0.75, 20.0],
#   ("gnu", 2): [0.27955060118474129, 0.0, 0.0, 0.94713263528551006, 0.0076398049940541654, 0.46242007806615826, 22.758284696585228, 0.07628649333395944, 0.0051247277708940846, 5.6391784712330182, 3.5, 1.5, 2.0, 0.5, 0.4, 0.5, 1.0, 0.5, 0.9 , 3.0],
  
#   ("shark", 0): [0.27955060118474129, 0.0, 0.0, 0.94713263528551006, 0.0076398049940541654, 0.46242007806615826, 22.758284696585228, 0.07628649333395944, 0.0051247277708940846, 5.6391784712330182, 2.0, 0.0, 0.9, 1.0, 0.2, 1.6, 0.5, 1.5, 0.6, 20.0],
#   ("shark", 1): [0.27955060118474129, 0.0, 0.0, 0.94713263528551006, 0.0076398049940541654, 0.46242007806615826, 22.758284696585228, 0.07628649333395944, 0.0051247277708940846, 5.6391784712330182, 3.0, 1.0, 1.0, 1.4, 0.5, 1.0, 0.5, 1.2, 0.7, 12.0],
#   ("shark", 2): [0.27955060118474129, 0.0, 0.0, 0.94713263528551006, 0.0076398049940541654, 0.46242007806615826, 22.758284696585228, 0.07628649333395944, 0.0051247277708940846, 5.6391784712330182, 3.5, 1.5, 1.0, 1.5, 0.6, 0.2, 0.5, 0.9, 0.9,  2.0],

# For mission levels
#  ("killer", 0): [0.27955060118474129, 0.0, 0.0, 0.94713263528551006, 0.0076398049940541654, 0.46242007806615826, 22.758284696585228, 0.07628649333395944, 0.0051247277708940846, 5.6391784712330182, 2.0, 0.0, 1.2, 0.0, 0.0, 0.0, 0.6, 0.5, 0.85, 1.0],
#  ("killer", 1): [0.27955060118474129, 0.0, 0.0, 0.94713263528551006, 0.0076398049940541654, 0.46242007806615826, 22.758284696585228, 0.07628649333395944, 0.0051247277708940846, 5.6391784712330182, 3.0, 0.0, 1.8, 0.0, 0.0, 0.0, 0.7, 0.2, 0.92,  1.0],
#  ("killer", 2): [0.27955060118474129, 0.0, 0.0, 0.94713263528551006, 0.0076398049940541654, 0.46242007806615826, 22.758284696585228, 0.07628649333395944, 0.0051247277708940846, 5.6391784712330182, 3.5, 0.0, 2.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.05,  1.0],
  
  ("killer", 0):    FightChromosom(0.6,  150.0, 0.2, 0.0, 1.2, 1.0, 0.1, 2.0, 0.6, 1.5),
  ("killer", 1):    FightChromosom(0.75, 150.0, 0.7, 0.0, 1.8, 0.6, 0.3, 1.2, 0.7, 1.1),
  ("killer", 2):    FightChromosom(0.9,  150.0, 1.0, 1.5, 2.0, 0.5, 0.4, 0.5, 1.0, 0.5),
  
  ("killer_flight", 0): FightChromosom(0.6,  150.0, -10.0, 0.0, 1.2, 1.0, 0.1, 2.0, 0.6, 1.5),
  ("killer_flight", 1): FightChromosom(0.75, 150.0, -10.0, 0.0, 1.8, 0.6, 0.3, 1.2, 0.7, 1.1),
  ("killer_flight", 2): FightChromosom(0.9,  150.0, -10.0, 1.5, 2.0, 0.5, 0.4, 0.5, 1.0, 0.5),
  
  ("alien_boss", 0):    FightChromosom(0.9, 150.0, 1.5, 1.5, 2.0, 0.5, 0.4, 0.5, 1.0, 0.5),
  ("alien_boss", 1):    FightChromosom(0.9, 150.0, 1.0, 0.0, 1.8, 0.6, 0.3, 1.2, 0.7, 1.1),
  ("alien_boss", 2):    FightChromosom(0.9, 150.0, 0.7, 0.0, 1.2, 1.0, 0.1, 2.0, 0.6, 1.5),
  }

class Fighter(slune_character.NonPlayerCharacter):
  def __init__(self, parent = None, chromosom = None):
    slune_character.NonPlayerCharacter.__init__(self, parent)
    
    self.chromosom = chromosom
    self.clan = 2
    
  def choose_target(self):
    best      = None
    best_dist = 10000.0
    for level in self.get_root():
      if isinstance(level, py2p_level.Level):
        for character in level.characters:
          if (not character is self) and (character.clan > 0) and (character.clan != self.clan):
            dist = character.distance_to(self)
            if dist < best_dist:
              best      = character
              best_dist = dist
    return best
  
  def choose_strategy(self, target):
    dist = self.distance_to(target)
    c = self.chromosom
    return max(
      (self.life              + self.random.random() * c.run,      STRATEGY_RUN),
      (self.life - 0.1 * dist + self.random.random() * c.dodge,    STRATEGY_DODGE),
      (1.0 - 2.0 * self.life  + self.random.random() * c.flee,     STRATEGY_FLEE),
      (self.life              + self.random.random() * c.frontrun, STRATEGY_FRONTRUN),
      (self.life              + self.random.random() * c.siderun,  STRATEGY_SIDERUN),
      (                         self.random.random() * c.wander,   STRATEGY_WANDER),
      )[1]
  
  def init(self):
    if not self.perso_name:
      persos = list(globdef.CHARACTERS)
      self.random.shuffle(persos)
      for perso in persos:
        perso = perso.lower()
        for c in self.level:
          if (hasattr(c, "perso_name")) and (c.perso_name == perso): break
        else:
          self.perso_name = perso
          break
      else: self.perso_name = persos[0].lower()
    self.set_perso(self.perso_name)
    self.set_vehicle(self.random.choice(globdef.VEHICLES.values()))
    
  def IAControler(self):
    c = self.chromosom = self.chromosom or CHROMOSOMS[self.perso_name, self.level.difficulty]
    c.mutate(self.random)
    self.max_speed = c.max_speed
    
    target = None
    while 1:
      target   = self.choose_target() or target
      strategy = self.choose_strategy(target)
      
      if   strategy == STRATEGY_RUN:
        yield slune.controler.AttackRun(self, target, c.will, c.autododge, c.turbosity + 2.0 * self.life)
        
      elif strategy == STRATEGY_FRONTRUN:
        yield slune.controler.AttackFrontRun(self, target, c.will, c.autododge, c.turbosity + 2.0 * self.life)
        
      elif strategy == STRATEGY_SIDERUN:
        yield slune.controler.AttackSideRun(self, target, c.will, c.autododge, c.turbosity + 2.0 * self.life)
        
      elif strategy == STRATEGY_FLEE:
        yield slune.controler.Flee(self, target, c.will)
        
      elif strategy == STRATEGY_DODGE:
        yield slune.controler.Feinte(self, target, c.will, c.autododge + 3.0)
        
      elif strategy == STRATEGY_WANDER:
        yield slune.controler.Wander(self, c.will)

        
class AlienBoss(Fighter, slune_character.Competitor):
  def __init__(self, parent = None):
    from py2play.player import CURRENT_PLAYER
    Fighter.__init__(self, parent, CHROMOSOMS["alien_boss", CURRENT_PLAYER.level.difficulty])


class Mission6Killer(slune_character.NonPlayerCharacter):
  def __init__(self, parent = None, chromosom = None):
    slune_character.NonPlayerCharacter.__init__(self, parent)
    
    self.chromosom = chromosom
    self.clan = 2
    
  def choose_target(self):
    best      = None
    best_dist = 10000.0
    for level in self.get_root():
      if isinstance(level, py2p_level.Level):
        for character in level.characters:
          if (not character is self) and (character.clan > 0) and (character.clan != self.clan):
            dist = character.distance_to(self)
            if dist < best_dist:
              best      = character
              best_dist = dist
    return best
  
  def init(self):
    self.set_perso(self.perso_name)
    
  def IAControler(self):
    c = self.chromosom = self.chromosom or CHROMOSOMS[self.perso_name, self.level.difficulty]
    self.max_speed = c.max_speed
    
    from py2play.idler import IDLER
    
    while 1:
      target = self.choose_target() or target
      if not hasattr(target, "nb_avertissements"):
        target.disabled          = 0
        target.nb_avertissements = {0:4, 1:2, 2:0}[target.level.difficulty]
        
      for i in range(100):
        fx, fy, fz = self.transform_point(target.x, target.y, target.z, target.parent)
        
        if   target.disabled: target.disabled -= 1
        elif (target.y < 1.4) and (fz < 0.0) and (self.distance_to(target) < 3.0):
          IDLER.message(_("__scenar6-1__"))
          if target.nb_avertissements:
            target.disabled = 100
            target.nb_avertissements -= 1
          else: # You loose...
            from videosequence import GnuSpeech
            GnuSpeech((_("__scenar6-2__"), _("__gameover__")), 1).start(tux = target)
            
            while 1: yield slune_character.Action()
            
        yield slune.controler.runto(self, target, canjump = 0)
        

class Mission7Pusher(slune_character.NonPlayerCharacter):
  def __init__(self, parent = None, chromosom = None):
    slune_character.NonPlayerCharacter.__init__(self, parent)
    
    self.chromosom = chromosom
    
    self.clan = 2
    self.check_ground_vector = Vector(self, 0.0, -2.0, -2.0)
    self.jumping = 0
    self.current_action = slune_character.Action()
    
  def choose_target(self):
    best      = None
    best_dist = 10000.0
    for level in self.get_root():
      if isinstance(level, py2p_level.Level):
        for character in level.characters:
          if (not character is self) and (character.clan > 0) and (character.clan != self.clan):
            dist = character.distance_to(self)
            if dist < best_dist:
              best      = character
              best_dist = dist
    return best
  
  def init(self): self.set_perso(self.perso_name)
  
  def IAControler(self):
    c = self.chromosom = self.chromosom or CHROMOSOMS[self.perso_name, self.level.difficulty]
    self.max_speed = c.max_speed
    
    from py2play.idler import IDLER
    
    for i in range([10000, 10, 6][self.parent.difficulty]):
      target = self.choose_target() or target
      yield slune.controler.PushToKill(self, target, c.turbosity + 2.0 * self.life)
      
    while 1: # Turn berserk
      target = self.choose_target() or target
      yield slune.controler.AttackRun(self, target, turbosity = c.turbosity + 2.0 * self.life)
      

