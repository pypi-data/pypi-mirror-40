#! /usr/bin/python -O
# -*- python -*-

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

# launch this script to generate the level

import math, os, os.path
import copy

import soya
import soya.editor.main

import slune.globdef


sand0 = soya.Material()
sand0.texture = soya.Image.get("sand0.png")
sand0.filename = "sand0"
sand0.save()

sand2 = soya.Material()
sand2.texture = soya.Image.get("sand2.png")
sand2.separate_specular = 1
sand2.specular = (1.0, 1.0, 0.7, 1.0)
sand2.shininess = 10.0
sand2.filename = "sand2"
sand2.save()


w = soya.World()
atm = soya.SkyAtmosphere()
atm.ambient = (0.4, 0.3, 0.2, 1.0)
#atm.bg_color = atm.fog_color = (0.5, 0.4, 0.2, 1.0) # pour la tempête ?
atm.bg_color = atm.fog_color = (0.7, 0.6, 0.7, 1.0)
atm.skyplane = 1
atm.sky_color = (0.3, 0.7, 1.0, 1.0)
atm.fog_type    = 0
atm.fog_start   = 20.0
atm.fog_end     = 70.0
atm.fog         = 1
atm.fog_density = 0.001
atm.cloud = soya.Material.get("clouds1")
w.atmosphere = atm

sun = soya.Light(w)
sun.directional = 1
sun.look_at(soya.Vector(w, -0.4, -1.0, -0.3))
sun.diffuse = 0.8, 0.7, 0.4, 1.0

land = soya.Land(w)
land.from_image(soya.Image.get("map-desert.png"))
land.map_size = 8
land.scale_factor = 1.5
land.multiply_height(30.0)
land.set_material_layer(soya.Material.get("sand0"),  0.0,  6.0)
land.set_material_layer(soya.Material.get("sand1"), 5.0,  14.0)
land.set_material_layer(soya.Material.get("sand2"),  13.0, 22.0)
land.set_material_layer(soya.Material.get("rocks1"),  21.0, 50.0)

import Image # PIL

circuit = Image.open("/home/jiba/src/slune/images/map-desert-grass.png")
m = soya.Material.get("grass1")
i = 0
while(i < 257):
  j = 0
  while(j < 257):
    if circuit.getpixel((i, j)) == 255:
      land.set_material(i, j, m)
    j += 1
  i += 1


ww = soya.World()

v = soya.Volume(w)



w.filename = "world-desertic-sorry"
w.save()



print '[ OK ]'
