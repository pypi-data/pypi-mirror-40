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


w = soya.World()
#w.set_xyz(-20.0, -20.0, -20.0)
atm = soya.SkyAtmosphere()
atm.ambient = (0.2, 0.3, 0.5, 1.0)
atm.bg_color = atm.fog_color = (0.2, 0.5, 0.9, 1.0)
atm.skyplane = 1
atm.sky_color = (1.0, 1.0, 0.2, 1.0)
atm.fog_type    = 0
atm.fog_start   = 23.0
atm.fog_end     = 70.0
atm.fog         = 1
atm.fog_density = 0.001
atm.cloud = soya.Material.get("clouds1")
w.atmosphere = atm

sun = soya.Light(w)
sun.directional = 1
sun.look_at(soya.Vector(w, 0.4, -1.0, 0.3))
sun.diffuse = 1.0, 0.9, 0.6, 1.0
sun.diffuse = 0.6, 0.6, 0.3, 1.0

land = soya.Land(w)
land.from_image(soya.Image.get("map-airport.png"))
land.map_size = 8
land.scale_factor = 1.5
land.multiply_height(30.0)
land.set_material_layer(soya.Material.get("sand1"),  0.0,  13.0)
land.set_material_layer(soya.Material.get("grass1"), 12.0,  17.0)
land.set_material_layer(soya.Material.get("grass2"),  16.0, 22.0)
land.set_material_layer(soya.Material.get("rocks1"),  21.0, 50.0)

import Image # PIL

circuit = Image.open("/home/jiba/src/slune/images/map-airport-road.png")
m = soya.Material.get("ground5")
i = 0
while(i < 513):
  j = 0
  while(j < 129):
    if circuit.getpixel((i, j)) == (255, 255, 255):
      land.set_material(i, j, m)
    j = j + 1
  i = i + 1

circuit = Image.open("/home/jiba/src/slune/images/map-airport-road2.png")
m = soya.Material.get("ground1")
i = 0
while(i < 513):
  j = 0
  while(j < 129):
    if circuit.getpixel((i, j)) == (255, 255, 255):
      land.set_material(i, j, m)
    j = j + 1
  i = i + 1

# circuit = Image.open("/home/blam/data/construct/racinde_3.png")
# m = model.Material.get("ground6")
# i = 0
# while(i < 129):
#   j = 0
#   while(j < 129):
#     if circuit.getpixel((i, j)) == (0, 0, 0):
#       land.set_texture(i, j, m)
#     j = j + 1
#   i = i + 1




ww = soya.World()

#w2 = soya.World.get("construct-racinde")
#i = 0
#while (i < 3):
#  w3 = w2.children[i]
#  for face in w3:
#    ww.add(face)
#  i = i + 1

v = soya.Volume(w)
#shap = ww.shapify()
#shap.subdivide(50, 30.0)
#shap.build_tree()
#v.shape = shap
##v.set_xyz(20.0, 20.0, 20.0)



w.filename = "world-airport"
#w.save()



print '[ OK ]'
