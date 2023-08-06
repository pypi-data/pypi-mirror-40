#---------------
# town generator
#---------------
# written by Bertrand 'BLam' Lamy (blam@tuxfamily.org)
# use this code to make Slune level faster!!!

import math
import random
import Tkinter
import Image

import soya, soya.editor


def distance(p1, p2):
  x = p1[0] - p2[0]
  y = p1[1] - p2[1]
  z = p1[2] - p2[2]
  return math.sqrt(x * x + y * y + z * z)


def intersect_2D_lines(p1, v1, p2, v2):
  k = ((p2[1] - p1[1]) * v2[0] + (p1[0] - p2[0]) * v2[1]) / (v1[1] * v2[0] - v1[0] * v2[1])
  # t = ((p2[1] - p1[1]) * v1[0] + (p1[0] - p2[0]) * v1[1]) / (v2[0] * v1[1] - v2[1] * v1[0])
  return (k * v1[0] + p1[0], k * v1[1] + p1[1])


def distance_point_line(point, line_point, line_vector):
  perpend = (-line_vector[1], line_vector[0])
  p1 = point
  v1 = perpend
  p2 = line_point
  v2 = line_vector
  return ((p2[1] - p1[1]) * v2[0] + (p1[0] - p2[0]) * v2[1]) / (v1[1] * v2[0] - v1[0] * v2[1])


def side_of_line(point_to_test, line_point, line_vector, point_inside):
  d1 = distance_point_line(point_to_test, line_point, line_vector)
  d2 = distance_point_line(point_inside, line_point, line_vector)
  if (d1 > 0 and d2 > 0) or (d1 < 0 and d2 < 0): return 1
  return 0
  

def point_is_inside(point_to_test, points):
  i = 0
  while i < len(points):
    p1 = points[i - 1]
    p2 = points[i]
    j = i + 1
    if j >= len(points): j = 0
    p3 = points[j]
    v = (p2[0] - p1[0], p2[1] - p1[1])
    if side_of_line(point_to_test, p1, v, p3) == 0: return 0
    i += 1
  return 1



def translate_points(points, x, z):
  ps = []
  for p in points:
    ps.append((p[0] + x, p[1] + z))
  return ps
    
def rotate_points(points, angle):
  a = angle / 180.0 * math.pi
  coss = math.cos(a)
  sinn = math.sin(a)
  ps = []
  for p in points:
    ps.append((p[0] * coss - p[1] * sinn, p[1] * coss + p[0] * sinn))
  return ps

def make_square(w, d):
  x = w * 0.5
  z = d * 0.5
  return [(-x, -z), (-x, z), (x, z), (x, -z)]

def make_octogon(x, z):
  p = [(x, z), (z, x), (-z, x), (-x, z), (-x, -z), (-z, -x), (z, -x), (x, -z)]
  p.reverse()
  return p

class House:

  def __init__(self, points = [], height = 0.0):
    self.points = points
    self.height = height
    # Section drawer
    self.section = None
    self.section_size = -1.0
    self.materials = None
    # list materials: [(material, x fill style, x scale, y fill style, y scale), ...]
    #   fill style: 'complete', 'plak'
    self.roof = None
    #   roof: ('pyramid', material, height, x scale, y fill style, y scale)
    #         ('trapez',  material1, material2, height, border_incline, x fill scale, y fill scale)
    #         ('flat',    material)

  def translate_points(self, x, z):
    points = []
    for p in self.points:
      points.append((p[0] + x, p[1] + z))
    self.points = points

  def scale_points(self, f):
    points = []
    for p in self.points:
      points.append((p[0] * f, p[1] * f))
    self.points = points

  def rotate_points(self, angle):
    a = angle / 180.0 * math.pi
    coss = math.cos(a)
    sinn = math.sin(a)
    points = []
    for p in self.points:
      points.append((p[0] * coss - p[1] * sinn, p[1] * coss + p[0] * sinn))
    self.points = points

  def make_square(self, w, d):
    x = w * 0.5
    z = d * 0.5
    self.points = [(-x, -z), (-x, z), (x, z), (x, -z)]

  def draw_sections(self, world):
    # create main sections
    section_points = []
    w = soya.World(world)
    i = 0
    while i < len(self.points):
      # section is (x, z)
      curr_section = self.points[i]
      if i + 1 >= len(self.points):
        next_section = self.points[0]
      else:
        next_section = self.points[i + 1]
      prev_section = self.points[i - 1]
      prev_vector = (curr_section[0] - prev_section[0], curr_section[1] - prev_section[1])
      curr_vector = (next_section[0] - curr_section[0], next_section[1] - curr_section[1])
      list = []
      for point in self.section:
        # point is (x, y)
        if point[0] == 0.0:
          list.append((curr_section[0], self.height + point[1], curr_section[1]))
        else:
          # compute point for current section
          w.set_identity()
          p = soya.Point(w, point[0], point[1], 0.0)
          w.look_at(soya.Point(world, curr_vector[0], 0.0, curr_vector[1]))
          cp = p % world
          # compute point for previous section
          w.set_identity()
          p = soya.Point(w, point[0], point[1], 0.0)
          w.look_at(soya.Point(world, prev_vector[0], 0.0, prev_vector[1]))
          pp = p % world
          # compute intersection
          p = intersect_2D_lines((cp.x, cp.z), curr_vector, (pp.x, pp.z), prev_vector)
          # translate
          list.append((p[0] + curr_section[0], self.height + point[1], p[1] + curr_section[1]))
      section_points.append(list)
      i += 1
    world.remove(w)

    # create sub sections
    if self.section_size <= 0.0:
      sub_sections = []
      i = 0
      while i < len(self.points):
        sub_section = [section_points[i - 1], section_points[i]]
        sub_sections.append(sub_section)
        i += 1
    else:
      sub_sections = []
      i = 0
      while i < len(self.points):
        sub_section = []
        prev_section = section_points[i - 1]
        curr_section = section_points[i]
        # add previous section
        sub_section.append(prev_section)
        # compute intermediary section
        prev = self.points[i - 1]
        curr = self.points[i]
        vector = (curr[0] - prev[0], curr[1] - prev[1])
        perpend = (-vector[1], vector[0])
        size = math.sqrt(vector[0] * vector[0] + vector[1] * vector[1])
        nb = int(round(size / self.section_size)) - 1
        j = 0
        while j < nb:
          section = []
          f = (j + 1.0) / (nb + 1.0)
          k = 0
          while k < len(self.section):
            p = intersect_2D_lines(
              (prev_section[k][0], prev_section[k][2]),
              vector,
              (prev[0] + vector[0] * f, prev[1] + vector[1] * f),
              perpend)
            section.append((p[0], prev_section[k][1], p[1]))
            k += 1
          sub_section.append(section)
          j += 1
        # add current section          
        sub_section.append(curr_section)
        sub_sections.append(sub_section)
        i += 1

    # create faces
    for sections in sub_sections:
      i = 0
      while i < len(sections) - 1:
        curr_section = sections[i]
        next_section = sections[i + 1]
        j = 0
        while j < len(curr_section) - 1:
          p1 = curr_section[j]
          p2 = next_section[j]
          p3 = next_section[j + 1]
          p4 = curr_section[j + 1]
          if self.materials:
            material_data = self.materials[j]
            if material_data[1] == 'complete':
              u1 = 0.0
              u2 = material_data[2]
              u3 = u2
              u4 = u1
            elif material_data[1][:4] == 'plak':
              v = (p2[0] - p1[0], p2[2] - p1[2])
              d = 1.0 / math.sqrt(v[0] * v[0] + v[1] * v[1])
              vector = (v[0] * d, v[1] * d)
              perpend = (-vector[1], vector[0])
              ref = intersect_2D_lines((p1[0], p1[2]), vector,
                                       (0.0, 0.0), perpend)
              if vector[0] == 0.0:
                u1 = (p1[2] - ref[1]) / vector[1]
                u2 = (p2[2] - ref[1]) / vector[1]
              else:
                u1 = (p1[0] - ref[0]) / vector[0]
                u2 = (p2[0] - ref[0]) / vector[0]
              ref = intersect_2D_lines((p4[0], p4[2]), vector,
                                       (0.0, 0.0), perpend)
              if vector[0] == 0.0:
                u3 = (p3[2] - ref[1]) / vector[1]
                u4 = (p4[2] - ref[1]) / vector[1]
              else:
                u3 = (p3[0] - ref[0]) / vector[0]
                u4 = (p4[0] - ref[0]) / vector[0]
              u1 *= material_data[2]
              u2 *= material_data[2]
              u3 *= material_data[2]
              u4 *= material_data[2]
            if material_data[1] == 'plak round':
              u1 = round(u1)
              u2 = round(u2)
              u3 = round(u3)
              u4 = round(u4)
            if material_data[3] == 'complete':
              v1 = material_data[4]
              v2 = 0.0
            elif material_data[3] == 'plak':
              v1 = -p1[1]
              v2 = -p3[1]
              v1 *= material_data[4]
              v2 *= material_data[4]
            f = soya.Face(
              world,
              [soya.Vertex(world, p1[0], p1[1], p1[2], u1, v1),
               soya.Vertex(world, p2[0], p2[1], p2[2], u2, v1),
               soya.Vertex(world, p3[0], p3[1], p3[2], u3, v2),
               soya.Vertex(world, p4[0], p4[1], p4[2], u4, v2)], material_data[0])
          else:
            f = soya.Face(
              world,
              [soya.Vertex(world, p1[0], p1[1], p1[2]),
               soya.Vertex(world, p2[0], p2[1], p2[2]),
               soya.Vertex(world, p3[0], p3[1], p3[2]),
               soya.Vertex(world, p4[0], p4[1], p4[2])])
          j += 1
        i += 1

    # create roof
    if self.roof:

      if self.roof[0] == 'pyramid':
        x = 0.0
        z = 0.0
        for point in self.points:
          x += point[0]
          z += point[1]
        center = (x / len(self.points), self.section[-1][1] + self.roof[2], z / len(self.points))
        for sections in sub_sections:
          i = 0
          while i < len(sections) - 1:
            p1 = sections[i][-1]
            p2 = sections[i + 1][-1]
            if self.roof[1]:
              if self.roof[4] == 'plak':
                v1 = distance(p1, center)
                v2 = distance(p2, center)
              elif self.roof[4] == 'complete':
                v1 = self.roof[5]
                v2 = self.roof[5]
              v = (p2[0] - p1[0], p2[2] - p1[2])
              d = 1.0 / math.sqrt(v[0] * v[0] + v[1] * v[1])
              vector = (v[0] * d, v[1] * d)
              perpend = (-vector[1], vector[0])
              ref = intersect_2D_lines((sections[0][-1][0], sections[0][-1][2]), vector, (center[0], center[2]), perpend)
              if vector[0] == 0.0:
                u1 = (p1[2] - ref[1]) / vector[1]
                u2 = (p2[2] - ref[1]) / vector[1]
              else:
                u1 = (p1[0] - ref[0]) / vector[0]
                u2 = (p2[0] - ref[0]) / vector[0]
              u1 *= self.roof[3]
              u2 *= self.roof[3]
              f = soya.Face(
                world,
                [soya.Vertex(world, p1[0], p1[1], p1[2], u1, v1),
                 soya.Vertex(world, p2[0], p2[1], p2[2], u2, v2),
                 soya.Vertex(world, center[0], center[1], center[2], 0.0, 0.0)
                 ], self.roof[1])
            else:
              pass
              f = soya.Face(
                world,
                [soya.Vertex(world, p1[0], p1[1], p1[2]),
                 soya.Vertex(world, p2[0], p2[1], p2[2]),
                 soya.Vertex(world, center[0], center[1], center[2])])
            i += 1

      elif self.roof[0] == 'flat':
        # simple implementation: self.points must be convex or given in the good order
        points = []
        for sections in sub_sections:
          points.append(sections[0][-1])
        points.append(sub_sections[0][0][-1])
        i = 0
        while i + 3 <= len(points):
          p1 = points[i]
          p2 = points[i + 1]
          p3 = points[i + 2]
          if i + 4 <= len(points):
            # make a quad
            p4 = points[i + 3]
            f = soya.Face(
              world,
              [soya.Vertex(world, p1[0], p1[1], p1[2], p1[0], p1[2]),
               soya.Vertex(world, p2[0], p2[1], p2[2], p2[0], p2[2]),
               soya.Vertex(world, p3[0], p3[1], p3[2], p3[0], p3[2]),
               soya.Vertex(world, p4[0], p4[1], p4[2], p4[0], p4[2])],
               self.roof[1])
            i += 3
          else:
            # make a triangle
            f = soya.Face(
              world,
              [soya.Vertex(world, p1[0], p1[1], p1[2], p1[0], p1[2]),
               soya.Vertex(world, p2[0], p2[1], p2[2], p2[0], p2[2]),
               soya.Vertex(world, p3[0], p3[1], p3[2], p3[0], p3[2])],
               self.roof[1])
            i += 2
        
      elif self.roof[0] == 'trapez':
        spine_points = []
        base_points  = []
        for sections in sub_sections:
          base_points.append(sections[0][-1])
        if len(base_points) == 4:
          
          d1 = distance(base_points[0], base_points[1])
          d2 = distance(base_points[0], base_points[-1])
          if d2 < d1:
            p = base_points[-1]
            base_points.remove(p)
            base_points.insert(0, p)
          spine_points = (
            ((base_points[0][0] + base_points[1][0]) * 0.5,
             (base_points[0][1] + base_points[1][1]) * 0.5 + self.roof[3],
              (base_points[0][2] + base_points[1][2]) * 0.5),
            ((base_points[2][0] + base_points[3][0]) * 0.5,
             (base_points[2][1] + base_points[3][1]) * 0.5 + self.roof[3],
             (base_points[2][2] + base_points[3][2]) * 0.5)
            )
          ref = spine_points[0]
          # incline border
          v = (spine_points[1][0] - spine_points[0][0],
               spine_points[1][1] - spine_points[0][1],
               spine_points[1][2] - spine_points[0][2])
          d = 1.0 / math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])
          v = (v[0] * d, v[1] * d, v[2] * d)
          f = self.roof[4]
          spine_points = (
            (spine_points[0][0] + f * v[0], spine_points[0][1] + f * v[1], spine_points[0][2] + f * v[2]),
            (spine_points[1][0] - f * v[0], spine_points[1][1] - f * v[1], spine_points[1][2] - f * v[2]))
          # draw 2 triangles
          u = 0.5 * distance(base_points[0], base_points[1]) * self.roof[5]
          v1 = soya.Vertex(world, spine_points[0][0], spine_points[0][1], spine_points[0][2], 0.0, 0.0)
          v2 = soya.Vertex(world, base_points[0][0], base_points[0][1], base_points[0][2],   -u, self.roof[6])
          v3 = soya.Vertex(world, base_points[1][0], base_points[1][1], base_points[1][2],    u, self.roof[6])
          f = soya.Face(world, [v1, v2, v3], self.roof[2])
          v1 = soya.Vertex(world, spine_points[1][0], spine_points[1][1], spine_points[1][2], 0.0, 0.0)
          v2 = soya.Vertex(world, base_points[2][0], base_points[2][1], base_points[2][2],   -u, self.roof[6])
          v3 = soya.Vertex(world, base_points[3][0], base_points[3][1], base_points[3][2],    u, self.roof[6])
          f = soya.Face(world, [v1, v2, v3], self.roof[2])

          # draw 2 quads

          u = distance(spine_points[0], ref) * self.roof[5]
          v1 = soya.Vertex(world, spine_points[0][0], spine_points[0][1], spine_points[0][2], u, 0.0)
          v2 = soya.Vertex(world, base_points[1][0], base_points[1][1], base_points[1][2],  0.0, self.roof[6])
          u = distance(base_points[2], base_points[1]) * self.roof[5]
          v3 = soya.Vertex(world, base_points[2][0], base_points[2][1], base_points[2][2],    u, self.roof[6])
          u = distance(spine_points[1], ref) * self.roof[5]
          v4 = soya.Vertex(world, spine_points[1][0], spine_points[1][1], spine_points[1][2], u, 0.0)
          f = soya.Face(world, [v1, v2, v3, v4], self.roof[1])

          u = distance(spine_points[1], ref) * self.roof[5]
          v1 = soya.Vertex(world, spine_points[1][0], spine_points[1][1], spine_points[1][2], u, 0.0)
          u = distance(base_points[0], base_points[3]) * self.roof[5]
          v2 = soya.Vertex(world, base_points[3][0], base_points[3][1], base_points[3][2],    u, self.roof[6])
          v3 = soya.Vertex(world, base_points[0][0], base_points[0][1], base_points[0][2],  0.0, self.roof[6])
          u = distance(spine_points[0], ref) * self.roof[5]
          v4 = soya.Vertex(world, spine_points[0][0], spine_points[0][1], spine_points[0][2], u, 0.0)
          f = soya.Face(world, [v1, v2, v3, v4], self.roof[1])


  def draw(self, world):
    if self.section:
      self.draw_sections(world)

  def set_on_land (self, land, house_world = None):
    factor = land.scale_factor
    x1 = self.points[0][0]
    z1 = self.points[0][1]
    x2 = x1
    z2 = z1
    for p in self.points:
      if p[0] < x1: x1 = p[0]
      if p[0] > x2: x2 = p[0]
      if p[1] < z1: z1 = p[1]
      if p[1] > z2: z2 = p[1]
    x1 = math.floor(x1 / factor)
    z1 = math.floor(z1 / factor)
    x2 = math.ceil(x2 / factor)
    z2 = math.ceil(z2 / factor)
    j = z1
    min_h = 10000000.0
    while j < z2:
      i = x1
      while i < x2:
        if point_is_inside((i * factor, j * factor), self.points) == 1:
          land.add_point_option(int(i), int(j), 1)
          h = land.get_height(int(i), int(j))
          if h < min_h: min_h = h
        i += 1
      j += 1
    if min_h == 10000000.0:
      min_h = 0.0
# hack
#    if house_world: house_world.y = min_h


    
def make_city(filename_buildings_map, filename_styles_map, styles_dict, land = None, scale = 1.0):

  buildings = soya.World()

  def make_building(points, style = None):
    v = soya.World(buildings)
    h = House(points)
    h.scale_points(scale)

    if style:
      style_func = styles_dict[style]
    else:
      style_func = styles_dict[int(random.random() * len(styles_dict))]
    style_func(h)

    h.draw(v)
    if land: h.set_on_land(land, v)



  # auto make buildings from image
  #   RED  building has only vertical or horizontal walls
  #   BLUE building uses the extreme points in the 2 dimensions of the filled surface

  img = Image.open(filename_buildings_map)
  map = []
  i = 0
  while(i < img.size[0]):
    j = 0
    col = []
    while(j < img.size[1]):
      if img.getpixel((i, j)) == (255, 0, 0):
        col.append(1)
      elif img.getpixel((i, j)) == (0, 0, 255):
        col.append(2)
      else:
        col.append(0)
      j += 1
    map.append(col)
    i += 1

  if filename_styles_map: img_styles = Image.open(filename_styles_map)

  def map_fill(map, x, y):
    if map[x][y] == 1:
      map[x][y] = 0
      map_fill(map, x - 1, y)
      map_fill(map, x + 1, y)
      map_fill(map, x, y - 1)
      map_fill(map, x, y + 1)

  def red_house(map, X, Y):
    global x, y
    global startx, starty
    x = X
    y = Y
    startx = X
    starty = Y
    points = [(float(x), float(y))]
    def search_left():
      global x, y, startx, starty
      while 1:
        if x == startx and y == starty: return
        x -= 1
        if map[x][y] == 0:
          x += 1
          points.append((float(x), float(y)))
          search_up()
          return
        if map[x][y + 1] == 1:
          points.append((float(x), float(y)))
          search_down()
          return
    def search_right():
      global x, y, startx, starty
      while 1:
        if x == startx and y == starty: return
        x += 1
        if map[x][y] == 0:
          x -= 1
          points.append((float(x), float(y)))
          search_down()
          return
        if map[x][y - 1] == 1:
          points.append((float(x), float(y)))
          search_up()
          return
    def search_up():
      global x, y, startx, starty
      while 1:
        if x == startx and y == starty: return
        y -= 1
        if map[x][y] == 0:
          y += 1
          points.append((float(x), float(y)))
          search_right()
          return
        if map[x - 1][y] == 1:
          points.append((float(x), float(y)))
          search_left()
          return
    def search_down():
      global x, y, startx, starty
      while 1:
        if x == startx and y == starty: return
        y += 1
        if map[x][y] == 0:
          y -= 1
          points.append((float(x), float(y)))
          search_left()
          return
        if map[x + 1][y] == 1:
          points.append((float(x), float(y)))
          search_right()
          return
    x += 1
    search_right()
    points.reverse()
    map_fill(map, X, Y)
    return points
            
  def blue_house(map, X, Y):
    points = [(X, Y), (X, Y), (X, Y), (X, Y)]
    def search_extremes(map, x, y, list):
      if map[x][y] == 2:
        minx = list[0][0]
        miny = list[1][1]
        maxx = list[2][0]
        maxy = list[3][1]
        if x == minx:
          if len(list[0]) == 3:
            y1 = list[0][1]
            y2 = list[0][2]
            if y < y1: list[0] = (minx, y, y2)
            if y > y2: list[0] = (minx, y1, y)
          else:
            y0 = list[0][1]
            if y < y0: list[0] = (minx, y, y0)
            if y > y0: list[0] = (minx, y0, y)
        if y == miny:
          if len(list[1]) == 3:
            x1 = list[1][0]
            x2 = list[1][2]
            if x < x1: list[1] = (x, miny, x2)
            if x > x2: list[1] = (x1, miny, x)
          else:
            x0 = list[1][0]
            if x < x0: list[1] = (x, miny, x0)
            if x > x0: list[1] = (x0, miny, x)
        if x == maxx:
          if len(list[2]) == 3:
            y1 = list[2][1]
            y2 = list[2][2]
            if y < y1: list[2] = (maxx, y, y2)
            if y > y2: list[2] = (maxx, y1, y)
          else:
            y0 = list[2][1]
            if y < y0: list[2] = (maxx, y, y0)
            if y > y0: list[2] = (maxx, y0, y)
        if y == maxy:
          if len(list[3]) == 3:
            x1 = list[3][0]
            x2 = list[3][2]
            if x < x1: list[3] = (x, maxy, x2)
            if x > x2: list[3] = (x1, maxy, x)
          else:
            x0 = list[3][0]
            if x < x0: list[3] = (x, maxy, x0)
            if x > x0: list[3] = (x0, maxy, x)
        if x < list[0][0]: list[0] = (x, y)
        if x > list[2][0]: list[2] = (x, y)
        if y < list[1][1]: list[1] = (x, y)
        if y > list[3][1]: list[3] = (x, y)
        map[x][y] = 0
        search_extremes(map, x - 1, y, list)
        search_extremes(map, x + 1, y, list)
        search_extremes(map, x, y - 1, list)
        search_extremes(map, x, y + 1, list)
        
    search_extremes(map, X, Y, points)

    pts = []
    p = points[0]
    if len(p) == 3:
      pts.append((float(p[0]), float(p[2])))
    pts.append((float(p[0]), float(p[1])))
    p = points[1]
    pts.append((float(p[0]), float(p[1])))
    if len(p) == 3:
      pts.append((float(p[2]), float(p[1])))
    p = points[2]
    pts.append((float(p[0]), float(p[1])))
    if len(p) == 3:
      pts.append((float(p[0]), float(p[2])))
    p = points[3]
    if len(p) == 3:
      pts.append((float(p[2]), float(p[1])))
    pts.append((float(p[0]), float(p[1])))

    points = []
    for p in pts:
      if len(points) == 0 or p != points[-1]:
        points.append(p)
    if points[0] == points[-1]: points.remove(points[-1])
            
    points.reverse()
    return points
        

  j = 0
  while(j < img.size[1]):
    i = 0
    while(i < img.size[0]):
      points = None
      if map[i][j] == 1:
        points = red_house(map, i, j)
      elif map[i][j] == 2:
        points = blue_house(map, i, j)
      if points:
        if filename_styles_map:
          styl = img_styles.getpixel((i, j))
        else:
          styl = None
        make_building(points, styl)
      i = i + 1
    j = j + 1
        

  return buildings





# HACK
soya.Material.PATH = "/home/blam/prog/slune/materials"


scene = soya.World()


m1 = soya.Material.get('house3')
m2 = soya.Material.get('inde_2')
m3 = soya.Material.get('bark1')
m4 = soya.Material.get('house3b')
m5 = soya.Material.get('inde_4')
m6 = soya.Material.get('inde_1')
m7 = soya.Material.get('inde_3')
m9 = soya.Material.get('taj3')

ms1 = (m1, 'plak round', 0.5, 'complete', 1.0)
ms2 = (m2, 'plak', 1.0, 'plak', 1.0)
ms3 = (m3, 'plak', 1.0, 'plak', 1.0)
ms4 = (m4, 'plak round', 1.0, 'complete', 1.0)
ms6 = (m6, 'plak round', 1.0, 'complete', 1.0)
ms7 = (m7, 'plak round', 1.0, 'complete', 1.0)
ms8 = (m9, 'plak', 1.0, 'complete', 2.0)
ms9 = (m9, 'plak', 1.0, 'complete', 1.0)



def set_style_1 (house):
  house.section = [(0.0, 0.0), (0.0, 1.0), (0.0, 3.0), (0.2, 3.2), (0.2, 4.2), (0.4, 4.3)]
  house.materials = [ ms2, ms1, ms3, ms4, ms3 ]
  house.roof = ('trapez',  m5, m5, 1.5, 2.0, 0.5, 1.0)
  
def set_style_2 (house):
  house.section = [(0.2, 0.0), (0.2, 1.0), (0.2, 2.0), (0.0, 2.2), (0.0, 3.2), (0.0, 4.2)]
  house.materials = [ ms2, ms6, ms3, ms7, ms2 ]
  house.roof = ('trapez',  m3, m2, 1.5, 0.0, 1.0, 1.5)

def set_style_round (house):
  house.section = [(0.0, 0.0), (0.0, 1.0), (0.0, 3.0), (0.3, 3.3), (0.3, 4.3)]
  house.materials = [ ms6, ms2, ms3, ms7 ]
  house.roof = ('pyramid',  m5, 2.0, 0.5, 'complete', 3.0)


#house = House([(-4.0, -2.0), (-4.0, 2.0), (4.0, 2.0), (4.0, -2.0)])
#house = House([(2.0, 2.0), (2.0, -3.0), (0.0, -3.0), (0.0, 0.0), (-4.0, 0.0), (-4.0, 2.0)])
#house.section_size = -1.0

#house.roof = ('pyramid', soya.Material.get('inde_4'), 2.0, 'complete', 2.0)
#house.roof = ('flat', soya.Material.get('ground1'))
#house.roof = ('trapez',  m5, m5, 1.5, 2.0, 0.5, 1.0)

#set_style_2(house)




# octogon house
#house = House([(-2.0, 5.0), (2.0, 5.0), (5.0, 2.0), (5.0, -2.0), (2.0, -5.0), (-2.0, -5.0), (-5.0, -2.0), (-5.0, 2.0)])

# square house + triangle side
#house = House([(-4.0, -3.0), (-4.0, -2.0), (-5.5, 0.0), (-4.0, 2.0), (-4.0, 3.0), (4.0, 3.0), (4.0, 2.0), (5.5, 0.0), (4.0, -2.0), (4.0, -3.0)])
#house.section = [(0.2, 0.0), (0.2, 2.0), (0.0, 2.2), (0.0, 3.2)]
#house.materials = [ ms8, ms3, ms9 ]
#house.roof = ('pyramid',  m5, 2.0, 'complete', 2.0)
#house.draw(scene)

#scene.filename = "cyberbombay-shape"
#scene.save()

#soya.editor.edit(scene)
#Tkinter.mainloop()

