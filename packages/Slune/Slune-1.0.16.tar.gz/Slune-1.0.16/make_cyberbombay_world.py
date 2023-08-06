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



def make_land():

    land = soya.land.Land()
    land.from_image(model.Image("/home/blam/data/bombay2.png"))
    land.map_size = 8
    land.scale_factor = 1.5
    land.multiply_height(35.0)
    land.add_height(-10.0)
    land.set_texture_layer(model.Material.get("ground4"), 0.0,  150.0)
    land.set_texture_layer(model.Material.get("rocks3"), 7.0, 150.0)
    land.set_texture_layer_angle(model.Material.get("sand1"), 0.0, 150.0, 0.0, 10.0)
    land.set_texture_layer_angle(model.Material.get("ground5"), 0.0, 4.0, 0.0, 10.0)
    land.set_texture_layer_angle(model.Material.get("rocks3"), 0.0, 150.0, 50.0, 90.0)

    # make wholes for metro

    def make_whole (x, y, w, h):
        j = 0
        while j < h:
            i = 0
            while i < w:
                land.add_point_option(x + i, y + j, 1 | 4 | 8)
                i += 1
            j += 1

    def add_height (x, y, h):
        land.set_height(x, y, land.get_height (x, y) + h)

    def add_height_area (x, y, w, h, a):
        j = 0
        while j < h:
            i = 0
            while i < w:
                land.set_height(x + i, y + j, land.get_height (x + i, y + j) + a)
                i += 1
            j += 1

    # whole 1
    add_height_area (50, 85, 4, 2, 0.4)
    add_height_area (50, 86, 4, 1, 0.2)
    add_height(50, 86, -0.2)
    make_whole(50, 86, 4, 3)

    add_height(54, 88, -0.4)
    add_height(53, 88, -0.6)
    add_height(52, 88, -0.4)

    # whole 2
    land.set_height(66, 44, land.get_height (66, 44) + 0.1)
    land.set_height(67, 45, land.get_height (67, 45) + 0.4)
    land.set_height(68, 45, land.get_height (68, 45) + 0.5)
    land.set_height(67, 44, land.get_height (67, 44) + 0.4)
    land.set_height(68, 44, land.get_height (68, 44) + 0.4)
    add_height(66, 44, -0.1)
    add_height(65, 43, -1.0)
    land.add_point_option(65, 43, 1 | 4 | 8)
    land.add_point_option(65, 44, 1 | 4 | 8)
    land.add_point_option(67, 45, 1 | 4 | 8)
    land.add_point_option(66, 44, 1 | 4 | 8)
    land.add_point_option(66, 45, 1 | 4 | 8)
    land.add_point_option(64, 44, 1 | 4 | 8)
    land.add_point_option(65, 45, 1 | 4 | 8)
    land.add_point_option(66, 46, 1 | 4 | 8)
    land.add_point_option(64, 45, 1 | 4 | 8)
    land.add_point_option(65, 46, 1 | 4 | 8)
    land.add_point_option(64, 46, 1 | 4 | 8)
    add_height(64, 46, -1.2)
    add_height(66, 46, 1.0)

    # whole 3
    make_whole(32, 39, 4, 3)
    add_height(36, 39, -1.3)
    add_height(35, 39, -1.8)
    add_height(34, 39, -1.3)
    add_height(33, 39, -0.8)
    add_height(35, 38, -0.5)
    add_height(32, 42, 0.5)
    add_height(33, 42, 0.5)
    add_height(35, 42, -0.5)
    add_height(33, 41, 0.3)
    add_height(35, 41, -0.8)
    add_height(35, 40, -0.4)
    add_height(34, 40, -0.4)

    add_height(31, 38, 0.6)
    add_height(32, 38, 1.0)
    add_height(33, 38, 0.6)

    add_height(31, 37, 0.5)
    add_height(32, 37, 0.5)
    add_height(33, 37, 0.5)

    # whole 4
    make_whole(31, 63, 3, 5)
    make_whole(30, 64, 5, 3)
    
    # planed terrain for labs
    m = model.Material.get("ground6")
    j = 88
    while j <= 93:
        i = 70
        while i <= 82:
            land.set_height(i, j, 1.5)
            land.set_texture(i, j, m)
            i += 1
        j += 1

    # planed terrain for houses
    add_height(80, 41, 0.4)
    add_height(79, 41, 0.64)
    add_height(80, 42, 0.4)
    add_height(78, 41, 0.64)
    add_height(79, 40, 0.64)
    add_height(78, 40, 0.64)
    add_height(78, 42, 0.64)
    add_height(79, 42, 0.64)

    add_height(89, 42, 0.2)

    add_height_area (25, 24, 3, 8, 0.5)
    add_height_area (25, 11, 3, 6, 0.2)

    add_height_area (82, 99, 4, 4, 0.2)

    # roads
    import Image

    circuit = Image.open("/home/blam/data/bombay2_ways.png")
    m = model.Material.get("ground6")
    i = 0
    while(i < 129):
        j = 0
        while(j < 129):
            if circuit.getpixel((i, j)) == (255, 0, 0):
                land.set_texture(i, j, m)
                add_height(i, j, -0.5)
            j = j + 1
        i = i + 1

    return land

land = make_land()

def make_metro():

    w = soya3d.World()
    w.shapify_args = ('tree', {})

    # metro light
    light = soya3d.Light(w)
    light.directional = 1
    light.diffuse = (-0.1, -0.1, -0.1, 1.0)
    light._matrix = (-1.0, -0.0, 0.0, 0.0, -0.0, 0.0, -1.0, 0.0, -0.0, -1.0, -0.0, 0.0, 0.0, 5.0, 0.0, 1.0, 1.0, 1.0, 1.0)

    # add tubes
    v = soya3d.World(w)
    s = model.Shape.get('metro_all')
    s.to_faces(v)

    w.filename = "shape-cyberbombay-1"
    w.save()

    return w


def make_houses():
    w = soya3d.World()
    houses = soya3d.World(w)

    w.shapify_args = ('tree', {})

    # houses light
    light = soya3d.Light(w)
    light.directional = 1
    light.static = 1
    light._matrix = (0.63844746351242065, 0.0, 0.76966547966003418, 0.0, 0.33340060710906982, -0.90130943059921265, -0.27656009793281555, 0.0, 0.6937066912651062, 0.43317598104476929, -0.57543867826461792, 0.0, 0.0, 5.0, 0.0, 1.0, 1.0, 1.0, 1.0)

    # add entrances
    v = soya3d.World(w)
    s = model.Shape.get('metro_entrance1')
    s.to_faces(v)
    v.set_xyz(77.25, 5.0, 132.6)
    
    v = soya3d.World(w)
    s = model.Shape.get('metro_entrance1')
    s.to_faces(v)
    v.rotate_lateral(135.0)
    v.set_xyz(99.5, 2.8, 65.5)

    v = soya3d.World(w)
    s = model.Shape.get('metro_entrance1')
    s.to_faces(v)
    v.rotate_lateral(180.0)
    v.set_xyz(50.5, 5.2, 57.75)

    v = soya3d.World(w)
    s = model.Shape.get('metro_entrance2')
    s.to_faces(v)
    v.scale(1.5, 1.5, 1.5)
    v.set_xyz(48.0, 11.2, 97.5)

    # houses
    model.Material.PATH = "/home/blam/prog/slune/materials"
    m1 = model.Material.get('house3')
    m2 = model.Material.get('inde_2')
    m3 = model.Material.get('bark1')
    m4 = model.Material.get('house3b')
    m5 = model.Material.get('inde_4')
    m6 = model.Material.get('inde_1')
    m7 = model.Material.get('inde_3')
    m8 = model.Material.get('thatch1')
    m9 = model.Material.get('taj3')
    m10 = model.Material.get('inde_5')
    m11 = model.Material.get('bloc3')
    m12 = model.Material.get('bloc3win')
    m13 = model.Material.get('ground5')
    m14 = model.Material.get('taj1')

    ms1 = (m1, 'plak round', 0.5, 'complete', 1.0)
    ms2 = (m2, 'plak', 1.0, 'plak', 1.0)
    ms3 = (m3, 'plak', 1.0, 'plak', 1.0)
    ms4 = (m4, 'plak round', 1.0, 'complete', 1.0)
    ms6 = (m6, 'plak round', 1.0, 'complete', 1.0)
    ms7 = (m7, 'plak round', 1.0, 'complete', 1.0)
    ms8 = (m9, 'plak', 1.0, 'complete', 2.0)
    ms9 = (m9, 'plak', 1.0, 'complete', 1.0)
    ms10 = (m10, 'plak round', 1.0, 'complete', 1.0)
    ms11 = (m11, 'plak round', 1.0, 'complete', 1.0)
    ms12 = (m12, 'plak round', 1.0, 'complete', 1.0)
    ms13 = (m4, 'plak round', 1.0, 'complete', 2.0)
    ms14 = (m14, 'plak round', 1.0, 'complete', 2.0)
    ms15 = (m6, 'plak round', 1.0, 'complete', 2.0)

    def make_house(points, style, x = 0.0, z = 0.0, angle = 0.0, add_y = 0.0):
        v = soya3d.World(houses)
        h = town_generator.House(points)
        if style == 1:
            h.section = [(0.0, 0.0), (0.0, 1.0), (0.0, 3.0), (0.2, 3.2), (0.2, 4.2), (0.4, 4.3)]
            h.materials = [ ms2, ms1, ms3, ms4, ms3 ]
            h.roof = ('trapez', m5, m5, 1.5, 2.0, 0.5, 1.0)
        elif style == 2:
            h.section = [(0.2, 0.0), (0.2, 1.0), (0.2, 2.0), (0.0, 2.2), (0.0, 3.2), (0.0, 4.2)]
            h.materials = [ ms2, ms6, ms3, ms7, ms2 ]
            h.roof = ('trapez', m3, m2, 1.5, 0.0, 1.0, 1.5)
        elif style == 3:
            h.section = [(0.0, 0.0), (0.0, 1.0), (0.0, 3.0), (0.3, 3.3), (0.3, 4.3)]
            h.materials = [ ms6, ms2, ms3, ms7 ]
            h.roof = ('pyramid', m5, 2.0, 0.5, 'complete', 3.0)
        elif style == 4:
            h.section = [(0.3, 0.0), (0.3, 1.0), (0.0, 1.2), (0.0, 2.2), (0.0, 3.2), (0.0, 4.2), (0.0, 5.2), (0.3, 5.4), (0.3, 6.4)]
            h.materials = [ ms10, ms2, ms11, ms12, ms11, ms12, ms2, ms10 ]
            h.roof = ('flat', m13)
        elif style == 5:
            h.section = [(0.0, 0.0), (0.0, 1.0), (0.0, 2.0), (0.0, 3.0), (0.3, 3.2), (0.3, 4.2)]
            h.materials = [ ms11, ms12, ms11, ms2, ms10 ]
            h.roof = ('flat', m13)
        elif style == 6:
            h.section = [(0.0, 0.0), (0.0, 1.0), (0.0, 3.0), (0.0, 4.0), (0.0, 6.0), (0.3, 6.2)]
            h.materials = [ ms6, ms13, ms6, ms13, ms3 ]
            h.roof = ('pyramid', m3, 2.5, 0.5, 'complete', 2.0)
        elif style == 7:
            h.section = [(0.0, 0.0), (0.0, 4.0), (0.2, 5.0)]
            h.materials = [ ms14, ms9 ]
            h.roof = ('pyramid', m13, 1.5, 0.5, 'complete', 2.0)
        elif style == 8:
            h.section = [(0.0, 0.0), (0.0, 2.0), (-0.2, 2.2), (-0.2, 4.2), (-0.4, 4.4), (-0.4, 6.4), (-0.6, 6.6), (-0.6, 8.6)]
            h.materials = [ ms15, ms3, ms15, ms3, ms15, ms3, ms15 ]
            h.roof = ('trapez', m5, m2, 1.0, 0.0, 1.0, 2.0)
        h.rotate_points(angle)
        h.translate_points(x, z)
        h.draw(v)
        h.set_on_land(land, v)
        v.y += add_y
        return v

    # add labo
    v = soya3d.World(w)
    s = model.Shape.get('labs1')
    s.to_faces(v)
    v.set_xyz(108.0, 4.24, 135.0)

    ps = [(116.09649658, 132.345474243), (122.88722229, 132.361022949), (122.877716064, 138.14730835), (116.095108032, 138.137893677)]
    h = town_generator.House(ps)
    h.set_on_land(land)
    ps = [(107.111419678, 132.110473633), (112.877716064, 132.110473633), (112.877716064, 134.912887573), (107.104621887, 134.877944946)]
    h = town_generator.House(ps)
    h.set_on_land(land)

    # add temple
    v = soya3d.World(w)
    s = model.Shape.get('pagode_3')
    s.to_faces(v)
    v.rotate_lateral(-90.0)
    v.set_xyz(65.0, 11.2, 98.0)

    ps = [(67.2001876831, 93.2055587769), (75.7270202637, 93.2624893188), (75.7912521362, 105.295455933), (67.1547546387, 105.295455933)]
    h = town_generator.House(ps)
    h.set_on_land(land)

    v = soya3d.World(w)
    s = model.Shape.get('pagode_1')
    s.to_faces(v)
    v.set_xyz(64.0, 12.4, 86.0)

    # rempart
    v = soya3d.World(w)
    s = model.Shape.get('rempart_indus1')
    s.to_faces(v)
    v.rotate_lateral(180.0)
    v.set_xyz(140.0, 1.5, 80.0)
    
    v = soya3d.World(w)
    s = model.Shape.get('rempart_indus4')
    s.to_faces(v)
    v.rotate_lateral(-80.0)
    v.set_xyz(72.0, 0.6, 147.0)

    v = soya3d.World(w)
    s = model.Shape.get('rempart_indus5')
    s.to_faces(v)
    v.set_xyz(50.0, 1.34, 13.0)

    # special house
    v = soya3d.World(w)
    s = model.Shape.get('house_indus1')
    s.to_faces(v)
    v.rotate_lateral(-20.0)
    v.set_xyz(137.0, 1.6, 54.0)
    
    ps = [(132.055343628, 55.507106781), (139.790344238, 58.2436523438), (141.824035645, 52.4744377136), (134.17678833, 49.7211456299)]
    h = town_generator.House(ps)
    h.set_on_land(land)

    v = soya3d.World(w)
    s = model.Shape.get('house_indus2')
    s.to_faces(v)
    v.rotate_lateral(-45.0)
    v.set_xyz(134.0, 3.0, 108.0)

    # generic houses
    make_house(town_generator.make_square(6.0, 10.0), 1, 148.5, 39.0)
    make_house(town_generator.make_square(12.0, 6.0), 2, 136.0, 35.5, 22.0, add_y = -0.2)
    make_house(town_generator.make_square(4.0, 4.0), 4, 126.0, 50.0, 18.0, add_y = -0.2)
    make_house(town_generator.make_square(4.0, 4.0), 4, 119.0, 64.0, 17.0, add_y = -0.1)
    make_house(town_generator.make_square(6.0, 12.0), 1, 109.0, 40.0, add_y = -0.2)
    make_house(town_generator.make_square(12.0, 6.0), 5, 116.0, 20.0)
    make_house(town_generator.make_square(4.0, 4.0), 6, 83.0, 44.5)
    make_house(town_generator.make_square(6.0, 10.0), 6, 133.0, 67.2, add_y = -0.15)
    make_house([(-2.0, 5.0), (2.0, 5.0), (5.0, 2.0), (5.0, -2.0), (2.0, -5.0), (-2.0, -5.0), (-5.0, -2.0), (-5.0, 2.0)], 3, 98.0, 158.0, add_y = -0.1)
    make_house(town_generator.make_square(6.0, 6.0), 3, 128.0, 85.0, add_y = -0.1)
    make_house(town_generator.make_square(6.0, 12.0), 2, 168.0, 70.0, add_y = -0.0)
    make_house(town_generator.make_square(10.0, 8.0), 2, 87.0, 33.0, add_y = -0.0)
    make_house(town_generator.make_square(20.0, 4.0), 7, 82.0, 18.0, add_y = -0.0)
    make_house(town_generator.make_square(4.0, 8.0), 1, 57.0, 37.0, -30.0, add_y = -0.0)
    make_house(town_generator.make_square(4.0, 4.0), 8, 22.0, 50.0, 45.0, add_y = -0.32)
    make_house(town_generator.make_square(14.0, 6.0), 1, 80.0, 174.0, -10.0, add_y = -0.0)
    make_house([(-4.0, 3.0), (4.0, 3.0), (6.0, 0.0), (4.0, -3.0), (-4.0, -3.0), (-6.0, 0.0)], 7, 138.0, 21.0, -40.0, add_y = -0.0)
    make_house(town_generator.make_square(12.0, 10.0), 4, 130.0, 154.0, 0.0, add_y = 0.25)
    make_house(town_generator.make_square(4.0, 4.0), 8, 95.0, 143.0, 45.0, add_y = -0.32)
    make_house(town_generator.make_square(6.0, 14.0), 6, 149.0, 105.0, add_y = -0.0)
    make_house(town_generator.make_square(12.0, 6.0), 2, 141.0, 122.0, add_y = -0.0)
    make_house(town_generator.make_square(8.0, 10.0), 7, 156.0, 128.0, add_y = -0.33)
    make_house(town_generator.make_square(6.0, 12.0), 1, 135.0, 137.0, add_y = -0.0)
    make_house(town_generator.make_square(10.0, 5.0), 2, 150.0, 142.0, add_y = -0.0)
    make_house(town_generator.make_square(4.0, 4.0), 8, 18.0, 122.0, add_y = -0.0)


    # palmtrees
    v = soya3d.World(w)
    s = model.Shape.get('palmtree1')
    s.to_faces(v)
    v.scale(0.4, 0.4, 0.4)
    v.set_xyz(40.0, 0.8, 146.0)

    v = soya3d.World(w)
    s.to_faces(v)
    v.scale(0.3, 0.3, 0.3)
    v.rotate_vertical(30.0)
    v.rotate_lateral(-45.0)
    v.set_xyz(39.5, 0.7, 146.5)

    v = soya3d.World(w)
    s.to_faces(v)
    v.scale(0.4, 0.4, 0.4)
    v.rotate_lateral(90.0)
    v.set_xyz(34.0, 12.3, 85.0)

    v = soya3d.World(w)
    s.to_faces(v)
    v.scale(0.4, 0.4, 0.4)
    v.rotate_lateral(100.0)
    v.set_xyz(167.0, 1.65, 39.0)

    v = soya3d.World(w)
    s.to_faces(v)
    v.scale(0.4, 0.4, 0.4)
    v.rotate_lateral(180.0)
    v.set_xyz(171.0, 0.85, 161.0)

    v = soya3d.World(w)
    s.to_faces(v)
    v.scale(0.4, 0.4, 0.4)
    v.rotate_lateral(180.0)
    v.rotate_incline(-20.0)
    v.set_xyz(162.0, 2.25, 166.0)

    def del_vertices_color(obj):
        if isinstance(obj, soya3d.World):
            for o in obj.children:
                del_vertices_color(o)
        elif isinstance(obj, model.Face):
            for v in obj.vertices:
                v.color = None

    del_vertices_color(w)

# hack
#    w.filename = "shape-cyberbombay-2"
#    w.save()
    return w


def make_world():

    w = soya3d.World()
    w.shape = land
    make_houses()

    atm = soya3d.Atmosphere()
    atm.ambient = (0.45, 0.43, 0.4, 1.0)
    atm.bg_color  = (0.6, 0.6, 0.8, 1.0)
    atm.skyplane = 1
    atm.sky_color = (0.8, 0.8, 1.0, 1.0)
    atm.fog_color = atm.bg_color
    atm.fog_type    = 0
    atm.fog_start   = 20.0
    atm.fog_end     = 50.0
    atm.fog         = 1
    atm.fog_density = 0.001
    atm.cloud = model.Material.get("clouds1")
    w.atmosphere = atm

    # houses light
    light = soya3d.Light(w)
    light.directional = 1
    light.static = 1
    light._matrix = (0.63844746351242065, 0.0, 0.76966547966003418, 0.0, 0.33340060710906982, -0.90130943059921265, -0.27656009793281555, 0.0, 0.6937066912651062, 0.43317598104476929, -0.57543867826461792, 0.0, 0.0, 5.0, 0.0, 1.0, 1.0, 1.0, 1.0)

    # add labo smoke
    import soya
    smoke = soya.Smoke(w)
    smoke.nb_max = 20
    smoke.auto_generate_particle = 1
    smoke.set_xyz(121.9, 4.5, 131.5)
    
    v = soya3d.Volume(w)
    v.shape = model.Shape.get('shape-cyberbombay-2')

    land.compute_static_light([light], 1)

    v = soya3d.World(w)
    v.shape = model.Shape.get('shape-cyberbombay-1')
    atm = soya3d.Atmosphere()
    atm.ambient = (0.3, 0.3, 0.3, 1.0)
    atm.bg_color  = (0.0, 0.0, 0.0, 1.0)
    atm.skyplane = 0
    atm.fog_color = atm.bg_color
    atm.fog_type    = 0
    atm.fog_start   = 20.0
    atm.fog_end     = 50.0
    atm.fog         = 1
    atm.fog_density = 0.001
    v.atmosphere = atm

    w.filename = "world-cyberbombay"
    w.save()
    return w



#print 'shape-cyberbombay-1 ...'
#make_metro()
#print '  [ OK ]'
#print 'shape-cyberbombay-2 ...'
#make_houses()
#print '  [ OK ]'
print 'world-cyberbombay ...'
make_world()
print '  [ OK ]'


#soya.editor.edit(w)
#Tkinter.mainloop()


