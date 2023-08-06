#! /usr/bin/python -O
# -*- python -*-

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

# launch this script to generate the level

import math, os, os.path
import copy

import Tkinter

import soya
import soya.model  as model
import soya.soya3d as soya3d
import soya.editor.main
import soya.land

import slune.level

import circuit_generator
import town_generator

soya.init()



c = soya3d.World.get('construct-urbancall')

w = soya3d.World()
w.shapify_args = ('tree', {})
w.add(c.children[0])
b = c.children[1]

for v in b:
    if v.shape:
        q = soya3d.World(w)
        q._matrix = v._matrix
        v.shape.to_faces(q)
        for f in q:
            for ve in f:
                ve.color = None
    else:
        w.add(v)


w.filename = "shape-urbancall"
w.save()

print '[ OK ]'

import sys
sys.exit(0)



scene = soya3d.World()

atm = soya3d.Atmosphere()
atm.ambient = (0.55, 0.53, 0.5, 1.0)
atm.bg_color  = (0.51, 0.51, 0.51, 1.0)
atm.skyplane = 1
atm.sky_color = (0.8, 0.6, 1.0, 1.0)
atm.fog_color = atm.bg_color
atm.fog_type    = 0
atm.fog_start   = 20.0
atm.fog_end     = 50.0
atm.fog         = 1
atm.fog_density = 0.001
atm.cloud = model.Material.get("clouds1")
scene.atmosphere = atm

light = soya3d.Light(scene)
light.directional = 1



model.Material.PATH = "/home/blam/prog/slune/materials"




def make_land():

    def set_material_area(material, x, y, w, h):
        j = 0
        while j < h:
            i = 0
            while i < w:
                land.set_texture(x + i, y + j, m)
                i += 1
            j += 1
    
    land = soya.land.Land()
    land.scale_factor = 1.5
    land.from_image(model.Image("/home/blam/data/urbancall_land.png"))
    land.map_size = 8
    land.multiply_height(8.0)
#    land.add_height(-10.0)
    land.set_texture_layer(model.Material.get("ground2"), 0.0,  150.0)
    land.set_texture_layer(model.Material.get("sand1"), 1.0,  150.0)
#    land.set_texture_layer(model.Material.get("grass1"), 1.0,  150.0)

    m = model.Material.get("grass1")
    set_material_area(m, 36, 87, 2, 9)
    set_material_area(m, 41, 87, 2, 9)
    set_material_area(m, 36, 100, 2, 11)
    set_material_area(m, 41, 100, 2, 11)

    import Image

    map = Image.open("/home/blam/data/urbancall_land_materials.png")
    m = model.Material.get("ground4")
    i = 0
    while(i < 129):
        j = 0
        while(j < 129):
            if map.getpixel((i, j)) == (255, 0, 0):
                land.set_texture(i, j, m)
            j = j + 1
        i = i + 1

    land.set_texture_layer(model.Material.get("grass1"), 3.0,  150.0)
    land.set_texture_layer_angle(model.Material.get("rocks3"), 0.0, 150.0, 40.0, 90.0)

    return land










m1 = model.Material.get('building1')
m2 = model.Material.get('house1win')
m3 = model.Material.get('ground1')
m4 = model.Material.get('building4')

m5 = model.Material.get('house3')
m6 = model.Material.get('house3b')
m7 = model.Material.get('bark1')

m8 = model.Material.get('inde_2')
m9 = model.Material.get('inde_4')
m10 = model.Material.get('inde_1')
m11 = model.Material.get('inde_3')

m12 = model.Material.get('building3')
m13 = model.Material.get('building5')
m14 = model.Material.get('building6')

m15 = model.Material.get('brick1')
m16 = model.Material.get('brick1win')
m17 = model.Material.get('tile2')

m18 = model.Material.get('planches1')
m19 = model.Material.get('window1')
m20 = model.Material.get('thatch1')

m21 = model.Material.get('taj1')

m22 = model.Material.get('column2a')
m23 = model.Material.get('column2b')

m24 = model.Material.get('house1')
m25 = model.Material.get('house1win')

m26 = model.Material.get('house2a')
m27 = model.Material.get('house2b')

m28 = model.Material.get('inde_6')

m_glass_1 = (m12, 'plak round', 0.5, 'complete', 1.0)
m_glass_2 = (m12, 'plak round', 0.5, 'complete', 2.0)
m_wall_1 = (m1, 'plak', 1.0, 'complete', 1.0)
m_wall_2 = (m1, 'plak', 1.0, 'complete', 2.0)
m_roof = (m3, 'plak', 1.0, 'plak', 1.0)
m_corniche = (m4, 'plak', 1.0, 'complete', 1.0)
m_house3_1 = (m5, 'plak round', 0.5, 'complete', 1.0)
m_house3_2 = (m6, 'plak round', 1.0, 'complete', 1.0)
m_bark = (m7, 'plak', 1.0, 'plak', 1.0)
m_indebloc_1 = (m8, 'plak round', 1.0, 'complete', 1.0)
m_indebloc_2 = (m8, 'plak round', 1.0, 'complete', 2.0)
m_indehole = (m11, 'plak round', 1.0, 'complete', 1.0)
m_indefrise = (m10, 'plak round', 1.0, 'complete', 1.0)
m_indefrise2 = (m8, 'plak round', 1.0, 'complete', 2.0)
m_build_1 = (m13, 'plak round', 0.5, 'complete', 1.0)
m_build_2 = (m13, 'plak round', 0.5, 'complete', 2.0)
m_glass_3 = (m14, 'plak round', 0.5, 'complete', 3.0)
m_glass_4 = (m14, 'plak round', 0.5, 'complete', 2.0)
m_ground_1 = (m3, 'plak', 1.0, 'complete', 1.0)
m_ground_2 = (m3, 'plak', 1.0, 'complete', 2.0)
m_ground_3 = (m3, 'plak', 1.0, 'complete', 3.0)
m_church = (m15, 'plak round', 1.0, 'complete', 2.0)
m_churchwin = (m16, 'plak round', 1.0, 'complete', 1.0)
m_churchtile = (m17, 'plak', 1.0, 'plak', 1.0)
m_wood = (m18, 'plak round', 1.0, 'complete', 2.0)
m_woodwin = (m19, 'plak round', 1.0, 'complete', 1.0)
m_minaret = (m21, 'plak round', 1.0, 'complete', 1.0)
m_old_1 = (m23, 'plak', 1.0, 'complete', 2.0)
m_old_2 = (m22, 'plak', 1.0, 'complete', 2.0)
m_old_3 = (m23, 'plak', 1.0, 'complete', 1.0)
m_tavern = (m24, 'plak round', 0.5, 'complete', 3.0)
m_tavernwin = (m25, 'plak round', 1.0, 'complete', 1.0)
m_white = (m27, 'plak round', 1.0, 'complete', 1.0)
m_whitewin = (m26, 'plak round', 1.0, 'complete', 1.0)
m_gold = (m28, 'plak', 1.0, 'plak', 1.0)


def set_style_tower1(h):
    h.section = [(0.0, 0.0), (0.0, 2.0), (0.0, 4.0), (0.25, 4.25),
                 (0.0, 4.5), (0.0, 8.5), (0.25, 8.75),
                 (0.0, 9.0), (0.0, 13.0), (0.25, 13.25)
                 ]
    h.materials = [ m_wall_2, m_glass_1, m_corniche, m_corniche,
                    m_glass_2, m_corniche, m_corniche,
                    m_glass_2, m_corniche
                    ]
    if len(h.points) <= 4:
        h.roof = ('flat', m3)

def set_style_tower2(h):
    h.section = [(0.0, 0.0), (0.0, 1.0), (0.0, 5.0),
                 (0.0, 6.0), (0.0, 10.0),
                 (0.0, 11.0), (0.0, 15.0),
                 (0.0, 16.0), (0.0, 18.0), (0.0, 19.0)
                 ]
    h.materials = [ m_wall_1, m_build_2, m_wall_1, m_build_2, m_wall_1, m_build_2, m_wall_1, m_build_1, m_wall_1
                    ]
    if len(h.points) <= 4:
        h.roof = ('flat', m3)

def set_style_tower_decal(h):
    h.section = [(0.0, 0.0), (0.0, 1.0), (0.0, 5.0), (0.0, 6.0),
                 (-1.0, 6.0), (-1.0, 7.0), (-1.0, 9.0), (-1.0, 10.0),
                 (-2.0, 10.0), (-2.0, 11.0), (-2.0, 13.0), (-2.0, 14.0)
                 ]
    h.materials = [ m_wall_1, m_build_2, m_wall_1, m_ground_1,
                    m_wall_1, m_build_1, m_wall_1, m_ground_1,
                    m_wall_1, m_build_1, m_wall_1
                    ]
    if len(h.points) <= 4:
        h.roof = ('flat', m3)

def set_style_tower3(h):
    h.section = [(0.0, 0.0), (0.0, 1.0), (0.0, 7.0),
                 (0.0, 8.0), (0.0, 14.0), (0.0, 15.0)
                 ]
    h.materials = [ m_wall_1, m_glass_3, m_wall_1, m_glass_3, m_wall_1
                    ]
    if len(h.points) <= 4:
        h.roof = ('flat', m3)
        
def set_style_tower_high_decal(h):
    h.section = [(0.0, 0.0), (0.0, 1.0), (0.0, 5.0), (0.0, 6.0), (0.0, 8.0), (0.0, 9.0),
                 (-3.0, 9.0), (-3.0, 10.0), (-3.0, 14.0), (-3.0, 15.0)
                 ]
    h.materials = [ m_wall_1, m_glass_4, m_wall_1, m_build_1, m_wall_1, m_ground_3,
                    m_wall_1, m_glass_4, m_wall_1
                    ]
    if len(h.points) <= 4:
        h.roof = ('flat', m3)

def set_style_yellow(h):
    h.section = [(0.0, 0.0), (0.0, 2.0), (0.2, 2.2), (0.2, 3.2),
                 (0.0, 3.4), (0.0, 5.4), (0.2, 5.6), (0.2, 6.6),
                 ]
    h.materials = [ m_house3_1, m_bark, m_house3_2, m_bark, m_house3_1, m_bark, m_house3_2 ]
    if len(h.points) == 4:
        h.roof = ('trapez', m7, m7, 3.0, 3.0, 0.5, 3.0)

def set_style_church(h):
    h.section = [(0.0, 0.0), (0.0, 2.0), (0.0, 3.0), (-1.0, 4.0),
                 (-1.0, 6.0), (-1.0, 7.0)
                 ]
    h.materials = [ m_church, m_churchwin, m_churchtile, m_church, m_churchwin
                    ]
    h.roof = ('pyramid', m17, 3.0, 0.5, 'complete', 3.0)

def set_style_wood(h):
    h.section = [(0.0, 0.0), (0.0, 2.0), (0.0, 3.0), 
                 ]
    h.materials = [ m_wood, m_woodwin
                    ]
    h.roof = ('pyramid', m20, 2.5, 0.5, 'complete', 2.5)

def set_style_indus(h):
    h.section = [(0.0, 0.0), (0.0, 2.0), (0.0, 3.0), (-0.5, 4.0), (-0.5, 5.0), (-0.5, 6.0), (-0.5, 7.0)
                 ]
    h.materials = [ m_indebloc_2, m_indehole, m_bark, m_indebloc_1, m_indehole, m_indefrise ]
#    h.section = [(0.0, 0.0), (0.0, 2.0), (0.0, 3.0), (-0.5, 4.0), (-0.5, 5.0), (-0.5, 6.0), (-1.0, 7.0)
#                 ]
#    h.materials = [ m_indebloc_2, m_indehole, m_indefrise, m_indebloc_1, m_indehole, m_indefrise ]
    if len(h.points) == 4:
        h.roof = ('trapez', m9, m8, 2.5, 0.0, 0.5, 3.0)

def set_style_minaret(h):
    h.section = [(0.0, 0.0), (0.0, 1.0), (0.0, 3.0), (0.0, 4.0), (0.0, 6.0), (1.0, 7.0)
                 ]
    h.materials = [ m_wall_1, m_minaret, m_wall_1, m_minaret, m_wall_1 ]
    h.roof = ('pyramid', m17, 3.0, 0.5, 'complete', 3.0)

def set_style_minaret2(h):
    h.section = [(0.0, 0.0), (0.0, 1.0), (0.0, 3.0), (0.0, 4.0), (0.0, 6.0), (1.0, 7.0),
                 (-1.0, 7.0), (-1.0, 8.0), (-1.0, 10.0), (0.0, 11.0)
                 ]
    h.materials = [ m_wall_1, m_minaret, m_wall_1, m_minaret, m_wall_1,
                    m_ground_2, m_wall_1, m_minaret, m_wall_1
                    ]
    h.roof = ('pyramid', m17, 3.0, 0.5, 'complete', 3.0)

def set_style_old(h):
    h.section = [(0.0, 0.0), (-0.5, 1.0), (-0.5, 3.0), (0.0, 4.0),
                 (-1.0, 5.0), (-3.0, 6.0)
                 ]
    h.materials = [ m_old_1, m_old_2, m_old_1,
                    m_gold, m_gold ]
    h.roof = ('pyramid', m28, 1.5, 1.0, 'complete', 1.0)
        
def set_style_tavern(h):
    h.section = [(0.0, 0.0), (0.0, 3.0), (0.0, 4.0), (-1.0, 5.0), (-1.0, 8.0), (-1.0, 9.0)
                 ]
    h.materials = [ m_tavern, m_tavernwin, m_bark, m_tavern, m_tavernwin
                    ]
    if len(h.points) == 4:
        h.roof = ('trapez', m7, m7, 2.5, 2.0, 0.5, 3.0)

def set_style_white(h):
    h.section = [(0.0, 0.0), (0.0, 1.0), (0.0, 3.0), (0.0, 4.0), (0.0, 6.0)
                 ]
    h.materials = [ m_white, m_whitewin, m_white, m_whitewin
                    ]
    if len(h.points) == 4:
        h.roof = ('trapez', m17, m27, 2.5, 0.0, 0.5, 3.0)

def set_style_tower_inde(h):
    h.section = [(0.0, 0.0), (0.0, 2.0), (-0.2, 2.2), (-0.2, 4.2), (-0.4, 4.4), (-0.4, 6.4), (-0.6, 6.6), (-0.6, 8.6)]
    h.materials = [ m_indefrise2, m_bark,
                    m_indefrise2, m_bark,
                    m_indefrise2, m_bark,
                    m_indefrise2
                    ]
    h.roof = ('trapez', m7, m8, 3.0, 0.0, 1.0, 2.0)
    

STYLES = [
    set_style_tower1,
    set_style_tower2,
    set_style_tower3,
    set_style_tower_decal,
    set_style_tower_high_decal,
    set_style_indus,
    set_style_yellow,
    set_style_church,
#    set_style_wood,
    set_style_minaret,
    set_style_minaret2,
    set_style_old,
    set_style_tavern,
    set_style_white,

    ]


STYLES_DICT = {

    (0, 0, 0) : set_style_old,
    (128, 128, 128) : set_style_indus,
    (0, 255, 0) : set_style_minaret,
    (0, 128, 0) : set_style_minaret2,
    (255, 255, 0) : set_style_yellow,
    (128, 0, 0) : set_style_tavern,
    (128, 128, 255) : set_style_tower_inde,

    (255, 0, 255) : set_style_tower1,
    (255, 0, 0) : set_style_tower2,
    (0, 0, 255) : set_style_tower3,

    (0, 0, 128) : set_style_tower_decal,
    (0, 255, 255) : set_style_tower_high_decal,

    (255, 255, 255) : set_style_tower3,

    }



land = make_land()
scene.shape = land

#buildings = soya3d.World()
buildings = town_generator.make_city("/home/blam/data/urbancall.png", "/home/blam/data/urbancall_styles.png", STYLES_DICT, land, scale = 1.5)

#buildings = town_generator.make_city("/home/blam/data/densecity2.png", "/home/blam/data/urbancall_styles.png", STYLES_DICT, scene.shape, scale = 1.0)
#buildings = town_generator.make_city("/home/blam/data/densecity.png", None, STYLES, scene.shape)


# some special buildings added
v = soya3d.World(buildings)
h = town_generator.House(town_generator.make_octogon(3.0, 1.0))
h.section = [(0.0, 0.0), (0.0, 0.25), (-0.25, 0.5)]
h.materials = [ m_old_3, m_old_3 ]
h.roof = ('pyramid', m28, 0.0, 1.0, 'plak', 1.0)
h.translate_points(150.0, 123.0)
h.draw(v)
h.set_on_land(land, v)
v.y = -1.5


# for concave buildings, must hide landscape specialy
ps = [(102.089859009, 58.6109313965), (116.946487427, 58.5390625), (116.91015625, 65.921875), (102.089859009, 65.921875)]
h = town_generator.House(ps)
h.set_on_land(land)
ps = [(102.08984375, 58.6007843018), (102.08984375, 73.4265670776), (109.383399963, 73.3726577759), (109.383399963, 58.6007843018)]
h = town_generator.House(ps)
h.set_on_land(land)
ps = [(117.059570312, 75.0983123779), (121.389450073, 75.0773468018), (121.389450073, 89.9033889771), (117.101951599, 89.9033889771)]
h = town_generator.House(ps)
h.set_on_land(land)
ps = [(114.123146057, 82.5742263794), (124.385452271, 82.6014404297), (124.385452271, 86.9033889771), (114.101951599, 86.9033889771)]
h = town_generator.House(ps)
h.set_on_land(land)
ps = [(138.28843689, 109.77797699), (161.723068237, 109.766601562), (161.723068237, 113.515975952), (138.28843689, 113.495613098)]
h = town_generator.House(ps)
h.set_on_land(land)
ps = [(138.293716431, 132.481170654), (161.705337524, 132.491348267), (161.705337524, 136.208969116), (138.293716431, 136.197601318)]
h = town_generator.House(ps)
h.set_on_land(land)
ps = [(91.602645874, 132.106262207), (110.903335571, 132.085296631), (110.903335571, 139.429168701), (91.5986480713, 139.429168701)]
h = town_generator.House(ps)
h.set_on_land(land)
ps = [(71.9325332642, 150.075393677), (71.8901519775, 164.903640747), (68.9972763062, 164.903640747), (69.0614547729, 150.075393677)]
h = town_generator.House(ps)
h.set_on_land(land)


# add palmtrees
v = soya3d.World(buildings)
v.shape = model.Shape.get('palmtree1')
v.scale(0.4, 0.4, 0.4)
v.set_xyz(55.0, 1.9, 133.5)

v = soya3d.World(buildings)
v.shape = model.Shape.get('palmtree1')
v.scale(0.4, 0.4, 0.4)
v.rotate_lateral(180.0)
v.set_xyz(62.5, 1.9, 133.5)

v = soya3d.World(buildings)
v.shape = model.Shape.get('palmtree1')
v.scale(0.4, 0.4, 0.4)
v.set_xyz(55.0, 1.9, 138.5)

v = soya3d.World(buildings)
v.shape = model.Shape.get('palmtree1')
v.scale(0.4, 0.4, 0.4)
v.rotate_lateral(180.0)
v.set_xyz(62.5, 1.9, 138.5)

v = soya3d.World(buildings)
v.shape = model.Shape.get('palmtree1')
v.scale(0.4, 0.4, 0.4)
v.set_xyz(55.0, 1.9, 153.5)

v = soya3d.World(buildings)
v.shape = model.Shape.get('palmtree1')
v.scale(0.4, 0.4, 0.4)
v.rotate_lateral(180.0)
v.set_xyz(62.5, 1.9, 153.5)

v = soya3d.World(buildings)
v.shape = model.Shape.get('palmtree1')
v.scale(0.4, 0.4, 0.4)
v.set_xyz(55.0, 1.9, 161.0)

v = soya3d.World(buildings)
v.shape = model.Shape.get('palmtree1')
v.scale(0.4, 0.4, 0.4)
v.rotate_lateral(180.0)
v.set_xyz(62.5, 1.9, 161.0)

v = soya3d.World(buildings)
v.shape = model.Shape.get('shape-urbancall-add')






#for v in buildings.children:
#    if isinstance(v, soya3d.World):
#        if not v.shape:
#            v.shape = v.shapify()
#            v.children = []
##         if v.shape:
##             v.translate(0.0, -1.5, 0.0)
##             v.shape.to_faces(v)
##             for f in v:
##                 for ve in f:
##                     ve.color = None
##             v.shape = None
#scene.add(buildings)


v = soya3d.Volume(scene)
#v.shape = buildings.shapify()
#v.y = 1.5
v.shape = model.Shape.get('shape-urbancall')



scene.filename = "world-urbancall"
scene.save()


print '[ OK ]'

soya.editor.edit(scene)
Tkinter.mainloop()


