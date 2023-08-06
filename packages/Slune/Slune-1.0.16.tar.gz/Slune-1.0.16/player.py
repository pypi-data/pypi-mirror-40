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

import soya, slune.globdef as globdef
import py2play.idler as idler
from py2play.player import ActivePlayer
import py2play.player, py2play.level
from slune.character import PlayerCharacter
from slune.controler import *
from slune.sound import end_music


def start_new_game(level_name):
  #soya.init(width = globdef.SCREEN_WIDTH, height = globdef.SCREEN_HEIGHT)
  #soya.cursor_set_visible(0)
  #if globdef.FULLSCREEN: soya.toggle_fullscreen()
  
  import slune.level
  idler = slune.level.Idler()
  idler.show_fps()
  idler.camera.fov  = 60.0
  idler.camera.back = 50.0
  
  # HACK ! Needed because CURRENT_PLAYER == None means that we are in "editor mode" and not in "game mode" (see slune.level.Level.__setstate__).
  py2play.player.CURRENT_PLAYER = 1
  
  level  = py2play.level.CREATE(level_name)
  player = create_player(globdef.NAME, globdef.PORT, level)
  
  if level.filename.startswith("level-mission"):
    player.character.set_perso("tux")
    
  level.set_active(1)
  level.filename = None
  
  #idler.camera.add_traveling(soya.ThirdPersonTraveling(player.character.camera_target))
  t = soya.ThirdPersonTraveling(player.character.camera_target)
  t.offset_y = 0.9
  idler.camera.add_traveling(t)
  
  idler.init_game()
  
  
  #idler.camera.add_traveling(soya.FixTraveling(None, Vector(None, 0.0, 0.0, 1.0)))
  #idler.camera.add_traveling(soya.FixTraveling(None, Vector(None, 1.0, 0.0, 0.0)))
  #idler.camera.add_traveling(soya.FixTraveling(None, Vector(None, -1.0, 0.0, 0.0)))
  #idler.camera.set_xyz(290.0, 22.0, 130.0)
  
#   for e in level.recursive():
#     if isinstance(e, soya.Light):
#       e.look_at(soya.Vector(None, 0.0, -1.0, 1.0))
#   w = soya.World()
#   f = soya.Face(w, [
#     soya.Vertex(w, -10.0, 0.0, -10.0),
#     soya.Vertex(w,  10.0, 0.0, -10.0),
#     soya.Vertex(w,  10.0, 0.0,  10.0),
#     soya.Vertex(w, -10.0, 0.0,  10.0),
#     ])
#   f.double_sided = 1
#   w.shapifier = soya.SimpleShapifier()
#   w.shapifier.shadow = 1
#   v = soya.Volume(level, w.shapify())
#   v.set_xyz(290.0, 30.0, 120.0)
  
  r = idler.idle()
  
  #soya.cursor_set_visible(1)
  #if globdef.FULLSCREEN: soya.toggle_fullscreen()
  
  
  #import gc, weakref, soya.soya3d as soya3d, memtrack
  #idler_ = weakref.ref(idler)
  #level_ = weakref.ref(level)
  #player_= weakref.ref(player)
  
  # Del these ref in order to clean_mem() to be able to work.
  idler = None
  level = None
  player = None
  clean_mem()
  
  end_music()
  
#   if idler_():
#     print "Idler :"
#     for i in gc.get_referrers(idler_()):
#       print
#       print repr(i)
#       print
      
#       #if isinstance(i, dict):
#       #  for k in i.keys():
#       #    if i[k] is idler_(): i[k] = None
#       #if hasattr(i, "parent"):
#       #  i.parent.remove(i)
      
#   if level_():
#     print "Level :"
#     refs = gc.get_referrers(level_())
#     #refs = filter(lambda i: not isinstance(i, soya3d.Volume), refs)
#     #world_ = weakref.ref(filter(lambda i: isinstance(i, soya3d.World), refs)[0])
#     #refs = filter(lambda i: not isinstance(i, soya3d.World), refs)
#     refs = filter(lambda i: not isinstance(i, dict), refs)
    
#     for i in refs:
#       print
#       print repr(i)
#       print
      
#       if isinstance(i, dict):
#         for k in i.keys():
#           if i[k] is level_(): i[k] = None
#       if hasattr(i, "parent"):
#         i.parent.remove(i)
#     i    = None
#     refs = None
#   print
#   print
  
#  gc.collect()
#  gc.collect()
#  gc.collect()
#  gc.collect()
#  gc.collect()
  
#   if idler_():
#     print "idler :", gc.get_referrers(idler_())
#     print len(gc.get_referrers(idler_()))
#     print gc.garbage, idler_()
    
#   print
#  if level_():
#     print "level :"
#     for i in gc.get_referrers(level_()): print i
#     i = None
#     print len(gc.get_referrers(level_()))
#     print level_()

    
#    print
#    memtrack.dump(*memtrack.track(idler_()))
#    #memtrack.dump(*memtrack.reverse_track(idler_()))
    
#   #f = gc.get_referrers(idler_())[1]
#   #print "f", f
#   #print dir(f)
#   #print f.f_locals
    
#   from slune.character import HACK
#   memtrack.dump(*memtrack.reverse_track(HACK()))
  
  
#  print "garbage", gc.garbage
  
  return r

def join_network_game():
  #soya.init(width = globdef.SCREEN_WIDTH, height = globdef.SCREEN_HEIGHT)
  #soya.cursor_set_visible(0)
  #if globdef.FULLSCREEN: soya.toggle_fullscreen()
  
  import slune.level, socket
  idler = slune.level.Idler()
  idler.show_fps()
  idler.camera.fov  = 60.0
  idler.camera.back = 50.0
  
  try:
    player = parrain_by_player(globdef.NAME + "_2", globdef.PORT, globdef.PARRAIN_HOST, globdef.PARRAIN_PORT)
  except socket.error, ex:
    msg = _("Cannot join multiplayer game at %s:%s %s!") % (globdef.PARRAIN_HOST, globdef.PARRAIN_PORT, ex)
    try:
      print "* Slune * " + msg.encode("latin")
    except: pass
    
    if globdef.GUI:
      import tkMessageBox
      tkMessageBox.showerror(_("Network error!"), msg)
      
    return
    
  level = player.level
  
  level.set_active(1)
  level.filename = None
  
  idler.camera.add_traveling(soya.ThirdPersonTraveling(player.character.camera_target))
  idler.init_game()
  
  r = idler.idle()
  
  #soya.cursor_set_visible(1)
  #if globdef.FULLSCREEN: soya.toggle_fullscreen()
  
  end_music()
  return r
  

def create_player(name, port, level):
  player = ActivePlayer(level, name, "", port)
  
  
  character = PlayerCharacter(player)
  player.controler = KeyboardMouseControler(character)
  character.set_level(level, 1)
  
  
  idler.IDLER.lifebar.character = character
  
  return player

def parrain_by_player(name, port, parrain_host, parrain_port = 36079):
  player = ActivePlayer(None, name, "", port)
  player.parrained_by(parrain_host, parrain_port)
  
  character = PlayerCharacter(player)
  player.controler = KeyboardMouseControler(character)
  character.set_level(player.level, 1)
  
  idler.IDLER.lifebar.character = character
  
  return player

def clean_mem():
  import slune.character as slune_character
  
  idler.IDLER = None
  py2play.player.CURRENT_PLAYER = None
  
  slune_character._P  = soya.Point()
  slune_character._P2 = soya.Point()
  slune_character._P3 = soya.Point()
  slune_character._V  = soya.Vector()
  slune_character._V2 = soya.Vector()
  slune_character.explosions *= 0
  
  soya.set_root_widget(None)

  sound.clean_mem()
  
  import gc; gc.collect() # Perform GC after, rather than while, playing !!!
