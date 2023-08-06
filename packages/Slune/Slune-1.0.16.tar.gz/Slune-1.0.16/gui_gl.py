# Slune
# Copyright (C) 2002-2003 Bertrand LAMY, Jean-Baptiste LAMY
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

import sys, os, os.path, random, math

import soya, soya.opengl as soyaopengl, soya.sdlconst as soyasdlconst
import soya.widget   as widget

import slune.globdef as globdef

current_menu = None
old_menus = []

def MainScreen():

  #------------------------------#
  # internal classes for widgets #
  #------------------------------#

  def draw_window(width, height, color = (0.5, 0.5, 0.5, 0.75), border_size = 20):
    x = int(0.5 * (soya.get_screen_width()  - width))
    y = int(0.5 * (soya.get_screen_height() - height))
    w = x + width
    h = y + height
    bx = x - border_size
    by = y - border_size
    bw = w + border_size
    bh = h + border_size
    soyaopengl.glBegin(soyaopengl.GL_QUADS)
    soyaopengl.glColor4f(*color)
    soyaopengl.glVertex2i(x, y)
    soyaopengl.glVertex2i(x, h)
    soyaopengl.glVertex2i(w, h)
    soyaopengl.glVertex2i(w, y)
    soyaopengl.glVertex2i(x, y)
    soyaopengl.glVertex2i(w, y)
    soyaopengl.glColor4f(color[0], color[1], color[2], 0.0)
    soyaopengl.glVertex2i(bw, by)
    soyaopengl.glVertex2i(bx, by)
    soyaopengl.glVertex2i(bx, by)
    soyaopengl.glVertex2i(bx, bh)
    soyaopengl.glColor4f(*color)
    soyaopengl.glVertex2i(x, h)
    soyaopengl.glVertex2i(x, y)
    soyaopengl.glVertex2i(w, h)
    soyaopengl.glVertex2i(x, h)
    soyaopengl.glColor4f(color[0], color[1], color[2], 0.0)
    soyaopengl.glVertex2i(bx, bh)
    soyaopengl.glVertex2i(bw, bh)
    soyaopengl.glVertex2i(bw, bh)
    soyaopengl.glVertex2i(bw, by)
    soyaopengl.glColor4f(*color)
    soyaopengl.glVertex2i(w, y)
    soyaopengl.glVertex2i(w, h)
    soyaopengl.glEnd()

  class MsgWindow(widget.Widget):
    def __init__(self, master = None, title = '', text = '', color = (1.0, 1.0, 1.0, 0.8), font = widget.default_font, bg_color = (0.5, 0.5, 0.5, 0.75)):
      widget.Widget.__init__(self, master)
      self.title = title
      self.text = text
      self.color = color
      self.highlight = (1.0, 1.0, 0.0, 1.0)
      self.font = font
      self.bg_color = bg_color
      self.top = int(soya.get_screen_height() * 0.5)
      self.valid = 0
    def process_event(self, event):
      if (event[0] == soyasdlconst.JOYBUTTONDOWN) or (event[0] == soyasdlconst.MOUSEBUTTONDOWN) or (event[0] == soyasdlconst.KEYDOWN and event[1]):
        if self.master: self.master.children.remove(self)
        go_back()
    def resize(self, p_x, p_y, p_w, p_h):
      self.valid = 0
      self.width = int(soya.get_screen_width() * 0.75)
    def render(self):
      self.left = int((soya.get_screen_width() - self.width) * 0.5)
      if self.valid == 0:
        # HACK
        self.height = self.font.wordwrap(self.title, self.width)[1] + self.font.wordwrap(self.text, self.width)[1]
        soyaopengl.glColor4f(0.0, 0.0, 0.0, 0.0)
        self.font.draw_area(self.title, self.left, 0.0, 0.0, self.width, soya.get_screen_height(), 1)
        self.font.draw_area(self.text , self.left, 0.0, 0.0, self.width, soya.get_screen_height(), 0)
        self.top = int((soya.get_screen_height() - self.height) * 0.5)
        self.valid = 1
      soyaopengl.glEnable(soyaopengl.GL_BLEND)
      soyaopengl.glColor4f(0.0, 0.0, 0.0, 0.5)
      soyaopengl.glBegin(soyaopengl.GL_QUADS)
      soyaopengl.glVertex2i(0, 0)
      soyaopengl.glVertex2i(0, soya.get_screen_height())
      soyaopengl.glVertex2i(soya.get_screen_width(), soya.get_screen_height())
      soyaopengl.glVertex2i(soya.get_screen_width(), 0)
      soyaopengl.glEnd()
      draw_window(self.width, self.height, self.bg_color)
      soyaopengl.glDisable(soyaopengl.GL_BLEND)

      soyaopengl.glColor4f(*self.highlight)
      self.font.draw_area(self.title, self.left, self.top, 0.0, self.width, soya.get_screen_height(), 1)
      self.height = self.font.wordwrap(self.title, self.width)[0]
      
      soyaopengl.glColor4f(*self.color)
      self.font.draw_area(self.text, self.left, self.top + self.height, 0.0, self.width, soya.get_screen_height(), 0)
      self.height += self.font.wordwrap(self.text, self.width)[0]
      
      self.top = int((soya.get_screen_height() - self.height) * 0.5)
      
  class Rectangle(soya.widget.Widget):
    def __init__(self, master = None, color = (0.0, 0.0, 0.0, 0.5)):
      soya.widget.Widget.__init__(self, master)
      self.color = color
      self.visible = 1
    def render(self):
      if self.visible:
        if self.color[3] < 1.0: soyaopengl.glEnable(soyaopengl.GL_BLEND)
        soyaopengl.glColor4f (*self.color)
        soyaopengl.glBegin   (soyaopengl.GL_QUADS)
        soyaopengl.glVertex2f(self.left, self.top)
        soyaopengl.glVertex2f(self.left, self.top + self.height)
        soyaopengl.glVertex2f(self.left + self.width, self.top + self.height)
        soyaopengl.glVertex2f(self.left + self.width, self.top)
        soyaopengl.glEnd()
        if self.color[3] < 1.0: soyaopengl.glDisable(soyaopengl.GL_BLEND)
          
          
  # Inits Soya
  
  #soya.init(width = globdef.SCREEN_WIDTH, height = globdef.SCREEN_HEIGHT, fullscreen = globdef.FULLSCREEN)

  #--------------------#
  # create some shapes #
  #--------------------#

  world = soya.World()
  soya.Face(world, [soya.Vertex(world, -2.0,  0.5, 0.0, 0.0, 0.0),
                    soya.Vertex(world, -2.0, -0.5, 0.0, 0.0, 1.0),
                    soya.Vertex(world,  2.0, -0.5, 0.0, 1.0, 1.0),
                    soya.Vertex(world,  2.0,  0.5, 0.0, 1.0, 0.0)
                    ], soya.Material.get('slune_title'))
  stitle = world.shapify()

  world = soya.World()
  soya.Face(world, [soya.Vertex(world, -0.5,  0.5, 0.0, 0.0, 0.0, (0.0, 0.0, 1.0, 0.75)),
                    soya.Vertex(world, -0.5, -0.5, 0.0, 0.0, 1.0, (0.0, 0.0, 1.0, 0.75)),
                    soya.Vertex(world,  0.5, -0.5, 0.0, 1.0, 1.0, (0.0, 0.0, 1.0, 0.75)),
                    soya.Vertex(world,  0.5,  0.5, 0.0, 1.0, 0.0, (0.0, 0.0, 1.0, 0.75))
                    ], soya.Material.get('halo-noadd'))
  seffect1 = world.shapify()

  world = soya.World()
  soya.Face(world, [soya.Vertex(world, -0.5,  0.5, 0.0, 0.0, 0.0, (1.0, 1.0, 0.0, 1.0)),
                    soya.Vertex(world, -0.5, -0.5, 0.0, 0.0, 1.0, (1.0, 1.0, 0.0, 1.0)),
                    soya.Vertex(world,  0.5, -0.5, 0.0, 1.0, 1.0, (1.0, 1.0, 0.0, 1.0)),
                    soya.Vertex(world,  0.5,  0.5, 0.0, 1.0, 0.0, (1.0, 1.0, 0.0, 1.0))
                     ], soya.Material.get('halo'))
  seffect2 = world.shapify()


  #----------------#
  # create widgets #
  #----------------#

  root = widget.Group()

  #soya.widget.Clearer(root)

  bg_img = soya.widget.Image(root, soya.Material.get('slune_splash'))
  bg_img.resize_style = ('maximize', ('keep ratio', 1024 / 768.0), 'center x', 'center y')
  bg_img.resize_style = ('maximize', 'center x', 'center y')
  bg_rect = Rectangle(root)
  BG_RECT_RESIZE = ('maximize', ('percent top', 0.4), 'maximize height', ('margin bottom', 20), ('margin left', 20), ('margin right', 20))
  bg_rect.resize_style = BG_RECT_RESIZE
  bg_rect.visible = 0

  #--------#
  # banner #
  #--------#

  pub_rect = Rectangle(root)
  pub_rect.resize_style = (('percent left', 0), ('percent top', 0.0), 'maximize width')
  pub_rect.height = soya.widget.default_font.height * 1.3
  pub_banner = soya.widget.HorizontalBanner(root)
  pub_banner.add_elements_from_strings((_('__banner_text__') % globdef.VERSION).split('|'), {}, '  . . .  ')
  
  info_banner = soya.widget.VerticalBanner(root)
  info_banner.add_elements_from_strings(_('__info__').split('|'), {})
  info_banner.speed = 2
  info_banner.resize_style = ('maximize', ('margin left', 20), ('margin right', 20))
  info_banner.loop = 1
  info_banner.visible = 0
  
  
  #-----------------#
  # create 3D scene #
  #-----------------#

  scene = soya.World()
  camera = soya.Camera(scene)
  root.add(camera)
  camera.set_xyz(0.0, -0.5, 5.0)

  atm = soya.NoBackgroundAtmosphere()
  atm.ambient  = (0.2, 0.2, 0.2, 1.0)
  scene.atmosphere = atm
  
  light = soya.Light(scene)
  light.set_xyz(0.0, 1.0, 5.0)
  
  effect1 = soya.Volume(scene, seffect1)
  effect1.set_xyz (-6.0, 0.0, -1.0)
  
  effect2 = soya.Volume(scene, seffect2)
  
  title = soya.Volume(scene, stitle)


  #----------------#
  # menus creation #
  #----------------#

  def set_current_menu(menu):
    global current_menu
    global old_menus
    if current_menu:
      current_menu.visible = 0
      old_menus.append(current_menu)
    current_menu = menu
    current_menu.visible = 1

  def go_back():
    global current_menu
    global old_menus
    if len(old_menus) == 0:
      globdef.generate_dot_slune()
      import sys
      sys.exit()
    if current_menu:
      current_menu.visible = 0
    current_menu = old_menus.pop()
    current_menu.visible = 1

  def popup_msg_window(msg_title, msg_text):
    w = MsgWindow(root, msg_title, msg_text)
    global current_menu
    if current_menu:
      old_menus.append(current_menu)
    current_menu = w
    return w

  def show_h_option():
    menu_h_option.choices[0].value = str(globdef.SCREEN_WIDTH) + 'x' + str(globdef.SCREEN_HEIGHT)
    menu_h_option.choices[1].value = menu_h_option.choices[1].range[globdef.FULLSCREEN]
    menu_h_option.choices[2].value = menu_h_option.choices[2].range[globdef.QUALITY]
    menu_h_option.choices[3].value = globdef.MAX_VISION
    #menu_h_option.choices[4].value = menu_h_option.choices[4].range[globdef.SOUND]
    #menu_h_option.choices[5].value = menu_h_option.choices[5].range[globdef.MUSIC]
    #menu_h_option.choices[6].value = menu_h_option.choices[6].range[globdef.ASYNC_LOAD_MUSIC]
    #menu_h_option.choices[7].value = globdef.SOUND_SYSTEM
    menu_h_option.choices[4].value = str(int(round(globdef.SOUND_VOLUME * 100)))
    set_current_menu(menu_h_option)

  def back_h_option():
    resa = menu_h_option.choices[0].value
    globdef.SCREEN_WIDTH     = int(resa[: resa.find("x")])
    globdef.SCREEN_HEIGHT    = int(resa[resa.find("x") + 1:])
    globdef.FULLSCREEN       = (menu_h_option.choices[1].value == _('on'))
    globdef.QUALITY          = menu_h_option.choices[2].range.index(menu_h_option.choices[2].value)
    globdef.MAX_VISION       = float(menu_h_option.choices[3].value)
    #globdef.SOUND            = (menu_h_option.choices[4].value == _('on'))
    #globdef.MUSIC            = (menu_h_option.choices[5].value == _('on'))
    #globdef.ASYNC_LOAD_MUSIC = (menu_h_option.choices[6].value == _('on'))
    #globdef.SOUND_SYSTEM     = menu_h_option.choices[7].value
    globdef.SOUND_VOLUME     = int(menu_h_option.choices[4].value) / 100.0
    soya.set_quality(globdef.QUALITY)
    soya.set_video(globdef.SCREEN_WIDTH, globdef.SCREEN_HEIGHT, globdef.FULLSCREEN, 1)
    soya.set_sound_volume(globdef.SOUND_VOLUME)
    #import slune.sound; reload(slune.sound)
    go_back()

  def show_p_option():
    menu_p_option.choices[0].value = globdef.NAME
    menu_p_option.choices[1].value = globdef.CHARACTER
    menu_p_option.choices[2].value = menu_p_option.choices[2].range[globdef.VEHICLE]
    menu_p_option.choices[3].value = menu_p_option.choices[3].range[globdef.DIFFICULTY]
    set_current_menu(menu_p_option)

  def back_p_option():
    globdef.NAME       = menu_p_option.choices[0].value
    globdef.CHARACTER  = menu_p_option.choices[1].value
    globdef.VEHICLE    = menu_p_option.choices[2].range.index(menu_p_option.choices[2].value)
    globdef.DIFFICULTY = menu_p_option.choices[3].range.index(menu_p_option.choices[3].value)
    go_back()

  def show_campain():
    set_current_menu(campain)
    
  def show_level():
    menu_level.choices[1].value = globdef.RACE_NB_LAPS
    menu_level.choices[2].value = globdef.RACE_NB_OPPONENTS
    set_current_menu(level)
    
  def show_references():
    pub_banner.visible = 0
    pub_rect.visible = 0
    bg_rect.resize_style = soya.widget.WIDGET_RESIZE_MAXIMIZE
    bg_rect.resize(0, 0, soya.get_screen_width(), soya.get_screen_height())
    info_banner.visible = 1
    info_banner._position = - info_banner.height
    current_menu.visible = 0
    gui_idler.step = -1
    light.visible = 0
    effect1.visible = 0
    effect2.visible = 0
    title.visible = 0
    
  def play_campain():
    import slune.player
    r = slune.player.start_new_game("level-" + select_campain.choices[select_campain.selected])
    if r: # r is the next mission
      globdef.NEXT_MISSION = max(globdef.NEXT_MISSION, int(r[0][8:]))
      missions = map(lambda level_name: int(level_name[14:]), filter(lambda world_name: world_name and world_name.startswith("level-mission"), soya.World.availables()))
      #missions = filter(lambda mission: mission <= globdef.NEXT_MISSION, missions)
      missions.sort()
      missions = map(lambda mission: (_("mission") + "-%s" % mission), missions)
      select_campain.choices = missions
      
      if os.path.exists(os.path.join(soya.path[0], soya.World.DIRNAME, "level-" + r[0] + ".data")):
        select_campain.select(select_campain.selected + 1)
        
    soya.set_root_widget(root)
    
  def play_level():
    #soyaopengl.glEnable(soyaopengl.GL_LIGHTING)
    #soyaopengl.glDisable(soyaopengl.GL_BLEND)
    globdef.RACE_NB_LAPS = menu_level.choices[1].value
    globdef.RACE_NB_OPPONENTS = menu_level.choices[2].value
    import slune.player
    r = slune.player.start_new_game("level-" + select_level.choices[select_level.selected])
    soya.set_root_widget(root)
    
  CHOICELIST_RESIZE_STYLE = ('maximize', ('percent top', 0.4), 'maximize height', ('margin bottom', 20))
  game_menu_1 = soya.widget.ChoiceList(root, [
    soya.widget.Choice(_('Play campain'), show_campain),
    soya.widget.Choice(_('Play level'), show_level),
    soya.widget.Choice(_('Player options'), show_p_option),
    soya.widget.Choice(_('Hardware options'), show_h_option),
    soya.widget.Choice(_('References'), show_references),
    soya.widget.Choice(_('Quit'), go_back)
    ], cancel = 5)
  game_menu_1.resize_style = CHOICELIST_RESIZE_STYLE
  game_menu_1.visible = 0

  checkbox = [_('off'), _('on')]

  menu_h_option = soya.widget.ChoiceList(root, [
    soya.widget.Choice(_('Resolution'), None, None, ['320x240', '640x480', '800x600', '1024x768', '1152x864', '1280x1024', '1400x1050', '1680x1050', '1920x1080']),
    soya.widget.Choice(_('Fullscreen'), None, None, checkbox),
    soya.widget.Choice(_('Graphic quality'), None, None, [_('Low'), _('Medium'), _('High')]),
    soya.widget.Choice(_('Max vision distance'), None, None, [0.5, 2.0], 0.1),
    soya.widget.Choice(_('Sound volume'), None, None, ['0', '10', '20', '30', '40', '50', '60', '70', '80', '90', '100']),
    #soya.widget.Choice(_('Sounds'), None, None, checkbox),
    #soya.widget.Choice(_('Music'), None, None, checkbox),
    #soya.widget.Choice(_('Async load music'), None, None, checkbox),
    #soya.widget.Choice(_('Sound system'), None, None, ["OpenAL", "OpenAL (old)", "SDL_mixer"]),
    soya.widget.Choice(_('Back'), back_h_option)
    ], cancel = -1)
  menu_h_option.resize_style = CHOICELIST_RESIZE_STYLE
  menu_h_option.visible = 0

  menu_p_option = soya.widget.ChoiceList(root, [
    soya.widget.ChoiceInput(_('Name')),
    soya.widget.Choice(_('Character'), None, None, map(_, globdef.CHARACTERS)),
    soya.widget.Choice(_('Vehicle'), None, None, [_('Biplane'), _('Car'), _('Truck'), _('Scooter'), _('Tanker')]),
    soya.widget.Choice(_('Difficulty'), None, None, [_('Newbie'), _('Hacker'), _('Guru')]),
    soya.widget.Choice(_('Back'), back_p_option)
    ], cancel = 4)
  menu_p_option.resize_style = CHOICELIST_RESIZE_STYLE
  menu_p_option.visible = 0

  campain = widget.Group(root)
  campain.visible = 0
  def campain_process_event(event):
    if (event[0] == soyasdlconst.MOUSEMOTION):
      if (event[1] < campain.width * 0.5):
        select_campain.enabled = 1
        menu_campain.selected = -1
      else:
        select_campain.enabled = 0
    elif (event[0] == soyasdlconst.KEYDOWN):
      if   (event[1] == soyasdlconst.K_LEFT):
        select_campain.enabled = 1
        menu_campain.selected = -1
        return
      elif (event[1] == soyasdlconst.K_RIGHT):
        select_campain.enabled = 0
        menu_campain.selected = 0
        return
      elif (event[1] == soyasdlconst.K_ESCAPE):
        go_back()
        return
    elif (event[0] == soyasdlconst.JOYAXISMOTION) and (event[1] == 0):
      if   event[2] < 0:
        select_campain.enabled = 1
        menu_campain.selected = -1
        return
      elif event[2] > 0:
        select_campain.enabled = 0
        menu_campain.selected = 0
        return
      
    if (select_campain.enabled == 1):
      select_campain.process_event(event)
    else:
      menu_campain.process_event(event)
  campain.process_event = campain_process_event
  del campain_process_event
  
  missions = map(lambda level_name: int(level_name[14:]), filter(lambda world_name: world_name and world_name.startswith("level-mission"), soya.World.availables()))
  #missions = filter(lambda mission: mission <= globdef.NEXT_MISSION, missions)
  missions.sort()
  missions = map(lambda mission: (_("mission") + "-%s" % mission), missions)
  select_campain = soya.widget.Selector(campain, missions, _('Select level'), arrows = soya.Material.get('widget_arrow'))
  SELECTOR_RESIZE_STYLE = (('percent top', 0.4), 'maximize height', ('margin bottom', 20), ('percent left', 0.0), ('percent width', 0.5))
  select_campain.resize_style = SELECTOR_RESIZE_STYLE
  
  HALF_CHOICELIST_RESIZE_STYLE = (('percent left', 0.5), 'maximize width', ('percent top', 0.4), 'maximize height', ('margin bottom', 20))

  menu_campain = soya.widget.ChoiceList(campain, [
    soya.widget.Choice(_('Back'), go_back),
    soya.widget.Choice(_('Start'), play_campain),
    ], cancel = 0)
  menu_campain.resize_style = HALF_CHOICELIST_RESIZE_STYLE

  level = widget.Group(root)
  level.visible = 0
  def level_process_event(event):
    if (event[0] == soyasdlconst.MOUSEMOTION):
      if (event[1] < level.width * 0.5):
        select_level.enabled = 1
        menu_level.selected = -1
      else:
        select_level.enabled = 0
    elif (event[0] == soyasdlconst.KEYDOWN and (select_level.enabled == 1 or menu_level.selected == 0 or menu_level.selected == 3)):
      if (event[1] == soyasdlconst.K_LEFT):
        select_level.enabled = 1
        menu_level.selected = -1
        return
      elif (event[1] == soyasdlconst.K_RIGHT):
        select_level.enabled = 0
        menu_level.selected = 0
        return
      elif (event[1] == soyasdlconst.K_ESCAPE):
        go_back()
        return
    elif (event[0] == soyasdlconst.JOYAXISMOTION) and (event[1] == 0):
      if   event[2] < 0:
        select_level.enabled = 1
        menu_level.selected = -1
        return
      elif event[2] > 0:
        select_level.enabled = 0
        menu_level.selected = 0
        return

    if (select_level.enabled == 1):
      select_level.process_event(event)
    else:
      menu_level.process_event(event)
  level.process_event = level_process_event
  del level_process_event

  levels = map(lambda level_name: level_name[6:], filter(lambda world_name: world_name and world_name.startswith("level-") and not world_name.startswith("level-mission"), soya.World.availables()))
  select_level = soya.widget.Selector(level, levels, _('Select level'), arrows = soya.Material.get('widget_arrow'))
  select_level.resize_style = SELECTOR_RESIZE_STYLE

  menu_level = soya.widget.ChoiceList(level, [
    soya.widget.Choice(_('Back'), go_back),
    soya.widget.Choice(_('Lap number'), None, None, [1, 8], 1),
    soya.widget.Choice(_('Opponents'), None, None, [2, 6], 1),
    soya.widget.Choice(_('Start'), play_level),
    ], cancel = 0)
  menu_level.resize_style = HALF_CHOICELIST_RESIZE_STYLE


  #----------#
  # start !! #
  #----------#
  
  soya.set_root_widget(root)
  
  class Idler(soya.Idler):
    ltime = 0.0
    step = 0
    nb_step = 2
    
    def begin_round(self):
      soya.MAIN_LOOP = soya.IDLER = self
      soya.Idler.begin_round(self)
      if self.step == -1:
        # reference
        for event in soya.process_event():
          if (event[0] == soyasdlconst.KEYDOWN and event[1]) or (event[0] == soyasdlconst.MOUSEBUTTONDOWN) or (event[0] == soyasdlconst.JOYBUTTONDOWN):
            info_banner.visible = 0
            pub_banner.visible = 1
            pub_rect.visible = 1
            bg_rect.resize_style = BG_RECT_RESIZE
            bg_rect.resize(0, 0, soya.get_screen_width(), soya.get_screen_height())
            current_menu.visible = 1
            self.step = 3
            light.visible = 1
            effect1.visible = 1
            effect2.visible = 1
            title.visible = 1
            break
      elif self.step < 2:
        for event in soya.process_event():
          if (event[0] == soyasdlconst.JOYBUTTONDOWN) or (event[0] == soyasdlconst.KEYDOWN and event[1]) or (event[0] == soyasdlconst.MOUSEBUTTONDOWN):
            self.end_step_1()
            self.end_step_2()
            self.step = 3
            break
      elif current_menu:
        for event in soya.process_event(): current_menu.process_event(event)
        
    def end_step_1(self):
      effect1.set_identity()
      effect1.scale(20.0, 4.0, 4.0)
      effect1.rotate_incline(180.0)
      effect1.set_xyz(0.0, 0.0, -1.0)
      effect2.set_identity()
      effect2.scale(4.0, 0.1, 0.1)
      effect2.set_xyz(0.0, -0.6, -1.0)
      title.set_identity()

    def end_step_2(self):
      camera.set_xyz(0.0, -1.5, 5.0)
      set_current_menu(game_menu_1)
      bg_rect.visible = 1

    def advance_time(self, proportion):
      if self.step == -1:
        info_banner.widget_advance_time(proportion)
      else:
        pub_banner.widget_advance_time(proportion)

      if self.step == 0:
        if self.ltime < 150.0:
          self.ltime = self.ltime + proportion
          percent = self.ltime / 150.0

          effect1.set_identity()
          effect1.scale(20.0 * percent, 4.0 * percent, 4.0 * percent)
          effect1.rotate_incline(180.0 * percent)
          effect1.set_xyz(0.0, 0.0, -1.0)

          effect2.set_identity()
          effect2.scale(4.0 * percent, 0.1 * percent, 0.1 * percent)
          effect2.set_xyz(0.0, -0.6, -1.0)

          title.set_identity()
          title.scale(percent, percent, percent)
          title.rotate_incline(360.0 * percent)
        else:
          self.end_step_1()
          self.step = 1
          self.ltime = 0.0

      elif self.step == 1:
        if self.ltime < 40.0:
          self.ltime = self.ltime + proportion
          percent = self.ltime / 40.0
          camera.set_xyz(0.0, -0.5 - 1.0 * percent, 5.0)
        else:
          self.end_step_2()
          self.step = 2
          self.ltime = 0.0

    def render(self):
      soya.render()


  gui_idler = Idler()
  action = gui_idler.idle()
  
  
  
