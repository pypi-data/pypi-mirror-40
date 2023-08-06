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

import math

import soya, soya.sdlconst as soyasdlconst
import py2play.action as action

from slune.character import *
from slune.level     import Level, LifeBonus, FlameThrowerBonus

def Debug(character):
  yield Action(ACTION_DEBUG)
  yield Action(ACTION_DEBUG)
  yield Action(ACTION_DEBUG)
  yield Action(ACTION_DEBUG)
  
def Wall_climber(character):
  yield Action(ACTION_JUMP, character.default_mouse_x(), -1.0)
  
  while character.parent.transform_vector(0.0, 1.0, 0.0, character)[1] > 0.0:
    yield Action(ACTION_ROTUP, character.default_mouse_x(), -1.0)
    
  i = 0
  for i in range(10):
    yield Action(ACTION_ROTDOWN, character.default_mouse_x(), -1.0)
    
  while (not character.on_ground) and (i < 25.0 * 7.0 / character.rotup_speed):
    i += 1
    yield Action(ACTION_ROTDOWN, character.default_mouse_x(), -1.0)
    
def Dodge(character):
  yield Action(ACTION_JUMP, 0.0, 0.0)
  
  for j in range(30):
    yield Action(ACTION_ROTUP, 0.0, 0.0)
    
  for j in range(30):
    yield Action(ACTION_WAIT, 0.0, 0.0)
    
def nearest_character(character):
  best      = None
  best_dist = 10000.0
  for level in character.get_root():
    if isinstance(level, Level):
      for charac in level.characters:
        if not charac is character:
          dist = character.distance_to(charac)
          if dist < best_dist:
            best      = charac
            best_dist = dist
            
  return best
  
GOTO_X_2_TURN         = 0.21412933552126162
GOTO_X_2_SPEED        = 0.49762284312684019
GOTO_Y_2_SPEED        = 0.49762284312684019
GOTO_Z_2_SPEED        = 1.6085952599320903
GOTO_NOGROUND_2_SPEED = -18.661345433135967
GOTO_Y_2_JUMP         = 0.38818320682881224
GOTO_Z_2_JUMP         = 0.059585204340943942
GOTO_NOGROUND_2_JUMP  = 13.608682920401893

def check_vertical_angle(self):
  if self.on_ground and not self.gripped:
    if self.vertical_angle < -45.0:
      self.vertical_angle = 0.0
      return ACTION_ROTDOWN
    
  return ACTION_WAIT

def goto(self, target, coordsyst = None, x = None, y = None, z = None, dodge = 0.0, canjump = 1, turbosity = -100.0, turbo_period = -1.0):
  if coordsyst: fx, fy, fz = self.transform_point(x, y, z, coordsyst)
  else:         fx, fy, fz = self.transform_point(target.x, target.y, target.z, target.parent)
  
  if dodge and (fz > 0.0) and (self.distance_to(target) < dodge): return Dodge(self)
  
  if self.jumping:
    if self.on_ground: self.jumping = 0
    no_ground = 0 # It is normal that there is no ground !
  elif self.context:
    no_ground = (not self.on_ground) and (not self.context.raypick_b(self, self.check_ground_vector, 6.0, 3))
  else: no_ground = not self.on_ground

  if self.gripped: # Avoid jumping while gripped
    if canjump and ((GOTO_Y_2_JUMP * fy + GOTO_Z_2_JUMP * fz + GOTO_NOGROUND_2_JUMP * no_ground > 8.0) or (self.speed.length() < 0.001)):
      self.jumping = 1
      action = ACTION_JUMP
    else: action = check_vertical_angle(self)
  else:
    if   canjump and ((fy > 3.5) and (abs(fx) < 2.0) and (-10.0 < fz < 0.0)):
      self.jumping = 1
      return Wall_climber(self)
    elif canjump and ((GOTO_Y_2_JUMP * fy + GOTO_Z_2_JUMP * fz + GOTO_NOGROUND_2_JUMP * no_ground > 2.0) or ((self.speed.length() < 0.001) and (self.current_action.mouse_y < 1.0))):
      self.jumping = 1
      action = ACTION_JUMP
    else: action = check_vertical_angle(self)

  if not self.flame_thrower:
    if (turbosity > 0.0) and (action == ACTION_WAIT) and not self.gripped:
      if turbo_period == -1.0:
        if turbosity * (-fz - abs(fx) - abs(fy)) > 45.0: action = ACTION_TURBO
      else:
        if fz < 0.0:
          if turbosity * (fz - abs(fx) - abs(fy)) > -10.0: action = ACTION_TURBO
      
      
  return Action(
    action,
    (5.0 * self.current_action.mouse_x + min(1.0, max(-1.0, GOTO_X_2_TURN * fx))) / 6.0,
    (5.0 * self.current_action.mouse_y + min(1.0, max(-self.max_speed, 1.0 + GOTO_X_2_SPEED * abs(fx) + GOTO_Y_2_SPEED * fy + GOTO_Z_2_SPEED * fz + GOTO_NOGROUND_2_SPEED * no_ground))) / 6.0,
    )
  
runto = goto
  
def Goto(self, target, min_distance = 0.7):
  while self.distance_to(target) > min_distance:
    yield goto(self, target)
    
Runto = Goto

def CheckBonus(self, aggressivity = 0.5):
  for bonus in self.level.bonuss:
    if bonus.visible and (self.distance_to(bonus) < 25.0):
      if   isinstance(bonus, LifeBonus) and (self.life < 0.6):
        for i in range(250):
          yield goto(self, bonus)
          if (bonus.visible == 0) or (self.distance_to(bonus) < getattr(bonus, "radius", 0.3)): break
      elif isinstance(bonus, FlameThrowerBonus) and (self.random.random() < aggressivity):
        for i in range(250):
          yield goto(self, bonus)
          if (bonus.visible == 0) or (self.distance_to(bonus) < getattr(bonus, "radius", 0.3)): break
          
def AttackRun(self, target, duration = 100, dodge = 0.0, turbosity = -100.0):
  for i in range(int(duration)):
    a =  runto(self, target, dodge = dodge, turbosity = turbosity, turbo_period = 1.0)
    if self.flame_thrower and isinstance(a, Action):
      fx, fy, fz = self.transform_point(target.x, target.y, target.z, target.parent)
      if (-15.0 < fz < -0.2) and (-0.5 < fy / fz < 0.5) and (-0.5 < fx / fz < 0.5):
        if a.action == ACTION_WAIT: a.action = ACTION_TURBO
    yield a
    
def AttackFrontRun(self, target, duration = 100, dodge = 0.0, turbosity = -100.0):
  for i in range(int(duration)):
    gx, gy, gz = target.transform_point(self.x, self.y, self.z, self.parent)
    if (gz <= 0.0) or self.distance_to(target) > 10.0: a = runto(self, target, dodge = dodge, turbosity = turbosity, turbo_period = 1.0)
    else:
      if gx < 0: a = runto(self, target, target, -3.0, 0.0, -7.0, dodge = dodge, turbosity = turbosity, turbo_period = 1.0)
      else:      a = runto(self, target, target,  3.0, 0.0, -7.0, dodge = dodge, turbosity = turbosity, turbo_period = 1.0)
    if self.flame_thrower and isinstance(a, Action):
      fx, fy, fz = self.transform_point(target.x, target.y, target.z, target.parent)
      if (-15.0 < fz < -0.2) and (-0.5 < fy / fz < 0.5) and (-0.5 < fx / fz < 0.5):
        if a.action == ACTION_WAIT: a.action = ACTION_TURBO
    yield a
    
def AttackSideRun(self, target, duration = 100, dodge = 0.0, turbosity = -100.0):
  for i in range(int(duration)):
    gx, gy, gz = target.transform_point(self.x, self.y, self.z, self.parent)
    if (gz <= 0.0) or self.distance_to(target) > 10.0: a = runto(self, target, dodge = dodge, turbosity = turbosity, turbo_period = 1.0)
    else:
      if gx < 0: a = runto(self, target, target, -7.0, 0.0, 0.0, dodge = dodge, turbosity = turbosity, turbo_period = 1.0)
      else:      a = runto(self, target, target,  7.0, 0.0, 0.0, dodge = dodge, turbosity = turbosity, turbo_period = 1.0)
    if self.flame_thrower and isinstance(a, Action):
      fx, fy, fz = self.transform_point(target.x, target.y, target.z, target.parent)
      if (-15.0 < fz < -0.2) and (-0.5 < fy / fz < 0.5) and (-0.5 < fx / fz < 0.5):
        if a.action == ACTION_WAIT: a.action = ACTION_TURBO
    yield a
      
def Flee(self, target, duration = 100):
  no_ground = 0
  
  for i in range(int(duration)):
    fx, fy, fz = self.transform_point(target.x, target.y, target.z, target.parent)
    dist       = self.distance_to(target)
    
    if self.jumping:
      if not no_ground: self.jumping = 0
      no_ground = 0 # It is normal that there is no ground !
    else:
      if self.context: no_ground = not self.context.raypick_b(self, self.check_ground_vector, 4.0, 3)
      
    if self.speed.length() * 10.0 + dist < 3.0:
      h = self.random.random()
      if   h < 0.2: break # Try another strategy
      elif h < 0.4: yield Dodge(self)
    
    yield Action(
      ACTION_WAIT,
      (5.0 * self.current_action.mouse_x + min(1.0, max(-1.0, -0.27955060118474129 * fx))) / 6.0,
      (5.0 * self.current_action.mouse_y + min(1.0, max(-self.max_speed, -0.94713263528551006 * abs(fx) + -0.0076398049940541654 * fy + -0.46242007806615826 * fz + 22.758284696585228 * no_ground))) / 6.0,
      )

def Feinte(self, target, duration = 100, dodge = 1.0):
  for i in range(int(duration)):
    if (self.distance_to(target) < dodge):
      yield Dodge(self)
      break # Change strategy !
    
    yield Action(ACTION_WAIT, 0.5, 0.1)
    
def Wander(self, duration = 100):
  mouse_x = self.current_action.mouse_x
  mouse_y = self.current_action.mouse_y
  for i in range(int(duration)):
    mouse_x += min(1.0, max(-1.0, (self.random.random() - 0.5) / 20.0))
    mouse_y += min(1.0, max(-1.0, (self.random.random() - 0.5) / 20.0))
    yield Action(ACTION_WAIT, mouse_x, mouse_y)
    
def PushToKill(self, target, turbosity = -100.0):
  fx, fy, fz = self.transform_point(target.x, target.y, target.z, target.parent)
  dist = self.distance_to(target)
  best = None
  best_dist = 1000000.0
  target_front = Point(target, 0.0, 0.0, -15.0) % target.parent
  
  for pushable in self.level.pushables:
    if (not isinstance(pushable, Character)) and pushable.distance_to(target_front) < 55.0:
      px, py, pz = self.transform_point(pushable.x, pushable.y, pushable.z, pushable.parent)
      cur_dist = self.distance_to(pushable)
      if (cur_dist < dist) and (cur_dist < best_dist):
        best_dist = cur_dist
        best = pushable
        
  if not best: # Nothing to push
    if dist > 50.0: yield AttackRun(self, target)
    else:           yield Flee(self, target)
    return
  
  pushable = best
  while 1:
    if not pushable.parent: break
    v = target >> pushable
    v.set_length(pushable.radius * 2.0)
    t = pushable + v
    
    dist  = math.sqrt((t.x - self.x) ** 2 + (t.z - self.z) ** 2) #self.distance_to(t)
    distp = self.distance_to(pushable)
    if dist < 1.5: break
    
    if (not self.jumping) and (self.on_ground) and (distp < dist - 1.0) and (distp < pushable.radius * 2.5):
      self.jumping = 1
      yield Action(ACTION_JUMP, self.current_action.mouse_x, -1.0)
      
    yield goto(self, t, turbosity = turbosity)
    
  v = target >> pushable
  v.set_length(pushable.radius + self.radius - 0.1)
  t = pushable + v
  
  yield LookAt(self, t)
  
  for i in range(50):
    if pushable.worth_playing or not pushable.parent: break
    yield Action(ACTION_WAIT, 0.0, -1.0)
    
  if self.random.random() < 0.5:
    for i in range(10): yield Action(ACTION_WAIT, -1.0, 0.0)
  else:
    for i in range(10): yield Action(ACTION_WAIT,  1.0, 0.0)
  for i in range(10):   yield Action(ACTION_WAIT, 0.0, -1.0)
  

def LookAt(self, target):
  while 1:
    x, y, z = self.transform_point(target.x, target.y, target.z, target.parent)
    if abs(x / z) < 0.2: break
    if z < 0.0: yield Action(ACTION_WAIT, cmp(x, 0.0)) 
    else:       yield Action(ACTION_WAIT, cmp(x, 0.0))
    
Look_at = LookAt # old name
    
class Wait:
  def next(self): return Action()
WAIT = Wait()


class StackControler:
  def __init__(self, controlers  = None):
    self.controlers = controlers or []
    self.uncancelable_controler = None
    
  def animate(self, controler):
    self.controlers.append(controler)
    if not self.uncancelable_controler in self.controlers:
      self.uncancelable_controler = controler
      
  def append(self, controler):
    if not self.uncancelable_controler in self.controlers:
      self.controlers.append(controler)
      
  def next(self):
    try:
      c = self.controlers[-1]
      r = c.next() # calling c.next() may add a new controler ! => c may no longer be self.controlers[-1]
    except StopIteration:
      self.controlers.remove(c)
      if self.uncancelable_controler is c: self.uncancelable_controler = None
      return self.next()
    
    if not isinstance(r, Action):
      self.controlers.append(r)
      return self.next()
    
    return r

# A controler for phantom character, needed for them to play video sequences.
class PhantomControler(StackControler):
  def next(self):
    if self.controlers: return StackControler.next(self)


import soya.widget as widget, soya.opengl as soyaopengl

class KeyboardMouseControler(StackControler, widget.Widget):
  key_controlers = {}
  
  def __init__(self, character = None):
    StackControler.__init__(self)
    
    self.d_mouse_x     = self.d_mouse_y = 0.0
    self.mouse_x       = 0.0
    self.mouse_y       = 1.0
    self.character     = character
    self.enabled       = 1
    self.keyboard_mode = 0
    self.pixel_x = self.pixel_y = 0.0
    self.allow_move_back = 0
    
    from py2play.idler import IDLER
    IDLER.no_blackbands_group.add(self)
    IDLER.blackbands_group.add(self)
    
    
  def resize(self, parent_left, parent_top, parent_width, parent_height):
    self.parent_left   = parent_left
    self.parent_top    = parent_top
    self.parent_width  = parent_width
    self.parent_height = parent_height

  if globdef.QUALITY > 1:
    def render(self):
      if not self.keyboard_mode:
        angle = math.atan(self.mouse_x / (self.mouse_y - 1.01))
        
        if self.allow_move_back < 10:
          size = 30.0 - self.mouse_y * 10.0
          soyaopengl.glEnable(soyaopengl.GL_BLEND)
          soyaopengl.glColor4f(0.0, 0.0, 0.0, 0.5)
          soyaopengl.glBegin(soyaopengl.GL_TRIANGLES)
          soyaopengl.glVertex2f(self.pixel_x - 9.0, self.pixel_y + 9.0)
          soyaopengl.glVertex2f(
            self.pixel_x - 9.0 - size * math.cos(angle) + size * math.sin(angle),
            self.pixel_y + 9.0 + size * math.cos(angle) + size * math.sin(angle),
            )
          soyaopengl.glVertex2f(
            self.pixel_x - 9.0 + size * math.cos(angle) + size * math.sin(angle),
            self.pixel_y + 9.0 + size * math.cos(angle) - size * math.sin(angle),
            )
          soyaopengl.glEnd()
          soyaopengl.glDisable(soyaopengl.GL_BLEND)

          soyaopengl.glColor4f(1.0, 1.0, 1.0, 1.0)
          soyaopengl.glBegin(soyaopengl.GL_TRIANGLES)
          soyaopengl.glVertex2f(self.pixel_x, self.pixel_y)
          soyaopengl.glVertex2f(
            self.pixel_x - size * math.cos(angle) + size * math.sin(angle),
            self.pixel_y + size * math.cos(angle) + size * math.sin(angle),
            )
          soyaopengl.glVertex2f(
            self.pixel_x + size * math.cos(angle) + size * math.sin(angle),
            self.pixel_y + size * math.cos(angle) - size * math.sin(angle),
            )
          soyaopengl.glEnd()
        else:
          size = 10.0 + self.mouse_y * 10.0
          soyaopengl.glEnable(soyaopengl.GL_BLEND)
          soyaopengl.glColor4f(0.0, 0.0, 0.0, 0.5)
          soyaopengl.glBegin(soyaopengl.GL_TRIANGLES)
          soyaopengl.glVertex2f(self.pixel_x - 9.0, self.pixel_y + 9.0)
          soyaopengl.glVertex2f(
            self.pixel_x - 9.0 + size * math.cos(angle) + size * math.sin(angle),
            self.pixel_y + 9.0 - size * math.cos(angle) + size * math.sin(angle),
            )
          soyaopengl.glVertex2f(
            self.pixel_x - 9.0 - size * math.cos(angle) + size * math.sin(angle),
            self.pixel_y + 9.0 - size * math.cos(angle) - size * math.sin(angle),
            )
          soyaopengl.glEnd()
          soyaopengl.glDisable(soyaopengl.GL_BLEND)

          soyaopengl.glColor4f(1.0, 1.0, 1.0, 1.0)
          soyaopengl.glBegin(soyaopengl.GL_TRIANGLES)
          soyaopengl.glVertex2f(self.pixel_x, self.pixel_y)
          soyaopengl.glVertex2f(
            self.pixel_x + size * math.cos(angle) + size * math.sin(angle),
            self.pixel_y - size * math.cos(angle) + size * math.sin(angle),
            )
          soyaopengl.glVertex2f(
            self.pixel_x - size * math.cos(angle) + size * math.sin(angle),
            self.pixel_y - size * math.cos(angle) - size * math.sin(angle),
            )
          soyaopengl.glEnd()
  else:
    def render(self):
      if not self.keyboard_mode:
        angle = math.atan(self.mouse_x / (self.mouse_y - 1.01))
        
        soyaopengl.glColor4f(1.0, 1.0, 1.0, 1.0)
        soyaopengl.glBegin(soyaopengl.GL_TRIANGLES)
        soyaopengl.glVertex2f(self.pixel_x, self.pixel_y)
        
        if self.allow_move_back < 10:
          size = 30.0 - self.mouse_y * 10.0
          soyaopengl.glVertex2f(
            self.pixel_x - size * math.cos(angle) + size * math.sin(angle),
            self.pixel_y + size * math.cos(angle) + size * math.sin(angle),
            )
          soyaopengl.glVertex2f(
            self.pixel_x + size * math.cos(angle) + size * math.sin(angle),
            self.pixel_y + size * math.cos(angle) - size * math.sin(angle),
            )
        else:
          size = 10.0 + self.mouse_y * 10.0
          soyaopengl.glVertex2f(
            self.pixel_x + size * math.cos(angle) + size * math.sin(angle),
            self.pixel_y - size * math.cos(angle) + size * math.sin(angle),
            )
          soyaopengl.glVertex2f(
            self.pixel_x - size * math.cos(angle) + size * math.sin(angle),
            self.pixel_y - size * math.cos(angle) - size * math.sin(angle),
            )
        soyaopengl.glEnd()
        
  def next(self):
    character = self.character
    a = character.player.default_action
    
    if (character.player.default_action == ACTION_ROTUP) or (character.player.default_action == ACTION_ROTDOWN):
      if character.on_ground:
        character.player.default_action = a = ACTION_WAIT
        
    for event in soya.coalesce_motion_event(soya.process_event()):
      if   event[0] == soyasdlconst.MOUSEMOTION:
        self.keyboard_mode = 0
        camera = character.get_root().camera
        h = camera.get_screen_width ()
        w = camera.get_screen_height()
        self.pixel_x = float(event[1])
        self.pixel_y = float(event[2])
        self.mouse_x = ((float(event[1]) / camera.get_screen_width ()) - 0.5) * 2.0
        if self.allow_move_back < 10:
          self.mouse_y = ((float(event[2]) / camera.get_screen_height()) - 0.5) * 2.0
          if self.mouse_y > 0.95: self.allow_move_back += 2
        else:
          self.mouse_y = ((float(event[2]) / camera.get_screen_height()) * 3.0) - 1.0
          if self.mouse_y < 1.0: self.allow_move_back = 0
        
      elif self.enabled:
        if self.controlers and (event[0] != soyasdlconst.MOUSEBUTTONUP) and (not self.uncancelable_controler in self.controlers):
          self.controlers *= 0
          
        if event[0] == soyasdlconst.MOUSEBUTTONDOWN:
          if   event[1] == 1:
            if character.on_ground: a = ACTION_JUMP
            else:             character.player.default_action = a = ACTION_ROTUP
          elif event[1] == 2:
            if character.on_ground:
              character.player.controler.append(Wall_climber(character))
              return
            else: character.player.default_action = a = ACTION_ROTDOWN
          elif event[1] == 3: character.player.default_action = a = ACTION_TURBO
          elif event[1] == 4:
            if character.player.default_action == ACTION_ROTUP  : character.player.default_action = a = action.ACTION_WAIT
            else:                                                 character.player.default_action = a = ACTION_ROTDOWN
          elif event[1] == 5:
            if character.player.default_action == ACTION_ROTDOWN: character.player.default_action = a = action.ACTION_WAIT
            else:                                                 character.player.default_action = a = ACTION_ROTUP
            
        elif event[0] == soyasdlconst.MOUSEBUTTONUP:
          if   event[1] == 1: character.player.default_action = a = ACTION_WAIT
          elif event[1] == 3: character.player.default_action = a = ACTION_WAIT
          
        elif event[0] == soyasdlconst.KEYDOWN:
          if   (event[1] == soyasdlconst.K_LCTRL) or (event[1] == soyasdlconst.K_RCTRL):
            if character.on_ground: a = ACTION_JUMP
            else: character.player.default_action = a = ACTION_ROTUP
            
          elif (event[1] == soyasdlconst.K_LSHIFT) or (event[1] == soyasdlconst.K_RSHIFT):
            if character.on_ground:
              character.player.controler.append(Wall_climber(character))
              return
            else: character.player.default_action = a = ACTION_ROTDOWN
            
          elif (event[1] == soyasdlconst.K_LALT) or (event[1] == soyasdlconst.K_RALT):
            character.player.default_action = a = ACTION_TURBO
            
          elif event[1] == soyasdlconst.K_DOWN:  self.keyboard_mode = 1; self.d_mouse_y =  0.15
          elif event[1] == soyasdlconst.K_UP:    self.keyboard_mode = 1; self.d_mouse_y = -0.15
          elif event[1] == soyasdlconst.K_LEFT:  self.keyboard_mode = 1; self.d_mouse_x = -0.1
          elif event[1] == soyasdlconst.K_RIGHT: self.keyboard_mode = 1; self.d_mouse_x =  0.1
          
          elif (event[1] == soyasdlconst.K_q) or (event[1] == soyasdlconst.K_ESCAPE):
            from py2play.idler import IDLER
            IDLER.end_game()
            
          elif event[1] == soyasdlconst.K_s:
            import tempfile
            screenshot_file = tempfile.mktemp(".jpeg")
            soya.screenshot(screenshot_file)
            print "* Slune * Screenshot saved as %s" % screenshot_file
            
          elif event[1] == soyasdlconst.K_w:
            soya.toggle_wireframe()

          elif event[1]:
            Controler = self.key_controlers.get(event[1])
            if Controler:
              character.player.controler.append(Controler(character))
              
        elif event[0] == soyasdlconst.KEYUP:
          if   event[1] == soyasdlconst.K_DOWN:
            if self.d_mouse_y > 0.0: self.d_mouse_y = 0.0
            if self.mouse_y == 1.0: self.allow_move_back = 10
          elif event[1] == soyasdlconst.K_UP:
            if self.d_mouse_y < 0.0: self.d_mouse_y = 0.0
          elif event[1] == soyasdlconst.K_LEFT:
            if self.d_mouse_x < 0.0: self.d_mouse_x = 0.0
          elif event[1] == soyasdlconst.K_RIGHT:
            if self.d_mouse_x > 0.0: self.d_mouse_x = 0.0
            
          elif (event[1] == soyasdlconst.K_LALT) or (event[1] == soyasdlconst.K_RALT) or (event[1] == soyasdlconst.K_LCTRL) or (event[1] == soyasdlconst.K_RCTRL) or (event[1] == soyasdlconst.K_LSHIFT) or (event[1] == soyasdlconst.K_RSHIFT):
            character.player.default_action = a = ACTION_WAIT
            
        elif event[0] == soyasdlconst.JOYAXISMOTION:
          if event[1] == 0: # X Axis
            self.d_mouse_x = float(event[2]) / 327680
            self.keyboard_mode = 1
          elif event[1] == 1:   # Y Axis
            self.d_mouse_y = float(event[2]) / 327680
            self.keyboard_mode = 1
            
        elif event[0] == soyasdlconst.JOYBUTTONDOWN:
          if event[1] == 0:
            character.player.default_action = a = ACTION_TURBO
          elif event[1] == 1:
            if character.on_ground: a = ACTION_JUMP
            else: character.player.default_action = a = ACTION_ROTUP
          elif event[1] == 2:
            if character.on_ground:
              character.player.controler.append(Wall_climber(character))
              return
            else: character.player.default_action = a = ACTION_ROTDOWN

        elif event[0] == soyasdlconst.JOYBUTTONUP:
          character.player.default_action = a = ACTION_WAIT

      elif (event[0] == soyasdlconst.JOYBUTTONDOWN) or (event[0] == soyasdlconst.MOUSEBUTTONDOWN) or ((event[0] == soyasdlconst.KEYDOWN) and (not event[1] in (0, soyasdlconst.K_UP, soyasdlconst.K_DOWN, soyasdlconst.K_LEFT, soyasdlconst.K_RIGHT))):
        return Action(ACTION_STARTGAME)
      
    from py2play.idler import IDLER
    if self.controlers:
      if self.uncancelable_controler and not IDLER.blackbands_visible: IDLER.show_blackbands()
      
      return StackControler.next(self)
    
    else:
      if IDLER.blackbands_visible: IDLER.hide_blackbands()
      
      if self.keyboard_mode:
        self.mouse_x *= 0.9
        if self.mouse_y < 0.0: self.mouse_y *= 0.9
        
        self.mouse_x += self.d_mouse_x
        if   self.mouse_x < -1.0: self.mouse_x = -1.0
        elif self.mouse_x >  1.0: self.mouse_x =  1.0
        
        self.mouse_y += self.d_mouse_y
        if   self.mouse_y < -1.0: self.mouse_y = -1.0
        else:
          if self.allow_move_back < 10:
            if self.mouse_y > 1.0: self.mouse_y =  1.0
          else:
            if   self.mouse_y < 1.0: self.allow_move_back = 0
            elif self.mouse_y > 2.0: self.mouse_y =  2.0
            
      return Action(a, self.mouse_x, self.mouse_y)
    
    
    
#KeyboardMouseControler.key_controlers[soyasdlconst.K_z] = Push_nearest_character #z
#KeyboardMouseControler.key_controlers[soyasdlconst.K_e] = Wall_climber #e
#KeyboardMouseControler.key_controlers[soyasdlconst.K_f] = Goto_next_flag #f
KeyboardMouseControler.key_controlers[soyasdlconst.K_g] = Dodge #g



          
