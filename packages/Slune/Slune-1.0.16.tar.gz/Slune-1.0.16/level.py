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

import os.path, time, random, cPickle as pickle
import py2play.level as level
import py2play.idler as idler
import soya, soya.widget as widget, soya.opengl as soyaopengl
import slune.globdef as globdef, slune.character, slune.sound as sound

from soya import Point, Vector

# class TravelingCamera(soya.TravelingCamera):
#   def begin_round(self):
#     pass

#   def advance_time(self, proportion):
#     pass

class FPSLabel(widget.Widget):
  """FPSLabel

A label that shows the FPS."""
  
  def resize(self, parent_left, parent_top, parent_width, parent_height):
    self.x = parent_left + parent_width  - 150
    self.y = parent_top  + parent_height - 37
    
  def render(self):
    soya.DEFAULT_MATERIAL.activate()
    soyaopengl.glColor4f(1.0, 1.0, 1.0, 1.0)
    if idler.IDLER:
      widget.default_font.draw("%.1f FPS" % idler.IDLER.fps, self.x, self.y)
    else:
      widget.default_font.draw("No idler", self.x, self.y)
      
      
class BlackBands(widget.Widget):
  """Black bands for 16/9 look."""
  
  def render(self):
    w = float(soya.get_screen_width ())
    h = float(soya.get_screen_height())
    t = h / 10.0
    soyaopengl.glColor4f(0.0, 0.0, 0.0, 1.0)
    soyaopengl.glBegin(soyaopengl.GL_QUADS)
    
    soyaopengl.glVertex2f(0.0, 0.0)
    soyaopengl.glVertex2f(0.0, t)
    soyaopengl.glVertex2f(w, t)
    soyaopengl.glVertex2f(w, 0.0)
    
    soyaopengl.glVertex2f(0.0, h - t)
    soyaopengl.glVertex2f(0.0, h)
    soyaopengl.glVertex2f(w, h)
    soyaopengl.glVertex2f(w, h - t)
    
    soyaopengl.glEnd()
    
#BLACK_BANDS =  BlackBands()


class Idler(soya.World, idler.Idler):
  #def __del__(self):
  #  print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! del Idler"
  will_render = 1
  
  def __init__(self, camera = None):
    soya .World.__init__(self)
    idler.Idler.__init__(self)
    
    self.camera = camera or soya.TravelingCamera(self)
    soya.set_root_widget(widget.Group())
    soya.root_widget.add(self.camera)

    #def f():
    #  print "!"
    #self.camera.begin_round = f
    
    sound.init(self.camera)
    
    self.blackbands_group    = widget.Group() 
    self.no_blackbands_group = widget.Group()
    soya.root_widget.add(self.no_blackbands_group)
    
    self.lifebar = slune.character.LifeBar()
    self.no_blackbands_group.add(self.lifebar)
    
    self.blackbands_group.add(BlackBands())
    
    self.blackbands_visible = 0
    
    self.players_info = []
    self.waiting_until_ready = 0
    self.paused = None
    
    soya.IDLER     = self
    soya.MAIN_LOOP = self
    
    text = soya.widget.Label(None, "", 1)
    
    def text_resize(parent_left, parent_top, parent_width, parent_height):
      text.width  = parent_width - 50 # The lifebar takes about 50 pixels !
      text.height = int(parent_height * 0.5)
      text.left   = parent_left
      text.top    = parent_top
      
    text.resize = text_resize
    soya.root_widget.add(text)
    self.messageboard = text
    self.messages = []
    
    if globdef.VERIFICATION_SERVER: self.logon_verif()
    
  def show_fps(self): soya.root_widget.add(FPSLabel())
  
  def show_blackbands(self):
    if not self.blackbands_visible:
      self.blackbands_visible = 1
      h = soya.get_screen_height()
      h2 = h / 10
      soya.root_widget.remove(self.no_blackbands_group)
      soya.root_widget.resize(0, h2, soya.get_screen_width(), h - 2 * h2)
      soya.root_widget.insert(1, self.blackbands_group)
      
  def hide_blackbands(self):
    if self.blackbands_visible:
      self.blackbands_visible = 0
      soya.root_widget.remove(self.blackbands_group)
      soya.root_widget.resize(0, 0, soya.get_screen_width(), soya.get_screen_height())
      soya.root_widget.add   (self.no_blackbands_group)
      #self.messageboard.font._image().save("/home/jiba/tmp/font.png")
    
    
  def logon_verif(self):
    """Log on the verif server."""
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((globdef.VERIFICATION_SERVER, 36081))
    self.verif = s.makefile("w", 0)
    self.verif.write("R") # Check rounds value
    
  def idle(self):
    self.message(_("__ready__"))
    
    from slune.controler import KeyboardMouseControler
    
    self.waiting_until_ready = 1
    wait = WaitUntilReady(self)
    
    for level in self:
      if isinstance(level, Level):
        for character in level.characters:
          if character.controler:
            character.controler.animate(wait)
            if isinstance(character.controler, KeyboardMouseControler):
              character.controler.enabled = 0
              
    return idler.Idler.idle(self)
    
  def pause(self, max_duration = -1): self.next_round_tasks.append(lambda : self._pause(max_duration))
  
  def _pause(self, max_duration = -1):
    if not self.paused:
      from slune.controler import KeyboardMouseControler

      self.paused = wait = WaitClick(self, max_duration)

      for level in self:
        if isinstance(level, Level):
          for character in level.characters:
            if character.controler:
              character.controler.animate(wait)
              if isinstance(character.controler, KeyboardMouseControler):
                character.controler.enabled = 0
              
  def unpause(self): self.next_round_tasks.append(self._unpause)
  
  def _unpause(self):
    if self.paused:
      from slune.controler import KeyboardMouseControler
      
      for level in self:
        if isinstance(level, Level):
          for character in level.characters:
            if isinstance(character.controler, KeyboardMouseControler):
              character.controler.enabled = 1
              
      self.paused.stop() # Stop the WaitClick instance !
      self.paused = None
      
      
  def init_game(self):
    self.camera.zap()
    
    for o in self.recursive():
      if isinstance(o, soya.World) and o.atmosphere:
        if o.atmosphere.fog:
          self.camera.back = o.atmosphere.fog_end = o.atmosphere.fog_end * globdef.MAX_VISION
          break
        
  def start_game(self):
    if self.waiting_until_ready:
      self.waiting_until_ready = 0
      self.clear_message()
      
      from slune.controler import KeyboardMouseControler
      
      for level in self:
        if isinstance(level, Level):
          for character in level.characters:
            if isinstance(character.controler, KeyboardMouseControler):
              character.controler.controlers[-1].stop() # Stop the WaitUntilReady instance !
              character.controler.enabled = 1
              
      from py2play.player import CURRENT_PLAYER
      CURRENT_PLAYER.level.start_game()
      
  def level_completed(self, character, winner = None, message = None):
    import videosequence
    
    videosequence.MissionCompleted(winner, message).start(tux = character)
    
  def begin_round(self):
    time.sleep(0.00001) # for sound
    
    # In THIS order !!! Say to Py2Play the round begin before doing anything !
    idler.Idler.begin_round(self)
    
    # The camera must be played AFTER the character, for a better visual effect (ie to avoid the character to move after the camera has been moved)
    for child in self.children: child.begin_round()
      
    soya.root_widget.widget_begin_round()
    
    if globdef.VERIFICATION_SERVER:
      import py2play.player, cPickle as pickle
      
      players_rounds = {}
      for level in self:
        if isinstance(level, Level):
          for character in level.characters:
            if hasattr(character, "player"):
              players_rounds[character.player.name] = character.round
              
      pickle.dump((players_rounds, py2play.player.CURRENT_PLAYER.name), self.verif)
      
  def advance_time(self, proportion):
    #soya.advance_time(proportion)
    for child in self.children: child.advance_time(proportion)
    soya.root_widget.widget_advance_time(proportion)
    
  def render(self):
    for i in soya.BEFORE_RENDER: i()
    soya.render()
    
  def end_round(self):
    current = time.time()
    if self.messages and (self.messages[0][1] <= current):
      del self.messages[0]
      self.messageboard.text = "\n".join([text for (text, duration) in self.messages])
      
    # In THIS order !!! Really ends the round before saying to Py2Play it is ended !
    # The camera must be played AFTER the character, for a better visual effect (ie to avoid the character to move after the camera has been moved)
    for child in self.children:
      if hasattr(child, "end_round"): child.end_round()
      
    soya.root_widget.widget_end_round()
    
    idler.Idler .end_round(self)
    
  def clear_message(self):
    self.messages *= 0
    self.messageboard.text = ""
    
  def message(self, text, duration = 7.0):
    self.messages.append((text, duration + time.time()))
    
    if len(self.messages) > 3: del self.messages[0]
    
    self.messageboard.text = "\n".join([text for (text, duration) in self.messages])
    
  def message_append(self, text, duration = 7):
    self.messages[-1] = (self.messages[-1][0] + text, duration + time.time())
    
    self.messageboard.text = "\n".join([text for (text, duration) in self.messages])
    
class WaitUntilReady:
  def __init__(self, idler):
    self._stop = 0
    self.idler = idler
    
    self.players_info = ()
    
  def stop(self): self._stop = 1
  
  def next(self):
    if self._stop: raise StopIteration
    
    from py2play.player import CURRENT_PLAYER
    
    if self.players_info != CURRENT_PLAYER.players_info:
      for player_info in CURRENT_PLAYER.players_info:
        if not player_info in self.players_info:
          self.idler.message(_("__connection__") % (player_info[0], player_info[1]))
      self.players_info = CURRENT_PLAYER.players_info[:]
        
    return slune.character.Action()
  
class WaitClick:
  def __init__(self, idler, duration = -1):
    self._stop = 0
    self.idler = idler
    self.duration = duration
  def stop(self): self._stop = 1
  
  def next(self):
    if self._stop: raise StopIteration
    if not self.duration:
      from py2play.idler import IDLER
      IDLER.unpause()
    self.duration -= 1
    return slune.character.Action()



class MessageBoard(soya.widget.Label):
  def __init__(self, master = None):
    soya.widget.Label.__init__(self, master, "", 1)
    self.messages = []
    self.left   = 0
    self.top    = 0
    self.width  = 200
    self.height = 200
  def add_message(self, text, color = soya.WHITE, time = 300):
    self.messages.append(text)
    
    if len(self.messages) > 3:
      del self.messages[0]
      
    self.text = "\n".join(self.messages)
    
  def resize(self, parent_left, parent_top, parent_width, parent_height):
    self.left   = 0
    self.top    = 0
    self.width  = parent_width
    self.height = int(parent_height * 0.5)
    
    
class Level(level.Level, soya.World):
  pushables = () # HACK ! No push before the game really starts !
  bonuss    = () # HACK !
  
  #def __del__(self):
  #  print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! del Level", self.name
  
  def set_active(self, active):
    level.Level.set_active(self, active)
    
    # The camera must be played AFTER the character, for a better visual effect (ie to avoid the character to move after the camera has been moved)
    # => insert the level at the position 0 (=before the camera)
    if self.active: idler.IDLER.insert(0, self)
    else:           idler.IDLER.remove(self)
    
  def __init__(self, parent = None):
    level.Level.__init__(self, "")
    soya .World.__init__(self, parent)
    
    self.init_script = self.init_character_script = self.start_script = self.end_script = ""
    
  def init_character(self, character):
    if isinstance(character, slune.character.Competitor) and character.controler:
      character.rank = len([character for character in self.characters if isinstance(character, slune.character.Competitor)]) - 1
      
      exec self.init_character_script in globals(), locals()
      
      character.y += character.floating
      
    character.init()
    
  def remove_character(self, character):
    if self.pushables and isinstance(character, slune.character.Pusher):
      try: self.pushables.remove(character)
      except: pass
      
    level.Level.remove_character(self, character)
    self.remove(character)
    
  def __setstate__(self, state):
    level.Level.__setstate__(self, state)
    
    from py2play.player import CURRENT_PLAYER
    if CURRENT_PLAYER:
      if not hasattr(self, "inited"): # Else already inited, e.g. by another player (in network game)
        self.inited     = 1
        self.random     = random.Random()
        self.difficulty = globdef.DIFFICULTY # Store difficulty in level, because, in network gaming, all players plays at the same difficulty !
        
        exec self.init_script
        
      if hasattr(self, "music_name"):
        if self.music_name: sound.play_music(self.music_name)
      else:
        sound.play_music("summum_of_the_light.ogg") # Default music
        
  def start_game(self):
    exec self.start_script in globals(), locals()
    
    self.pushables = [x for x in self if isinstance(x, slune.character.Pusher)]
    self.bonuss    = [x for x in self if isinstance(x, Bonus                 )]
    
    for pushable in [x for x in self if isinstance(x, slune.character.Pushable)]:
      h = self.random.random()
      if   h < pushable.bonus_chance:
        pushable.bonus_type = 1
      elif h < 2 * pushable.bonus_chance:
        pushable.bonus_type = 2
        
  def end_game(self):
    exec self.end_script in globals(), locals()
    
    sound.end_music()
    
  def begin_round(self):
    for child in self.children:
      
      #if child.__class__.__name__ in ["Bowling", "World", "Pushable", "PlayerCharacter"]:
      #if child.__class__.__name__ in ["Bowling", "World", "Pushable"]:
      #if child.__class__.__name__ in ["PlayerCharacter"]:
        child.begin_round()
        
        
def CREATE(level_name):
  if isinstance(level_name, unicode): level_name = level_name.encode("latin")
  lev = pickle.load(open(os.path.join(soya.path[0], soya.World.DIRNAME, level_name + ".data"), "rb"))
  lev.name = level_name
  level.store(lev)
  
  return lev
level.CREATE = CREATE


class SphericalScript(soya.Volume):
  def __init__(self, parent = None, script = ""):
    soya.Volume.__init__(self, parent, soya.Shape.get("sphericalscript"))
    self.script   = script
    self.radius   = 1.0
    self.disabled = 0
    
  def set_radius(self, radius):
    r = radius / self.radius
    self.scale(r, r, r)
    self.radius = radius
    
  def disable(self, nb_round = None):
    if nb_round is None: self.parent.remove(self)
    else: self.disabled += nb_round
    
  def __setstate__(self, state):
    soya.Volume.__setstate__(self, state)
    
    from py2play.player import CURRENT_PLAYER
    if CURRENT_PLAYER: self.set_shape(None)
    
  def begin_round(self):
    if not self.shape:
      if self.disabled: self.disabled -= 1
      else:
        self.set_shape(None)
        for character in self.parent.characters:
          if character.distance_to(self) <= self.radius:
            exec self.script in globals(), locals()


class Bonus:
  come_back = 1

class LifeBonus(Bonus, soya.Bonus):
  radius = 3.0
  
  def __init__(self, parent = None):
    soya.Bonus.__init__(self, parent, soya.Material.get("life1"), soya.Material.get("halo"))
    self.color    = (1.0, 0.40000000596046448, 0.20000000298023224, 1.0)
    self.disabled = 0
    
  def begin_round(self):
    if self.disabled:
      self.disabled -= 1
      if not self.disabled: self.visible = 1
      
    else:
      for character in self.parent.characters:
        if self.distance_to(character) < self.radius:
          character.life = 1.0
          sound.play("bonus-1.wav", character)
          
          LifeBonusParticle(character.parent).set_xyz(self.x, self.y + 0.3, self.z)
          
          if self.come_back:
            self.disabled  = 150
            self.visible   = 0
          else:
            self.parent.bonuss.remove(self)
            self.parent.remove(self)
          break
        
class FlameThrowerBonus(Bonus, soya.Bonus):
  radius = 3.0
  
  def __init__(self, parent = None):
    soya.Bonus.__init__(self, parent, soya.Material.get("bonus2"), soya.Material.get("halo"))
    self.color    = (0.5, 1.0, 0.5, 1.0)
    self.disabled = 0
    
  def begin_round(self):
    if self.disabled:
      self.disabled -= 1
      if not self.disabled: self.visible = 1
      
    else:
      for character in self.parent.characters:
        if self.distance_to(character) < self.radius:
          character.flame_thrower += 2
          sound.play("bonus-1.wav", character)
          
          LifeBonusParticle(character.parent).set_xyz(self.x, self.y + 0.3, self.z)
          
          if self.come_back:
            self.disabled  = 150
            self.visible   = 0
          else:
            self.parent.bonuss.remove(self)
            self.parent.remove(self)
          break
        
import math, soya

class LifeBonusParticle(soya.Particles):
  def __init__(self, parent = None, material = None, nb_particles = 30):
    soya.Particles.__init__(self, parent, material, nb_particles, 1)
    self.set_colors((0.2, 0.0, 0.1, 1.0), (1.0, 0.2, 0.6, 1.0), (0.1, 0.0, 0.0, 1.0))
    self.set_sizes ((1.0, 1.0))
    self.life = 10
    #self.regenerate()
    
  def generate(self, index):
    angle = random.random() * 3.1417
    sx =  math.cos (angle)
    sy = -math.sqrt(random.random() * 3.0)
    sz =  math.sin (angle)
    l = (0.06 * (1.5 + random.random())) / math.sqrt(sx * sx + sy * sy + sz * sz)
    self.set_particle(index, 0.5 + random.random(), sx * l, sy * l, sz * l, 0.0, 0.03, 0.0)
    
  def aaabegin_round(self):
    soya.Particles.begin_round(self)
    if   self.life >  0: self.life -= 1
    elif self.life == 0:
      self.auto_generate_particle = 0
      #self.removable = 1
      self.life = -1

