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

import soya, soyasdlconst
import editobj, editobj.editor as editor, editobj.custom as custom
import soya.editor, soya.editor.world
from soya import Point, Vector

import slune.level, slune.race, slune.fight, slune.character

custom.EVAL_ENV.update({
  "race"  : slune.race,
  "fight" : slune.fight,
  })

custom.register_attr("script"               , editor.TextEditor)
custom.register_attr("init_script"          , editor.TextEditor)
custom.register_attr("init_character_script", editor.TextEditor)
custom.register_attr("start_script"         , editor.TextEditor)
custom.register_attr("end_script"           , editor.TextEditor)

slune.race.Flag                .__clickmanager__ = soya.editor.world.MoveClickManager
slune.level.LifeBonus          .__clickmanager__ = soya.editor.world.MoveClickManager
slune.level.FlameThrowerBonus  .__clickmanager__ = soya.editor.world.MoveClickManager
slune.level.SphericalScript    .__clickmanager__ = soya.editor.world.MoveClickManager
slune.character.Pushable       .__clickmanager__ = soya.editor.world.MoveClickManager
slune.character.TakeableVehicle.__clickmanager__ = soya.editor.world.MoveClickManager

_LAST_BARRIER = None
_LAST_BARRIER_TYPE = 0
_BARIER_TYPES = [slune.character.Barrier, slune.character.Barrier2, slune.character.TreeTrunc, slune.character.Quille, slune.character.Ball]

def _add_flag              (root, current): slune.race.Flag(root)
def _add_life_bonus        (root, current): slune.level.LifeBonus(root)
def _add_flamethrower_bonus(root, current): slune.level.FlameThrowerBonus(root)
def _add_sphericalscript   (root, current): slune.level.SphericalScript(root)
def _add_takeablevehicle   (root, current): slune.character.TakeableVehicle(root)
def _add_barrier           (root, current):
  global _LAST_BARRIER
  _LAST_BARRIER = _BARIER_TYPES[_LAST_BARRIER_TYPE](root)
def _change_last_barrier(root, current):
  global _LAST_BARRIER_TYPE
  if _LAST_BARRIER_TYPE < len(_BARIER_TYPES) - 1: _LAST_BARRIER_TYPE += 1
  else:                                           _LAST_BARRIER_TYPE  = 0
  _BARIER_TYPES[_LAST_BARRIER_TYPE](root, _LAST_BARRIER)

def _put_down(root, current):
  cursor = root.parent.parent["cursor"]
  
  result = root.raypick(cursor, Vector(root, 0.0, -1.0, 0.0), -1.0, 2)
  
  if result:
    p, v = result
    cursor.add_vector(cursor >> p)
    cursor.button_pressed(1)
    cursor.button_released(1)
    
soya.editor.world.KEY_BINDINGS[soyasdlconst.K_d] = _put_down
soya.editor.world.KEY_BINDINGS[soyasdlconst.K_f] = _add_flag
soya.editor.world.KEY_BINDINGS[soyasdlconst.K_s] = _add_sphericalscript
soya.editor.world.KEY_BINDINGS[soyasdlconst.K_b] = _add_barrier
soya.editor.world.KEY_BINDINGS[soyasdlconst.K_n] = _change_last_barrier
soya.editor.world.KEY_BINDINGS[soyasdlconst.K_l] = _add_life_bonus
soya.editor.world.KEY_BINDINGS[soyasdlconst.K_p] = _add_flamethrower_bonus
soya.editor.world.KEY_BINDINGS[soyasdlconst.K_v] = _add_takeablevehicle
