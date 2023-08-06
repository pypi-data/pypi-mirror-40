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

import slune.globdef as globdef
import soya

def init         (*args): pass
def play_music   (*args): pass
def end_music    (): pass
def preload_sound(*args): pass
def play         (filename, position = None, speed = None, looping = 0, gain = 0): pass
def clean_mem    (*args): pass

if globdef.MUSIC or globdef.SOUND:
  def play_music   (filename):
    filename = filename.replace(".ogg", ".wav")
    soya.SoundPlayer(soya.IDLER, soya.Sound.get(filename), play_in_3D = 0, loop = 1)


  def end_music    ():
    pass

  def preload_sound(*args): pass
  def play         (filename, position = None, speed = None, looping = 0, gain = 1.0):
    filename = filename.replace(".ogg", ".wav")
    while position and (not isinstance(position, soya.World)): position = position.parent
    if position:
      soya.SoundPlayer(position, soya.Sound.get(filename), loop = looping, gain = gain)
    elif soya.IDLER:
      soya.SoundPlayer(soya.IDLER, soya.Sound.get(filename), play_in_3D = 0, loop = looping, gain = gain)
      
