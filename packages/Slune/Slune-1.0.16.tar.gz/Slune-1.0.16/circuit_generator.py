#------------------
# circuit generator
#------------------
# written by Bertrand 'BLam' Lamy (blam@tuxfamily.org)
# use this code to make Slune level faster!!!

import math
import Tkinter

import soya
import soya.editor


def is_null(v):
  return abs(v) < 0.01

def normalize(a, b, c, size = 1.0):
  s = size / math.sqrt(a * a + b * b + c * c)
  return (a * s, b * s, c * s)

def cross(v1, v2):
  return (  v1[1] * v2[2] - v1[2] * v2[1],
          - v1[0] * v2[2] + v1[2] * v2[0],
            v1[0] * v2[1] - v1[1] * v2[0])

def express(u, v, w):
  # u = kv + tw
  # return (k, t)
  d = v[0] * w[1] - v[1] * w[0]
  if(is_null(d)):
    d = v[0] * w[2] - v[2] * w[0]
    if(is_null(d)):
      d = v[2] * w[1] - v[1] * w[2]
      k = (u[2] * w[1] - u[1] * w[2]) / d
      t = (u[1] * v[2] - u[2] * v[1]) / d
    else:
      k = (u[0] * w[2] - u[2] * w[0]) / d
      t = (u[2] * v[0] - u[0] * v[2]) / d
  else:
    k = (u[0] * w[1] - u[1] * w[0]) / d
    t = (u[1] * v[0] - u[0] * v[1]) / d
  return (k, t)

class Quaternion:
  def __init__(self, x = 0.0, y = 0.0, z = 0.0, w = 0.0):
    self.x = x
    self.y = y
    self.z = z
    self.w = w
  def set_length(self, length):
    l = length / math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z + self.w * self.w)
    self.x *= l
    self.y *= l
    self.z *= l
    self.w *= l
  def normalize(self):
    self.set_length(1.0)
  def slerp(self, q2, alpha):
    costheta = self.x * q2.x + self.y * q2.y + self.z * q2.z + self.w * q2.w
    if(costheta < 0.0):
      qa = (-self.x, -self.y, -self.z, -self.w)
      costheta = - costheta
    else:
      qa = (self.x, self.y, self.z, self.w)
    if(1.0 - costheta > 0.01):
      theta = math.acos(costheta)
      sintheta = math.sin(theta)
      scale1 = math.sin(theta * (1.0 - alpha)) / sintheta
      scale2 = math.sin(theta * alpha)         / sintheta
    else:
      scale1 = 1.0 - alpha
      scale2 = alpha
    q = Quaternion(scale1 * qa[0] + scale2 * q2.x,
                   scale1 * qa[1] + scale2 * q2.y,
                   scale1 * qa[2] + scale2 * q2.z,
                   scale1 * qa[3] + scale2 * q2.w)
    q.normalize()
    return q
  def to_matrix(self):
    q = Quaternion(self.x, self.y, self.z, self.w)
    q.normalize()
    xx = q.x * q.x
    yy = q.y * q.y
    zz = q.z * q.z
    xy = q.x * q.y
    xz = q.x * q.z
    yz = q.y * q.z
    wx = q.x * q.w
    wy = q.y * q.w
    wz = q.z * q.w
    return (1.0 - 2.0 * (yy + zz),       2.0 * (xy + wz),       2.0 * (xz - wy), 0.0,
                  2.0 * (xy - wz), 1.0 - 2.0 * (xx + zz),       2.0 * (yz + wx), 0.0,
                  2.0 * (xz + wy),       2.0 * (yz - wx), 1.0 - 2.0 * (xx + yy), 0.0,
            0.0, 0.0, 0.0, 1.0,
            1.0, 1.0, 1.0)
  def from_matrix(self, m):
    s = math.sqrt(abs(m[0] / m[16] + m[5] / m[17] + m[10] / m[18] + m[15]))
    self.x = - m[9] / m[18] + m[6] / m[17]
    self.y = - m[2] / m[16] + m[8] / m[18]
    self.z = - m[4] / m[17] + m[1] / m[16]
    self.w = s * 0.5
    if(s == 0.0):
      x = abs(self.x)
      y = abs(self.y)
      z = abs(self.z)
      w = abs(self.w)
      if(x >= y and x >= z and x >= w):
        self.x = 1.0
        self.y = 0.0
        self.z = 0.0
      else:
        if(y >= x and y >= z and y >= w):
          self.x = 0.0
          self.y = 1.0
          self.z = 0.0
        else:
          if(z >= x and z >= y and z >= w):
            self.x = 0.0
            self.y = 0.0
            self.z = 1.0
          else:
            print '*** arg'
    else:
      s = 0.5 / s
      self.x *= s
      self.y *= s
      self.z *= s
    self.normalize()
  def from_vector_and_angle(self, vector, angle):
    v = soya.Vector(vector.x, vector.y, vector.z)
    v.normalize()
    a = 0.5 * (angle * math.pi / 180.0)
    s = math.sin(a)
    self.x = v.x * s
    self.y = v.y * s
    self.z = v.z * s
    self.w = - math.cos(a)

    
def check_quad(quad):
  # compute normals of 2 triangles
  def triangle_normal(p1, p2, p3):
    v1 = soya.Vector()
    v1.set_start_end(p2, p1)
    v2 = soya.Vector()
    v2.set_start_end(p3, p1)
    return v1.cross_product(v2)
  v1 = triangle_normal(quad.vertices[0], quad.vertices[1], quad.vertices[2])
  v2 = triangle_normal(quad.vertices[1], quad.vertices[2], quad.vertices[3])
  EPSILON = 0.001
  if(abs(v1.x - v2.x) > EPSILON or abs(v1.y - v2.y) > EPSILON or abs(v1.z - v2.z) > EPSILON):
    w = quad.parent
    f = soya.Face(w, [quad.vertices[0], quad.vertices[1], quad.vertices[2]], quad.material)
    f.smooth_lit = quad.smooth_lit
    f = soya.Face(w, [quad.vertices[2], quad.vertices[3], quad.vertices[0]], quad.material)
    f.smooth_lit = quad.smooth_lit
    w.remove(quad)


class Circuit:
  def __init__(self):
    #--------------------
    # CIRCUIT GENERATOR
    #
    # circuit attribute:
    # - self           : list of tuples vectors (x, y, z[, incline]) that defines the circuit
    # - self.section   : list of 2D points (x, y) that represent a section of the circuit
    # - self.materials : list of materials to use associated with each couple of points
    #--------------------
    self.current_direction = (0.0, 0.0, 1.0)
    self.section = []
    self.matrices = []
    self.materials = []
    self.world = soya.World()
    self.matrix = self.world._matrix
    self.step = 1.0
    self.length = 50
    
  def to_faces(self, world):

    w = soya.World(world)
    points = []
    for p in self.section:
      points.append(soya.Point(w, p[0], p[1], 0.0))

    #>> compute new sections and create faces
    w._matrix = self.matrices[0]
    distance = 0.0
    for matrix in self.matrices[1:]:
      #>> compute distance between old and new matrix
      x = matrix[12] - w._matrix[12]
      y = matrix[13] - w._matrix[13]
      z = matrix[14] - w._matrix[14]
      d = math.sqrt(x * x + y * y + z * z)
      #>> compute old_points
      old_points = []
      for point in points:
        old_points.append(point % world)
      #>> compute new_points
      w._matrix = matrix
      new_points = []
      for point in points:
        new_points.append(point % world)
      #>> create faces
      i = 0
      distance2 = 0
      while(i < len(points) - 1):
        pt1 = old_points[i]
        pt2 = new_points[i]
        i += 1
        pt3 = new_points[i]
        pt4 = old_points[i]
        x = pt2.x - pt1.x
        y = pt2.y - pt1.y
        z = pt2.z - pt1.z
        d2 = math.sqrt(x * x + y * y + z * z)
        try:
          material = self.materials[i - 1]
          # (material, mode)
          if(material[1] == 0):
            # mode 0: use distance and allways all the texture height
            tex_x1 = distance
            tex_x2 = distance + d
            tex_y1 = 0.0
            tex_y2 = 1.0
          elif(material[1] == 1):
            # mode 1: use distance for x and y
            tex_x1 = distance
            tex_x2 = distance + d
            tex_y1 = distance2
            tex_y2 = distance2 + d2
          p1 = soya.Vertex(world, pt1.x, pt1.y, pt1.z, tex_x1, tex_y1)
          p2 = soya.Vertex(world, pt2.x, pt2.y, pt2.z, tex_x2, tex_y1)
          p3 = soya.Vertex(world, pt3.x, pt3.y, pt3.z, tex_x2, tex_y2)
          p4 = soya.Vertex(world, pt4.x, pt4.y, pt4.z, tex_x1, tex_y2)
          face = soya.Face(world, [p1, p2, p3, p4], material[0])
        except:
          p1 = soya.Vertex(world, pt1.x, pt1.y, pt1.z)
          p2 = soya.Vertex(world, pt2.x, pt2.y, pt2.z)
          p3 = soya.Vertex(world, pt3.x, pt3.y, pt3.z)
          p4 = soya.Vertex(world, pt4.x, pt4.y, pt4.z)
          face = soya.Face(world, [p1, p2, p3, p4], None)
        face.smooth_lit = 1
        distance2 += d2
        #>> cut quad if it is not plane
        check_quad(face)
        
      distance += d
      
    world.remove(w)

  def scale_section(self, scale_x, scale_y):
    old_section = self.section
    self.section = []
    for point in old_section:
      self.section.append((point[0] * scale_x, point[1] * scale_y))

  def add_section(self, nb_transition = 0):
    i = 0
    q1 = Quaternion()
    q2 = Quaternion()
    q1.from_matrix(self.matrix)
    q2.from_matrix(self.world._matrix)
    while(i < nb_transition):
      f = float(i) / nb_transition
      q = q1.slerp(q2, f)
      matrix = q.to_matrix()
      sx = (1.0 - f) * self.matrix[16] + f * self.world._matrix[16]
      sy = (1.0 - f) * self.matrix[17] + f * self.world._matrix[17]
      sz = (1.0 - f) * self.matrix[18] + f * self.world._matrix[18]
      m = (matrix[ 0] * sx, matrix[ 1] * sx, matrix[ 2] * sx, matrix[ 3],
           matrix[ 4] * sy, matrix[ 5] * sy, matrix[ 6] * sy, matrix[ 7],
           matrix[ 8] * sz, matrix[ 9] * sz, matrix[10] * sz, matrix[11],
           (1.0 - f) * self.matrix[12] + f * self.world._matrix[12], 
           (1.0 - f) * self.matrix[13] + f * self.world._matrix[13],
           (1.0 - f) * self.matrix[14] + f * self.world._matrix[14],
           1.0,
           sx, sy, sz)
      self.matrices.append(m)
      i += 1
    self.matrices.append(self.world._matrix)
    self.matrix = self.world._matrix

  def apply_transform(self, transform, time):
    if(transform[0] == 'step'):
      # ('step', time_start, new_step)
      if(time >= transform[1]):
        self.step = transform[2]
        return 0
      else:
        return 1
    elif(transform[0] == 'advance'):
      # ('advance', time_start, length)
      if((time - transform[1]) * self.step >= transform[2]):
        return 0
      else:
        return 1
    elif(transform[0] == 'turn lateral'):
      # ('turn lateral', time_start, radius, angle)
      angle_deg = math.asin(self.step * 0.5 / transform[2]) * 2.0 * 180.0 / math.pi
      if(angle_deg * (time - transform[1] + 1) >= abs(transform[3])):
        angle_deg = abs(transform[3]) - angle_deg * (time - transform[1])
        if(transform[3] < 0.0): angle_deg = -angle_deg
        self.world.turn_lateral(angle_deg)
        return 0
      else:
        if(transform[3] < 0.0): angle_deg = -angle_deg
        self.world.turn_lateral(angle_deg)
        return 1
    elif(transform[0] == 'rotate lateral'):
      # ('rotate lateral', time_start, radius, angle)
      d = self.step * 0.5 / transform[2]
      if(d > 1.0):
        angle_deg = abs(transform[3])
      else:
        angle_deg = math.asin(d) * 2.0 * 180.0 / math.pi
      if(angle_deg * (time - transform[1] + 1) >= abs(transform[3])):
        angle_deg = abs(transform[3]) - angle_deg * (time - transform[1])
        if(transform[3] < 0.0): angle_deg = -angle_deg
        self.world.rotate_lateral(angle_deg)
        return 0
      else:
        if(transform[3] < 0.0): angle_deg = -angle_deg
        self.world.rotate_lateral(angle_deg)
        return 1
    elif(transform[0] == 'turn vertical'):
      # ('turn vertical', time_start, radius, angle)
      d = self.step * 0.5 / transform[2]
      if(d > 1.0):
        angle_deg = abs(transform[3])
      else:
        angle_deg = math.asin(d) * 2.0 * 180.0 / math.pi
      if(angle_deg * (time - transform[1] + 1) >= abs(transform[3])):
        angle_deg = abs(transform[3]) - angle_deg * (time - transform[1])
        if(transform[3] < 0.0): angle_deg = -angle_deg
        self.world.turn_vertical(angle_deg)
        return 0
      else:
        if(transform[3] < 0.0): angle_deg = -angle_deg
        self.world.turn_vertical(angle_deg)
        return 1
    elif(transform[0] == 'rotate vertical'):
      # ('rotate vertical', time_start, radius, angle)
      d = self.step * 0.5 / transform[2]
      if(d > 1.0):
        angle_deg = abs(transform[3])
      else:
        angle_deg = math.asin(d) * 2.0 * 180.0 / math.pi
      if(angle_deg * (time - transform[1] + 1) >= abs(transform[3])):
        angle_deg = abs(transform[3]) - angle_deg * (time - transform[1])
        if(transform[3] < 0.0): angle_deg = -angle_deg
        self.world.rotate_vertical(angle_deg)
        return 0
      else:
        if(transform[3] < 0.0): angle_deg = -angle_deg
        self.world.rotate_vertical(angle_deg)
        return 1
    elif(transform[0] == 'turn incline'):
      # ('turn incline', time_start, length, angle)
      angle = float(transform[3]) / transform[2] * self.step
      if((time - transform[1]) * self.step >= transform[2]):
        a = float(transform[3]) - angle * (time - transform[1])
        self.world.turn_incline(a)
        return 0
      else:
        self.world.turn_incline(angle)
        return 1
    elif(transform[0] == 'scale'):
      # ('scale', time_start, length, scale_x, scale_y, scale_z)
      # TO DO
      pass
    elif(transform[0] == 'stabilize'):
      # ('stabilize', time_start, length, lateral, vertical, incline, scale_x, scale_y, scale_z)
      v = soya.Volume()
      v.turn_lateral (transform[3])
      v.turn_vertical(transform[4])
      v.turn_incline (transform[5])
      v.scale(transform[6], transform[7], transform[8])
      if((time - transform[1]) * self.step >= transform[2]):
        self.world._matrix = (v._matrix[ 0], v._matrix[ 1], v._matrix[ 2], v._matrix[ 3],
                              v._matrix[ 4], v._matrix[ 5], v._matrix[ 6], v._matrix[ 7],
                              v._matrix[ 8], v._matrix[ 9], v._matrix[10], v._matrix[11],
                              self.world._matrix[12], self.world._matrix[13], self.world._matrix[14], 1.0,
                              v._matrix[16], v._matrix[17], v._matrix[18])
        return 0
      else:
        q1 = Quaternion()
        q2 = Quaternion()
        q1.from_matrix(self.world._matrix)
        q2.from_matrix(v._matrix)
        f = 1.0 / (transform[2] / self.step - time)
        q = q1.slerp(q2, f)
        matrix = q.to_matrix()
        sx = (1.0 - f) * self.world._matrix[16] + f * v._matrix[16]
        sy = (1.0 - f) * self.world._matrix[17] + f * v._matrix[17]
        sz = (1.0 - f) * self.world._matrix[18] + f * v._matrix[18]
        sx = 1.0
        sy = 1.0
        sz = 1.0
        self.world._matrix = (matrix[ 0] * sx, matrix[ 1] * sx, matrix[ 2] * sx, matrix[ 3],
                              matrix[ 4] * sy, matrix[ 5] * sy, matrix[ 6] * sy, matrix[ 7],
                              matrix[ 8] * sz, matrix[ 9] * sz, matrix[10] * sz, matrix[11],
                              self.world._matrix[12], self.world._matrix[13], self.world._matrix[14], 1.0,
                              sx, sy, sz)
        return 1
    else:
      print 'WARNING : discarding unknwon transformation', tranform[0]
      return 0

  def apply_transforms(self, transforms, time_start = 0):
    i = time_start
    while(len(transforms) > 0):
      current_transforms = []
      synchronize = 0
      to_remove = []
      for transform in transforms:
        if(transform[0] == 'synchronize'):
          synchronize = 1
          to_remove.append(transform)
          break
        elif(transform[0] == 'start'):
          # ('start', lateral, vertical, incline, scale_x, scale_y, scale_z)
          self.world.turn_lateral (transform[1])
          self.world.turn_vertical(transform[2])
          self.world.turn_incline (transform[3])
          self.world.scale(transform[4], transform[5], transform[6])
          self.matrices.append(self.world._matrix)
          to_remove.append(transform)
        elif(transform[0] == 'end'):
          return
        else:
          if(transform[1] <= i):
            current_transforms.append(transform)
          else:
            break
      for transform in to_remove:
        transforms.remove(transform)
      if(synchronize == 1):
        for transform in current_transforms:
          transforms.remove(transform)
        self.apply_transforms(current_transforms, i)
        i = 0
      else:
        for transform in current_transforms:
          if(self.apply_transform(transform, i) == 0):
            transforms.remove(transform)
        self.world.advance(0.0, 0.0, self.step)
        self.matrices.append(self.world._matrix)
        i += 1

  def to_matrices(self):
    self.apply_transforms(self.transforms)

  def generate(self, world):
    self.to_matrices()
    self.to_faces(world)




#circuit_vector = (0.0, 0.2, 1.0)
#circuit_vectors = []

#circuit_vector = add_straight_road(circuit_vectors, circuit_vector, 2.0, 5)
#circuit_vector = add_turn_road(circuit_vectors, circuit_vector, 90.0, 4.0, 5)

c = Circuit()
#c.current_direction = (0.0, 0.2, 0.8)
#c.section = [(0.0, 0.0), (-1.0, 0.5), (1.0, 0.5), (0.0, 0.0)]

c.section = [( 0.0, -1.0),
             (-2.4,  0.5),
             (-2.0,  1.0),
             (-1.5,  1.0),
             (-1.1,  0.3),
             (-0.5,  0.0),
             ( 0.5,  0.0),
             ( 1.1,  0.3),
             ( 1.5,  1.0),
             ( 2.0,  1.0),
             ( 2.4,  0.5),
             ( 0.0, -1.0)
             ]

c.scale_section(0.6, 0.6)

#c.go_straight(8.0, 10)
#c.turn(4.0, -90.0, 10, 20.0, 0.2)
#c.go_straight(4.0, 4)
#c.turn(8.0, 90.0, 10, 40.0, 1.0)

c.transforms = [
  ('start', 5.0, 36.0, 0.0, 1.0, 1.0, 1.0),
  ('step', 0, 4.0),
  ('advance', 0, 3.0),
  ('synchronize', ),
  ('turn vertical', 0, 12.0, -35.0),
  ('synchronize', ),
  ('advance', 0, 8.0),
  ('synchronize', ),
  ('step', 0, 3.0),
  ('rotate lateral', 0, 6.0, -(360.0 + 170.0)),
  ('turn incline', 0, 10.0, 30.0),
  ('rotate vertical', 0, 1.0, -10.0),
  ('synchronize', ),
  ('step', 0, 4.0),
  ('stabilize', 0, 16.0, 190.0, 0.0, 0.0, 1.0, 1.0, 1.0),
  ('synchronize', ),
  ('step', 0, 1.0),
  ('rotate vertical', 0, 4.0, -195.0),
  ('synchronize', ),
  ('rotate vertical', 0, 2.5, -165.0),
  ('synchronize', ),
  ('step', 0, 4.0),
  ('rotate vertical', 0, 10.0, -30.0),
  ('synchronize', ),
  ('stabilize', 0, 8, 180.0, 0.0, 0.0, 1.0, 1.0, 1.0),
  ('step', 0, 3.0),
  ('synchronize', ),
  ('rotate vertical', 0, 8.0, 90.0),
  ('synchronize', ),
  ('step', 0, 2.0),
  ('turn lateral', 0, 3.0, 180.0),
  ('synchronize', ),
  ('step', 0, 4.0),
  ('advance', 0, 6.0),
  ('synchronize', ),
  ('step', 0, 2.0),
  ('rotate vertical', 0, 8.0, -90.0),
  ('synchronize', ),
  ('rotate lateral', 0, 6.0, 90.0),
  ('synchronize', ),
  ('turn vertical', 0, 12.0, 10.0),
  ('synchronize', ),
  ('turn vertical', 0, 6.0, -70.0),
  ('synchronize', ),
  ('turn vertical', 0, 5.0, 120.0),
  ('synchronize', ),
  ('turn vertical', 0, 6.0, -60.0),
  ('synchronize', ),
  ('turn vertical', 0, 5.0, -60.0),
  ('synchronize', ),
  ('turn vertical', 0, 4.0, 60.0),
  ('synchronize', ),
  ('turn vertical', 0, 4.0, -60.0),
  ('synchronize', ),
  ('turn vertical', 0, 4.0, 60.0),
  ('synchronize', ),
  ('advance', 0, 4.0),
  ('synchronize', ),
  ('turn incline', 0, 6.0, -50.0),
  ('rotate lateral', 0, 8.0, 80.0),
  ('synchronize', ),
  ('turn incline', 0, 6.0, 50.0),
  ('rotate lateral', 0, 8.0, 80.0),
  ('synchronize', ),
  ('step', 0, 2.0),
  ('turn incline', 0, 36.0, 360.0),
  ('synchronize', ),
  ('step', 0, 3.0),
  ('rotate lateral', 0, 8.0, 110.0),
  ('turn vertical', 0, 8.0, -5.0),
  ('synchronize', ),
  ('step', 0, 4.0),
  ('rotate lateral', 0, 35.0, 5.0),
  ('synchronize', ),
  ('step', 0, 2.0),
  ('rotate vertical', 0, 5.5, -340.0),
  ('synchronize', ),
  ('step', 0, 3.0),
  ('rotate vertical', 0, 14.0, -36.0),
  ]

soya.Material.PATH = "/home/jiba/src/slune/materials"

c.materials = [
  (soya.Material.get("trail1"), 0),
  (soya.Material.get("yellowroad1"), 0),
  (soya.Material.get("yellowroad1"), 0),
  (soya.Material.get("tole1"), 0),
  (soya.Material.get("tole1"), 0),
  (soya.Material.get("tole2"), 0),
  (soya.Material.get("tole1"), 0),
  (soya.Material.get("tole1"), 0),
  (soya.Material.get("yellowroad1"), 0),
  (soya.Material.get("yellowroad1"), 0),
  (soya.Material.get("trail1"), 0),
  ]
#c.world.turn_incline(0.0)
#c.matrices.append(c.world._matrix)
#c.matrix = c.world._matrix

#c.world.translate(4.0, 0.0, 4.0)
#c.world.turn_lateral(90.0)
#c.world.turn_incline(20.0)
#c.add_section(10)

#c.world.translate(4.0, 0.0, -4.0)
#c.world.turn_lateral(90.0)
#c.world.turn_incline(20.0)
#c.add_section(10)

#c.turn(90.0, 4.0, 5)
#c.go_straight(4.0, 2)
#c.vertical_loop(360.0, 4.0, 0.2, 20.0)

#print c

# looping
#i = 0.1
#while(i < 6.28):
#  circuit_vectors.append((0.2, math.sin(i), math.cos(i)))
#  i += 0.5


#circuit_points = [(0.0, -0.25), (-1.0, 0.25), (1.0, 0.25), (0.0, -0.25)]

print 'ok'

scene = soya.World()
c.generate(scene)
#c.to_faces(scene)

#f = soya.Face(scene, [soya.Vertex(scene, -20.0, -0.5, -20.0),
#                            soya.Vertex(scene, -20.0, -0.5,  20.0),
#                            soya.Vertex(scene,  20.0, -0.5,  20.0),
#                            soya.Vertex(scene,  20.0, -0.5, -20.0)
#                            ])

scene.scale(4.0, 4.0, 4.0)

scene.filename = "freestylepark-shape"
scene.save()

soya.editor.edit(scene)
Tkinter.mainloop()

