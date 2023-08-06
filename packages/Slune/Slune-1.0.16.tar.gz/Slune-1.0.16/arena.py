# -*- coding: utf-8 -*-

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

from slune.fight import *
import soya.opengl as soyaopengl
import slune.globdef as globdef, slune.sound as sound

def init_arena_game(level, start_pos):
  random.shuffle(start_pos)
  level.start_pos = start_pos
  
  # Copy them in level, since the different player may have different config.
  level.arena_nb_frags     = globdef.RACE_NB_LAPS
  level.arena_nb_opponents = globdef.RACE_NB_OPPONENTS
  
  slune_character.PlayerCharacter._old_die = slune_character.PlayerCharacter.die
  slune_character.PlayerCharacter.die = _die
  
  slune_character.Character._old_die = slune_character.Character.die
  slune_character.Character.die = _die
  
def init_arena_opponent(level, character, frags_label = 1, minimap = 1):
  pos = level.start_pos.pop(0)
  if isinstance(pos, tuple):
    character.move   (pos[0])
    character.look_at(pos[1])
  else:
    character.move   (pos)
    
  level.start_pos.append(pos)
  
  character.nb_frags = 0
  
  if character.played and character.player.active:
    from py2play.idler import IDLER
    if frags_label: IDLER.no_blackbands_group.insert(0, FragsLabel(character))
    if minimap:     IDLER.no_blackbands_group.insert(0, MiniMap(character.level))
    
def start_arena_game(level):
  for i in range(level.arena_nb_opponents - len(level.characters)):
    character = Opponent()
    character.set_level(level, 1)
    init_arena_opponent(level, character)
    
  #for character in level.characters:
  #  if isinstance(character, slune_character.Competitor): init_arena_opponent(character)
  
def end_arena_game(level):
  for widget in soya.root_widget.children:
    if isinstance(widget, FragsLabel):
      soya.root_widget.remove(widget)
      break

  slune_character.PlayerCharacter.die = slune_character.PlayerCharacter._old_die
  slune_character.Character      .die = slune_character.Character      ._old_die

        

def _die(character):
  if not hasattr(character.level, "start_pos"):
    if isinstance(character, slune_character.PlayerCharacter):
      slune_character.PlayerCharacter._old_die(character)
    else:
      slune_character.Character      ._old_die(character)
    return
    
  if len(slune_character.explosions) < 4: # Limit the number of simultaneous explosions
    explode = slune_character.Explosion(character.parent)
    explode.move(character)
    explode.life = 60
    explode.particle_width = explode.particle_height = 0.7

    sound.play("explose-3.wav", explode)

  if hasattr(character.pushed_by, "nb_frags"):
    from py2play.idler  import IDLER
    from py2play.player import CURRENT_PLAYER
    IDLER.message(_("%s fragged %s!") % (character.pushed_by.displayname(), character.displayname()))
    
    character.pushed_by.nb_frags += 1
    if character.pushed_by.nb_frags >= character.level.arena_nb_frags: # Pusher has won !
      characters = character.level.characters[:]
      characters.sort(lambda a, b: cmp(b.nb_frags, a.nb_frags))
      recapitulatif = "\n".join(["%s : %s frags" % (c.displayname(), c.nb_frags) for c in characters])

      if character.pushed_by is CURRENT_PLAYER.character:
        IDLER.level_completed(CURRENT_PLAYER.character, 1, _("You have won!") + "\n" + recapitulatif)
      else:
        IDLER.level_completed(CURRENT_PLAYER.character, 0, _("__gameover__") + "\n" + recapitulatif)

    #print _("%s fragged %s!") % (character.pushed_by.displayname(), character.displayname())
    #for c in character.level.characters:
    #  print c.displayname(), c.nb_frags
    #print
    
    character.pushed_by = None # Avoid multiple frags
    
  pos = character.level.start_pos.pop(0)
  if isinstance(pos, tuple):
    character.teleport(pos[0].x, pos[0].y, pos[0].z)
    character.look_at(pos[1])
  else:
    character.teleport(pos.x, pos.y, pos.z)
  
  character.level.start_pos.append(pos)
  
  character.life = 2.0


class FragsLabel(widget.Label):
  def __init__(self, character):
    self.character = character
    self.format = "Frags : %s"
    widget.Label.__init__(self)
    
    self.left = 10
    self.width  = 400
    self.height = 100
    self.old_nb_frags = -1
    
  def resize(self, parent_left, parent_top, parent_width, parent_height):
    self.top = parent_top + soya.root_widget.height - 43
    
  def widget_begin_round(self):
    if self.old_nb_frags != self.character.nb_frags:
      self.text = self.format % self.character.nb_frags
      self.old_nb_frags = self.character.nb_frags


      
class Opponent(Fighter, slune_character.Competitor):
  die = _die
  
  def choose_target(self):
    best      = None
    best_dist = 10000.0
    for level in self.get_root():
      if isinstance(level, py2p_level.Level):
        for character in level.characters:
          if (not character is self):
            dist = character.distance_to(self)
            if dist < best_dist:
              best      = character
              best_dist = dist
    return best
  








class MiniMap(widget.Widget):
  def __init__(self, level):
    self.level = level
    self.point = Point()
    
    self.top = 10
    self.width  = 200
    self.height = 200
    self.left = soya.root_widget.width - self.width - 40
    
    flags = level.start_pos
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
    
#     for character in self.level.characters:
#       if isinstance(character, slune_character.Competitor):
#         x = self.cleft + self.f * (character.x - self.min_x)
#         y = self.ctop  + self.f * (character.z - self.min_y)
        
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
  
        
