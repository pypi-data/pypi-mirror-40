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

import soya, soya.widget as widget, soya.opengl as soyaopengl
import py2play.level as py2p_level, py2play.action as action, py2play.character as character
import slune.character as slune_character
import slune.controler
import slune.globdef as globdef, slune.sound as sound, slune.level as slune_level

class Medoc(soya.Volume):
  radius = 2.5
  
  def __init__(self, parent = None):
    soya.Volume.__init__(self, parent, soya.Shape.get("medoc2"))
    
  def begin_round(self):
    for character in self.parent.characters:
      if isinstance(character, slune_character.Competitor) and (character.distance_to(self) < self.radius):
        sound.play("flag-1.wav", character)
        firework = soya.Smoke(character.level, nb_particles = 10, removable = 1)
        firework.move(self)
        firework.regenerate()
        
        if hasattr(character, "nb_medoc"):
          character.nb_medoc += 1
          if character.nb_medoc >= self.nb_max:
            from py2play.idler import IDLER
            IDLER.level_completed(character, 1, _("__medoc_winner__"))
            
        else:
          character.nb_medoc = 1
          #if character.vehicle == 2:
          #  character.medoc = soya.Volume(character.internal, soya.Shape.get("medoc2"))
            
        self.parent.remove(self)
        

def add_medocs(level, nb, minimap = 1):
  down = soya.Vector(level, 0.0, -1.0, 0.0)
  
  for i in range(nb):
    m = Medoc(level)
    m.nb_max = nb
    while 1:
      m.set_xyz(level.random.uniform(5.0, 200.0), 1000.0, level.random.uniform(5.0, 200.0))
      
      r = level.raypick(m, down, -1, 3)
      if r:
        r[0].convert_to(level)
        m.y = r[0].y + 0.5
        break
      
  from py2play.idler import IDLER
  if minimap: IDLER.no_blackbands_group.insert(0, MiniMap(level))
  

class MiniMap(widget.Widget):
  def __init__(self, level):
    self.level = level
    self.point = soya.Point()
    
    self.top = 10
    self.width  = 200
    self.height = 200
    self.left = soya.root_widget.width - self.width - 40
    
    medocs = [x for x in level if isinstance(x, Medoc)]
    min_x = min_y =  10e1000
    max_x = max_y = -10e1000
    for medoc in medocs:
      if medoc.x < min_x: min_x = medoc.x
      if medoc.x > max_x: max_x = medoc.x
      if medoc.z < min_y: min_y = medoc.z
      if medoc.z > max_y: max_y = medoc.z
    f_x = self.width  / (max_x - min_x)
    f_y = self.height / (max_y - min_y)
    if f_x < f_y:
      f = f_x
      left = self.left
    else:
      f = f_y
      left = self.left + ((max_y - min_y) - (max_x - min_x)) * f
    top = self.top
    
    self.f     = f
    self.cleft = left
    self.ctop  = top
    self.min_x = min_x
    self.min_y = min_y
    
  def resize(self, parent_left, parent_top, parent_width, parent_height):
    self.left = parent_width - self.width - 40
    self.screen_width  = parent_width
    self.screen_height = parent_height
    
  def render(self):
    soyaopengl.glColor4f(1.0, 1.0, 1.0, 1.0)
    soyaopengl.glBegin(soyaopengl.GL_QUADS)
    for medoc in [x for x in self.level if isinstance(x, Medoc)]:
      x = self.cleft + self.f * (medoc.x - self.min_x)
      y = self.ctop  + self.f * (medoc.z - self.min_y)
      soyaopengl.glVertex2f(x - 4.0, y - 4.0)
      soyaopengl.glVertex2f(x - 4.0, y + 4.0)
      soyaopengl.glVertex2f(x + 4.0, y + 4.0)
      soyaopengl.glVertex2f(x + 4.0, y - 4.0)
      
    soyaopengl.glEnd()
    
    for character in self.level.characters:
      if isinstance(character, slune_character.Competitor):
        x  = self.cleft + self.f * (character.x - self.min_x)
        y  = self.ctop  + self.f * (character.z - self.min_y)
        
        self.point.__init__(character, 0.0, 0.0, -25.0)
        self.point.convert_to(self.level)
        x2 = self.cleft + self.f * (self.point.x - self.min_x)
        y2 = self.ctop  + self.f * (self.point.z - self.min_y)
        
        soya.DEFAULT_MATERIAL.activate()
        soyaopengl.glBegin(soyaopengl.GL_LINES)
        soyaopengl.glVertex2f(x , y )
        soyaopengl.glVertex2f(x2, y2)
        soyaopengl.glEnd()
        
        material = soya.Material.get("head_" + character.perso_name + "_1")
        material.activate()
        soyaopengl.glEnable(soyaopengl.GL_BLEND)
        soyaopengl.glBegin(soyaopengl.GL_QUADS)
        soyaopengl.glTexCoord2f(0.0, 0.0); soyaopengl.glVertex2f(x - 20.0, y - 20.0)
        soyaopengl.glTexCoord2f(0.0, 1.0); soyaopengl.glVertex2f(x - 20.0, y + 20.0)
        soyaopengl.glTexCoord2f(1.0, 1.0); soyaopengl.glVertex2f(x + 20.0, y + 20.0)
        soyaopengl.glTexCoord2f(1.0, 0.0); soyaopengl.glVertex2f(x + 20.0, y - 20.0)
        soyaopengl.glEnd()
        soyaopengl.glDisable(soyaopengl.GL_BLEND)
        soya.DEFAULT_MATERIAL.activate()



class MedocWaiter(soya.Volume):
  def __init__(self, parent, x, y, z):
    soya.Volume.__init__(self, parent, soya.Shape.get("girafe1"))
    self.set_xyz(x, y, z)
    self.medoc_received = 0
    
  def begin_round(self):
    if not self.medoc_received:
      from py2play.player import CURRENT_PLAYER
      
      if CURRENT_PLAYER.character.distance_to(self) < 10.0:
        self.medoc_received = 1
        sound.play("flag-1.wav", self)
        GiveMedoc(self.parent, CURRENT_PLAYER.character, self)
        
        
class GiveMedoc(soya.Volume):
  def __init__(self, parent, character, receiver):
    soya.Volume.__init__(self, parent, soya.Shape.get("medoc2"))
    self.move   (soya.Point (character, 0.0, 0.5,  0.3))
    self.look_at(soya.Vector(character, 0.0, 0.0, -1.0))
    self.receiver = receiver
    
  def begin_round(self):
    if self.distance_to(self.receiver) < 1.0:
      for e in self.parent:
        if isinstance(e, MedocWaiter) and (e.medoc_received == 0): break
      else:
        import slune.videosequence as videosequence
        videosequence.Mission14Outro().start(
          tux   = videosequence.PLAYER,
          gnu   = videosequence.add_perso("gnu"  , 1),
          shark = videosequence.add_perso("shark", 4),
          )
        
      self.parent.remove(self)
      
      
    
  def advance_time(self, proportion):
    if self.parent:
      v = self >> self.receiver
      v.set_length(0.2 * proportion)
      self += v
      
      
class MedocWaiterMiniMap(widget.Widget):
  def __init__(self, level):
    self.level = level
    self.point = soya.Point()
    
    self.top = 10
    self.width  = 200
    self.height = 200
    self.left = soya.root_widget.width - self.width - 40
    
    flags = [e for e in level.children if isinstance(e, MedocWaiter)]
    min_x = min_y =  10e1000
    max_x = max_y = -10e1000
    for flag in flags:
      if flag.x < min_x: min_x = flag.x
      if flag.x > max_x: max_x = flag.x
      if flag.z < min_y: min_y = flag.z
      if flag.z > max_y: max_y = flag.z
    f_x = self.width  / (max_x - min_x)
    f_y = self.height / (max_y - min_y)
    if f_x < f_y:
      f = f_x
      left = self.left
    else:
      f = f_y
      left = self.left + ((max_y - min_y) - (max_x - min_x)) * f
    top = self.top
    
    self.f     = f
    self.cleft = left
    self.ctop  = top
    self.min_x = min_x
    self.min_y = min_y
    
    self.flags_pos = []
    self._calllist = soyaopengl.glGenList()
    soyaopengl.glNewList(self._calllist)
    soyaopengl.glColor4f(1.0, 1.0, 1.0, 1.0)
    soyaopengl.glBegin(soyaopengl.GL_QUADS)
    for flag in flags:
      x = left + f * (flag.x - min_x)
      y = top  + f * (flag.z - min_y)
      soyaopengl.glVertex2f(x - 4.0, y - 4.0)
      soyaopengl.glVertex2f(x - 4.0, y + 4.0)
      soyaopengl.glVertex2f(x + 4.0, y + 4.0)
      soyaopengl.glVertex2f(x + 4.0, y - 4.0)
    soyaopengl.glEnd()
    
    soyaopengl.glEndList()
    
  def resize(self, parent_left, parent_top, parent_width, parent_height):
    self.left = parent_width - self.width - 40
    self.screen_width  = parent_width
    self.screen_height = parent_height
    
  def render(self):
    soyaopengl.glCallList(self._calllist)
    
    for character in self.level.characters:
      if isinstance(character, slune_character.Competitor):
        x = self.cleft + self.f * (character.x - self.min_x)
        y = self.ctop  + self.f * (character.z - self.min_y)
        
        self.point.__init__(character, 0.0, 0.0, -25.0)
        self.point.convert_to(self.level)
        x2 = self.cleft + self.f * (self.point.x - self.min_x)
        y2 = self.ctop  + self.f * (self.point.z - self.min_y)
        
        soya.DEFAULT_MATERIAL.activate()
        soyaopengl.glBegin(soyaopengl.GL_LINES)
        soyaopengl.glVertex2f(x , y )
        soyaopengl.glVertex2f(x2, y2)
        soyaopengl.glEnd()
        
        material = soya.Material.get("head_" + character.perso_name + "_1")
        material.activate()
        soyaopengl.glEnable(soyaopengl.GL_BLEND)
        soyaopengl.glBegin(soyaopengl.GL_QUADS)
        soyaopengl.glTexCoord2f(0.0, 0.0); soyaopengl.glVertex2f(x - 20.0, y - 20.0)
        soyaopengl.glTexCoord2f(0.0, 1.0); soyaopengl.glVertex2f(x - 20.0, y + 20.0)
        soyaopengl.glTexCoord2f(1.0, 1.0); soyaopengl.glVertex2f(x + 20.0, y + 20.0)
        soyaopengl.glTexCoord2f(1.0, 0.0); soyaopengl.glVertex2f(x + 20.0, y - 20.0)
        soyaopengl.glEnd()
        soyaopengl.glDisable(soyaopengl.GL_BLEND)
        soya.DEFAULT_MATERIAL.activate()
  
        
