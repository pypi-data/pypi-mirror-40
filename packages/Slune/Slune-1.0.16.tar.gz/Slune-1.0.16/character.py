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

import struct, math, random
import py2play.action as action, py2play.character as py2play_character
#from py2play import recvall
import soya, soya.ray as ray, soya.widget as widget

from soya import Point, Vector
import slune.globdef as globdef, slune.sound as sound

ACTION_WAIT      = action.ACTION_WAIT
ACTION_JUMP      = "j"
ACTION_TURBO     = "t"
ACTION_ROTUP     = "u"
ACTION_ROTDOWN   = "d"
ACTION_ROTLAT    = "l"
ACTION_DEBUG     = "°"
ACTION_STARTGAME = "!"

class Action:
  def __init__(self, action = ACTION_WAIT, mouse_x = 0.0, mouse_y = 1.0, round = None):
    self.round   = round
    self.action  = action
    self.mouse_x = mouse_x
    self.mouse_y = mouse_y
    
  def __repr__(self):
    return "<Action %s at round %s, (%s, %s)>" % (self.action, self.round, self.mouse_x, self.mouse_y)
  

from socket import MSG_WAITALL


#def WRITE_ACTION(socket, action):
#  socket.sendall(struct.pack("!cddi", action.action, action.mouse_x, action.mouse_y, action.round))
  
#def READ_ACTION(socket):
#  return Action(*struct.unpack("!cddi", recvall(socket, 21)))

action.Action       = Action
#action.READ_ACTION  = READ_ACTION
#action.WRITE_ACTION = WRITE_ACTION

RIGHT  = Vector(None, 1.0,  0.0,  0.0)
DOWN   = Vector(None, 0.0, -1.0,  0.0)
UP     = Vector(None, 0.0,  1.0,  0.0)
FRONT  = Vector(None, 0.0,  0.0, -1.0)

# Re-useable Points and Vectors

_P  = Point()
_P2 = Point()
_P3 = Point()
_V  = Vector()
_V2 = Vector()

VEHICLE_PERSO_COORDS = [
  (0.0, 0.1 , 0.03),
  (0.0, 0.1 , 0.03),
  (0.0, 0.4 , -0.2),
  (0.0, 0.3 , 0.35),
  (0.0, 0.48, 0.0),
  ]

class Pusher: pass
class Competitor: pass

class Character(soya.World, Pusher):
  nitro_enabled  = 1
  push_fly       = 0.3
  context        = None
  
  def get_force(self   ): return self.__dict__["force"]
  def set_force(self, f): self.__dict__["force"] = f
  force = property(get_force, set_force)
  
  def __init__(self, parent = None):
    soya.World.__init__(self, parent)
    
    self.radius      = 0.7
    self.floating    = 0.3
    self.weight      = 1.0
    self.rotup_speed = 7.0
    self.mode_grip   = 0
    self.gripped     = 0
    self.rot_vert = 0.0
    self.speed  = Vector(self)
    self.force  = Vector(None)
    self.solid  = 0
    self.nitro = None
    self.nitro_time = 0
    self.flame_thrower = 0
    self.flame_throw_time = 0
    
    self.camera_target = self
    self.old_speed_x = 0.0
    self.context = None
    self.on_ground = 0
    self.was_on_ground = 0
    self.vertical_angle = 0.0
    self.platform_speed = None
    
    self.CENTER = Point(self, 0.0, 0.3,  0.0)
    
    self.scramble = 0.0
    self.next_pos = Point(self, 0.0, 0.0, 0.0)
    
    self.internal = soya.World(self)
    self.perso    = soya.Volume(self.internal)
    
    self.perso_name = None
    self.vehicle = 1
    self.life  = 1.0
    self.pushed_by = None
    
    # IA stuff
    self.jumping   = 0.0
    self.max_speed = 1.0
    self.current_action = Action()
    self.speed.y = 0.01 # Avoid null speed (null speed => jumping for AI). The speed will be overrided later.
    self.check_ground_vector = Vector(self, 0.0, -1.0, -2.0)
    
    # blam hack to test raypicking
    #import soya.laser
    #laser = soya.laser.Laser(self)
    #laser.rotate_vertical(-90.0)
    #laser.reflect = 1
    
    
  def __getstate__(self):
    state = soya.World.__getstate__(self)
    if state[1] is self.__dict__: state = state[0], state[1].copy()
    del state[1]["context"]
    return state
  def __setstate__(self, state):
    state = soya.World.__setstate__(self, state)
    self.context = None
    
  def set_perso(self, perso_name):
    self.perso_name = perso_name
    self.perso.set_shape(soya.Shape.get(self.perso_name + "1"))
    
  def displayname(self): return self.perso_name.title()
  
  def set_vehicle(self, vehicle, add_ray = 1):
    self.vehicle = vehicle
    self.internal.set_shape(soya.Shape.get("vehicle" + str(self.vehicle)))
    if hasattr(self, "ray"):
      self.internal.remove(self.ray)
      del self.ray
    if hasattr(self, "ray2"):
      self.internal.remove(self.ray2)
      del self.ray2
      
    if   vehicle == 0:
      self.radius      = 0.7
      self.floating    = 0.5
      self.weight      = 1.3
      self.maxspeedx   = 0.8
      self.maxspeedz   = 0.98
      self.rotup_speed = 7.0
      self.mode_grip   = 0
      
      if add_ray:
        self.ray = ray.Ray(self.internal, RAY_MATERIAL2)
        self.ray.set_xyz(-0.84, 0.10, 0.0)
        self.ray.endpoint.set_xyz(0.45, 0.0, 0.0)
        self.ray.length = 20
        
        self.ray2 = ray.Ray(self.internal, RAY_MATERIAL2)
        self.ray2.set_xyz(0.84, 0.10, 0.0)
        self.ray2.endpoint.set_xyz(-0.45, 0.0, 0.0)
        self.ray2.length = 20
        
    elif vehicle == 1:
      self.radius      = 0.7
      self.floating    = 0.3
      self.weight      = 1.0
      self.maxspeedx   = 1.0
      self.maxspeedz   = 1.0
      self.rotup_speed = 8.0
      self.mode_grip   = 0
      
      if add_ray:
        self.ray = ray.Ray(self.internal, RAY_MATERIAL)
        self.ray.set_xyz(-0.3, 0.15, 0.5)
        self.ray.endpoint.set_xyz(0.6, 0.0, 0.0)
        self.ray.length = 20
        
    elif vehicle == 2:
      self.radius      = 0.8
      self.floating    = 0.3
      self.weight      = 1.6
      self.maxspeedx   = 0.9
      self.maxspeedz   = 0.95
      self.rotup_speed = 6.0
      self.mode_grip   = 0
      
      if add_ray:
        self.ray = ray.Ray(self.internal, RAY_MATERIAL2)
        self.ray.set_xyz(-0.5, 0.2, 1.0)
        self.ray.endpoint.set_xyz(1.0, 0.0, 0.0)
        self.ray.length = 20
        
    elif vehicle == 3:
      self.radius      = 0.7
      self.floating    = 0.3
      self.weight      = 0.6
      self.maxspeedx   = 1.0
      self.maxspeedz   = 1.0
      self.rotup_speed = 9.0
      self.mode_grip   = 1
      self.DOWN = Vector(self, 0.0, -1.0, 0.0)
      
      if add_ray:
        self.ray = ray.Ray(self.internal, RAY_MATERIAL2)
        self.ray.set_xyz(0.0, 0.07, 0.65)
        self.ray.endpoint.set_xyz(0.0, 0.3, 0.0)
        self.ray.length = 20
        
    elif vehicle == 4:
      self.radius      = 1.0
      self.floating    = 0.5
      self.weight      = 2.2
      self.maxspeedx   = 0.7
      self.maxspeedz   = 0.8
      self.rotup_speed = 4.0
      self.mode_grip   = 0
      self.DOWN = Vector(self, 0.0, -1.0, 0.0)
      
      if add_ray:
        self.ray = ray.Ray(self.internal, RAY_MATERIAL3)
        self.ray.set_xyz(-0.6, 0.35, 0.6)
        self.ray.endpoint.set_xyz(1.2, 0.0, 0.0)
        self.ray.set_xyz(-0.95, -0.4, 0.0)
        self.ray.endpoint.set_xyz(1.9, 0.0, 0.0)
        self.ray.length = 10
        
    self.perso.set_xyz(*VEHICLE_PERSO_COORDS[vehicle])
    self.perso_y = self.perso.y
    
  def add_headlight(self):
    light = self.light = soya.Light(self)
    light.set_xyz(0.0, 1.2, -0.5)
    light.diffuse     = (0.5, 0.6, 1.0, 1.0)
    light.specular    = (0.0, 0.0, 0.0, 1.0)
    light.quadratic   = 0.0
    light.linear      = 0.07
    light.constant    = 0.0
    light.exponent    = 3.0
    light.angle       = 90.0
    light.cast_shadow = 0
    
  def init(self): pass
  
  def default_mouse_x(self): return 0.0
    
  def set_level(self, level, init = 0):
    level.add(self)
    
    super(Character, self).set_level(level, init)
    
  def begin_action(self, action):
    from py2play.idler import IDLER as root
    
    speed = self.speed
    force = self.force
    
    self.internal.rotate_incline((self.old_speed_x - speed.x) *  6000.0)
    self.perso   .rotate_lateral((self.old_speed_x - speed.x) * 12000.0)
    self.old_speed_x = speed.x
    self.turn_lateral(-500.0 * speed.x)
    
    if self.flame_throw_time: self.flame_throw_time -= 1
    if self.nitro_time:
      self.nitro.set_sizes((
        1.0 - (10 - self.nitro_time) / 15.0,
        1.0 - (10 - self.nitro_time) / 15.0,
        ))
      self.nitro_time -= 1
      if not self.nitro_time:
        self.nitro.auto_generate_particle = 0
        
    self.life = min(1.0, self.life + 0.0003)
    
    if   action.action == ACTION_ROTUP  : self.turn_vertical( self.rotup_speed)
    elif action.action == ACTION_ROTDOWN: self.turn_vertical(-self.rotup_speed)
    elif action.action == ACTION_ROTLAT : self.rotate_lateral(30.0)
    elif (action.action == ACTION_TURBO) and (self.flame_throw_time == 0):
      if self.flame_thrower and ((not self.nitro) or not self.nitro.auto_generate_particle):
        self.flame_thrower -= 1
        self.flame_throw_time = 50
        flame_thrower = FlameThrower(self)
        
      elif self.nitro_enabled:
        length = force.length()
        d = 0.09 * max(0.0, (1.0 - length))
        if self.life > d:
          force.add_vector(Vector(self, 0.0, 0.0, -2.0) % root)
          force.set_length(max(1.0, length))
          self.life -= 0.08 * max(0.0, (1.0 - length))
          if self.nitro is None:
            self.nitro = Nitro(self)
            sound.play("nitro-1.wav", self)
          elif not self.nitro.auto_generate_particle:
            self.nitro.auto_generate_particle = 1
            sound.play("nitro-1.wav", self)
          self.nitro.set_sizes((1.0, 1.0))
          self.nitro_time = 10
          
    elif action.action == ACTION_DEBUG  :
      print self.position(), self.round
      print self.level.parent.camera.position(), Point(self.level.parent.camera, 0.0, 0.0, -1.0) % self.get_root()
      self.hurt(2.0)
      poqjfcpjk
      
    elif (action.action == ACTION_JUMP) and self.was_on_ground:
      force.y       += 0.4
      self.rot_vert += 0.4
      
    if self.context:
      self.was_on_ground = self.on_ground
      
      if   self.context.raypick(self.CENTER, DOWN, self.floating + 0.45, 1, 1, _P, _V):
        self.on_ground = 1
        self.gripped   = 0
      elif self.mode_grip and self.context.raypick(self.CENTER, self.DOWN, 6.0 * self.speed.length(), 1, 1, _P, _V):
        self.on_ground = self.gripped = 1
      else:
        self.on_ground = self.gripped = 0

    if self.context and self.on_ground:
      _P.convert_to(self.parent)
      
      if (self.y < _P.y + self.floating - force.y):
        if (not self.scramble) and self.parent:
          self.scramble = min(30.0, ((force.y + self.parent.transform_vector(speed.x, speed.y, speed.z, self)[1]) * 7.0) ** 2)
          
          #if (self.scramble > 2) and (-20.0 < self.y < 20.0):
          #  Snow(self.level).move(self)

        # "force.y = _P.y + self.floating - self.y" give better visual effect, but clashes
        # with mode grip.
        if self.gripped: force.y = 0.0
        else: force.y = _P.y + self.floating - self.y
        
      elif self.y > _P.y + self.floating + 0.1: force.y -= 0.03
      
      if force.y < 0.2:
        if (action.action != ACTION_ROTUP) and (action.action != ACTION_ROTDOWN):
          _V.convert_to(self)
          
          if _V.y < -0.3: self.turn_incline(10.0)
          elif (_V.y < 0.996) and _V.y:
            #soya.cross_vector(_V, UP, _V2)
            _V.cross_product(UP, _V2)
            _V2.convert_to(self.parent)
            self.vertical_angle = -_V.angle_to(UP)
            self.rotate_axe(self.vertical_angle / 3.0, _V2)
            #self.rotate_axe(-_V.angle_to(UP) / 4.0, _V2.x, _V2.y, _V2.z)
    else:
      force.y -= 0.03 # comment this line if you want to fly
      if self.y < -35.0: self.hurt(1.0)
      
    force.__imul__(0.95)
    
    if self.rot_vert > 0.0:
      self.turn_vertical(self.rot_vert * 14.0)
      self.rot_vert -= 0.03
      
    x, y, z = self.transform_vector(force.x, force.y, force.z, self.parent)
    speed.x += x
    speed.y += y
    speed.z += z
    
    if speed.length() > 0.75: speed.set_length(0.75)
    
    for character in self.level.pushables:
      if not character is self:
        if self.distance_to(character) < self.radius + character.radius:
          _V.set_start_end(self, character)
          
          f = 3.0 * max(0.0, _V.dot_product(self.speed)) * self.weight / character.weight
          if f:
            _V.set_length(f)
            character.push(_V.x, _V.y + character.push_fly * f, _V.z, self)
            f = -0.3 * character.weight / self.weight
            self.push(f * _V.x, f * _V.y, f * _V.z, character)
            
    _P2.__init__(self, 0.0, 0.3, 0.0)
    _P2.add_vector(speed)
    _P2.convert_to(root)

    self.context = root.RaypickContext(_P2, max(self.radius, 0.7) + 0.5, self.context)
    bouree = 0
    
    
    for vec in (RIGHT, FRONT):
      if self.context.raypick(_P2, vec, self.radius, 0, 0, _P, _V):
        _P.convert_to(root)
        _V.convert_to(root)
        
        #a = _V.cross_product(Vector(self, 0.0, 1.0, 0.0)) % root
        #print a
        #self.turn_axe(-15.0, a.x, a.y, a.z)
        
        if vec.dot_product(_V) > 0.0: _P3.__init__(root, _P2.x - self.radius * vec.x, _P2.y - self.radius * vec.y, _P2.z - self.radius * vec.z)
        else:                         _P3.__init__(root, _P2.x + self.radius * vec.x, _P2.y + self.radius * vec.y, _P2.z + self.radius * vec.z)
        
        if force.dot_product(_V) < 0.0:
          if abs(force.x) + abs(force.z) > 0.1: # Else force is only due to gravity!
            _V2.clone(_V)
            _V2.set_length(-2.0 * force.dot_product(_V2))
            force += _V2
            force *= 0.5
            
          bouree = 1
          
        if (_P.x - _P2.x) * _V.x + (_P.y - _P2.y) * _V.y + (_P.z - _P2.z) * _V.z > 0.0:
          _V.set_start_end(_P2, _P)
        else: _V.set_start_end(_P3, _P)
        
        _P2  .__iadd__(_V)
        speed.__iadd__(_V)
        
    _P2.y += 0.2
    if self.context.raypick(_P2, DOWN, 0.7, 0, 1, _P, _V):
      _P.convert_to(root)
      _V.convert_to(root)
      if DOWN.dot_product(_V) > 0.0: _P3.__init__(root, _P2.x - self.radius * DOWN.x, _P2.y - self.radius * DOWN.y, _P2.z - self.radius * DOWN.z)
      else:
        if force.y > 0.0: force.y = 0.0 # Stop and break a jump
        _P3.__init__(root, _P2.x + self.radius * DOWN.x, _P2.y + self.radius * DOWN.y, _P2.z + self.radius * DOWN.z)
      if force.dot_product(_V) < -0.4:
        bouree = 1
      
      _V.set_start_end(_P3, _P)
      
      #_P2   .__iadd__(_V) # Useless since it is the last raypicking.
      speed.__iadd__(_V)
      
    #if bouree and not self.nitro.auto_generate_particle:
    if bouree:
      couic = min(0.5, force.x ** 2 + force.z ** 2) * 0.8
      if couic > 0.01:
        #force.x = force.z = 0.0
        
        if self.hurt(couic) and (len(explosions) < 4): # Limit the number of simultaneous explosions
          explode = Explosion(self.parent)
          explode.move(self)
          sound.play("explose-1.wav", explode)
          
    self.next_pos.clone(speed)
    self.next_pos.convert_to(self.parent)
    self.next_pos.parent = None
    
  def push(self, x, y, z, pusher = None, play_sound = 1):
    if play_sound: sound.play("push-1.wav", self)
    
    from py2play.idler import IDLER
    def f():
      self.force.add_xyz(x, y, z)
      self.rot_vert += max(0.0, y)
    IDLER.next_round_tasks.append(f)
    
    self.pushed_by = pusher
    
  def end_round(self):
    # Restore the real position -- advance_time may cause rounding error on the position !!!
    self.move(self.next_pos)
    if self.platform_speed:
      self += self.platform_speed
      self.platform_speed = None
      
  def advance_time(self, proportion):
    soya.World.advance_time(self, proportion)
    
    self.add_mul_vector(proportion, self.speed)
    
    if self.scramble:
      if self.scramble <= proportion:
        self.internal.y = 0.0
        self.scramble   = 0.0
      else:
        self.internal.y = abs(math.sin(self.scramble)) * self.scramble * 0.04
        self.scramble  -= proportion / 3.0
      self.perso.y = self.perso_y + self.internal.y
      
  def teleport(self, x, y, z):
    self.set_xyz(x, y, z)
    self.force.set_xyz(0.0, 0.0, 0.0)
    if self.scramble:
      self.scramble   = 0.0
      self.internal.y = 0.0
      self.perso.y    = self.perso_y
    if hasattr(self, "ray" ): self.ray .zap()
    if hasattr(self, "ray2"): self.ray2.zap()
    self.context = None # The raypick context is no longer valid !!!
    
  def hurt(self, life):
    """Kills LIFE life to this character. Returns true if the character is still alive."""
    self.life -= life
    if self.life < 0.0: self.die()
    else: return 1
    
  def die(self): 
    explode = Explosion(self.parent)
    explode.move(self)
    explode.life = 60
    explode.particle_width = explode.particle_height = 0.7
    
    sound.play("explose-3.wav", explode)
    self.level.remove_character(self)

class NonPlayerCharacter(Character, py2play_character.NonPlayerCharacter):
  clan = 0
  
  def __init__(self, parent = None):
    py2play_character.NonPlayerCharacter.__init__(self)
    Character.__init__(self, parent)
    
    import slune.controler
    self.controler = slune.controler.StackControler([self.IAControler()])
    
  def choose_action(self):
    return self.controler.next()
  
  def begin_round(self):
    py2play_character.NonPlayerCharacter.begin_round(self)
    Character.begin_round(self)
    
  def begin_action(self, action):
    self.speed.set_xyz(action.mouse_x / 120.0 * self.maxspeedx, 0.0, (action.mouse_y * 0.2 - 0.2) * self.maxspeedz)
    
    Character.begin_action(self, self.current_action)
    
  def __getstate__(self):
    state = Character.__getstate__(self)
    del state[0]["controler"]
    return state
  def __setstate__(self, state):
    state = Character.__setstate__(self, state)
    import slune.controler
    self.controler = slune.controler.StackControler([self.IAControler()])
    
  def IAControler(self):
    while 1: yield Action() # Does nothing !
    
  
class Pushable(soya.Volume, Pusher):
  clan           = 0
  bonus_chance   = 0.15
  bonus_type     = 0
  on_bourre      = None
  push_fly       = 0.3
  
  def get_force(self   ): return self.__dict__["force"]
  def set_force(self, f): self.__dict__["force"] = f
  force = property(get_force, set_force)
  
  def __init__(self, parent = None):
    soya.Volume.__init__(self, parent)
    
    self.radius      = 1.0
    self.radius_y    = 1.0
    self.weight      = 1.0
    self.life        = 1.0
    self.on_ground   = 1 # 0 ???
    
    self.speed       = Vector(self)
    self.force       = Vector(None)
    self.solid       = 0
    self.worth_playing = 0
    
    self.CENTER = Point(self, 0.0, 0.3,  0.0)
    
    self.next_pos = Point(self, 0.0, 0.0, 0.0)
    
  def begin_round(self):
    soya.Volume.begin_round(self)
    
    force = self.force
    if not self.worth_playing:
      if (abs(force.x) > 0.1) or (abs(force.y) > 0.1) or (abs(force.z) > 0.1):
        self.worth_playing = 1
        if self.on_bourre:
          if self.on_bourre == "win":
            from videosequence import MissionCompleted, PLAYER
            MissionCompleted(1).start(tux = PLAYER)
            
            from py2play.idler import IDLER
            IDLER.camera.add_traveling(soya.ThirdPersonTraveling(self))
            
          else: self.on_bourre()
      else: return
      
    speed = self.speed
    speed.set_xyz(0.0, 0.0, 0.0)
    
    from py2play.idler import IDLER as root
    
    if root.raypick(self.CENTER, DOWN, self.radius_y / 2.0 + 0.45, 1, 1, _P, _V):
      _P.convert_to(self.parent)
      self.on_ground = 1
      
      if (self.y < _P.y + self.radius_y / 2.0 - self.force.y):
        force.y = 0.0
        self.force.y += _P.y + self.radius_y / 2.0 - self.y
      elif self.y > _P.y + self.radius_y / 2.0 + 0.1: force.y -= 0.03
      
      if self.force.y < 0.05:
        _V.convert_to(self)
        
        if _V.y < 0.0: self.turn_incline(10.0)
        elif _V.y < 0.999:
          _V.cross_product(UP, _V2)
          _V2.convert_to(self.parent)
          angle = _V.angle_to(UP)
          self.rotate_axe(-angle / 4.0, _V2)
        else:
          self.worth_playing = 0
          
    else:
      self.on_ground = 0
      force.y -= 0.03
      if self.y < -35.0: self.die()
      
    force.__imul__(0.95)
    
    if force.y > 0.0: self.turn_vertical(force.y * 14.0)
    
    x, y, z = self.transform_vector(force.x, force.y, force.z, self.parent)
    speed.x += x
    speed.y += y
    speed.z += z
    
    if speed.length() > 0.5: speed.set_length(0.5)
    
    if self.parent:
      for character in self.parent.pushables:
        if not character is self:
          if self.distance_to(character) < self.radius + character.radius:
            _V.set_start_end(self, character)

            _V.y += character.push_fly
            f = 2.5 * max(0.0, _V.dot_product(self.speed))
            if f:
              _V.set_length(f * self.weight / character.weight)
              character.push(_V.x, _V.y, _V.z, self)
            
    _P2.__init__(self, 0.0, self.radius_y / 2.0, 0.0)
    _P2.add_vector(speed)
    _P2.convert_to(root)
    
    context = root.RaypickContext(_P2, max(self.radius, 0.7))
    
    bouree = 0
    
    for vec in (RIGHT, FRONT):
      if context.raypick(_P2, vec, self.radius, 0, 0, _P, _V):
        _P.convert_to(root)
        _V.convert_to(root)
        if vec.dot_product(_V) > 0.0: _P3.__init__(root, _P2.x - self.radius * vec.x, _P2.y - self.radius * vec.y, _P2.z - self.radius * vec.z)
        else:                        _P3.__init__(root, _P2.x + self.radius * vec.x, _P2.y + self.radius * vec.y, _P2.z + self.radius * vec.z)
        
        if force.dot_product(_V) < 0.0:
          _V2.clone(_V)
          _V2.set_length(-2.0 * force.dot_product(_V2))
          force += _V2
          #force *= 0.5
          
          bouree = 1
          
        if (_P.x - _P2.x) * _V.x + (_P.y - _P2.y) * _V.y + (_P.z - _P2.z) * _V.z > 0.0:
          _V.set_start_end(_P2, _P)
        else: _V.set_start_end(_P3, _P)
        
        _P2  .__iadd__(_V)
        speed.__iadd__(_V)
        
    _P2.y += 0.2
    if context.raypick(_P2, DOWN, self.radius_y, 0, 1, _P, _V):
      _P.convert_to(root)
      _V.convert_to(root)
      if DOWN.dot_product(_V) > 0.0: _P3.__init__(root, _P2.x - self.radius_y * DOWN.x, _P2.y - self.radius_y * DOWN.y, _P2.z - self.radius_y * DOWN.z)
      else:
        if force.y > 0.0: force.y = 0.0 # Stop and break a jump
        _P3.__init__(root, _P2.x + self.radius_y * DOWN.x, _P2.y + self.radius_y * DOWN.y, _P2.z + self.radius_y * DOWN.z)
        
      if force.dot_product(_V) < 0.0: bouree = 1
      
      _V.set_start_end(_P3, _P)
      
      #_P2   .__iadd__(_V) # Useless since it is the last raypicking.
      speed.__iadd__(_V)
      
    if bouree:
      couic = min(0.5, force.x ** 2 + force.z ** 2)
      if couic > 0.01:
        #force.x = force.z = 0.0
        
        if self.hurt(couic) and (len(explosions) < 4): # Limit the number of simultaneous explosions
          explode = Explosion(self.parent, nb_particles = 15)
          sound.play("explose-1.wav", explode)
          explode.move(self)
          
    self.next_pos.clone(speed)
    self.next_pos.convert_to(self.parent)
    self.next_pos.parent = None
    
  def push(self, x, y, z, pusher = None, play_sound = 1):
    if play_sound: sound.play("push-2.wav", self)
    from py2play.idler import IDLER
    IDLER.next_round_tasks.append(lambda : self.force.add_xyz(x, y, z))
    
  def end_round(self):
    if self.worth_playing:
      # Restore the real position -- advance_time may cause rounding error on the position !!!
      self.move(self.next_pos)
      
  def advance_time(self, proportion):
    if self.worth_playing:
      self.add_mul_vector(proportion, self.speed)
      
  def hurt(self, life):
    """Kills LIFE life to this character. Returns true if the character is still alive."""
    
    self.life -= life
    if self.life < 0.0: self.die()
    else: return 1
    
  def die(self):
    explode = Explosion(self.parent, nb_particles = 20)
    explode.move(self)
    explode.life = 30
    explode.particle_width = explode.particle_height = 0.7
    
    if self.bonus_type:
      import slune.level as slune_level
      if   self.bonus_type == 1: bonus = slune_level.LifeBonus(self.parent)
      elif self.bonus_type == 2: bonus = slune_level.FlameThrowerBonus(self.parent)
      bonus.move(self)
      bonus.come_back = 0
      self.parent.bonuss.append(bonus)
      sound.play("explose-2.wav", explode)
    else:
      sound.play("explose-2.wav", explode)
    
    self.parent.pushables.remove(self)
    self.parent.remove(self)
    
def Barrier(parent, p = None):
  p = p or Pushable(parent)
  p.set_shape(soya.Shape.get("gate3"))
  p.radius_y = 0.5
  p.life     = 0.5
  p.weight   = 0.6
  return p
def Barrier2(parent, p = None):
  p = p or Pushable(parent)
  p.set_shape(soya.Shape.get("gate4"))
  p.radius_y = 0.5
  p.life     = 0.5
  p.weight   = 0.6
  return p
def TreeTrunc(parent, p = None):
  p = p or Pushable(parent)
  p.set_shape(soya.Shape.get("tree_trunc"))
  p.radius   = 2.0
  p.radius_y = 0.3
  p.life     = 2.0
  p.weight   = 1.2
  return p
def Quille(parent, p = None):
  p = p or Pushable(parent)
  p.set_shape(soya.Shape.get("quille-1"))
  p.radius   = 0.7
  p.radius_y = 0.7
  p.life     = 0.1
  p.weight   = 0.4
  return p
def Ball(parent, p = None):
  p = p or Pushable(parent)
  p.set_shape(soya.Shape.get("ball1"))
  p.radius   = 0.9
  p.radius_y = 0.9
  p.life     = 50.0
  p.weight   = 0.1
  p.bonus_chance = 0.0
  return p


class TakeableVehicle(soya.Volume):
  radius = 5.0
  
  def __init__(self, parent = None, vehicle = 3):
    soya.Volume.__init__(self, parent)
    self.set_vehicle(vehicle)
    self.disabled = {}
    self.changing = 0
    self.solid    = 0
    
  def set_vehicle(self, vehicle):
    self.vehicle = vehicle
    self.set_shape(soya.Shape.get("vehicle" + str(self.vehicle)))
    
  def disable(self, character):
    self.disabled[character] = 1
    self.changing = 0
    
  def begin_round(self):
    soya.Volume.begin_round(self)
    
    if not self.changing:
      for character in self.parent.characters:
        if isinstance(character, PlayerCharacter):
          if self.disabled.get(character, 0):
            if (self.distance_to(character) > self.radius * 2.0): del self.disabled[character]
          elif (self.distance_to(character) < self.radius):
            self.changing = 1 # Avoid 2 changing at the same time !!!
            from videosequence import ChangeVehicle
            ChangeVehicle(character, self).start(character = character)
            
class Remorque(NonPlayerCharacter, py2play_character.NonPlayerCharacter):
  clan = 0
  
  def __init__(self, parent = None, remorqued_by = None, remorqued_distance = 1.5):
    py2play_character.NonPlayerCharacter.__init__(self)
    NonPlayerCharacter.__init__(self, parent, 0)
    
    self.remorqued_by       = remorqued_by
    self.remorqued_distance = remorqued_distance
    
    self.set_vehicle(1)
    
  def begin_action(self, action):
    self.current_action = Action()
    self.speed.set_xyz(0.0, 0.0, 0.0)
    
    if self.remorqued_by:
      _V.set_start_end(self, self.remorqued_by)
      _V.convert_to(self)
      _V.set_length(_V.length() - self.remorqued_distance)
      if _V.length() > 0.48: _V.set_length(0.48)
      _V.y = _V.y - self.force.y
      self.speed.set_xyz(_V.x / 20.0, _V.y, _V.z)
    else:
      self.speed.set_xyz(0.0, 0.0, 0.0)
      
    Character.begin_action(self, self.current_action)
    
RAY_MATERIAL = soya.Material()
RAY_MATERIAL.diffuse = (0.7, 0.4, 0.95, 1.0)
RAY_MATERIAL.additive_blending = 1

RAY_MATERIAL2 = soya.Material()
RAY_MATERIAL2.diffuse = (0.9, 0.6, 0.3, 1.0)
RAY_MATERIAL2.additive_blending = 1

RAY_MATERIAL3 = soya.Material()
RAY_MATERIAL3.diffuse = (0.0, 0.0, 0.9, 1.0)
RAY_MATERIAL3.additive_blending = 1

def PlayerLight(parent):
  return None
  light = soya.Light(parent)
  light.set_xyz(0.0, 1.2, -0.5)
  light.diffuse   = (0.5, 0.6, 1.0, 1.0)
  light.specular  = (0.0, 0.0, 0.0, 1.0)
  light.quadratic = 0.005
  light.linear    = 0.2
  light.constant  = 0.0
  light.exponent  = 1.0
  
  light.look_at(Vector(parent, 0.0, 0.0, -1.0))
  
  light.angle = 90.0
  
  return light

class PlayerCharacter(Character, py2play_character.PlayerCharacter, Competitor):
  clan = 1
  
  def __init__(self, player = None):
    py2play_character.PlayerCharacter.__init__(self, player)
    Character.__init__(self)
    
    if player: player.default_action = action.ACTION_WAIT
    
    self.set_perso  (globdef.CHARACTER.lower())
    self.set_vehicle(globdef.VEHICLE)
    
    #self.light = PlayerLight(self)
    
    if globdef.VERIFICATION_SERVER and self.player: self.logon_verif()
    
  def displayname(self): return self.perso_name.title() + " (" + self.player.name + ")"
  
  def default_mouse_x(self):
    if self.controler.uncancelable_controler: return 0.0
    return self.player.controler.mouse_x
  
  def logon_verif(self):
    """Log on the verif server."""
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((globdef.VERIFICATION_SERVER, 36081))
    self.player.verif = s.makefile("w", 0)
    self.player.verif.write("P") # Check position
    
  def begin_round(self):
    if self.player.active: self.plan_action(self.player.controler.next())
    else:                  self.controler.next()
    
    py2play_character.PlayerCharacter.begin_round(self)
    Character.begin_round(self)
    
  def begin_action(self, action):
    if globdef.VERIFICATION_SERVER:
      import cPickle as pickle
      pickle.dump((self.player.name, self.round, (self.x, self.y, self.z), None), self.player.verif)
      
    # Compute the speed
    #self.speed.set_xyz(action.mouse_x / 120.0 * self.maxspeedx, 0.0, (action.mouse_y * 0.2 - 0.28)  * self.maxspeedz)
    self.speed.set_xyz(action.mouse_x / 120.0 * self.maxspeedx, 0.0, (action.mouse_y * 0.2 - 0.2)  * self.maxspeedz)
    
    if action.action == ACTION_STARTGAME:
      from py2play.idler import IDLER
      if IDLER.waiting_until_ready: IDLER.start_game()
      else:                         IDLER.unpause()
      
    Character.begin_action(self, action)
    
  def get_controler(self):
    return self.player.controler
    if self.player.active: return self.player.controler
    return None
  controler = property(get_controler)
  
  def hurt(self, life):
    if   self.level.difficulty == 0: return Character.hurt(self, 0.6 * life)
    elif self.level.difficulty == 1: return Character.hurt(self, 0.9 * life)
    else:                            return Character.hurt(self, life)
    
  def die(self):
    if len(explosions) < 4: # Limit the number of simultaneous explosions
      explode = Explosion(self.parent)
      explode.move(self)
      explode.life = 60
      explode.particle_width = explode.particle_height = 0.7
      
      sound.play("explose-3.wav", explode)
      
    oldlevel = self.level
    self.level.remove_character(self)
    self.player.level = oldlevel # May be required !!!
    
    if self.player.active:
      from py2play.idler import IDLER
      IDLER.show_blackbands()
      IDLER.camera.add_traveling(soya.FixTraveling(IDLER.camera, Vector(IDLER.camera, 0.0, 0.0, -1.0) % IDLER))
      IDLER.message(_("__gameover__"), 100000)
      
      # As the character has been removed from the level, the controler
      # does no longer listen for event such as the "escape" key.
      AllowQuit(IDLER)
      
  def __getstate__(self):
    state = Character.__getstate__(self)
    return state[0], self._treat_getstate(state[1])
  
  def __setstate__(self, state):
    Character.__setstate__(self, state)
    self._treat_setstate(state)
    #py2play_character.PlayerCharacter.__setstate__(self, state)
    
    # Loaded => imply this character is a phantom one !!!
    from slune.controler import PhantomControler
    self.player.controler = PhantomControler()
    
    if globdef.VERIFICATION_SERVER: self.logon_verif()
    
  def __repr__(self):
    if self.player: return "<Vehicle %s@%s:%s>" % (self.player.name, self.player.host, self.player.port)
    

explosions = []
class Explosion(soya.Particles):
  def __init__(self, parent = None, material = None, nb_particles = 30):
    soya.Particles.__init__(self, parent, material, nb_particles)
    self.auto_generate_particle = 1
    self.set_colors((0.9, 0.0, 0.2, 0.4), (0.9, 0.2, 0.2, 0.8), (0.8, 0.7, 0.1, 0.9), (0.6, 0.4, 0.2, 0.2))
    self.set_sizes((1.0, 1.0))
    self.life = 25
    explosions.append(self)
    
  def generate(self, index):
    angle = random.random() * 3.1417
    sx = math.cos(angle)
    sy = -math.sqrt(random.random() * 3.0)
    sz = math.sin(angle)
    l = (0.06 * (1.5 + random.random())) / math.sqrt(sx * sx + sy * sy + sz * sz)
    self.set_particle(index, 0.5 + random.random(), sx * l, sy * l, sz * l, 0.0, 0.01, 0.0)

  def begin_round(self):
    soya.Particles.begin_round(self)
    if   self.life >  0: self.life -= 1
    elif self.life == 0:
      self.auto_generate_particle = 0
      self.removable = 1
      explosions.remove(self)
      self.life = -1
      
class FlameThrower(soya.Particles):
  def __init__(self, parent = None, material = None, nb_particles = 35):
    soya.Particles.__init__(self, parent, material, nb_particles)
    self.auto_generate_particle = 1
    self.set_colors((0.0, 0.8, 0.0, 0.4), (0.1, 0.8, 0.1, 0.9), (0.8, 0.1, 0.1, 0.9), (0.1, 0.1, 0.8, 0.9), (0.2, 0.2, 0.8, 0.2))
    self.set_sizes((2.0, 2.0))
    self.life = 30
    explosions.append(self)
    
  def generate(self, index):
    angle = random.random() * 3.1417
    v = Vector(self,
               random.uniform(-0.3,  0.3),
               random.uniform(-0.3,  0.3),
               random.uniform(-1.5, -1.0),
               )
    v.convert_to(self.parent.parent)
    a = Vector(self, 0.0, 0.00, 0.02)
    a.convert_to(self.parent.parent)
    
    self.set_particle(index, 0.5 + random.random(), v.x, v.y, v.z, a.x, a.y, a.z)

  def begin_round(self):
    soya.Particles.begin_round(self)
    
    if (self.life > 0) and self.parent:
      for character in self.parent.level.pushables:
        cx, cy, cz = self.transform_point(character.x, character.y, character.z, character.parent)
        if (-20.0 < cz < -0.2) and (-0.5 < cy / cz < 0.5) and (-0.5 < cx / cz < 0.5):
          character.hurt(-0.1 / (cz - 1.0))
          _V.set_start_end(self, character)
          _V.convert_to(character.parent)
          _V.set_length(-1.0 / (cz - 1.0) / character.weight)
          character.push(_V.x, _V.y + 0.04, _V.z, self.parent)
          
    if   self.life >  0: self.life -= 1
    elif self.life == 0:
      self.auto_generate_particle = 0
      self.removable = 1
      explosions.remove(self)
      self.life = -1
      
      
      
class Nitro(soya.Particles):
  def __init__(self, parent = None, material = None, nb_particles = 50):
    soya.Particles.__init__(self, parent, material, nb_particles)
    self.set_colors((0.4, 0.7, 0.8, 0.4), (0.2, 0.7, 0.9, 0.8), (0.2, 0.9, 0.9, 0.9), (0.1, 0.3, 0.3, 0.2))
    self.set_sizes((1.0, 1.0))
    self.life = 25
    self.max_particles_per_round = 4
    self.auto_generate_particle = 1
    
  def generate(self, index):
    angle = random.random() * 3.1417
    sx = math.cos(angle)
    sy = -math.sqrt(random.random() * 3.0)
    sz = math.sin(angle)
    l = (0.06 * (1.5 + random.random())) / math.sqrt(sx * sx + sy * sy + sz * sz)
    #self.set_particle(index, 0.5 + random.random(), 0.0, 0.0, 0.0, random.random() - 0.5, random.random() - 0.5, random.random() - 0.5)
    
    pos = self.get_root().transform_vector((random.random() - 0.5) * 0.2, (random.random() - 0.5) * 0.2, 0.2, self)
    self.set_particle(index, 0.5 + random.random(), pos[0], pos[1], pos[2], 0.0, 0.0, 0.0)
      
# class Explosion(particle.SpriteSystem):
#   def __init__(self, parent = None, material = None, nb_particles = 30):
#     particle.SpriteSystem.__init__(self, parent, particle.FireGenerator(initial_speed = 0.4), material or particle._default(), nb_particles = nb_particles)
#     self.particle_width = self.particle_height = 0.5
#     self.life           = 25
#     explosions.append(self)
    
#   def begin_round(self):
#     if   self.life >  0: self.life -= 1
#     elif self.life == 0:
#       self.generator = None
#       self.removable = 1
#       explosions.remove(self)
#       self.life = -1
      
# class Snow(particle.Particles):
#   def __init__(self, parent = None, material = None, nb_particles = 10):
#     particle.Particles.__init__(self, parent, material or particle._default(), nb_particles)
#     self.auto_generate_particle = 1
#     self.removable = 1
#     self.set_colors((0.6, 0.75, 0.8, 0.2), (0.6, 0.75, 0.8, 0.6), (0.4, 0.7, 0.8, 0.2))
#     self.set_sizes((1.0, 1.0))
#     self.life = 10
    
#   def generate(self, index):
#     angle = random.random() * 3.1417
#     sx = math.cos(angle)
#     sy = -math.sqrt(random.random() * 3.0)
#     sz = math.sin(angle)
#     l = (0.06 * (1.5 + random.random())) / math.sqrt(sx * sx + sy * sy + sz * sz)
#     self.set_particle(index, 0.5 + random.random(), sx * l, sy * l, sz * l, 0.0, 0.01, 0.0)
    
#   def begin_round(self):
#     particle.Particles.begin_round(self)
#     if   self.life >  0: self.life -= 1
#     elif self.life == 0:
#       self.auto_generate_particle = 0
#       self.removable = 1
#       self.life = -1
    
class LifeBar(widget.Widget):
  def __init__(self, character = None):
    widget.Widget.__init__(self)
    self.character = character
    
    self.left   = soya.get_screen_width() - 30.0
    self.top    = 10.0
    self.width  = 20.0
    self.height = soya.get_screen_height() - 20.0
    
  def render(self):
    if self.character:
      import soya.opengl as soyaopengl
      soyaopengl.glBegin(soyaopengl.GL_QUADS)
      soyaopengl.glColor4f(0.7, 0.0, 0.0, 1.0)
      
      soyaopengl.glVertex2f(self.left             , self.top + self.height)
      soyaopengl.glVertex2f(self.left + self.width, self.top + self.height)
      
      top = self.top + (1.0 - self.character.life) * self.height
      soyaopengl.glColor4f(1.0, 0.7, 0.0, 1.0)
      soyaopengl.glVertex2f(self.left + self.width, top)
      soyaopengl.glVertex2f(self.left             , top)
      soyaopengl.glEnd()

class BossLifeBar(widget.Widget):
  def __init__(self, character = None):
    widget.Widget.__init__(self)
    self.character = character
    
    self.left   = 20.0
    self.top    = 10.0
    self.width  = 20.0
    self.height = soya.get_screen_height() - 20.0
    
  def render(self):
    if self.character:
      import soya.opengl as soyaopengl
      soyaopengl.glBegin(soyaopengl.GL_QUADS)
      soyaopengl.glColor4f(0.0, 0.5, 0.0, 1.0)
      
      soyaopengl.glVertex2f(self.left             , self.top + self.height)
      soyaopengl.glVertex2f(self.left + self.width, self.top + self.height)
      
      top = self.top + (1.0 - self.character.life) * self.height
      soyaopengl.glColor4f(0.7, 1.0, 0.0, 1.0)
      soyaopengl.glVertex2f(self.left + self.width, top)
      soyaopengl.glVertex2f(self.left             , top)
      soyaopengl.glEnd()


class AllowQuit(soya.CoordSyst):
  def begin_round(self):
    soya.CoordSyst.begin_round(self)
    
    import soya.sdlconst as soyasdlconst
    
    for event in soya.process_event():
      if (event[0] == soyasdlconst.MOUSEBUTTONDOWN) or (event[0] == soyasdlconst.KEYDOWN) or (event[0] == soyasdlconst.JOYBUTTONDOWN):
        from py2play.idler import IDLER
        IDLER.end_game()
        

