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

import soya, soya.opengl as soyaopengl, soya.widget as widget
import py2play.level as py2p_level, py2play.action as action, py2play.character as character
import slune.character as slune_character
import slune.controler
import slune.globdef as globdef, slune.sound as sound, slune.level as slune_level

def init_race_game(level):
  """Hides all flags except the first."""
  
  # Copy them in level, since the different player may have different config.
  level.race_nb_laps      = globdef.RACE_NB_LAPS
  level.race_nb_opponents = globdef.RACE_NB_OPPONENTS
  
  level.ranks = []
  
  level.flags = [] # Indexes all flags
  
  for item in level:
    if isinstance(item, Flag):
      item.visible = (item.name == "flag_0")
      level.flags.append(item)
      
  level.flags.sort(lambda f1, f2: cmp(f1.flag_id, f2.flag_id))
  
  
def start_race_game(level, add_opponent1 = 1):
  """Inits time property and shows the race time label."""
  for i in range(level.race_nb_opponents - len(level.characters)):
    Opponent().set_level(level, 1)
    
  Checker(level)
  
  for character in level.characters:
    if isinstance(character, slune_character.Competitor): init_race_opponent(character)
    
def init_race_opponent(character, laps_label = 1, minimap = 1):
  character.next_flag_id = 0
  character.nb_laps   = 0
  character.lap_start = time.time()
  character.best_lap  = 9999.0
  if character.played and character.player.active:
    from py2play.idler import IDLER
    if laps_label: IDLER.no_blackbands_group.insert(0, LapsLabel(character))
    if minimap:    IDLER.no_blackbands_group.insert(0, MiniMap(character.level))

def end_race_game(level):
  """Hides the race time label."""
  for widget in soya.root_widget.children:
    if isinstance(widget, LapsLabel):
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
          
          #character.life = min(1.0, character.life + 0.1)
          
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
            
            if character.nb_laps >= character.level.race_nb_laps:
              firework = soya.FlagFirework(level, nb_particles = 6)
              firework.move(flag)
              
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
            
    # check if every one is killer, except the current player.
    from py2play.player import CURRENT_PLAYER
    
    if (len(self.parent.characters) == 1) and (self.parent.characters[0] is CURRENT_PLAYER.character):
      self.parent.ranks.append(CURRENT_PLAYER.character)
      if len(self.parent.ranks) == 1:
        IDLER.level_completed(CURRENT_PLAYER.character, 1, message = _("__race_winner__"))
      else:
        IDLER.level_completed(CURRENT_PLAYER.character, 1, message = _("__race_looser__") % len(self.parent.ranks))
        
      self.parent.remove(self)
  
  
class Flag(soya.Bonus):
  radius = 3.5
  
  def __init__(self, parent = None):
    if parent:
      parent.max_laps = 2
      
      nb = 0
      for item in parent:
        if isinstance(item, Flag): nb += 1
        
      soya.Bonus.__init__(self, parent, soya.Material.get("flag1"), soya.Material.get("halo"))
      
      self.flag_id = nb
      
    else:
      soya.Bonus.__init__(self, parent, soya.Material.get("flag1"), soya.Material.get("halo"))
      
    self.color = (1.0, 1.0, 0.20000000298023224, 1.0)
    
  def get_flag_id(self):
    try: return int(self.name[5:])
    except ValueError: return 0
  def set_flag_id(self, id): self.name = "flag_%s" % id
  flag_id = property(get_flag_id, set_flag_id)


class MiniMap(widget.Widget):
  def __init__(self, level):
    self.level = level
    
    self.top = 10
    self.width  = 200
    self.height = 200
    self.left = soya.root_widget.width - self.width - 40
    
    flags = [x for x in level if isinstance(x, Flag)]
    flags.sort(lambda f1, f2: cmp(f1.flag_id, f2.flag_id))
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
    soyaopengl.glBegin(soyaopengl.GL_LINE_LOOP)
    for flag in flags:
      self.flags_pos.append((
        left + f * (flag.x - min_x),
        top  + f * (flag.z - min_y),
        ))
      soyaopengl.glVertex2f(*self.flags_pos[-1])
    soyaopengl.glEnd()
    x, y = self.flags_pos[-1]
    soyaopengl.glBegin(soyaopengl.GL_QUADS)
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
    from py2play.player import CURRENT_PLAYER
    from py2play.idler import IDLER
    ca = IDLER.camera
    x, y, z = ca.transform_point(0.0, 0.0, 0.0, self.level.flags[CURRENT_PLAYER.character.next_flag_id])
    angle = math.atan(x / z)
    if z < 0.0:
      vx = -math.sin(angle)
      vy = -math.cos(angle)
    else:
      vx = math.sin(angle)
      vy = math.cos(angle)
    
    r = self.screen_width / self.screen_height
    if r > abs(vx / vy):
      if vy < 0.0:
        my = -self.screen_height / 2.0
        mx = vx * (my / vy) * r
      else:
        my = self.screen_height / 2.0
        mx = vx * (my / vy) * r
    else:
      if vx < 0.0:
        mx = -self.screen_width / 2.0
        my = vy * (mx / vx) / r
      else:
        mx = self.screen_width / 2.0
        my = vy * (mx / vx) / r
        
    x = mx + self.screen_width  / 2.0
    y = my + self.screen_height / 2.0
    
    x1 = x + (+ my - mx) * 0.06
    x2 = x + (- my - mx) * 0.06
    y1 = y + (- mx - my) * 0.06
    y2 = y + (+ mx - my) * 0.06

    if globdef.QUALITY > 1:
      soyaopengl.glEnable(soyaopengl.GL_BLEND)
      soyaopengl.glColor4f(0.0, 0.0, 0.0, 0.5)
      soyaopengl.glBegin(soyaopengl.GL_TRIANGLES)
      soyaopengl.glVertex2f(x  - 9.0, y  + 9.0)
      soyaopengl.glVertex2f(x1 - 9.0, y1 + 9.0)
      soyaopengl.glVertex2f(x2 - 9.0, y2 + 9.0)
      soyaopengl.glEnd()
      soyaopengl.glDisable(soyaopengl.GL_BLEND)
    
    soyaopengl.glColor4f(1.0, 1.0, 1.0, 1.0)
    soyaopengl.glBegin(soyaopengl.GL_TRIANGLES)
    soyaopengl.glVertex2f(x, y)
    soyaopengl.glVertex2f(x1, y1)
    soyaopengl.glVertex2f(x2, y2)
    soyaopengl.glEnd()
    
    soyaopengl.glCallList(self._calllist)
    for character in self.level.characters:
      if isinstance(character, slune_character.Competitor):
        x = self.cleft + self.f * (character.x - self.min_x)
        y = self.ctop  + self.f * (character.z - self.min_y)
        
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

#         if   character.perso_name == "tux":
#           material = soya.Material.get("tux1"); material.activate()
#           soyaopengl.glBegin(soyaopengl.GL_QUADS)
#           soyaopengl.glTexCoord2f(0.6, 0.0); soyaopengl.glVertex2f(x - 10.0, y - 10.0)
#           soyaopengl.glTexCoord2f(0.6, 1.0); soyaopengl.glVertex2f(x - 10.0, y + 10.0)
#           soyaopengl.glTexCoord2f(1.0, 1.0); soyaopengl.glVertex2f(x + 10.0, y + 10.0)
#           soyaopengl.glTexCoord2f(1.0, 0.0); soyaopengl.glVertex2f(x + 10.0, y - 10.0)
#           soyaopengl.glEnd()
#         elif character.perso_name == "gnu":
#           material = soya.Material.get("gnu"); material.activate()
#           soyaopengl.glBegin(soyaopengl.GL_QUADS)
#           soyaopengl.glTexCoord2f(0.52, 0.4); soyaopengl.glVertex2f(x - 10.0, y - 10.0)
#           soyaopengl.glTexCoord2f(0.52, 1.0); soyaopengl.glVertex2f(x - 10.0, y + 10.0)
#           soyaopengl.glTexCoord2f(1.0 , 1.0); soyaopengl.glVertex2f(x + 10.0, y + 10.0)
#           soyaopengl.glTexCoord2f(1.0 , 0.4); soyaopengl.glVertex2f(x + 10.0, y - 10.0)
#           soyaopengl.glEnd()
#         elif character.perso_name == "shark":
#           material = soya.Material.get("shark1"); material.activate()
#           soyaopengl.glBegin(soyaopengl.GL_QUADS)
#           soyaopengl.glTexCoord2f(0.46, 0.48); soyaopengl.glVertex2f(x - 10.0, y - 10.0)
#           soyaopengl.glTexCoord2f(0.46, 1.0 ); soyaopengl.glVertex2f(x - 10.0, y + 10.0)
#           soyaopengl.glTexCoord2f(1.0 , 1.0 ); soyaopengl.glVertex2f(x + 10.0, y + 10.0)
#           soyaopengl.glTexCoord2f(1.0 , 0.48); soyaopengl.glVertex2f(x + 10.0, y - 10.0)
#           soyaopengl.glEnd()
#         elif character.perso_name == "python":
#           material = soya.Material.get("python1"); material.activate()
#           soyaopengl.glBegin(soyaopengl.GL_QUADS)
#           soyaopengl.glTexCoord2f(1.0 , 0.36); soyaopengl.glVertex2f(x - 10.0, y - 10.0)
#           soyaopengl.glTexCoord2f(0.56, 0.36); soyaopengl.glVertex2f(x - 10.0, y + 10.0)
#           soyaopengl.glTexCoord2f(0.56, 1.0 ); soyaopengl.glVertex2f(x + 10.0, y + 10.0)
#           soyaopengl.glTexCoord2f(1.0 , 1.0 ); soyaopengl.glVertex2f(x + 10.0, y - 10.0)
#           soyaopengl.glEnd()
        
        
class LapsLabel(widget.Label):
  def __init__(self, character):
    self.character = character
    self.format = str(_("__racelapsformat__"))
    widget.Label.__init__(self)
    
    self.left = 10
    self.width  = 400
    self.height = 100
    self.old_nb_laps = -1
    
  def resize(self, parent_left, parent_top, parent_width, parent_height):
    self.top = parent_top + soya.root_widget.height - 43
    
  def widget_begin_round(self):
    if self.old_nb_laps != self.character.nb_laps:
      self.text = self.format % (self.character.nb_laps)
      self.old_nb_laps = self.character.nb_laps
    

class RaceChromosom:
  def __init__(self, max_speed, innitiative, will, agressivity, turbosity):
    self.max_speed   = max_speed
    self.innitiative = innitiative # Lower is better
    self.agressivity = agressivity
    self.will        = will
    self.turbosity   = turbosity
    
  def mutate(self, random):
    for attr, value in self.__dict__.iteritems():
      if attr != "max_speed":
        if random.random() < 0.4: 
          setattr(self, attr, value * (0.5 + random.random()))
      
    
  
# CHROMOSOMS = {
#   ("tux", 0): [0.23161940934461928, 0.54152636319441949, 0.057433463934462713, 1.5669823329989161, 15.877046130951882, 0.18908021610553249, 0.066441050148349098, 3.0216818334258322, 0.2 , 80.0, 30.0, 0.5],
#   ("tux", 1): [0.23161940934461928, 0.54152636319441949, 0.057433463934462713, 1.5669823329989161, 15.877046130951882, 0.18908021610553249, 0.066441050148349098, 3.0216818334258322, 0.55, 30.0, 50.0, 0.5],
#   ("tux", 2): [0.23161940934461928, 0.54152636319441949, 0.057433463934462713, 1.5669823329989161, 15.877046130951882, 0.18908021610553249, 0.066441050148349098, 3.0216818334258322, 1.0 , 20.0, 50.0, 0.6],
  
#   ("gnu", 0): [0.27955060118474129, 0.94713263528551006, 0.0076398049940541654, 0.46242007806615826, 22.758284696585228, 0.07628649333395944, 0.0051247277708940846, 5.6391784712330182, 0.1, 50.0, 50.0, 0.7],
#   ("gnu", 1): [0.27955060118474129, 0.94713263528551006, 0.0076398049940541654, 0.46242007806615826, 22.758284696585228, 0.07628649333395944, 0.0051247277708940846, 5.6391784712330182, 0.5 , 15.0, 80.0, 0.8],
#   ("gnu", 2): [0.27955060118474129, 0.94713263528551006, 0.0076398049940541654, 0.46242007806615826, 22.758284696585228, 0.07628649333395944, 0.0051247277708940846, 5.6391784712330182, 1.0 , 10.0, 99.0, 0.8],
  
#   ("shark", 0): [0.27955060118474129, 0.94713263528551006, 0.0076398049940541654, 0.46242007806615826, 22.758284696585228, 0.07628649333395944, 0.0051247277708940846, 5.6391784712330182, 0.1 , 50.0, 50.0, 0.4],
#   ("shark", 1): [0.27955060118474129, 0.94713263528551006, 0.0076398049940541654, 0.46242007806615826, 22.758284696585228, 0.07628649333395944, 0.0051247277708940846, 5.6391784712330182, 0.5 , 15.0, 50.0, 0.3],
#   ("shark", 2): [0.27955060118474129, 0.94713263528551006, 0.0076398049940541654, 0.46242007806615826, 22.758284696585228, 0.07628649333395944, 0.0051247277708940846, 5.6391784712330182, 1.0 , 10.0, 60.0, 0.2],
#   }
CHROMOSOMS = {
  ("tux",    0): RaceChromosom(0.2,  80.0,  30.0, 0.5, -7.0),
  ("tux",    1): RaceChromosom(0.6,  30.0,  50.0, 0.5, -1.0),
  ("tux",    2): RaceChromosom(1.1,  20.0,  50.0, 0.6,  0.5),
  
  ("gnu",    0): RaceChromosom(0.1,  50.0,  60.0, 0.7, -2.0),
  ("gnu",    1): RaceChromosom(0.5,  15.0,  90.0, 0.8,  0.7),
  ("gnu",    2): RaceChromosom(1.0,  10.0, 150.0, 0.9,  1.0),
  
  ("shark",  0): RaceChromosom(0.1,  40.0,  50.0, 0.3, -9.0),
  ("shark",  1): RaceChromosom(0.5,  15.0,  50.0, 0.3, -4.0),
  ("shark",  2): RaceChromosom(1.0,  10.0,  60.0, 0.2,  0.0),
  
  ("python", 0): RaceChromosom(0.2,  70.0,  30.0, 0.4, -1.0),
  ("python", 1): RaceChromosom(0.55, 25.0,  40.0, 0.4,  1.3),
  ("python", 2): RaceChromosom(1.0,  15.0,  50.0, 0.4,  2.0),
  }


class Opponent(slune_character.NonPlayerCharacter, slune_character.Competitor):
  def __init__(self, parent = None, chromosom = None):
    slune_character.NonPlayerCharacter.__init__(self, parent)
    self.chromosom = chromosom
    
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
    
    if self.vehicle == 1: self.set_vehicle(self.random.choice(globdef.VEHICLES.values()))
    
  def IAControler(self):
    c = self.chromosom = self.chromosom or CHROMOSOMS[self.perso_name, self.level.difficulty]
    self.max_speed = c.max_speed
    
    self.speed.y = 100.0 # Avoid null speed (null speed => jumping). The speed will be overrided later.
    
    while 1:
      for i in range(int(c.innitiative)):
        yield slune.controler.goto(self, self.level.flags[self.next_flag_id], turbosity = c.turbosity + 2.0 * self.life)
        
      # Check boosting
      p = [p for p in self.level.characters if p.played]
      if p:
        if len(p) == 1: p = p[0]
        else:           p = self.random.choice(p)
        delta = (self.nb_laps * len(self.level.flags) + self.next_flag_id) - (p.nb_laps * len(p.level.flags) + p.next_flag_id)
        if   (delta >  1.0) and p.level.difficulty < 2: self.max_speed = self.max_speed * 0.9
        elif (delta < -1.0) and p.level.difficulty > 0: self.max_speed = 1.1
        elif delta > 0.0: self.max_speed = c.max_speed
      else: self.max_speed = c.max_speed
      
      yield slune.controler.CheckBonus(self, self.chromosom.agressivity)
      
      if self.random.random() < c.agressivity: # Attack
        for competitor in self.level.characters:
          if not competitor is self:
            px, py, pz = self.transform_point(competitor.x, competitor.y, competitor.z, competitor.parent)
            if (-5.0 < pz < 0.0) and (-2.0 < py < 2.0) and (-5.0 < px < 5.0):
              yield slune.controler.AttackRun(self, competitor, c.will)
              break
            
            elif competitor.nb_laps >= self.nb_laps + 2: # Too late to win the race, try to kill everybody
              while 1:
                dist = 1000000.0
                best = None
                for competitor in self.level.characters:
                  d = self.distance_to(competitor) - 20.0 * competitor.nb_laps
                  if d < dist:
                    dist = d
                    best = competitor
                yield slune.controler.AttackRun(self, best, c.will)
                
          
      else: # Dodge
        for competitor in self.level.characters:
          if not competitor is self:
            px, py, pz = competitor.transform_point(self.x, self.y, self.z, self.parent)
            if (-5.0 < pz < 0.0) and (-2.0 < py < 2.0) and (-5.0 < px < 5.0):
              h = self.random.random()
              if h < 0.3:
                for i in range(10): yield slune_character.Action(slune_character.ACTION_WAIT, -1.0, self.max_speed)
              elif h < 0.6:
                for i in range(10): yield slune_character.Action(slune_character.ACTION_WAIT,  1.0, self.max_speed)
              else:
                jumping = 1
                
                yield slune_character.Action(slune_character.ACTION_JUMP, 0.0, self.max_speed)
                for i in range(2): yield slune_character.Action(slune_character.ACTION_ROTDOWN, 0.0, self.max_speed)
              break
