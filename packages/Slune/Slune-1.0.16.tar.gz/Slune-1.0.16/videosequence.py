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
from slune.controler import *

import soya, soya.opengl as soyaopengl, soya.widget as widget
import math, random

import slune.character as slune_character, slune.level as slune_level, slune.sound as sound

AUTO   = 0
PLAYER = 1

class VideoSequence:
  def __call__(self): yield Action()
  
  def start(self, **kargs):
    """Do not override this method ! Please override _start instead."""
    # It's more clean to start the video sequence BETWEEN 2 rounds.
    from py2play.idler  import IDLER
    IDLER.next_round_tasks.append(lambda : self._start(**kargs))
    
  def _start(self, **kargs):
    from py2play.idler  import IDLER
    from py2play.player import CURRENT_PLAYER
    
    for name, character in kargs.items():
      if   character == PLAYER:
        for character in CURRENT_PLAYER.level.characters:
          if character.played:
            character.controler.animate(self(tux = character))
            
      elif character == AUTO:
        for character in CURRENT_PLAYER.level.characters:
          if getattr(character, "name", "") == name:
            character.controler.animate(self(**{name : character}))
      elif character:
        if isinstance(character, tuple):
          character = character[0]
        character.controler.animate(self(**{name : character}))
        
def add_perso(name, vehicle = 1, clazz = NonPlayerCharacter, level = None, **kargs):
  if not level:
    from py2play.player import CURRENT_PLAYER
    level = CURRENT_PLAYER.level
    
  perso = clazz(**kargs)
  perso.name = name
  perso.set_perso(name)
  perso.set_vehicle(vehicle)
  perso.set_level(level)
  perso.light = PlayerLight(perso)
  return perso

def LookAtFrontOfCharacterTraveling(character, distance = 1.0):
  #target = character.camera_target.position()
  target = character.perso.position()
  target.y = target.y + 0.3
  traveling = soya.FixTraveling(target + Vector(character.perso, 0.0 * distance, 0.4 * distance, -1.2 * distance), target, 1, 1)
  return traveling
def LookAtBackOfCharacterTraveling(character, distance = 1.0):
  #target = character.camera_target.position()
  target = character.perso.position()
  target.y = target.y + 0.3
  traveling = soya.FixTraveling(target + Vector(character.perso, 0.0 * distance, 0.4 * distance, 1.2 * distance), target, 1, 1)
  return traveling
def LookAtLeftOfCharacterTraveling(character, distance = 1.0):
  #target = character.camera_target.position()
  target = character.perso.position()
  target.y = target.y + 0.3
  traveling = soya.FixTraveling(target + Vector(character.perso, 1.0 * distance, 0.4 * distance, -0.5 * distance), target, 1, 1)
  return traveling
def LookAtRightOfCharacterTraveling(character, distance = 1.0):
  #target = character.camera_target.position()
  target = character.perso.position()
  target.y = target.y + 0.3
  traveling = soya.FixTraveling(target + Vector(character.perso, -1.0 * distance, 0.4 * distance, -0.5 * distance), target, 1, 1)
  return traveling
  
def SayNo(character, duration):
  total_angle = 0.0
  for i in range(duration):
    angle = 25.0 * math.cos(i * 0.4)
    total_angle -= angle
    character.perso.rotate_lateral(angle)
    yield Action()
  character.perso.rotate_lateral(total_angle)
  
def SayYes(character, duration):
  total_angle = 0.0
  for i in range(duration):
    angle = 5.0 * math.cos(i * 0.3)
    total_angle -= angle
    character.perso.rotate_vertical(angle)
    yield Action()
  character.perso.rotate_vertical(total_angle)
  
def Hesitate(character, duration):
  total_angle = 0.0
  for i in range(duration):
    angle = 1.0 * math.cos(i * 0.1)
    total_angle -= angle
    character.perso.rotate_incline(angle)
    yield Action()
  character.perso.rotate_incline(total_angle)
  
class Fader(widget.Widget):
  def __init__(self):
    self.level = 0.0
    self._parent      = None
    
  def widget_begin_round(self):
    if self.level >= 2.0:
      self.master.remove(self)
      self.level = 0.0 # Re-useable
      
  def widget_advance_time(self, proportion):
    self.level += 0.05 * proportion
    
  def resize(self, parent_left, parent_top, parent_width, parent_height):
    self.parent_left   = float(parent_left)
    self.parent_top    = float(parent_top)
    self.parent_width  = float(parent_width)
    self.parent_height = float(parent_height)
    
  def render(self):
    if self.level <= 1.0:
      soyaopengl.glColor4f(0.0, 0.0, 0.0, self.level)
    else:
      soyaopengl.glColor4f(0.0, 0.0, 0.0, 2.0 - self.level)
    soyaopengl.glEnable(soyaopengl.GL_BLEND)
    soyaopengl.glBegin(soyaopengl.GL_QUADS)
    
    soyaopengl.glVertex2f(self.parent_left, self.parent_top)
    soyaopengl.glVertex2f(self.parent_left, self.parent_top + self.parent_height)
    soyaopengl.glVertex2f(self.parent_left + self.parent_width, self.parent_top + self.parent_height)
    soyaopengl.glVertex2f(self.parent_left + self.parent_width, self.parent_top)
    
    soyaopengl.glEnd()
    soyaopengl.glDisable(soyaopengl.GL_BLEND)
    
  def start(self, character = None):
    if not self in soya.root_widget.children: soya.root_widget.add(self)
    
    for i in range(20): yield Action()
    
Fade = Fader().start

def Pause(max_duration = -1):
  from py2play.idler import IDLER
  
  IDLER.pause(max_duration)
  yield Action()

class ExorbitedEye(soya.Volume):
  def __init__(self, parent = None, shape_name = ""):
    soya.Volume.__init__(self, parent, soya.Shape.get(shape_name))
    self.angle        = 0.0
    self.auto_destroy = 0
    
  def advance_time(self, proportion):
    self.angle += proportion / 10.0
    self.scale_x = self.scale_y = self.scale_z = abs(math.sin(self.angle)) / 10.0
    if self.auto_destroy and (self.scale_x < 0.01):
      from py2play.idler import IDLER
      IDLER.next_round_tasks.append(lambda : self.parent and self.parent.remove(self))
      
  def destroy(self):
    self.auto_destroy = 1
    
    
class MissionCompleted(VideoSequence):
  def __init__(self, winner = 0, message = None):
    self.winner  = winner
    self.message = message
    
  def __call__(self, tux):
    if tux.played and tux.player.active:
      from py2play.idler  import IDLER
      from py2play.player import CURRENT_PLAYER
      
      if self.message:
        IDLER.message(self.message)
        
      else:
        if self.winner:
          if CURRENT_PLAYER.level.name.startswith("level-mission"):
            IDLER.message(_("Level completed!"))
          else:
            IDLER.message(_("You have won!"))
        else:
          IDLER.message(_("__gameover__"))
          
      yield Pause()
      
      from py2play.player import CURRENT_PLAYER
      from py2play.idler  import IDLER
      if self.winner and CURRENT_PLAYER.level.name.startswith("level-mission"):
        IDLER.end_game("mission-" + str(int(CURRENT_PLAYER.level.name[14:]) + 1))
      else: IDLER.end_game()
      
      
class HuntFailed(VideoSequence):
  def __init__(self, message = None):
    self.message = message
    
  def __call__(self, praise = None, hunter = None):
    if hunter and hunter.played and hunter.player.active:
      from py2play.idler  import IDLER
      from py2play.player import CURRENT_PLAYER
      
      IDLER.message(self.message or _("__hunt_failed__"))
      IDLER.message(_("__gameover__"))
      
      yield Pause()
      
      from py2play.player import CURRENT_PLAYER
      from py2play.idler  import IDLER
      
      IDLER.end_game()
      
      
class GnuSpeech(VideoSequence):
  def __init__(self, messages, end_game_after = 1):
    self.messages       = messages
    self.end_game_after = end_game_after
    
  def __call__(self, tux = None, **other):
    from py2play.idler  import IDLER

    if tux:
      t = soya.FixTraveling(IDLER.camera, Vector(IDLER.camera, 0.0, 0.0, -1.0), 0, 0)
      IDLER.camera.add_traveling(t)
      IDLER.camera.zap()
      
      gnu = soya.Volume(tux.level, soya.Shape.get("gnu1"))
      gnu.move   (Point (IDLER.camera, -0.25, -0.5, -0.5))
      gnu.look_at(Vector(IDLER.camera, 1.0, 0.0, 0.5))
      
    for message in self.messages:
      if tux: IDLER.clear_message(); IDLER.message(message)
      
      yield Pause()
      
    if tux and self.end_game_after: IDLER.end_game()
    
class ChangeVehicle(VideoSequence):
  def __init__(self, character, vehicle):
    self.vehicle = vehicle
    
  def __call__(self, character = None):
    import copy
    from py2play.idler  import IDLER
    
    perso = soya.Volume(character.parent, character.perso.shape)
    perso.move(character.perso)
    perso.look_at(Vector(character, 0.0, 0.0, -1.0))
    character.perso.visible = 0
    
    t = soya.ThirdPersonTraveling(perso)
    IDLER.camera.add_traveling(t)
    
    v = perso >> Point(self.vehicle, *VEHICLE_PERSO_COORDS[self.vehicle.vehicle])
    v /= 30.0
    
    mouse_x = character.current_action.mouse_x
    mouse_y = character.current_action.mouse_y #((character.speed.z / character.maxspeedz) + 0.2) / 0.2
    
    for i in range(30):
      perso += v
      perso.y += -(i - 15) / 100.0
      mouse_y *= 0.9
      yield Action(ACTION_WAIT, mouse_x, mouse_y)
      
    self.vehicle.matrix, character.matrix = character.matrix, self.vehicle.matrix
    vehi = character.vehicle
    character.set_vehicle(self.vehicle.vehicle)
    self.vehicle.set_vehicle(vehi)
    
    perso.parent.remove(perso)
    character.perso.visible = 1
    IDLER.camera.remove_traveling(t)
    
    self.vehicle.disable(character)
    
class Mission1Intro(VideoSequence):
  def __call__(self, tux = None, gnu = None):
    from py2play.idler  import IDLER
    
    IDLER.camera.speed = 0.1
    
    if   tux:
      IDLER.clear_message(); IDLER.message(_("__scenar1-intro-0__"))
    elif gnu:
      gnu.teleport(85.4329071045, -5.0, -16.2530593872)
      gnu.look_at(Vector(gnu.level, 1.0, 0.0, 0.0))
      
    yield Pause()
    
    if   gnu:
      sound.play("phone.ogg")
      IDLER.clear_message(); IDLER.message(_("__scenar1-intro-1__"))
      
    elif tux:
      if tux.player.active:
        t = LookAtLeftOfCharacterTraveling(tux); IDLER.camera.add_traveling(t)
        
    if 0 and tux:
      r = Remorque(None, tux)
      r.set_level(tux.level)
      r.set_xyz(tux.x, tux.y, tux.z + 2.5)
      r2 = Remorque(None, r)
      r2.set_level(tux.level)
      r2.set_xyz(r.x, r.y, r.z + 2.5)
      r3 = Remorque(None, r2)
      r3.set_level(tux.level)
      r3.set_xyz(r2.x, r2.y, r2.z + 2.5)
      
    yield Pause(85); yield Fade()
    
    if   gnu:
      old_xyz = gnu.perso.x, gnu.perso.y, gnu.perso.z
      gnu.perso.z = -1.4
      gnu.perso.x = -0.4
      gnu.perso.y = 0.3
      t = LookAtRightOfCharacterTraveling(gnu, 2.0); IDLER.camera.add_traveling(t)
      IDLER.camera.zap()
      IDLER.clear_message(); IDLER.message(_("__scenar1-intro-2__"), 100.0)
      
    elif tux:
      if tux.player.active: IDLER.camera.remove_traveling(t)
      
    yield Pause(); yield Fade()
    
    if   gnu:
      IDLER.camera.remove_traveling(t)
      
      for i in range(70): yield Action()
      
    elif tux:
      if tux.player.active:
        IDLER.camera.add_traveling(t)
        IDLER.camera.zap()
        
      if tux.player.active: IDLER.clear_message(); IDLER.message(_("__scenar1-intro-3__"), 100.0)
      
      yield SayYes(tux, 50)
      for j in range(8): yield Action(ACTION_ROTUP)
      for j in range(12): yield Action()
        
    yield Pause(); yield Fade()
    
    if   gnu:
      IDLER.camera.add_traveling(t)
      IDLER.camera.zap()
      IDLER.clear_message(); IDLER.message(_("__scenar1-intro-4__"), 100.0)
      
    elif tux:
      if tux.player.active: IDLER.camera.remove_traveling(t)

    yield Pause(1000); yield Fade()
      
    if gnu: # Do this once
      IDLER.camera.remove_traveling(t)
      IDLER.camera.zap()
      
      gnu.perso.set_xyz(*old_xyz)
      
      IDLER.camera.speed = 0.3
      IDLER.clear_message()
      
      sound.play_music(gnu.level.preloaded_music_name) # Default music
      
      
class Mission1Outro(VideoSequence):
  def __call__(self, tux = None, gnu = None):
    from py2play.idler  import IDLER
    
    IDLER.camera.speed = 0.2
    
    self.tux_arrived = 0
    
    if   gnu:
      IDLER.clear_message(); IDLER.message(_("__scenar1-outro-1__"), 100.0)
      gnu.teleport(85.4329071045, -5.0, -16.2530593872)
      gnu.look_at(Vector(gnu.level, 1.0, 0.0, 0.0))
      
    elif tux:
      #tux.teleport(84.5, -5.325, -25.5)
      #tux.look_at(Vector(tux.level, 0.0, 0.0, 1.0))
      pass
    
    yield Pause()
    yield Fade()
    
    if   gnu:
      shark = soya.Volume(gnu.level, soya.Shape.get("shark1"))
      shark.set_xyz(78.6, -3.8, -8.04504203796)
      shark.rotate_incline(50.0)
      
      #t_shark = soya.FixTraveling(shark + Vector(shark.parent, -1.0, 0.2, -2.0), shark, 1, 1)
      t_shark = soya.FixTraveling(shark + Vector(shark.parent, -0.5, 0.1, -1.0), shark, 1, 1)
      IDLER.camera.add_traveling(t_shark)
      IDLER.camera.zap()
      
      IDLER.clear_message(); IDLER.message(_("__scenar1-outro-2__"), 100.0)
      
    elif tux: pass
    
    yield Pause()
    yield Fade()
    
    if   tux:
      rank = tux.rank % 2 # There is only space for 2 truck at the same time -- don't try to load 3 or more truck simultaneously, at least until you're waiting for some fight...
      yield LookAt(tux, Point(tux.level, 83.7683410645, -5.65 , -23.7621879578))
      yield Goto  (tux, Point(tux.level, 83.7683410645, -5.65 , -23.7621879578), 2.0)
      #yield Runto (tux, Point(tux.level, 77.706993103 , -5.65 , -18.1882820129 + 2.1 * rank), 2.0)
      #yield Runto (tux, Point(tux.level, 68.4753341675, -5.65 , -15.0001955032 + 2.1 * rank), 2.0)
      yield Runto (tux, Point(tux.level, 61.7737007141, -5.925, -4.8 + 2.1 * rank), 2.0)
      yield LookAt(tux, Vector(tux.level, -1.0, 0.0, 0.0))
      
      if tux.player.active:
        t = soya.FixTraveling(Point(tux.level, 63.5751266479, 0.286143124104, -0.177742660046), Point(tux, 0.0, 0.35, 0.0), 1, 1)
        t = soya.FixTraveling(Point(tux.level, 64.5751266479, 0.286143124104, -1.177742660046), Point(tux.level, 66.2650909424, -0.830011188984, -3.27568721771), 1, 1)
        IDLER.camera.add_traveling(t)
      
      for i in range(100): yield Action(ACTION_WAIT, 0.0, 2.5)
      
      if tux.player.active:
        
        self.tux_arrived = 1
        self.tux = tux
      
    elif gnu:
      IDLER.camera.remove_traveling(t_shark)
      shark.visible = 0
      
      while not self.tux_arrived: yield Action()
      
    for i in range(20): yield Action()
    
    yield Fade()
    
    if tux and tux.player.active:
      IDLER.camera.remove_traveling(t)
      t = soya.FixTraveling(Point(tux, 0.0, 0.7, 1.45), Point(tux, 0.0, 0.45, 0.0), 1, 1)
      IDLER.camera.add_traveling(t)
      IDLER.camera.zap()
      
    for i in range(20): yield Action()
    
    if gnu:
      TUX = self.tux
      class Medoc(soya.Volume):
        def __init__(self, parent):
          soya.Volume.__init__(self, parent, soya.Shape.get("medoc"))
          
        def advance_time(self, proportion):
          if self.y > TUX.y + 0.45:
            self.add_vector(Vector(TUX, 0.0, -0.01 * proportion, -0.01 * proportion))
            
      for i in range(3):
        m = Medoc(gnu.level)
        m.move(Point(self.tux, 0.2 * (i - 1), 0.8 + 0.2 * i, 1.2))
        m.rotate_lateral(15.0 * i - 10.0)
        
        
    for i in range(50): yield Action()
    
    if   tux:
      for i in range(30): yield Action()
      
    elif gnu:
      gnu.perso.rotate_lateral(130.0)
      gnu.perso.move(Point(self.tux, -1.0, 0.08, 1.0))
      v = Vector(self.tux, 0.02, 0.0, 0.0)
      for i in range(30):
        gnu.perso.add_vector(v)
        yield Action()
        
      IDLER.clear_message(); IDLER.message(_("__scenar1-outro-3__"), 100.0)
      
      e1 = ExorbitedEye(gnu.level, "gnu-eye")
      e1.move(Point(gnu.perso, -0.02214474081995, 0.43756651878349995, -0.1125))
      e1.rotate_lateral( 20.0)
      e2 = ExorbitedEye(gnu.level, "gnu-eye")
      e2.move(Point(gnu.perso,  0.02214474081995, 0.43756651878349995, -0.1125))
      e2.rotate_lateral(-20.0)
      
    yield Pause()
    
    if   tux:
      for i in range(35): yield Action()
      
    elif gnu:
      e1.destroy()
      e2.destroy()
      
      shark.visible = 1
      shark.rotate_incline(-50.0)
      shark.rotate_lateral(-130.0)
      shark.move(Point(self.tux, 1.0, 0.14, 1.0))
      v = Vector(self.tux, -0.02, 0.0, 0.0)
      for i in range(35):
        shark.add_vector(v)
        yield Action()
        
      IDLER.clear_message(); IDLER.message(_("__scenar1-outro-4__"), 100.0)
      
    yield Pause()
    
    if   tux:
      if tux.player.active:
        IDLER.clear_message(); IDLER.message(_("__scenar1-outro-5__"), 100.0)
        
        IDLER.camera.remove_traveling(t)
        t = soya.FixTraveling(tux.perso + Vector(tux.perso, -1.0, 0.0, -0.5), tux.perso, 1, 1)
        IDLER.camera.add_traveling(t)
        
    yield Pause()
    
    if tux: # Do this once
      if tux.player.active:
        IDLER.camera.speed = 0.3
        IDLER.level_completed(tux, 1)
        
        yield Action()
        yield Action()
        yield Action()



class Mission2Intro(VideoSequence):
  def __call__(self, tux = None, gnu = None, shark = None):
    from py2play.idler  import IDLER
    
    IDLER.camera.speed = 0.1
    
    if   gnu:
      gnu.teleport(85.4329071045, -5.25 + 0.3, -16.2530593872)
      gnu.look_at(Vector(gnu.level, 1.0, 0.0, 0.0))
      
      light = soya.Light(gnu.level)
      light.set_xyz(75.5, -3.5, -7.0)
      light.cast_shadow = 0
      
      gnu.perso.visible = 0
      gnu_perso = soya.Volume(gnu.level, gnu.perso.shape)
      gnu_perso.set_xyz(75.0, -4.35, -8.4)
      gnu_perso.rotate_lateral(-90.0)
      t = soya.FixTraveling(Point(gnu.level, 75.5, -3.35, -6.4), Point(gnu_perso, 0.0, 1.0, 0.0), 1, 1)
      
    elif shark:
      IDLER.clear_message(); IDLER.message(_("__scenar2-intro-1__"), 100.0)
      shark.teleport(69.4181060791, -5.625 + 0.3, -15.2002220154)
      shark.look_at(Vector(shark.level, -0.3, 0.0, 0.6))
      
      shark.perso.visible = 0
      shark_perso = soya.Volume(shark.level, shark.perso.shape)
      shark_perso.set_xyz(76.0, -4.3, -8.4)
      shark_perso.rotate_lateral(90.0)
      
      t  = soya.FixTraveling(Point(shark.level, 75.5, -3.35, -6.4), Point(shark_perso, 0.0, 0.95, 0.0), 1, 1)
      t2 = soya.FixTraveling(Point(shark.level, 75.5, -3.35, -6.4), t.direction % shark.level, 1, 1)
      IDLER.camera.add_traveling(t)
      
      self.shark_arrived = 0
      
      def print_message():
        if 0: yield 1 # Needed to get an (empty) generator
        IDLER.message(_("__scenar2-1__"))
        
        
      start = [
        Point(shark.level, 50.3923454285, -5.625, 8.96249961853),
        Point(shark.level, 40.7581253052, -5.625, 13.6631250381),
        Point(shark.level, 32.8351249695, -6.375, 10.6235160828), #28.5151557922, -6.375, 14.3637504578),
        print_message()
      ]
      
      ga = [
        Point(shark.level, 22.4124565125, -6.38087177277, 4.67110776901),
        Point(shark.level, 21.2822265625, -6.375, 4.576171875),
        Point(shark.level, 7.29548740387, -0.638323783875, 4.44479942322),
        Point(shark.level, -4.91449213028, -0.375, 4.22445392609),
        Point(shark.level, -3.81179690361, -1.125, -26.1578102112),
        ]
      
      gd = [
        Point(shark.level, 22.4124565125, -6.38087177277, 4.67110776901),
        Point(shark.level, 25.8687057495, -6.75, -35.6249084473),
        Point(shark.level, 36.8348083496, -6.75, -56.1541824341),
        Point(shark.level, 36.7147674561, -6.37904405594, -74.4520797729),
        ]
      
      af = [
        Point(shark.level, -3.81179690361, -1.125, -26.1578102112),
        Point(shark.level, 6.46447372437, 0.0, -19.9380531311),
        Point(shark.level, 9.95081996918, 0.0, -8.88684940338),
        Point(shark.level, 16.5414352417, 0.0, -7.946393013),
        Point(shark.level, 26.5414352417, 0.0, -7.946393013),
        ]
      
      fb = [
        Point(shark.level, 26.5414352417, 0.0, -7.946393013),
        Point(shark.level, 35.0200386047, 0.0, -7.946393013),
        Point(shark.level, 44.4480857849, 0.0, -18.4586982727),
        Point(shark.level, 55.1251296997, -5.25, -18.3392944336),
        ]
      
      fd = [
        Point(shark.level, 26.5414352417, 0.0, -7.946393013),
        Point(shark.level, 36.7147674561, -6.37904405594, -74.4520797729),
        ]
      
      ad = [
        Point(shark.level, -3.81179690361, -1.125, -26.1578102112),
        Point(shark.level, -13.2186756134, -1.125, -37.5811576843),
        Point(shark.level, -18.7928314209, -1.125, -48.8303947449),
        Point(shark.level, -2.38635921478, -1.5, -49.7544670105),
        Point(shark.level, 3.55569171906, -2.52949953079, -43.9239654541),
        Point(shark.level, 12.7745409012, -4.66128826141, -41.5636520386),
        Point(shark.level, 14.374162674, -5.8355588913, -34.8440742493),
        Point(shark.level, 24.2375221252, -6.75, -33.8340492249),
        Point(shark.level, 37.3864936829, -6.75, -53.8386001587),
        Point(shark.level, 36.7147674561, -6.37904405594, -74.4520797729),
        ]
      
      ae = [
        Point(shark.level, -3.81179690361, -1.125, -26.1578102112),
        Point(shark.level, -13.2186756134, -1.125, -37.5811576843),
        Point(shark.level, -18.7928314209, -1.125, -48.8303947449),
        Point(shark.level, -20.2157287598, -1.125, -58.9511184692),
        Point(shark.level, -20.3266277313, -4.84918022156, -83.0176239014),
        Point(shark.level, -33.139339447, -4.875, -85.9998779297),
        Point(shark.level, -40.6741409302, -4.875, -93.6274795532),
        Point(shark.level, -41.3330497742, -4.88650131226, -109.911811829),
        Point(shark.level, -19.4819507599, -4.875, -112.883102417),
        ]
      
      bc = [
        Point(shark.level, 55.1251296997, -5.25, -18.3392944336),
        Point(shark.level, 61.5, -1.6, -42.9324378967),
        Point(shark.level, 62.3, -1.6, -42.9324378967),
        Point(shark.level, 63.1, -1.6, -42.9324378967),
        Point(shark.level, 62.5395393372, -4.73901462555, -29.3159122467),
        Point(shark.level, 71.4511871338, -6.375, -29.7449493408),
        Point(shark.level, 71.5570297241, -6.375, -47.8265609741),
        Point(shark.level, 68.75, -6.75, -53.25),
        Point(shark.level, 83.6261444092, -6.75, -61.8628501892),
        Point(shark.level, 84.954574585, -6.75, -77.4120330811),
        ]
      
      bd = [
        Point(shark.level, 55.1251296997, -5.25, -18.3392944336),
        Point(shark.level, 61.7998275757, -6.75, -51.3839759827),
        Point(shark.level, 37.3864936829, -6.75, -53.8386001587),
        Point(shark.level, 36.7147674561, -6.37904405594, -74.4520797729),
        ]
      
      cd1 = [
        Point(shark.level, 84.954574585, -6.75, -77.4120330811),
        Point(shark.level, 74.9383087158, -6.75, -91.9014434814),
        Point(shark.level, 56.2909927368, -6.75, -92.180557251),
        Point(shark.level, 36.9404945374, -6.75, -91.0073547363),
        Point(shark.level, 36.7147674561, -6.37904405594, -74.4520797729),
        ]
      
      cd2 = [ # feinte
        Point(shark.level, 84.954574585, -6.75, -77.4120330811),
        Point(shark.level, 73.7326126099, -6.375, -79.3630218506),
        Point(shark.level, 84.3498153687, -6.75, -78.2598114014),
        Point(shark.level, 85.0124969482, -6.75, -64.4933624268),
        Point(shark.level, 76.25, -6.75, -58.25),
        Point(shark.level, 45.850944519, -6.75, -56.559967041),
        Point(shark.level, 37.3864936829, -6.75, -53.8386001587),
        Point(shark.level, 36.7147674561, -6.37904405594, -74.4520797729),
        ]

      ce = [
        Point(shark.level, 84.954574585, -6.75, -77.4120330811),
        Point(shark.level, 74.4355697632, -6.75454902649, -92.2824172974),
        Point(shark.level, 12.4784030914, -5.44571590424, -91.5136260986),
        Point(shark.level, 11.6511468887, -4.875, -112.090705872),
        Point(shark.level, -19.4819507599, -4.875, -112.883102417),
        ]

      de = [
        Point(shark.level, 36.7147674561, -6.37904405594, -74.4520797729),
        Point(shark.level, 32.1165390015, -6.375, -74.219833374),
        Point(shark.level, 29.6399059296, -6.41641902924, -74.2720947266),
        Point(shark.level, 24.3786563873, -6.31310939789, -74.284362793),
        Point(shark.level, 8.0750837326, -3.28853082657, -75.6640548706),
        Point(shark.level, -5.37833976746, -4.875, -87.4066848755),
        Point(shark.level, 0.75, -4.875, -94.0),
        Point(shark.level, 0.65097117424, -4.92752599716, -112.467048645),
        Point(shark.level, -19.4819507599, -4.875, -112.883102417),
        ]
      
      import hunt
      pc = hunt.PathComputer()
      pc.add_path("g", "a", ga)
      pc.add_path("g", "d", gd)
      pc.add_path("a", "f", af)
      pc.add_path("f", "b", fb)
      pc.add_path("f", "d", fd, 0)
      pc.add_path("a", "d", ad)
      pc.add_path("a", "e", ae, 0)
      pc.add_path("b", "c", bc, 0)
      pc.add_path("b", "d", bd, 0)
      pc.add_path("c", "d", cd1)
      pc.add_path("c", "d", cd2, 0)
      pc.add_path("c", "e", ce)
      pc.add_path("d", "e", de)

      if shark.level.difficulty == 0:
        # Easy path
        if shark.random.random() < 0.5: shark.path = start + gd + de
        else:                           shark.path = start + ga + ae
      else:
        shark.path = start + pc.random_path("g", "e", {0:0, 1:4, 2:7}[shark.level.difficulty], shark.random)
        
      characters = filter(lambda character: isinstance(character, slune_character.Competitor), shark.level.characters)
      
      def finished():
        for character in characters:
          if character.distance_to(shark) < 6.0:
            Mission2Outro().start(tux = character, shark = shark)
            
            characters.remove(character)
            break # Check the other next time !
          
        return 1
      
      shark.finished = finished

      def die():
        shark.__class__.die(shark)
        
        from py2play.player import CURRENT_PLAYER
        
        GnuSpeech([_("__scenar2-2__"), _("__gameover__")]).start(tux = CURRENT_PLAYER)
        
      shark.die = die
      
    elif tux:
      #if tux.player.active:
      #  t = LookAtLeftOfCharacterTraveling(tux); IDLER.camera.add_traveling(t)
      pass
    
    yield Pause()


    if   gnu:
      IDLER.clear_message(); IDLER.message(_("__scenar2-intro-2__"), 100.0)
      IDLER.camera.add_traveling(t)
      
    elif shark:
      IDLER.camera.remove_traveling(t)
    
    yield Pause()
    
    
    if   gnu:
      IDLER.camera.remove_traveling(t)
      
    elif shark:
      IDLER.clear_message(); IDLER.message(_("__scenar2-intro-3__"), 100.0)
      IDLER.camera.add_traveling(t)
    
    yield Pause()
      
    
    if   gnu:
      IDLER.clear_message(); IDLER.message(_("__scenar2-intro-4__"), 100.0)
      IDLER.camera.add_traveling(t)
      
    elif shark:
      IDLER.camera.remove_traveling(t)
    
    yield Pause()
    
    
    if   gnu:
      IDLER.camera.remove_traveling(t)
      
    elif shark:
      IDLER.clear_message(); IDLER.message(_("__scenar2-intro-5__"), 100.0)
      IDLER.camera.add_traveling(t2)
    
    yield Pause()
    
    
    if   gnu or tux:
      for i in range(45): yield Action()
      
    elif shark:
      for i in range(45):
        shark_perso.add_xyz(-0.06, 0.0, -0.007)
        yield Action()
        
    yield Fade()
    
    
    if   shark:
      IDLER.camera.remove_traveling(t2)
      t  = soya.FixTraveling(Point(shark.level, 75.5, -3.35, -6.4), Point(shark, 0.0, 0.95, 0.0), 1, 1)
      IDLER.camera.add_traveling(t)
      
      shark_perso.parent.remove(shark_perso)
      shark.perso.visible = 1
      
      IDLER.camera.zap()
      
      yield Goto(shark, Point(shark.level, 54.1, -5.625 + 0.3, 4.3))
      
      def f(): self.shark_arrived = 1
      IDLER.next_round_tasks.append(f)
      
    while not self.shark_arrived: yield Action()
    
    
    if   gnu:
      IDLER.clear_message(); IDLER.message(_("__scenar2-intro-6__"))
      IDLER.camera.add_traveling(t)
      
    elif shark:
      IDLER.camera.remove_traveling(t)
      
      
    yield Pause()
    yield Fade()
    
    if gnu: # Do this once
      IDLER.camera.remove_traveling(t)
      IDLER.camera.zap()
      
      gnu_perso.parent.remove(gnu_perso)
      
      IDLER.camera.speed = 0.3
      IDLER.clear_message()
      
      gnu.parent.pushables.remove(gnu)
      gnu.parent.remove(gnu)
      
      light.parent.remove(light)
      
    elif tux:
      tux.set_vehicle(1)
      
      tux.teleport(85.4329071045, -5.25 + 0.3, -16.2530593872)
      tux.look_at(Vector(tux.level, -1.0, 0.0, 0.0))
      
    elif shark:
      if   shark.level.difficulty == 2:
        shark.wait_dist = 0.0
        for i in range(10): yield Action()
        
        
class Mission2Outro(VideoSequence):
  def __call__(self, tux = None, shark = None):
    from py2play.idler import IDLER
    
    IDLER.camera.speed = 0.2
    
    self.shark_arrived = 0
    
    yield Fade()
    
    if   shark:
      t = soya.FixTraveling(Point(shark.level, -30.0, -2.0, -114.0), Vector(shark.level, 1.0, -0.2, -0.2), 0, 0)
      IDLER.camera.add_traveling(t)
      IDLER.camera.zap()
      
      self.door = shark.level["palace_door"]
      sound.play("porte-1.wav", self.door)
      for i in range(65):
        self.door.turn_lateral(-1.5)
        yield Action()
        
    elif tux:
      for i in range(64): yield Action()
      
      
    if   shark:
      yield LookAt(shark, Point(shark.level, -21.375, -4.5, -130.0))
      yield Goto  (shark, Point(shark.level, -21.375, -4.5, -118.0), 2.0)
      
      def f():
        self.shark_arrived = 1
        shark.level.remove_character(shark)
      IDLER.next_round_tasks.append(f)
      
      
    while not self.shark_arrived: yield Action()
    
    if tux:
      look_at = Look_at(tux, Point(tux.level, -21.375, -4.5, -130.0))
      goto    = Goto   (tux, Point(tux.level, -21.375, -4.5, -118.0))
      
      sound.play("porte-1.wav", self.door)
      for i in range(32):
        self.door.turn_lateral(3.0)
        try:    yield look_at.next()
        except:
          try: yield goto.next()
          except: pass
          
      while 1:
        try:    yield look_at.next()
        except:
          try: yield goto.next()
          except: break
          
    if tux: # Do this once
      if tux.player.active:
        IDLER.camera.speed = 0.3
        IDLER.level_completed(tux, 1)
        
        yield Action()
        yield Action()
        yield Action()


class Mission3Intro(VideoSequence):
  def __call__(self, tux = None):
    from py2play.idler  import IDLER
    
    IDLER.camera.speed = 0.1
    
    if tux:
      if tux.player.active:
        t_tux = LookAtRightOfCharacterTraveling(tux)
        t_gnu = soya.FixTraveling(Point(tux.level, -6.3, 2.1, 6.8), Point(tux.level, -9.53, 2.6, 6.6), 0, 0)
        
        gnu = soya.Volume(tux.level, soya.Shape.get("gnu1"))
        gnu.move   (Point (tux.level, -7.0, 1.6, 6.9))
        gnu.look_at(Vector(tux.level, 0.4, 0.0, -1.0))
        
        light = soya.Light(tux.level)
        light.set_xyz(-6.0, 3.0, 3.0)
        light.cast_shadow = 0
        
        IDLER.camera.add_traveling(t_tux)
        IDLER.clear_message(); IDLER.message(_("__scenar3-intro-1__"), 100.0)
        
    yield Pause(); yield Fade()
    
    if tux:
      if tux.player.active:
        IDLER.camera.remove_traveling(t_tux)
        IDLER.camera.add_traveling(t_gnu)
        
        IDLER.clear_message(); IDLER.message(_("__scenar3-intro-2__"), 100.0)
        
    yield Pause()
    
    if tux:
      if tux.player.active:
        IDLER.clear_message(); IDLER.message(_("__scenar3-intro-3__"), 100.0)
        
    yield Pause(); yield Fade()
    
    if tux:
      import slune.freestyle
      freestyle = slune.freestyle.FreeStyle(tux.level, tux)
      
      freestyle.phase  = 0
      factor = { 0 : 2.9, 1 : 1.0, 2 : 0.5 }[tux.level.difficulty]
      old_recognized = freestyle.recognized
      def recognized(figure):
        old_recognized(figure)
        for i in range(freestyle.phase, int((tux.score * factor) / 100.0)):
          freestyle.phase += 1
          
          if freestyle.phase == 6:
            if not getattr(tux.level, "door_opened", 0):
              tux.level.door_opened = 1
              class DoorOpener(soya.Volume):
                def __init__(self, parent, door):
                  soya.Volume.__init__(self, parent)
                  self.door = door
                  sound.play("porte-1.wav", self.door)
                  self.duration = 100.0
                def advance_time(self, proportion):
                  self.door.turn_lateral(-1.0 * proportion)
                  self.duration -= proportion
                  if self.duration <= 0.0: self.parent.remove(self)
              DoorOpener(tux.level, tux.level["palace_door"])
              passage = soya.Volume(tux.level, soya.Shape.get("secretpassage1-c"))
              passage.set_xyz(-22.5, -4.5, -118.5)
              script = slune_level.SphericalScript(tux.level, """
if not character in self.characters_ok:
  import videosequence
  videosequence.Mission3Outro().start(tux = character)
  self.characters_ok.append(character)
""")
              script.set_xyz(-21.0, -18.5, -160.5)
              script.set_radius(3.0)
              script.set_shape(None)
              script.characters_ok = []
            
          if freestyle.phase <= 6:
            IDLER.message(_("__scenar3-%s__" % freestyle.phase))
            
      freestyle.recognized = recognized
      
    if tux and tux.player.active: # Do this once
      light.parent.remove(light)
      gnu  .parent.remove(gnu)
      
      IDLER.camera.remove_traveling(t_gnu)
      IDLER.camera.zap()
      
      IDLER.camera.speed = 0.3
      IDLER.clear_message()
      
      from slune.freestyle import start_freestyle_game
      start_freestyle_game(tux.level, { 0 : 800.0, 1 : 100.0, 2 : 20.0 }[tux.level.difficulty], _("__scenar3-7__"))
      
class Mission3Outro(VideoSequence):
  def __call__(self, tux = None):
    from py2play.idler import IDLER
    
    if tux: # Do this once
      if tux.player.active:
        IDLER.level_completed(tux, 1)
        
        yield Action()
        yield Action()
        yield Action()




class Mission4Intro(VideoSequence):
  def __call__(self, tux = None, shark = None):
    from py2play.idler  import IDLER

    if shark:
      diplomat = soya.World(shark.level, soya.Shape.get("vehicle1"))
      diplomat.set_xyz(-0.186012268066, -3.9, -3.07724571228)
      diplomat.look_at(Vector(shark.level, 1.0, 0.0, 1.0))
      diplomat.solid = 0
      diplomat_perso = soya.Volume(diplomat, soya.Shape.get("monk1"))
      diplomat_perso.y = 0.1
      
      shark.escape_dist = 100
      shark.teleport(71.861579895, -7.61357212067 + 0.3, 233.545715332)
      
      shark.path = []
      DOWN = Vector(None, 0.0, -1.0, 0.0)
      for i in range({ 0 : 1, 1 : 3, 2 : 6 }[shark.level.difficulty]):
        p = Point(shark.level, float(shark.random.randrange(-13, 225)), 100.0, float(shark.random.randrange(-13, 225)))
        
        p, v = shark.level.raypick(p, DOWN, -1.0, 0)
        p.convert_to(shark.level)
        
        shark.path.append(p)
        
      shark.path.append(Point(shark.level, 3.25515937805, -3.92874336243, -3.19477081299))
      
      characters = filter(lambda character: isinstance(character, slune_character.Competitor), shark.level.characters)
      def finished():
        for character in characters:
          if character.distance_to(shark) < 6.0:
            Mission4Outro().start(tux = character, shark = shark)
            
            characters.remove(character)
            break # Check the other next time !
          
        return 1
      
      shark.finished = finished

      def die():
        shark.__class__.die(shark)
        
        from py2play.player import CURRENT_PLAYER
        
        GnuSpeech([_("__scenar2-2__"), _("__gameover__")]).start(tux = CURRENT_PLAYER)
        
      shark.die = die

      if shark.level.difficulty == 2:
        for i in range(100): yield Action()
        shark.wait_dist = 0.0
        
    yield Action()
    


class Mission4Outro(VideoSequence):
  def __call__(self, tux = None, shark = None):
    from py2play.idler import IDLER
    
    IDLER.camera.speed = 0.2
    
    #if   shark: shark.teleport(3.25515937805, -3.92874336243, -3.19477081299)
    #elif tux  : tux  .teleport(3.25515937805, -0.92874336243, -7.19477081299)
    #if shark:
    #  diplomat = soya.World(shark.level, soya.Shape.get("vehicle1"))
    #  diplomat.set_xyz(-0.186012268066, -3.9, -3.07724571228)
    #  diplomat.look_at(Vector(shark.level, 1.0, 0.0, 0.0))
    #  diplomat.solid = 0
    #  diplomat_perso = soya.Volume(diplomat, soya.Shape.get("monk1"))
    #  diplomat_perso.y = 0.1
    
    yield Fade()
    
    if   shark:
      shark.look_at(Vector(shark.level, 1.0, 0.0, -1.0))
      shark.look_at(Point(shark.level, -0.186012268066, shark.y, -3.07724571228))
      
      t_shark = LookAtRightOfCharacterTraveling(shark)
      t_diplo = soya.FixTraveling(Point(shark.level, 5.99515104294, 0.5, -10.5981006622), Point(shark.level, -0.186012268066, -3.7, -3.07724571228), 1, 1)
      t_diplo = soya.FixTraveling(
        Point(shark.level, -0.186012268066 - 0.5, -3.3, -2.07724571228),
        Point(shark.level, -0.186012268066      , -3.4, -3.07724571228),
        1, 1)
      IDLER.camera.add_traveling(t_diplo)
      IDLER.camera.zap()
      IDLER.clear_message(); IDLER.message(_("__scenar4-outro-1__"), 100.0)
      
    yield Pause()
    
    if   shark:
      IDLER.camera.remove_traveling(t_diplo)
      IDLER.camera.add_traveling(t_shark)
      IDLER.clear_message(); IDLER.message(_("__scenar4-outro-2__"), 100.0)
      
    yield Pause()
    
    if   shark:
      IDLER.camera.remove_traveling(t_shark)
      IDLER.camera.add_traveling(t_diplo)
      IDLER.clear_message(); IDLER.message(_("__scenar4-outro-3__"), 100.0)
      
    yield Pause()
    
    if   shark:
      IDLER.camera.remove_traveling(t_diplo)
      IDLER.camera.add_traveling(t_shark)
      IDLER.clear_message(); IDLER.message(_("__scenar4-outro-4__"), 100.0)
      
    yield Pause()
    
    if   shark:
      IDLER.camera.remove_traveling(t_shark)
      IDLER.camera.add_traveling(t_diplo)
      IDLER.clear_message(); IDLER.message(_("__scenar4-outro-5__"), 100.0)
      
    yield Pause()
    
    
    if tux: # Do this once
      if tux.player.active:
        IDLER.camera.speed = 0.3
        IDLER.level_completed(tux, 1)
        
        yield Action()
        yield Action()
        yield Action()




class Mission5Intro(VideoSequence):
  def __call__(self, tux = None, shark = None, killer1 = None, killer2 = None, killer3 = None):
    from py2play.idler  import IDLER
    
    if   shark:
      diplomat = soya.World(shark.level, soya.Shape.get("vehicle1"))
      diplomat.set_xyz(-0.186012268066, -3.9, -3.07724571228)
      diplomat.look_at(Vector(shark.level, 1.0, 0.0, 0.0))
      diplomat.solid = 0
      diplomat_perso = soya.Volume(diplomat, soya.Shape.get("monk1"))
      diplomat_perso.y = 0.1
      
      shark.teleport(3.25515937805, -3.92874336243 + 0.3, -3.19477081299)
      shark.rotate_lateral(90.0)
      shark.add_headlight()
      
    elif killer1:
      killer1.name = "killer1"
      killer1.teleport(7.90801048279, -2.74877929688 + 0.3, -4.25709342957)
      killer1.rotate_lateral(90.0)
      killer1.add_headlight()
      
    elif killer2:
      killer2.name = "killer2"
      killer2.teleport(111.350158691, 4.24810218811, 63.3203811646)
      killer2.rotate_lateral(60.0)
      killer2.add_headlight()
      
    elif killer3:
      killer3.name = "killer3"
      killer3.teleport(-3.10736656189, 2.05653381348, 34.0876617432)
      killer3.rotate_lateral(60.0)
      killer3.add_headlight()
      
    if tux:
      for i in range(15): yield Action(ACTION_WAIT, 0.0, 0.0)
    else:
      for i in range(15): yield Action()
      
    if tux and tux.player.active:
      t = LookAtFrontOfCharacterTraveling(tux)
      IDLER.camera.add_traveling(t)
      IDLER.clear_message(); IDLER.message(_("__scenar5-intro-1__"), 100.0)
      
    yield Pause()

    if   tux and tux.player.active:
      IDLER.camera.remove_traveling(t)
      
    elif shark:
      t = LookAtLeftOfCharacterTraveling(shark)
      IDLER.camera.add_traveling(t)
      IDLER.clear_message(); IDLER.message(_("__scenar5-intro-2__"), 100.0)
      
    yield Pause()
    
    if   shark:
      IDLER.camera.remove_traveling(t)
      
    elif tux:
      tux.turn_lateral(-60.0)
      
    elif killer1:
      t = LookAtFrontOfCharacterTraveling(killer1)
      IDLER.camera.add_traveling(t)
      IDLER.clear_message(); IDLER.message(_("__scenar5-intro-3__"), 100.0)
      
    yield Pause()
    
    if   killer1:
      IDLER.camera.remove_traveling(t)

    elif tux and tux.player.active:
      IDLER.camera.add_traveling(t)
      IDLER.clear_message(); IDLER.message(_("__scenar5-intro-4__"), 100.0)
      
    yield Pause()

    if shark:
      shark.level.remove_character(shark)
      diplomat.parent.remove(diplomat)
      
    if tux and tux.player.active: # Do this once
      #tux.teleport(72.0, -6.03447341919, 206.203475952)
      IDLER.camera.remove_traveling(t)
      IDLER.camera.zap()
      
      IDLER.clear_message()
      
      from slune.freestyle import start_freestyle_game
      
      
class Mission5Outro(VideoSequence):
  def __call__(self, tux = None, gnu = None, shark = None, killer1 = None, killer2 = None, killer3 = None):
    from py2play.idler import IDLER
    
    IDLER.camera.speed = 0.2
    
    if   gnu:
      gnu.teleport(72.0, -6.03447341919, 246.203475952)
      webcam = soya.Volume(gnu.internal, soya.Shape.get("webcam1"))
      webcam.move(Point(gnu.perso, -0.15, 0.43, -0.15))
      webcam.rotate_lateral(180.0)
      spot = soya.Light(gnu)
      spot.set_xyz(0.0, 2.0, -2.0)
      spot.look_at(gnu)
      spot.cast_shadow = 1
      
    elif shark:
      shark.teleport(70.9881744385, -7.94097805023, 230.705337524)
      shark.teleport(75.9881744385, -7.94097805023, 230.705337524)
      shark.rotate_lateral(180.0)
      
    elif tux:
      tux.light.parent.remove(tux.light)
      tux.light = None
      
    if gnu:
      self.door1 = gnu.level["door1"]
      self.door2 = gnu.level["door2"]
      sound.play("porte-1.wav", self.door1)
      for i in range(65):
        self.door1.turn_lateral( 1.5)
        self.door2.turn_lateral(-1.5)
        yield Action()
        
      for i in range(20): yield Action(ACTION_WAIT, 0.0, -0.7)
      
    else:
      for i in range(85): yield Action()
      
      
    if   gnu:
      target = gnu.perso.position()
      target.y = target.y + 0.3
      t = soya.FixTraveling(target + Vector(gnu.perso, 0.0, -0.15, -1.2), target, 1, 1)
      IDLER.camera.add_traveling(t)
      IDLER.clear_message(); IDLER.message(_("__scenar5-outro-1__"), 100.0)
      
    yield Pause(); yield Fade()
    
    if   gnu:
      IDLER.camera.remove_traveling(t)
      
    if   shark:
      target = shark.perso.position()
      target.y = target.y + 0.3
      target.convert_to(shark.level)
      t = soya.FixTraveling(target + Vector(shark.perso, 1.0, 0.4, -0.5), target, 1, 1)
      IDLER.camera.add_traveling(t)
      IDLER.camera.zap()
      IDLER.clear_message(); IDLER.message(_("__scenar5-outro-2__"), 100.0)
      
    yield Pause()
    
    if   shark or killer1 or killer2 or killer3:
      for i in range(30): yield Action(ACTION_WAIT, 0.0, 3.0)
    else:
      for i in range(30): yield Action()
    
    
    if tux: # Do this once
      if tux.player.active:
        IDLER.camera.speed = 0.3
        IDLER.level_completed(tux, 1)
        
        yield Action()
        yield Action()
        yield Action()




class Mission6Intro(VideoSequence):
  def __call__(self, tux = None, gnu = None, killer = None, killer2 = None):
    from py2play.idler  import IDLER
    
    IDLER.camera.speed = 0.1
    self.tux_arrived = 0
    
    if   tux:
      IDLER.clear_message(); IDLER.message(_("__scenar6-intro-0__"))
    elif gnu:
      gnu.teleport(-5.3388633728, -0.375, 5.75051689148)
      gnu.level["palace_door"].turn_lateral(-97.5) # Open the door.
      gnu.add_headlight()
    elif killer:
      killer.teleport(-8.65006446838, -1.125, -30.5899105072)
      killer.add_headlight()
    elif killer2:
      killer2.teleport(-1.49378943443, -1.69866323471, -65.828414917)
      killer2.add_headlight()
      
    yield Pause()
    
    if   tux:
      if tux.player.active:
        IDLER.clear_message(); IDLER.message(_("__scenar6-intro-1__"))
        t = LookAtRightOfCharacterTraveling(tux); IDLER.camera.add_traveling(t)
        
    yield Pause()
    
    if   gnu:
      IDLER.clear_message(); IDLER.message(_("__scenar6-intro-2__"))
      t = LookAtLeftOfCharacterTraveling(gnu); IDLER.camera.add_traveling(t)
      
    elif tux:
      IDLER.camera.remove_traveling(t)
      
    yield Pause()
    
    if   gnu:
      sound.play("phone.ogg")
      IDLER.clear_message(); IDLER.message(_("__scenar6-intro-3__"))
      
    yield Pause(); yield Fade()
    
    if   gnu:
      python = soya.Volume(gnu.level, soya.Shape.get("python1"))
      python.y = 100.0
      t_python = soya.FixTraveling(python + Vector(python, 0.2, 0.2, -0.5), python + Vector(python, 0.0, 0.4, 0.0), 0, 0)
      IDLER.camera.add_traveling(t_python)
      
      IDLER.clear_message(); IDLER.message(_("__scenar6-intro-4__"))
      
    yield Pause(); yield Fade()
    
    if   gnu:
      python.parent.remove(python)
      IDLER.camera.remove_traveling(t_python)
      IDLER.camera.zap()
      
      IDLER.clear_message(); IDLER.message(_("__scenar6-intro-5__"))
      
    yield Pause()
    
    if   gnu:
      sound.play("tutut.ogg")
      IDLER.clear_message(); IDLER.message(_("__scenar6-intro-6__"))
      
    yield Pause()
    
    if   gnu:
      IDLER.clear_message(); IDLER.message(_("__scenar6-intro-7__"))
      
    yield Pause()
    
    if   gnu:
      IDLER.camera.remove_traveling(t)
      
    if   killer:
      killer.rotate_lateral(90.0)
      t = soya.FixTraveling(killer + Vector(killer.level, 4.0, 1.0, 15.0), killer + Vector(killer, 0.0, 1.0, 0.0), 1, 1)
      IDLER.camera.add_traveling(t)
      
      for i in range(60): yield Action()
      for i in range(60): yield Action(ACTION_WAIT, 0.0, 0.6)
      
    else:
      for i in range(120): yield Action()
      
    if   killer:
      IDLER.camera.remove_traveling(t)
      
    elif gnu:
      IDLER.camera.add_traveling(t)
      IDLER.clear_message(); IDLER.message(_("__scenar6-intro-8__"))
      
    yield Pause()
    
    if   gnu:
      IDLER.camera.remove_traveling(t)
      IDLER.clear_message()
      
    elif tux:
      yield Goto  (tux, Point(tux.level, 2.5, -0.375, 3.15875339508))
      yield LookAt(tux, Vector(tux.level, 0.5, 0.0, -1.0))
      yield Wall_climber(tux)
      yield LookAt(tux, tux + Vector(tux.level, 0.0, 0.0, -1.0))
      
      def arrive(): self.tux_arrived = 1
      IDLER.next_round_tasks.append(arrive)
      
    while not self.tux_arrived: yield Action()
    
    yield Pause()
    
    if gnu: # Do this once
      IDLER.camera.speed = 0.3
      IDLER.clear_message()
      
      sound.play_music(gnu.level.preloaded_music_name) # Default music
      
      gnu.parent.remove_character(gnu)
      
class Mission6Outro(VideoSequence):
  def __call__(self, tux = None):
    from py2play.idler import IDLER
    
    if tux: # Do this once
      if tux.player.active:
        IDLER.level_completed(tux, 1)
        
        yield Action()
        yield Action()
        yield Action()

class Mission6YouLoose(VideoSequence):
  def __call__(self, tux = None, killer = None):
    from py2play.idler import IDLER
    
    if tux: # Do this once
      if tux.player.active:
        IDLER.level_completed(tux, 1)
        
        yield Action()
        yield Action()
        yield Action()


class Mission7Intro(VideoSequence):
  def __call__(self, tux = None):
    from py2play.idler  import IDLER
    
    if   tux:
      t = LookAtRightOfCharacterTraveling(tux); IDLER.camera.add_traveling(t)
      IDLER.clear_message(); IDLER.message(_("__scenar7-intro-1__"))
      
    yield Pause()
    
    if   tux:
      IDLER.camera.remove_traveling(t)
      
    if   tux and tux.player.active: # Do this once
      IDLER.clear_message()
      
      tux.level.python = python = soya.World(tux.level, model = soya.Shape.get("vehicle3"))
      python.set_xyz(34.326007843, 0.888233947754, 12.4514389038)
      python.rotate_lateral(180.0)
      soya.Volume(python, model = soya.Shape.get("python1")).set_xyz(0.0, 0.2, 0.35)
      
class Mission7AddEnemy(VideoSequence):
  def __init__(self, character, x, y, z, make_fall = None):
    self.character = character
    self.x = x
    self.y = y
    self.z = z
    self.make_fall = make_fall
    
  def __call__(self, tux = None, killer = None):
    from py2play.idler import IDLER
    
    if killer:
      killer.level.pushables.append(killer)
      killer.teleport(self.x, self.y + 0.3, self.z)
      #killer.look_at(Point(killer.level, self.character.x, killer.y, self.character.z))
      p = Point(self.character, 0.0, 0.0, -50.0)
      p.convert_to(killer.level)
      p.y = killer.y
      killer.look_at(p)
      
      t = LookAtLeftOfCharacterTraveling(killer, 1.8)
      IDLER.camera.add_traveling(t)
      IDLER.camera.speed = 0.1
      IDLER.clear_message(); IDLER.message(_("__scenar7-1__"), 100.0)
      
    yield Pause()
    
    if   killer:
      IDLER.camera.remove_traveling(t)
      t = LookAtRightOfCharacterTraveling(killer, 4.0)
      IDLER.camera.add_traveling(t)
      
      yield Action(ACTION_JUMP, 0.0, -1.0)
      for i in range(25): yield Action(ACTION_WAIT, 0.0, -1.0)
      for i in range(5): yield Action(ACTION_ROTDOWN, 0.0, -1.0)
      
      if self.make_fall:
        for trunc in killer.parent:
          if getattr(trunc, "name", "") == self.make_fall:
            trunc.worth_playing = 1
            
    elif tux:
      for i in range(31): yield Action()
      
    yield Fade()
    
    if killer:
      IDLER.camera.remove_traveling(t)
      IDLER.camera.zap()
      IDLER.camera.speed = 0.3
      IDLER.clear_message()
      
      
class Mission7Cabane(VideoSequence):
  def __init__(self, character):
    pass
  
  def __call__(self, tux = None):
    from py2play.idler import IDLER
    
    if tux:
      t = soya.FixTraveling(Point(tux.level, 39.0, 5.0, 50.0), tux.level.python, 1, 1)
      IDLER.camera.add_traveling(t)
      IDLER.camera.speed = 0.1
      IDLER.clear_message(); IDLER.message(_("__scenar7-3__"))
      
    yield Pause()
    
    if tux:
      IDLER.camera.remove_traveling(t)
      t = soya.FixTraveling(Point(tux.level, 39.0, 4.0, 12.0), tux.level.python, 1, 1)
      IDLER.camera.add_traveling(t)
      IDLER.clear_message(); IDLER.message(_("__scenar7-4__"))
      
    yield Pause()
    
      
    yield Fade()
    
    if tux:
      IDLER.camera.remove_traveling(t)
      IDLER.camera.zap()
      IDLER.clear_message()
      

class Mission7Outro(VideoSequence):
  def __call__(self, tux = None, python = None):
    from py2play.idler import IDLER
    
    if   python:
      python.level.remove(python.level.python) # Remove the "fake" Python
      python.teleport(34.326007843, 0.888233947754, 12.4514389038)
      python.rotate_lateral(180.0)
      
      t = LookAtLeftOfCharacterTraveling(python); IDLER.camera.add_traveling(t)
      IDLER.clear_message(); IDLER.message(_("__scenar7-outro-1__"))
      
    elif tux:
      t = LookAtFrontOfCharacterTraveling(tux);
      
    yield Pause()
    
    if   python:
      IDLER.clear_message(); IDLER.message(_("__scenar7-outro-2__"))
    
    yield Pause()
    
    if   python:
      IDLER.camera.remove_traveling(t)
      
    elif tux:
      IDLER.camera.add_traveling(t)
      IDLER.clear_message(); IDLER.message(_("__scenar7-outro-3__"))
    
    yield Pause()
    
    if   python:
      IDLER.camera.add_traveling(t)
      IDLER.clear_message(); IDLER.message(_("__scenar7-outro-4__"))
      
    elif tux:
      IDLER.camera.remove_traveling(t)
      
    yield Pause()
    
    if   python:
      IDLER.camera.remove_traveling(t)
      
    elif tux:
      IDLER.camera.add_traveling(t)
      IDLER.clear_message(); IDLER.message(_("__scenar7-outro-5__"))
      
    yield Pause()
    
    if   tux: # Do this once
      if tux.player.active:
        IDLER.level_completed(tux, 1)
        
        yield Action()
        yield Action()
        yield Action()
        
        


class Mission8Intro(VideoSequence):
  def __call__(self, tux = None, gnu = None, shark = None, killer1 = None, killer2 = None):
    from py2play.idler  import IDLER
    
    if   tux:
      t = LookAtBackOfCharacterTraveling(tux, 1.5); IDLER.camera.add_traveling(t)
      IDLER.clear_message(); IDLER.message(_("__scenar8-intro-0__"))
      
    elif gnu:
      gnu.teleport(21.9561328888, 0.397022294998, 28.5)
      gnu.rotate_lateral(-90.0)
      
    elif shark:
      shark.teleport(21.7788066864, 0.934619772434, 34.0)
      
    elif killer1:
      self.killer1 = killer1
      killer1.teleport(31.9246749878, 1.45169377327, 42.7683944702)
      
    elif killer2:
      self.killer2 = killer2
      if killer2.level.difficulty == 0: killer2.parent.remove_character(killer2)
      else: killer2.teleport(33.9246749878, 1.45169377327, 45.7683944702)
      
    yield Pause()
    
    if   gnu:
      t = LookAtBackOfCharacterTraveling(gnu, 1.0); IDLER.camera.add_traveling(t)
      IDLER.clear_message(); IDLER.message(_("__scenar8-intro-1__"))
      
    elif tux:
      IDLER.camera.remove_traveling(t)
      
    yield Pause()
    
    if   shark:
      t = LookAtRightOfCharacterTraveling(shark, 5.0); IDLER.camera.add_traveling(t)
      IDLER.clear_message(); IDLER.message(_("__scenar8-intro-2__"))
      
    elif gnu:
      IDLER.camera.remove_traveling(t)
      
    yield Pause()
    
    if   tux:
      t = LookAtRightOfCharacterTraveling(tux, 1.0); IDLER.camera.add_traveling(t)
      IDLER.clear_message(); IDLER.message(_("__scenar8-intro-3__"))
      
    elif shark:
      IDLER.camera.remove_traveling(t)
      
    yield Pause()
    
    if   gnu:
      t = LookAtRightOfCharacterTraveling(gnu, 1.0); IDLER.camera.add_traveling(t)
      IDLER.clear_message(); IDLER.message(_("__scenar8-intro-4__"))
      
    elif tux:
      IDLER.camera.remove_traveling(t)
      
    yield Pause()
    
    if   gnu:
      IDLER.camera.remove_traveling(t)
      
    if   tux and tux.player.active: # Do this once
      IDLER.clear_message()
      
      python_vehicle = soya.World(tux.level)
      python_vehicle.model = soya.Shape.get("vehicle3")
      python_vehicle.set_xyz(111.893669128, 1.8, 136.298706055)
      python_vehicle.rotate_lateral(180.0)
      python = soya.Volume(python_vehicle, soya.Shape.get("python1"))
      python.set_xyz(0.0, 0.2, 0.35)
      
      vid_seq = self
      class Checker(soya.Volume):
        def begin_round(self):
          #if (vid_seq.killer1.parent is None) and (vid_seq.killer2.parent is None) and (tux.distance_to(python_vehicle) < 10.0):
          if (vid_seq.killer1.parent is None) and (vid_seq.killer2.parent is None):
            Mission8Outro2().start(tux = PLAYER, killer1 = AUTO, killer2 = AUTO)
            self.parent.remove(self)
      Checker(tux.level)
      
    def KillerControler(killer, initial_wait, path):
      for i in range(initial_wait): yield Action()
      for p in path:
        yield Runto(killer, p, 2.0)
      for i in range(10): yield Action()
      Mission8Outro1().start(tux = PLAYER, killer1 = AUTO, killer2 = AUTO, winner = killer)
      
    if killer1:
      killer1.maxspeedz = 0.5
      killer1.weight    = 1.0
      level = killer1.level
      path = [
        Point(level, 34.8027191162, 1.44117641449, 29.5947685242),
        Point(level, 46.1448402405, 1.85601460934, 30.3215751648),
        Point(level, 81.4145278931, 0.97967171669, 25.0217971802),
        Point(level, 111.195541382, 1.05167841911, 29.1344203949),
        Point(level, 121.912506104, 0.637456178665, 37.2835159302),
        Point(level, 117.454689026, 0.754901885986, 49.2385520935),
        Point(level, 100.839179993, 2.17436337471, 64.9775848389),
        Point(level, 80.5361251831, 1.03603553772, 82.7462387085),
        Point(level, 83.7344207764, 1.67107856274, 88.8338546753),
        Point(level, 83.6148300171, 2.98795938492, 97.6328277588),
        Point(level, 77.1922988892, 3.52166175842, 122.451568604),
        Point(level, 77.2774047852, 4.43288946152, 133.972122192),
        Point(level, 87.7821273804, 0.435206890106, 164.775939941),
        Point(level, 99.5029144287, 0.191377609968, 171.15852356),
        Point(level, 120.222740173, 1.00903081894, 170.174957275),
        Point(level, 113.933013916, 0.985481381416, 153.547088623),
        Point(level, 111.715179443, 1.5, 137.749237061),
        ]
      killer1.controler.animate(KillerControler(killer1, 0, path))
      
    if killer2:
      killer2.maxspeedz = 0.5
      killer2.weight    = 1.0
      level = killer2.level
      path = [
        Point(level, 35.5492134094, 1.45529460907, 30.0423545837),
        Point(level, 39.0626983643, 1.5195453167, 29.293756485),
        Point(level, 46.2384185791, 1.22116327286, 33.888671875),
        Point(level, 50.2972183228, 4.51887798309, 55.5366172791),
        Point(level, 50.5635108948, 3.77171492577, 73.3933181763),
        Point(level, 54.1204223633, 4.86251068115, 79.1944656372),
        Point(level, 62.8503303528, 5.32229709625, 81.8691711426),
        Point(level, 80.2222290039, 1.01580369473, 82.4425430298),
        Point(level, 84.3109283447, 1.74578893185, 90.013092041),
        Point(level, 77.6757354736, 2.99731588364, 114.772651672),
        Point(level, 77.3346099854, 5.98569726944, 131.621459961),
        Point(level, 88.3166275024, 0.463613271713, 165.38381958),
        Point(level, 97.915977478, 0.106691598892, 170.075210571),
        Point(level, 120.215400696, 1.00970244408, 170.159225464),
        Point(level, 113.949005127, 1.03407847881, 152.886978149),
        Point(level, 111.71975708, 1.5, 138.088562012),
        ]
      killer2.controler.animate(KillerControler(killer2, 0, path))
      
class Mission8Outro1(VideoSequence):
  def __call__(self, tux = None, killer1 = None, killer2 = None, winner = None):
    from py2play.idler import IDLER
    
    if   winner:
      t = LookAtFrontOfCharacterTraveling(winner, 2.0); IDLER.camera.add_traveling(t)
      IDLER.clear_message(); IDLER.message(_("__scenar8-1__"))
      
    yield Pause()
    
    if   winner:
      sound.play("explose-3.wav", winner)
      from slune.character import Explosion
      e = Explosion(winner.level)
      e.move(winner)
      e.life = 1000
      e.set_sizes((2.0, 2.0))
      
    yield Pause()
    
    if   tux: # Do this once
      if tux.player.active:
        IDLER.level_completed(tux, 0)
        yield Action(); yield Action(); yield Action()
        
class Mission8Outro2(VideoSequence):
  def __call__(self, tux = None, killer1 = None, killer2 = None):
    from py2play.idler import IDLER
    
    yield Fade()
    
    if   tux:
      tux.teleport(108.586151123, 1.38258528709, 142.891616821)
      tux.look_at(Vector(None, 1.0, 0.0, -0.5))
      
    if   tux and tux.player.active:
      python_t = soya.FixTraveling(Point(tux.level, 111.893669128, 3.8, 139.0), Point(tux.level, 111.893669128, 2.8, 136.298706055))
      
      IDLER.camera.add_traveling(python_t)
      IDLER.camera.zap()
      IDLER.clear_message(); IDLER.message(_("__scenar8-outro-1__"))
      
      
    yield Pause()
    
    if   tux and tux.player.active:
      IDLER.clear_message(); IDLER.message(_("__scenar8-outro-2__"))
      
    yield Pause()
    
    if   tux and tux.player.active:
      IDLER.camera.remove_traveling(python_t)
      
    if   tux:
      t = LookAtRightOfCharacterTraveling(tux, 2.0); IDLER.camera.add_traveling(t)
      IDLER.clear_message(); IDLER.message(_("__scenar8-outro-3__"))
      
    yield Pause()
    
    if   tux and tux.player.active:
      IDLER.camera.add_traveling(python_t)
      IDLER.clear_message(); IDLER.message(_("__scenar8-outro-4__"))
      
    if   tux:
      IDLER.camera.remove_traveling(t)
      
    yield Pause()
    
    if   tux: # Do this once
      if tux.player.active:
        IDLER.level_completed(tux, 1)
        yield Action(); yield Action(); yield Action()
      
      
      
      
      
class Mission9Intro(VideoSequence):
  def __call__(self, tux = None, python = None, killer = None):
    from py2play.idler  import IDLER
    
    if   tux:
      pass
    
    elif python:
      self.python = python
      python.teleport(2.8, 0.3, 5.2)
      python.rotate_lateral(-30.0)
      
      t = LookAtLeftOfCharacterTraveling(python); IDLER.camera.add_traveling(t)
      IDLER.clear_message(); IDLER.message(_("__scenar9-intro-1__"))
      
    elif killer:
      self.killer = killer
      killer.teleport(10.0, 0.4, -1.0)
      killer.rotate_lateral(180.0)
      killer.weight   = 0.3
      killer.floating = 0.4
      killer.life     = 1000.0
      killer.push_fly = 0.1
      killer.radius   = 0.8
      
    yield Pause()
    
    if   tux:
      t = LookAtRightOfCharacterTraveling(tux); IDLER.camera.add_traveling(t)
      IDLER.clear_message(); IDLER.message(_("__scenar9-intro-2__"))
      
    elif python:
      IDLER.camera.remove_traveling(t)
      
    yield Pause()
    
    if   tux:
      IDLER.camera.remove_traveling(t)
      
    elif killer:
      t = LookAtFrontOfCharacterTraveling(killer); IDLER.camera.add_traveling(t)
      IDLER.clear_message(); IDLER.message(_("__scenar9-intro-3__"))
      
    yield Pause()
    
    if   tux:
      t = LookAtBackOfCharacterTraveling(tux, 2.5); IDLER.camera.add_traveling(t)
      IDLER.clear_message(); IDLER.message(_("__scenar9-intro-4__"))
      
    elif killer:
      IDLER.camera.remove_traveling(t)
      
    yield Pause()
      
    if   tux:
      IDLER.camera.remove_traveling(t)
    if   tux and tux.player.active: # Do this once
      IDLER.clear_message()
      
      def on_no_time_left(characters):
        Mission9Outro1().start(tux = PLAYER, python = AUTO, killer = AUTO)
        
      import slune.freestyle, time
      tux.score_start = time.time()
      IDLER.no_blackbands_group.add(slune.freestyle.TimerLabel([tux], 5, on_no_time_left))

      killer = self.killer
      python = self.python
      class Checker(soya.Volume):
        def begin_round(self):
          if killer.z < -30.0:
            for e in tux.level:
              if getattr(e, "name", "") == "quille": break
            else:
              Mission9Outro2().start(tux = tux, python = python, killer = killer)
              self.parent.remove(self)
              
      Checker(tux.level)
          
class Mission9Outro1(VideoSequence):
  def __call__(self, tux = None, python = None, killer = None):
    from py2play.idler import IDLER

    if   killer:
      t = LookAtFrontOfCharacterTraveling(killer); IDLER.camera.add_traveling(t)
      IDLER.clear_message(); IDLER.message(_("__scenar9-outro-1__"))
      
    yield Pause()
    
    if   tux: # Do this once
      if tux.player.active:
        IDLER.level_completed(tux, 0)
        yield Action(); yield Action(); yield Action()
      
class Mission9Outro2(VideoSequence):
  def __call__(self, tux = None, python = None, killer = None):
    from py2play.idler import IDLER
    
    if   python:
      t = LookAtLeftOfCharacterTraveling(python); IDLER.camera.add_traveling(t)
      IDLER.clear_message(); IDLER.message(_("__scenar9-outro-2__"))
      
    yield Pause()
    
    if   python:
      IDLER.camera.remove_traveling(t)
      
    if   python or tux:
      for i in range(120): yield Action()
      
    elif killer:
      t = soya.FixTraveling(IDLER.camera.position(), killer, 1, 1)
      IDLER.camera.add_traveling(t)
      IDLER.clear_message(); IDLER.message(_("__scenar9-outro-3__"))
      
      engine = soya.Volume(killer.level, soya.Shape.get("engine1"))
      engine.set_xyz(10.0, 11.0, -37.1)
      
      for i in range(20): yield Action()
      
      for i in range(50):
        engine.y -= 0.1
        yield Action()
      
      killer.visible = 0
      
      for i in range(50):
        engine.y += 0.1
        yield Action()
    
    yield Pause()
    
    if   tux: # Do this once
      if tux.player.active:
        IDLER.level_completed(tux, 1)
        yield Action(); yield Action(); yield Action()
        



class Mission10Intro(VideoSequence):
  def __call__(self, tux = None, shark = None):
    from py2play.idler  import IDLER
    
    if   tux:
      medocs = tux.medocs
      
      t = LookAtRightOfCharacterTraveling(tux); IDLER.camera.add_traveling(t)
      IDLER.clear_message(); IDLER.message(_("__scenar10-intro-1__"))
      
    elif shark:
      shark.teleport(40.0, 0.1, 146.5)
      shark.look_at(Vector(shark.level, 1.0, 0.0, 0.0))
      
    yield Pause()

    if   tux:
      IDLER.camera.remove_traveling(t)
      
    elif shark:
      t = LookAtRightOfCharacterTraveling(shark, 2.0); IDLER.camera.add_traveling(t)
      
    for i in range(40):
      if   tux:   yield Action()
      elif shark: yield Action(ACTION_TURBO, mouse_y = -1.0)
      
    if   tux:
      t = LookAtRightOfCharacterTraveling(tux, 4.0); IDLER.camera.add_traveling(t)
      for m in medocs:
        a = random.uniform(0.0, 6.2832)
        m.speed = Vector(tux.level, 0.3 * math.cos(a), 0.4, 0.3 * math.sin(a))
        
    elif shark:
      IDLER.camera.remove_traveling(t)
      
    if   tux:
      for i in range(20): yield Action()
      for i in range(80):
        for m in medocs:
          m += m.speed
          m.speed.y -= 0.01
        yield Action()
    elif shark:
      for i in range(10):
        yield Action(ACTION_TURBO, mouse_y = -1.0)
      for i in range(90): yield Action()
        
        
    if   tux:
      IDLER.camera.remove_traveling(t)
      
    elif shark:
      t = LookAtRightOfCharacterTraveling(shark, 2.0); IDLER.camera.add_traveling(t)
      IDLER.clear_message(); IDLER.message(_("__scenar10-intro-2__"))
      
    yield Pause()
    
    if   tux:
      pass
    
    elif shark:
      IDLER.clear_message(); IDLER.message(_("__scenar10-intro-3__"))
      
    yield Pause()
    
    if   tux:
      for m in medocs: m.parent.remove(m)
      del tux.medocs
      t = LookAtRightOfCharacterTraveling(tux, 2.0); IDLER.camera.add_traveling(t)
      IDLER.clear_message(); IDLER.message(_("__scenar10-intro-4__"))
      
    elif shark:
      IDLER.camera.remove_traveling(t)
      
    yield Pause()
    
    if   tux:
      IDLER.camera.remove_traveling(t)
      
    elif shark:
      shark.level.remove_character(shark)
      
    if   tux and tux.player.active: # Do this once
      IDLER.clear_message()
      def on_no_time_left(characters):
        from py2play.player import CURRENT_PLAYER
        GnuSpeech([_("__scenar10-1__"), _("__gameover__")]).start(tux = CURRENT_PLAYER)
        
      import slune.freestyle, time
      tux.score_start = time.time()
      IDLER.no_blackbands_group.add(slune.freestyle.TimerLabel([tux], { 0 : 1000, 1 : 450, 2 : 130 }[tux.level.difficulty], on_no_time_left))
      
      from slune.medoc import add_medocs
      add_medocs(tux.level, {0:4, 1:7, 2:8}[tux.level.difficulty])
      
      from slune.fight import Fighter
      killer = add_perso("killer", 0, Fighter, tux.level)
      killer.set_xyz(49.9499931335, 0.8, 14.455827713)
      killer.flame_thrower = tux.level.difficulty


class Mission11Intro(VideoSequence):
  def __call__(self, tux = None, gnu = None):
    from py2play.idler  import IDLER
    
    if   tux:
      t = LookAtLeftOfCharacterTraveling(tux); IDLER.camera.add_traveling(t)
      IDLER.clear_message(); IDLER.message(_("__scenar11-intro-1__"))
      
      import slune.airplane
      airplane = slune.airplane.Airplane(tux.level)
      airplane.look_at(Vector(None, 1.0, 0.0, 0.0))
      airplane.set_xyz(286.385559082, 18.117647171, 129.48248291)
      
    elif gnu:
      gnu.teleport(246.7, 26.2, 105.8)
      gnu.look_at(Vector(gnu.level, 0.5, 0.0, 1.0))
      
    yield Pause()
    yield Fade()
    
    if   tux:
      IDLER.camera.remove_traveling(t)
      target = soya.Point(airplane, 0.0, 5.0, 0.0)
      pos    = target + Vector(airplane, -7.0, -3.0, -15.0)
      t_airplane = soya.FixTraveling(pos, target, 0, 0)
      IDLER.camera.add_traveling(t_airplane)
      
      light = soya.Light(airplane)
      light.set_xyz(2.0, 5.0, -10.0)
      light.cast_shadow = 0
      
    yield Pause()
    yield Fade()
    
    if   tux:
      IDLER.camera.remove_traveling(t_airplane)
      light.parent.remove(light)
      
    elif gnu:
      t = LookAtLeftOfCharacterTraveling(gnu); IDLER.camera.add_traveling(t)
      IDLER.camera.zap()
      IDLER.clear_message(); IDLER.message(_("__scenar11-intro-2__"))
      
    yield Pause()
    
    if   gnu:
      IDLER.clear_message(); IDLER.message(_("__scenar11-intro-3__"))
      
    yield Pause()
    
    if   tux:
      IDLER.camera.add_traveling(t)
      IDLER.clear_message(); IDLER.message(_("__scenar11-intro-4__"))
      
    elif gnu:
      IDLER.camera.remove_traveling(t)
      
    yield Pause()
    
    if   tux:
      IDLER.camera.remove_traveling(t)
      
      
    if   tux and tux.player.active: # Do this once
      IDLER.clear_message()
      
      if   tux.level.difficulty == 1: airplane.start_in_round = 50
      elif tux.level.difficulty == 2: airplane.start()
      
      class Checker(soya.Volume):
        def begin_round(self):
          if airplane.x > 600.0:
            if airplane.characters_on:
              IDLER.level_completed(tux, 1)
              IDLER.camera.traveling.distance = 27.0
            else:
              from py2play.player import CURRENT_PLAYER
              GnuSpeech([_("__scenar11-1__"), _("__gameover__")]).start(tux = CURRENT_PLAYER)
            self.parent.remove(self)
      Checker(tux.level)
      
      
class Mission12Intro(VideoSequence):
  def __call__(self, tux = None):
    from py2play.idler  import IDLER
    
    if   tux:
      import slune.airplane
      for airplane in tux.level:
        if isinstance(airplane, slune.airplane.Airplane): break
        
      target = soya.Point(airplane, 0.0, 7.0, 0.0)
      pos    = target + Vector(airplane, -20.0, -5.0, -8.0)
      t_airplane = soya.FixTraveling(pos, target, 1, 1)
      IDLER.camera.add_traveling(t_airplane)
      IDLER.camera.zap()
      
      IDLER.clear_message(); IDLER.message(_("__scenar12-intro-1__"))
      
    yield Pause()
    
    if   tux:
      IDLER.camera.remove_traveling(t_airplane)
      IDLER.camera.speed = 0.7
      
      target = soya.Point(airplane, 0.0, 7.0, 0.0)
      pos    = target + Vector(airplane, -15.0, 5.0, -7.0)
      t = soya.FixTraveling(pos, target, 1, 1)
      IDLER.camera.add_traveling(t)
      
      #t = LookAtRightOfCharacterTraveling(tux, 10.0)
      #IDLER.camera.add_traveling(t)
      IDLER.clear_message(); IDLER.message(_("__scenar12-intro-2__"))
      
    yield Pause()
    
    
    if   tux:
      IDLER.camera.remove_traveling(t)
      
    if   tux and tux.player.active: # Do this once
      IDLER.clear_message()
      IDLER.camera.traveling.distance = 15.0
      
      import slune.fight
      
      killer = add_perso("killer", 1, slune.fight.Fighter, tux.level, chromosom = slune.fight.CHROMOSOMS[("killer_flight", tux.level.difficulty)])
      killer.set_xyz(1.0, 15.0, airplane.z - 15.0)
      
      class Checker(soya.Volume):
        def __init__(self, parent):
          soya.Volume.__init__(self, parent)
          self.round = 0
          
        def begin_round(self):
          self.round += 1
          
          if   self.round == 200:
            if tux.level.difficulty >= 1:
              killer = add_perso("killer", 3, slune.fight.Fighter, tux.level, chromosom = slune.fight.CHROMOSOMS[("killer_flight", tux.level.difficulty)])
              killer.set_xyz(0.0, 20.0, airplane.z - 20.0)
          
          elif self.round == 300:
            if tux.level.difficulty == 2:
              killer = add_perso("killer", 4, slune.fight.Fighter, tux.level, chromosom = slune.fight.CHROMOSOMS[("killer_flight", tux.level.difficulty)])
              killer.set_xyz( 1.0, 20.0, airplane.z - 20.0)
            
          elif self.round == 400:
            killer = add_perso("killer", 3, slune.fight.Fighter, tux.level, chromosom = slune.fight.CHROMOSOMS[("killer_flight", tux.level.difficulty)])
            killer.set_xyz( 1.0, 20.0, airplane.z - 20.0)

            if tux.level.difficulty == 2:
              killer = add_perso("killer", 3, slune.fight.Fighter, tux.level, chromosom = slune.fight.CHROMOSOMS[("killer_flight", tux.level.difficulty)])
              killer.set_xyz(-1.0, 20.0, airplane.z - 22.0)
            
          elif (self.round > 400) and (len(tux.level.characters) == 1):
            if airplane.characters_on:
              IDLER.level_completed(tux, 1)
              IDLER.camera.traveling.distance = 27.0
              self.parent.remove(self)
      Checker(tux.level)
      
      
class Mission13Intro(VideoSequence):
  def __call__(self, tux = None, girafe = None):
    from py2play.idler  import IDLER

    yield Fade()
    
    if   tux:
      IDLER.clear_message(); IDLER.message(_("__scenar13-intro-0__"))
      
    elif girafe:
      girafe.teleport(27.7, 12.1, 187.7)
      girafe.look_at(Vector(girafe.level, 1.0, 0.0, 0.0))
      
    yield Pause()
    
    if   girafe:
      t = LookAtLeftOfCharacterTraveling(girafe)
      IDLER.camera.add_traveling(t)
      IDLER.camera.zap()
      IDLER.clear_message(); IDLER.message(_("__scenar13-intro-1__"))
      
    yield Pause()
    
    
    if girafe:
      IDLER.camera.remove_traveling(t)
      IDLER.clear_message()
      
    for i in range(120):
      yield Action(ACTION_WAIT, 0.0, 0.0)
      
    yield Fade()
    
    if   tux:
      tux.teleport(192.968460083, 1.06084299088, 177.368118286)
      
      for i in range(70): yield Action()
      
    elif girafe:
      girafe.teleport(199.3, 2.2, 179.0)
      girafe.look_at(Vector(girafe.level, 1.0, 0.0, 0.0))
      girafe.rotate_lateral(33.0)
      
      t = soya.FixTraveling(
        Point(girafe.level, 189.499481201, 5.0965461731, 177.350845337),
        girafe,
        )
      IDLER.camera.add_traveling(t)
      IDLER.camera.zap()
      
      
      for i in range(70): yield Action(ACTION_TURBO, 0.0, -1.0)
      IDLER.camera.remove_traveling(t)
      girafe.parent.remove(girafe)
      
    if   tux:
      t = LookAtLeftOfCharacterTraveling(tux)
      IDLER.camera.add_traveling(t)
      IDLER.clear_message(); IDLER.message(_("__scenar13-intro-2__"))
      
    yield Pause()
    
    if   tux:
      IDLER.clear_message(); IDLER.message(_("__scenar13-intro-3__"))
      
    yield Pause()
    
    if   tux:
      IDLER.clear_message(); IDLER.message(_("__scenar13-intro-4__"))
      
    yield Pause()
    
    if   tux:
      IDLER.camera.remove_traveling(t)
      
    if   tux and tux.player.active: # Do this once
      IDLER.clear_message()
      
      import slune.freestyle
      freestyle = slune.freestyle.FreeStyle(tux.level, tux)
      old_recognized = freestyle.recognized
      def recognized(figure):
        old_recognized(figure)
        if tux.score > { 0 : 500, 1 : 2000, 2 : 5000 }[tux.level.difficulty]:
          Mission13Outro().start(tux = tux, girafe = add_perso("girafe", 3))
          freestyle.parent.remove(freestyle)
      freestyle.recognized = recognized
      
      slune.freestyle.start_freestyle_game(tux.level, { 0 : 500.0, 1 : 80.0, 2 : 80.0 }[tux.level.difficulty], _("__scenar13-1__"))

class Mission13Outro(VideoSequence):
  def __call__(self, tux = None, girafe = None):
    from py2play.idler  import IDLER

    yield Fade()
    
    if   tux:
      pass
      
    elif girafe:
      girafe.teleport(193.8, 17.0, 210.9)
      
      t = LookAtLeftOfCharacterTraveling(girafe)
      IDLER.camera.add_traveling(t)
      IDLER.camera.zap()
      IDLER.clear_message(); IDLER.message(_("__scenar13-outro-1__"))
      
    yield Pause()
    
    if   girafe:
      IDLER.clear_message(); IDLER.message(_("__scenar13-outro-2__"))
      
    yield Pause()
    
    if   girafe:
      IDLER.clear_message(); IDLER.message(_("__scenar13-outro-3__"))
      
    yield Pause()

    if   tux:
      t = LookAtLeftOfCharacterTraveling(tux)
      IDLER.camera.add_traveling(t)
      IDLER.clear_message(); IDLER.message(_("__scenar13-outro-4__"))
      
    elif girafe:
      IDLER.camera.remove_traveling(t)
      
    yield Pause()
    
    if   tux:
      IDLER.level_completed(tux, 1)
      
      
class Mission14Intro(VideoSequence):
  def __call__(self, tux = None, gnu = None):
    from py2play.idler  import IDLER
    
#     if tux:
#       import slune.videosequence as videosequence
#       videosequence.Mission14Outro().start(
#         tux   = videosequence.PLAYER,
#         gnu   = videosequence.add_perso("gnu"  , 1),
#         shark = videosequence.add_perso("shark", 4),
#         )
#     return
    
    if   tux:
      IDLER.camera.traveling.distance = 7.0
      
      import slune.airplane as airplane
      killer_airplane = airplane.KillerAirplane(tux.level, tux, {0:0.2, 1:0.4, 2:0.5}[tux.level.difficulty])
      killer_airplane.set_xyz(110.0, 34.5516757965, 229.495330811)
      killer_airplane.rotate_lateral(180.0)
      
    elif gnu:
      gnu.teleport(96.435836792, 28.2565994263, 144.252090454)
      gnu.look_at(Vector(gnu.level, 1.0, 0.0, -1.0))
      
      t = LookAtRightOfCharacterTraveling(gnu)
      IDLER.camera.add_traveling(t)
      
      IDLER.clear_message(); IDLER.message(_("__scenar14-intro-1__"))
      
    yield Pause()
    
    if   gnu:
      IDLER.clear_message(); IDLER.message(_("__scenar14-intro-2__"))
      
    yield Pause()
    yield Fade()
    
    if   gnu:
      IDLER.camera.remove_traveling(t)
      
      gnu.parent.pushables.remove(gnu)
      gnu.parent.remove(gnu)
      
    elif tux:
      pos = Point(killer_airplane, 1.0, 2.0, -3.0)
      t = soya.FixTraveling(
        pos + Vector(killer_airplane, -2.0, 3.0, -8.0),
        pos,
        1, 1)
      IDLER.camera.add_traveling(t)
      IDLER.camera.zap()
      IDLER.clear_message(); IDLER.message(_("__scenar14-intro-3__"))
      
    yield Pause()
      
    if   tux:
      IDLER.camera.remove_traveling(t)
      
    if   tux and tux.player.active: # Do this once
      IDLER.clear_message()
      
      import slune.medoc as medoc
      
      medoc.MedocWaiter(tux.level,  26.7519454956, 24.5517711639, 211.49319458)
      medoc.MedocWaiter(tux.level, 180.690795898 , 26.0294113159, 152.907470703)
      medoc.MedocWaiter(tux.level, 204.346420288 , 25.8917675018,  94.5336685181)
      medoc.MedocWaiter(tux.level,  89.7115478516, 25.9517688751,  72.2400970459)
      medoc.MedocWaiter(tux.level,  90.653137207 , 20.6758728027, 191.899993896)
      
      IDLER.no_blackbands_group.insert(0, medoc.MedocWaiterMiniMap(tux.level))
      
      if tux.level.difficulty == 2:
        from slune.fight import Fighter
        killer = add_perso("killer", 4, Fighter, tux.level)
        killer.set_xyz(202.747375488, 23.6, 163.512329102)
        killer.flame_thrower = tux.level.difficulty
        
      killer_airplane.play = 1


class Mission14Outro(VideoSequence):
  def __call__(self, tux = None, gnu = None, shark = None):
    from py2play.idler  import IDLER
    
    yield Fade()
    
    if   tux:
      import slune.airplane as airplane
      for e in tux.level:
        if isinstance(e, airplane.KillerAirplane): e.play = 0
        
    elif gnu:
      gnu.teleport(96.435836792, 28.2565994263, 144.252090454)
      gnu.look_at(Vector(gnu.level, 1.0, 0.0, -1.0))
      
    elif shark:
      shark.teleport(118.8, 26.2, 228.5)
      shark.look_at(Vector(shark.level, 0.0, 0.0, 1.0))
      
      t = LookAtLeftOfCharacterTraveling(shark)
      IDLER.camera.add_traveling(t)
      IDLER.camera.zap()
      IDLER.clear_message(); IDLER.message(_("__scenar14-outro-1__"))
      
    yield Pause()
    
    if   gnu:
      t = LookAtRightOfCharacterTraveling(gnu)
      IDLER.camera.add_traveling(t)
      IDLER.camera.zap()
      IDLER.clear_message(); IDLER.message(_("__scenar14-outro-2__"))
      
    elif shark:
      IDLER.camera.remove_traveling(t)

    yield Pause()

    if   gnu:
      IDLER.camera.remove_traveling(t)
      
    elif shark:
      IDLER.camera.add_traveling(t)
      IDLER.camera.zap()
      IDLER.clear_message(); IDLER.message(_("__scenar14-outro-3__"))

    yield Pause()
    
    if   shark:
      IDLER.camera.add_traveling(t)
      IDLER.camera.zap()
      IDLER.clear_message(); IDLER.message(_("__scenar14-outro-4__"))

    yield Pause()

    if   tux:
      t = LookAtFrontOfCharacterTraveling(tux)
      IDLER.camera.add_traveling(t)
      IDLER.camera.zap()
      IDLER.clear_message(); IDLER.message(_("__scenar14-outro-5__"))
      
    elif shark:
      IDLER.camera.remove_traveling(t)

    yield Pause()

    if   tux:
      IDLER.camera.remove_traveling(t)
      
    elif shark:
      p = Point (shark, 0.0, 0.8, 0.2)
      v = Vector(shark, 0.5, -0.6, -1.8)
      p.convert_to(shark.level)
      v.convert_to(shark.level)
      t = soya.FixTraveling(
        p + v,
        p % shark,
        1, 1)
      IDLER.camera.add_traveling(t)
      
      
      IDLER.camera.zap()
      IDLER.clear_message(); IDLER.message(_("__scenar14-outro-6__"))
      
    for i in range(10): yield Action()
    
    if shark:
      class Smoke(soya.Smoke):
        def generate(self, index):
          sx = random.random() - 0.5
          sy = random.random() - 0.5
          sz = random.random() - 0.5
          l  = (0.03 * (1.0 + random.random())) / math.sqrt(sx * sx + sy * sy + sz * sz) * 0.4
          self.set_particle(index, 1.0 + random.random(), sx * l, sy * l, sz * l, 0.0, 0.0, 0.0)

      import copy
      m = copy.deepcopy(soya.PARTICLE_DEFAULT_MATERIAL)
      m.additive_blending = 0
      p = Smoke(shark.level, m, 200, 1)
      p.set_colors((0.1, 0.1, 0.1, 1.0), (0.3, 1.0, 0.5, 1.0), (0.3, 1.0, 0.6, 1.0), (0.1, 0.1, 0.1, 1.0))
      p.set_xyz(shark.perso.x, shark.perso.y + 0.2, shark.perso.z)
      p.move(shark)
      p.y += 0.3
      p.max_particles_per_round = 1000
      p.regenerate()
      
    for i in range(20): yield Action()
    
    if shark: shark.perso.shape = soya.Shape.get("alien1")
    
    yield Pause()
    
    for i in range(50):
      if shark: shark.force.y += 15.0
      yield Action()
      
    if   shark:
      IDLER.camera.remove_traveling(t)
      shark.parent.remove(shark)
      
    elif tux:
      target = tux.perso.position()
      target.y = target.y + 0.3
      t = soya.FixTraveling(
        (target + Vector(tux.perso, 0.0, 0.4, -1.2)) % tux.level,
        target,
        1, 1)
      IDLER.camera.add_traveling(t)
      
      IDLER.camera.zap()
      IDLER.clear_message(); IDLER.message(_("__scenar14-outro-7__"))
      
    yield Pause()
    
    for i in range(50):
      if tux: tux.force.y += 15.0
      yield Action()
      
    if   tux:
      IDLER.level_completed(tux, 1)
  

class Mission15Intro(VideoSequence):
  def __call__(self, tux = None, shark = None):
    from py2play.idler  import IDLER
    
    yield Fade()
    
    if   tux:
      tux.level.start_pos = [Point(tux.level, 0.0, 0.0, 0.0), Point(tux.level, 316.0, 0.0, 316.0), ]
      
      import slune.arena
      IDLER.no_blackbands_group.insert(0, slune.arena.MiniMap(tux.level))
      
    elif shark:
      shark.teleport(78.0, 19.5, 130.7)
      shark.look_at(Vector(shark.level, 1.0, 0.0, 0.0))
      shark.set_perso("alien")
      
      #import slune.fight
      #shark.chromosom = slune.fight.CHROMOSOMS[("final_boss", shark.level.difficulty)]
      
      t1 = soya.FixTraveling(
        shark.perso + Vector(shark.perso, 0.0, 0.0, -0.6),
        Point(shark.perso, 0.0, 0.8, 0.0),
        1, 1)
      
      IDLER.camera.add_traveling(t1)
      IDLER.camera.zap()
      IDLER.clear_message(); IDLER.message(_("__scenar15-intro-1__"))
      
    yield Pause()
    
    if   shark:
      IDLER.camera.remove_traveling(t1)

      pos = Point(shark.perso, 0.3, 1.0, 0.0)
      t2 = soya.FixTraveling(
        pos + Vector(shark.perso, 0.5, 0.0, -0.5),
        pos,
        1, 1)
      
      IDLER.camera.add_traveling(t2)
      IDLER.clear_message(); IDLER.message(_("__scenar15-intro-2__"))
      
    yield Pause()
    
    if   shark:
      IDLER.camera.remove_traveling(t2)
      
      pos = Point(shark.perso, -0.3, 1.0, 0.0)
      t3 = soya.FixTraveling(
        pos + Vector(shark.perso, -0.5, 0.0, -0.5),
        pos,
        1, 1)
      
      IDLER.camera.add_traveling(t3)
      IDLER.clear_message(); IDLER.message(_("__scenar15-intro-3__"))
      
    yield Pause()
    yield Fade()
    
    if   tux:
      t = LookAtRightOfCharacterTraveling(tux); IDLER.camera.add_traveling(t)
      IDLER.camera.zap()
      IDLER.clear_message(); IDLER.message(_("__scenar15-intro-4__"))
      
    elif shark:
      IDLER.camera.remove_traveling(t3)

    yield Pause()
    yield Fade()
    
    if   tux:
      IDLER.camera.remove_traveling(t)
      
    elif shark:
      IDLER.camera.add_traveling(t1)
      IDLER.camera.zap()
      IDLER.clear_message(); IDLER.message(_("__scenar15-intro-5__"))

    yield Pause()
    
    if   shark:
      IDLER.camera.remove_traveling(t1)
      
      IDLER.no_blackbands_group.add(slune_character.BossLifeBar(shark))
      
    if   tux and tux.player.active: # Do this once
      IDLER.clear_message()
      
      class Checker(soya.Volume):
        def __init__(self, parent):
          soya.Volume.__init__(self, parent)
          
        def begin_round(self):
          if len(tux.level.characters) == 1:
            Mission15Outro().start(tux = tux)
            self.parent.remove(self)
            
      Checker(tux.level)
      
      
class Mission15Outro(VideoSequence):
  def __call__(self, tux = None, shark = None):
    from py2play.idler  import IDLER
    
    yield Fade()
    
    if   tux:
      shark = soya.Volume(tux.level, soya.Shape.get("alien1"))
      shark.set_xyz(127.4, 20.6, 53.2)
      shark.rotate_vertical(-90.0)
      
      p = Point(shark, 0.0, 0.0, 0.2)
      t1 = soya.FixTraveling(
        p + Vector(shark, 1.0, 0.8, 0.2),
        p,
        1, 1)
      
      IDLER.camera.add_traveling(t1)
      IDLER.camera.zap()
      IDLER.clear_message(); IDLER.message(_("__scenar15-outro-1__"))
      
      light = soya.Light(tux.level)
      light.move(soya.Point(IDLER.camera, -0.1, 1.0, 2.0))
      light.cast_shadow = 0
      light.constant  = 0.0
      light.quadratic = 0.2
      
    yield Pause()
    yield Fade()
    
    if   tux:
      IDLER.camera.remove_traveling(t1)
      
      t = LookAtLeftOfCharacterTraveling(tux); IDLER.camera.add_traveling(t)
      IDLER.camera.zap()
      IDLER.clear_message(); IDLER.message(_("__scenar15-outro-2__"))
      
    yield Pause()
    yield Fade()
    
    if   tux:
      IDLER.camera.remove_traveling(t)
      IDLER.camera.zap()
      GnuSpeech([_("__scenar15-outro-3__")], 0).start(tux = tux)
      
    yield Pause()
    yield Fade()
    
    if   tux:
      IDLER.camera.add_traveling(t1)
      IDLER.camera.zap()
      IDLER.clear_message(); IDLER.message(_("__scenar15-outro-4__"))
      
    yield Pause()

    if   tux:
      IDLER.clear_message(); IDLER.message(_("__scenar15-outro-5__"))
      
    yield Pause()
    
    if   tux:
      GnuSpeech([_("__scenar15-outro-6__")], 0).start(tux = tux)
      
      IDLER.camera.remove_traveling(t1)
    IDLER.level_completed(tux, 1)
      
