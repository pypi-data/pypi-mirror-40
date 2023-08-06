# Slune
# Copyright (C) 2004 Jean-Baptiste LAMY
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

import random

import soya

import slune.character as slune_character, slune.sound as sound

class AirplaneParticles(soya.Particles):
  def __init__(self, parent = None, material = None, nb_particles = 30):
    soya.Particles.__init__(self, parent, material, nb_particles)
    self.auto_generate_particle = 1
    self.set_colors((1.0, 1.0, 1.0, 1.0), (1.0, 1.0, 0.0, 1.0), (1.0, 0.0, 0.0, 1.0), (0.1, 0.0, 0.0, 1.0))
    self.set_sizes((1.0, 1.0))
    self.max_particles_per_round = 1
    
  def generate(self, index):
    self.set_particle(index, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
  

class Airplane(soya.World):
  def __init__(self, parent):
    soya.World.__init__(self, parent)
    self.shape          = soya.Shape.get("avion")
    self.characters_on  = ()
    self.speed          = soya.Vector(self)
    self.accelerate     = 0
    self.roof           = soya.Point(self, 0.0, 7.9, 0.0)
    self.start_in_round = 0
    self.particles      = ()
    
  def start(self):
    self.accelerate = 1
    self.create_particles()
    
  def create_particles(self):
    if not self.particles:
      self.particles = [AirplaneParticles(self), AirplaneParticles(self)]
      self.particles[0].set_xyz( 1.0, 3.5, 9.6)
      self.particles[1].set_xyz(-1.0, 3.5, 9.6)
      
  def advance_time(self, proportion):
    soya.World.advance_time(self, proportion)
    self.add_mul_vector(proportion, self.speed)
    for character in self.characters_on: character.add_mul_vector(proportion, self.speed)
      
  def begin_round(self):
    soya.World.begin_round(self)
    
    if self.accelerate:
      if self.speed.z > -2.0:
        self.speed.z -= 0.003
        if self.speed.z < -1.0: self.turn_vertical(0.05)
        
    self.characters_on = [
      character
      for character in self.parent.characters
      if character.on_ground and (abs(character.y - self.y - self.roof.y) < 2.0) and (character.distance_to(self.roof) < 11.0)
      ]

    for character in self.characters_on: character.platform_speed = self.speed

    if self.speed.z == 0.0:
      if   self.characters_on: self.start()
      elif self.start_in_round:
        self.start_in_round -= 1
        if self.start_in_round == 0: self.start()


class FlyingAirplane(Airplane):
  def __init__(self, parent):
    Airplane.__init__(self, parent)
    self.speed.z = -0.5
    self.create_particles()
    
    
class KillerAirplane(soya.World):
  def __init__(self, parent, target, speed = 0.4):
    soya.World.__init__(self, parent)
    self.volume = soya.Volume(self, soya.Shape.get("avion"))
    self.volume.scale(0.5, 0.5, 0.5)
    self.target = target
    self.phase  = 1
    self.v      = soya.Vector()
    self.p      = soya.Point(self.target, 0.0, 0.0, -4.0)
    self.speed  = speed
    self.solid  = 1
    self.play   = 0
    
  def begin_round(self):
    soya.World.begin_round(self)

    if self.play == 0: return
    
    if   self.phase == 1:
      self.p.convert_to(self.parent)
      
      if (abs(self.x - self.p.x) + abs(self.z - self.p.z)) < 2.0:
        r = self.parent.raypick(self, soya.Vector(self, 0.0, -1.0, 0.0))
        if r: 
          self.drop_y = max(r[0].y, 0.0)
          print self.drop_y
          self.phase = 2
          
          from py2play.idler import IDLER
          
          self.traveling = soya.FixTraveling(None, soya.Vector(IDLER.camera, 0.0, 0.0, -1.0))
          #self.traveling = soya.ThirdPersonTraveling(self)
          #self.traveling.distance = 400.0
          IDLER.camera.add_traveling(self.traveling)
          
      self.p.__init__(self.target, 0.0, 0.0, -4.0)
      
      #from py2play.idler  import IDLER
      #if hasattr(IDLER.camera.traveling, "distance") and (IDLER.camera.traveling.distance > 5.0): IDLER.camera.traveling.distance -= 1.0
      
    elif self.phase == 2:
      if self.y < self.drop_y:
        self.phase = 3

        from py2play.idler  import IDLER
        IDLER.camera.remove_traveling(self.traveling)
        
        for character in self.parent.characters:
          if self.distance_to(character) < 3.0:
            character.die()
            break
        else:
          sound.play("explose-3.wav", self)
          
          explode = slune_character.Explosion(self.parent)
          explode.move(self)
          explode.life = 30
          
      #from py2play.idler  import IDLER
      #if hasattr(IDLER.camera.traveling, "distance") and (IDLER.camera.traveling.distance < 20.0): IDLER.camera.traveling.distance += 1.0
      
      
    elif self.phase == 3:
      if self.y > self.drop_y + 10.0:
        self.phase = 1
        
        
      #from py2play.idler  import IDLER
      #if hasattr(IDLER.camera.traveling, "distance") and (IDLER.camera.traveling.distance > 5.0): IDLER.camera.traveling.distance -= 1.0
      
  def advance_time(self, proportion):
    soya.World.advance_time(self, proportion)
    
    if self.play == 0: return
    
    if   self.phase == 1:
      self.v.set_start_end(self, self.p)
      self.v.y = 0
      self.v.set_length(self.speed * proportion)
      self.look_at(self.v)
      self += self.v
      
    elif self.phase == 2:
      self.y -= self.speed * proportion
      
    elif self.phase == 3:
      self.y += self.speed * proportion
      
