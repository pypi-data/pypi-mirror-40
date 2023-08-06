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

import soya
import py2play.level as py2p_level, py2play.action as action, py2play.character as character
import slune.character as slune_character
import slune.controler

CHROMOSOMS = {
  0: [0.9, 0.54152636319441949, 0.057433463934462713, 1.5669823329989161, 15.877046130951882, 0.18908021610553249, 0.066441050148349098, 3.0216818334258322, 0.1 ],
  1: [0.9, 0.54152636319441949, 0.057433463934462713, 1.5669823329989161, 15.877046130951882, 0.18908021610553249, 0.066441050148349098, 3.0216818334258322, 0.5],
  2: [0.9, 0.54152636319441949, 0.057433463934462713, 1.5669823329989161, 15.877046130951882, 0.18908021610553249, 0.066441050148349098, 3.0216818334258322, 1.0 ],
  }

class Praise(slune_character.NonPlayerCharacter):
  def __init__(self, parent = None, chromosom = None, path = (), escape_dist = 40.0, wait_dist = 10.0):
    slune_character.NonPlayerCharacter.__init__(self, parent)
    
    self.chromosom           = chromosom
    self.path                = path
    self.escape_dist         = escape_dist
    self.wait_dist           = wait_dist
    self.check_ground_vector = soya.Vector(self, 0.0, -1.5, -2.0)
    
  def finished(self): pass
  
  def escaped_from(self, hunter):
    import videosequence
    videosequence.HuntFailed().start(praise = self, hunter = hunter)
    
  def IAControler(character):
    c = character.chromosom = character.chromosom or CHROMOSOMS[character.level.difficulty]
    max_speed = c[8]
    jumping = 0
    
    mouse_x = mouse_y = 0.0
    
    while not character.path: yield slune_character.Action()
    
    while character.wait_dist:
      for hunter in character.level.characters:
        if isinstance(hunter, slune_character.Competitor):
          if character.distance_to(hunter) < character.wait_dist: character.wait_dist = 0.0
          yield slune_character.Action()
          
    while 1:
      if not character.path:
        while character.finished(): yield slune_character.Action(slune_character.ACTION_WAIT)
        while 1: yield slune_character.Action(slune_character.ACTION_WAIT)
        
      else:
        character.speed.y = 100.0 # Avoid null speed (null speed => jumping). The speed will be overrided later.
        
        next_flag = character.path.pop(0)
        
        if hasattr(next_flag, "next"): yield next_flag
        else:
          dist = 10.0
          while dist > 2.0:
            dist = character.distance_to(next_flag)
            for hunter in character.level.characters:
              if isinstance(hunter, slune_character.Competitor):
                if not(getattr(hunter, "failed", 0)) and (character.distance_to(hunter) > character.escape_dist):
                  hunter.failed = 1
                  character.escaped_from(hunter)
                  
            fx, fy, fz = character.transform_point(next_flag.x, next_flag.y, next_flag.z, next_flag.parent)
            
            if jumping:
              if character.on_ground: jumping = 0
              no_ground = 0 # It is normal that there is no ground !
            else:
              no_ground = not character.context.raypick_b(character, character.check_ground_vector, 4.0, 3)
              
            if ((dist < 12.0) and (c[5] * fy + c[6] * fz + c[7] * no_ground > 2.0)) or (character.speed.length() < 0.05):
              if character.random.random() < 0.7:
                action = slune_character.ACTION_JUMP
                jumping = 1
              else: yield slune.controler.Wall_climber(character)
            else:
              action = slune_character.ACTION_WAIT
              
            _mouse_x = min(1.0, -c[0] * math.sqrt(abs(fx / fz)))
            if fx > 0.0: _mouse_x = -_mouse_x
            mouse_x = 0.8 * mouse_x + 0.2 * _mouse_x
            mouse_y = (5.0 * mouse_y + min(max_speed, max(-max_speed, c[1] * abs(fx) + c[2] * fy + c[3] * fz + c[4] * no_ground))) / 6.0
            
            yield slune_character.Action(action, mouse_x, mouse_y)
            


class PathComputer:
  def __init__(self):
    self.pathes = {}
    
    
  def add_path(self, from_, to, path, reverse = 1):
    if self.pathes.has_key(from_):
      if self.pathes[from_].has_key(to):
        self.pathes[from_][to].append(path)
        
      else:
        self.pathes[from_][to] = [path]
        
    else:
      self.pathes[from_] = { to : [path] }
      
    if reverse:
      reverse_path = path[:]
      reverse_path.reverse()
      self.add_path(to, from_, reverse_path, 0)
      
  def random_path(self, start, end, approx_length, random = None):
    if not random: import random

    old_location = None
    location     = start
    
    path   = []
    length = 0
    while location != end:
      if length >= approx_length:
        if self.pathes[location].has_key(end):
          path.extend(random.choice(self.pathes[location][end]))
          #print "->", end
          
          break
        
      new_locations = self.pathes[location].keys()
      if (length < approx_length) and (len(new_locations) > 1):
        try: new_locations.remove(end)
        except: pass
        
      if len(new_locations) > 1:
        try: new_locations.remove(old_location)
        except: pass
        
      #print "choix parmi", new_locations
      
      old_location = location
      location     = random.choice(new_locations)
      path.extend(random.choice(self.pathes[old_location][location]))
      length += 1
      
      #print "->", location
      
    return path

  def path(self, *locations):
    path = []
    
    old_location = locations[0]
    for location in locations[1:]:
      path.extend(self.pathes[old_location][location][0])
      old_location = location
      
    return path
