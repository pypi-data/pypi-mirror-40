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

import time, random, math, slune.sound as sound

import soya, soya.widget as widget, soya.ray as ray
import py2play.level as py2p_level, py2play.action as action, py2play.character as character
from soya import Point, Vector
import slune.character as slune_character
import slune.controler

def init_freestyle_game(level):
  pass
      
def start_freestyle_game(level, time_limit = -1.0, no_time_left_message = None):
  competitors = []
  for character in level.characters:
    if isinstance(character, slune_character.Competitor):
      character.score       = 0
      character.score_start = time.time()
      competitors.append(character)
      
  from py2play.idler import IDLER
  IDLER.no_blackbands_group.add(ScoreLabel(competitors, time_limit, no_time_left_message))
  
def end_freestyle_game(level):
  for widget in soya.root_widget.children:
    if isinstance(widget, ScoreLabel):
      soya.root_widget.remove(widget)
      break
    

def start_time_limit(level, time_limits, no_time_left_message = None, start_checker = 0):
  competitors = []
  for character in level.characters:
    if isinstance(character, slune_character.Competitor):
      character.score_start = time.time()
      competitors.append(character)
      
  from py2play.idler import IDLER
  IDLER.no_blackbands_group.add(TimerLabel(competitors, time_limits[level.difficulty], no_time_left_message))
  
  if start_checker:
    Checker(level)
    
    if not hasattr(level, "flags"):
      import race
      
      level.flags = [] # Indexes all flags
      
      for item in level:
        if isinstance(item, race.Flag):
          item.visible = (item.name == "flag_0")
          level.flags.append(item)
          
      level.flags.sort(lambda f1, f2: cmp(f1.flag_id, f2.flag_id))
      
    
def end_time_limit(level):
  for widget in soya.root_widget.children:
    if isinstance(widget, TimerLabel):
      soya.root_widget.remove(widget)
      break
    
    
class Checker(soya.Volume):
  def begin_round(self):
    from py2play.idler import IDLER
    
    level = self.parent
    
    for character in level.characters:
      if isinstance(character, slune_character.Competitor):
        flag = level.flags[character.next_flag_id]
        if character.distance_to(flag) < (flag.radius + character.radius):
          if character.next_flag_id + 1 < len(self.parent.flags):
            next_flag_id = character.next_flag_id + 1
            next_flag = self.parent.flags[next_flag_id]
          else:
            next_flag_id = 0
            next_flag = self.parent.flags[0]
            character.nb_laps += 1
            now = time.time()
            this_lap = now - character.lap_start
            if this_lap < character.best_lap: character.best_lap = this_lap
            character.lap_start = now

            if character.nb_laps >= 0:
              firework = soya.FlagFirework(level, nb_particles = 6)
              firework.move(flag)
              firework.regenerate()
              firework.removable = 1
              
              character.next_flag_id = 0
              
              level.ranks.append(character)

              if len(level.ranks) == 1: # Winner
                IDLER.level_completed(character, 1, _("__race_winner__"))
              else:
                IDLER.level_completed(character, 0, _("__race_looser__") % len(level.ranks))
                
              from py2play.player import CURRENT_PLAYER
              if not character is CURRENT_PLAYER.character:
                IDLER.message(_("__race_arrival__") % (character.displayname(), len(level.ranks)))
                
              if not character.played:
                character.level.remove_character(character)
              return
            
          character.next_flag_id = next_flag_id
          
          sound.play("flag-1.wav", character)
          
          if character.played and character.player.active:
            flag.visible = 0
            next_flag.visible = 1
            
            firework = soya.Smoke(level, nb_particles = 10, removable = 1)
            firework.move(flag)
            firework.regenerate()



V = Vector()

SCORES = {
  "jump"               :    5,
  "longjump"           :   10,
  "verylongjump"       :  150,
  "climbing"           :   10,
  "highjump"           :   15,
  
  "180"                :   50,
  "360"                :   85,
  "720"                :  110,
  "rotup"              :   50,
  "rotup180"           :  120,
  "rotup360"           :  150,
  "rotup720"           : 1000,
  
  "looping"            :  100,
  "doublelooping"      : 1000,
  "retrolooping"       :  200,
  "doubleretrolooping" : 1500,
  
  "s"                  :  100,
  "doubles"            : 1000,
  
  "spinfall"           :  150,
  "bigspinfall"        : 1200,
  "flamingtorch"       :   80,
  "bigflamingtorch"    :  800,
  }

class FreeStyle(soya.Volume):
  def __init__(self, parent = None, character = None):
    soya.Volume.__init__(self, parent)
    self.character = character
    
    self.last_figure        = ""
    self.last_figure_nb     = 0
    self.last_figure_time   = 0
    self.jump_direction     = Vector()
    self.last_180_direction = Vector()
    self.last_180_y         = 1.0
    self.on_ground          = 1
    self.y_angle            = 0.0
    self.y_direction        = Vector()
    self.jump_time          = 0
    self.nb_180             = 0
    self.nb_s               = 0
    self.next_s_dir         = -1.0
    self.jump_y             = 0.0
    self.max_y              = 0.0
    self.spinfall           = 0
    self.flamingtorch       = 0
    
  def recognized(self, figure):
    from py2play.idler import IDLER
    if (self.last_figure == figure) and (self.character.round - self.last_figure_time < 500):
      self.last_figure      = figure
      self.last_figure_nb  += 1
      self.last_figure_time = self.character.round
      
      bonus = self.last_figure_nb * SCORES[figure]
      IDLER.message(_("__figure_" + figure + "__") + " X " + str(self.last_figure_nb) + " (" + str(bonus) + ")")
      
    else:
      self.last_figure      = figure
      self.last_figure_nb   = 1
      self.last_figure_time = self.character.round
      
      bonus = SCORES[figure]
      IDLER.message(_("__figure_" + figure + "__") + " (" + str(bonus) + ")")
      
    self.character.score += bonus
    
  def begin_round(self):
    if self.on_ground and not self.character.on_ground: # Start jumping
      self.jump_time    = 0
      self.on_ground    = 0
      self.y_angle      = 0.0
      self.nb_180       = 0
      self.nb_s         = 0
      self.next_s_dir   = -1.0
      self.spinfall     = 0
      self.flamingtorch = 0
      self.jump_y       = self.character.y
      self.max_y        = self.jump_y
      self.last_180_y   = 1.0
      self.jump_direction.set_xyz(*self.character.level.transform_vector(0.0, 0.0, -1.0, self.character))
      self.last_180_direction.clone(self.jump_direction)
      self.y_direction.clone(self.jump_direction)
      
    elif self.character.on_ground and not self.on_ground: # End jumping
      self.on_ground = 1
      
      if self.jump_time <  20: return # NOT a valid jump !!!
      
      if (self.y_angle >  560.0): self.recognized("doublelooping"); return
      if (self.y_angle >  200.0): self.recognized("looping"); return
      if (self.y_angle < -560.0): self.recognized("doubleretrolooping"); return
      if (self.y_angle < -200.0): self.recognized("retrolooping"); return
      
      if self.nb_s == 2: self.recognized("s"); return
      if self.nb_s == 4: self.recognized("doubles"); return
      
      if self.spinfall > 27: self.recognized("bigspinfall"); return
      if self.spinfall > 10: self.recognized("spinfall"); return
      
      if self.flamingtorch > 30: self.recognized("bigflamingtorch"); return
      if self.flamingtorch > 10: self.recognized("flamingtorch"); return
      
      if   self.y_direction.y > 0.75:
        if self.nb_180 == 1: self.recognized("180"); return
        if self.nb_180 == 2: self.recognized("360"); return
        if self.nb_180 == 4: self.recognized("720"); return
        
      elif self.y_direction.y < -0.75:
        if self.nb_180 == 2: self.recognized("rotup180"); return
        if self.nb_180 == 3: self.recognized("rotup360"); return
        if self.nb_180 == 5: self.recognized("rotup720"); return
        
      if self.y_direction.y < -0.5: self.recognized("rotup"); return

      if self.jump_time > 200:                 self.recognized("verylongjump"); return
      if self.character.y - self.jump_y > 3.0: self.recognized("climbing"); return
      if self.max_y - self.jump_y >  7.0:      self.recognized("highjump"); return
      if self.jump_time >  70:                 self.recognized("longjump"); return
      if self.jump_time >  20:                 self.recognized("jump"); return
      
    if not self.character.on_ground: # Jumping
      self.jump_time += 1
      if self.max_y < self.character.y: self.max_y = self.character.y
      
      x, y, z = self.character.transform_vector(self.y_direction.x, self.y_direction.y, self.y_direction.z, self.character.level)
      
      #self.y_angle -= z
      
      if   self.character.current_action.action == slune_character.ACTION_ROTUP:
        self.y_angle += self.character.rotup_speed
      elif self.character.current_action.action == slune_character.ACTION_ROTDOWN:
        self.y_angle -= self.character.rotup_speed
      
      self.y_direction.set_xyz(*self.character.level.transform_vector(0.0, 1.0,  0.0, self.character))
      if self.y_direction.y * self.next_s_dir > 0.8:
        self.nb_s   += 1
        self.next_s_dir *= -1.0
        
      V.set_xyz(*self.character.level.transform_vector(0.0, 0.0, -1.0, self.character))
      if V.dot_product(self.last_180_direction) < -0.5:
        if self.last_180_y * self.y_direction.y > 0.3:
          self.nb_180 += 1
          self.last_180_direction *= -1
        else:
          self.last_180_y *= -1.0
          
      if self.character.current_action.action == slune_character.ACTION_ROTLAT:
        if   V.y < -0.6: self.spinfall += 1
        elif (V.y >  0.8) and self.character.current_action.mouse_y > 0.8: self.flamingtorch += 1
        

class ScoreLabel(widget.Label):
  def __init__(self, characters, time_limit = -1.0, no_time_left_message = None):
    self.characters = characters
    self.format1 = str(_("__scoreformat1__")) + "\n"
    format2 = str(_("__scoreformat2__"))
    self.format2s = "\n".join([character.displayname() + format2 for character in characters])
    widget.Label.__init__(self)
    
    self.left = 10
    self.top = soya.root_widget.height - 33 * (len(self.characters) + 1)
    self.width  = 400
    self.height = 100
    
    self.time_limit = time_limit
    self.no_time_left_message = no_time_left_message or _("__no_time_left__")
    
  def resize(self, parent_left, parent_top, parent_width, parent_height):
    self.top = soya.root_widget.height - 33 * (len(self.characters) + 1)
    
  def render(self):
    if self.time_limit == -1.0:
      time_left = 0.0
    else:
      time_left = (self.time_limit - (time.time() - self.characters[0].score_start))
      if time_left < 0.0:
        self.time_limit = -1.0
        
        import videosequence
        for character in self.characters:
          videosequence.MissionCompleted(0, self.no_time_left_message).start(tux = character)
          
    if len(self.characters) == 1:
      self.text = self.format1 % time_left + self.format2s % self.characters[0].score
    else:
      self.text = self.format1 % time_left + self.format2s % [str(character.score) for character in self.characters]
      
    widget.Label.render(self)
    

class TimerLabel(widget.Label):
  def __init__(self, characters, time_limit = -1.0, no_time_left = None):
    self.characters = characters
    self.format1 = str(_("__scoreformat1__")) + "\n"
    widget.Label.__init__(self)
    
    self.left = 10
    self.top = soya.root_widget.height - 33
    self.width  = 400
    self.height = 100
    
    self.time_limit = time_limit
    self.no_time_left = no_time_left or _("__no_time_left__")
    
  def resize(self, parent_left, parent_top, parent_width, parent_height):
    self.top = soya.root_widget.height - 33
    
  def render(self):
    if self.time_limit == -1.0:
      time_left = 0.0
    else:
      time_left = (self.time_limit - (time.time() - self.characters[0].score_start))
      if time_left < 0.0:
        self.time_limit = -1.0

        if callable(self.no_time_left): self.no_time_left(self.characters)
        else: 
          import videosequence
          for character in self.characters:
            videosequence.MissionCompleted(0, self.no_time_left).start(tux = character)
            
    self.text = self.format1 % time_left
      
    widget.Label.render(self)
    
