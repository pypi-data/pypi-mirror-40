# -*- coding: utf-8 -*-

# Slune
# Copyright (C) 2003 Jean-Baptiste LAMY
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

import soya, soya.widget as widget
import py2play.level as py2p_level, py2play.action as action, py2play.character as character
import slune.character as slune_character
import slune.controler


def init_bowling_game(level):
  pass
  
def start_bowling_game(level, add_opponent1 = 1):
  from py2play.idler import IDLER
  
  bowling = Bowling(level, level["ball"], 3 - level.difficulty)
  IDLER.no_blackbands_group.insert(0, BowlingLabel(bowling))
  
def end_bowling_game(level):
  pass


def GoBack(character):
  for i in range(20):
    if character.z >= 10.5: break
    
    p = soya.Point(character.level, 10.0, 0.5, 12.0)
    p.convert_to(character)
    
    if   p.x < -4.0: x =  0.7
    elif p.x >  4.0: x = -0.7
    else:            x =  0.0

    if p.z > 0: y = 2.0
    else:       y = 0.0

    yield slune_character.Action(slune_character.ACTION_WAIT, x, y)
  
class Bowling(soya.Volume):
  def __init__(self, parent, ball, nb_extra_ball):
    soya.Volume.__init__(self, parent)
    
    self.ball          = ball
    self.ball_fired    = 0
    self.nb_extra_ball = nb_extra_ball
    self.nb_quilles    = 0
    self.nb_balls_used = 1
    self.ball_pos      = ball.position()
    self.waiting       = 0
    
  def add_ball(self):
    self.nb_extra_ball -= 1
    self.nb_balls_used += 1

    ball = slune_character.Ball(self.parent)
    ball.name = "ball"
    ball.move(self.ball_pos)
    ball.set_shape(self.ball.shape)
    ball.radius   = self.ball.radius
    ball.radius_y = self.ball.radius_y
    ball.weight   = self.ball.weight
    self.parent.pushables.append(ball)
    self.ball = ball
    
    self.ball_fired = 0
    
  def begin_round(self):
    from py2play.idler import IDLER
    
    level = self.parent
    
    for character in level.characters:
      if character.z < -15.0:
        IDLER.level_completed(character, 0)
        level.remove(self)
    
    self.nb_quilles = len([e for e in level if getattr(e, "name", None) == "quille"])
    
    if self.waiting:
      self.waiting -= 1
      if not self.waiting:
        if level.characters[0].z < 10.0:
          level.characters[0].controler.append(GoBack(level.characters[0]))
          self.waiting = 10
        else:
          self.add_ball()
          
    elif not self.ball_fired:
      if self.ball.worth_playing: self.ball_fired = 1
      
    else:
      for e in level:
        if hasattr(e, "name") and ((e.name == "ball") or (e.name == "quille")):
          if e.worth_playing and e.parent: break
      else: # Current ball is finished
        if self.nb_quilles:
          if self.nb_extra_ball:
            self.waiting = 1
          else:
            IDLER.level_completed(character, 0)
            level.remove(self)
            
        else: # All quille are out !
          if self.nb_balls_used == 1:
            IDLER.level_completed(character, 1, _("__bowling_winner_strike__"))
          else:
            IDLER.level_completed(character, 1)
          level.remove(self)
          
  
class BowlingLabel(widget.Label):
  def __init__(self, bowling):
    self.bowling = bowling
    self.format = str(_("__bowlingformat__"))
    print self.format
    self.old_nb_balls   = -1
    self.old_nb_quilles = -1
    widget.Label.__init__(self)
    
    self.left = 10
    self.width  = 700
    self.height = 100
    
  def resize(self, parent_left, parent_top, parent_width, parent_height):
    self.top = parent_top + soya.root_widget.height - 43
    
  def widget_begin_round(self):
    if (self.old_nb_balls != self.bowling.nb_extra_ball) or (self.old_nb_quilles != self.bowling.nb_quilles):
      self.text = self.format % (self.bowling.nb_extra_ball, self.bowling.nb_quilles)
      self.old_nb_balls   = self.bowling.nb_extra_ball
      self.old_nb_quilles = self.bowling.nb_quilles
