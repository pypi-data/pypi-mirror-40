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

import Tkinter, socket, os, os.path
import slune.globdef as globdef, soya, soya.model, soya.soya3d as soya3d

class MainScreen(Tkinter.Tk):
  def __init__(self):
    globdef.GUI = 1 # Using GUI !
    
    Tkinter.Tk.__init__(self)
    self.wm_title("Slune")
    self.option_add("*Entry.relief"      , "flat")
    self.option_add("*Entry.background"  , "#FFFFFF")
    self.option_add("*Text.relief"       , "flat")
    self.option_add("*Text.background"   , "#FFFFFF")
    self.option_add("*Listbox.relief"    , "flat")
    self.option_add("*Listbox.background", "#FFFFFF")
    
    self.image = Tkinter.PhotoImage(master = self, file = os.path.join(soya.model.Image.PATH, "slune-splash.pgm"))
    Tkinter.Label(self, image = self.image, borderwidth = 0).grid(column = 0, row = 0, columnspan = 2)
    
    self.columnconfigure(0, weight = 1)
    self.columnconfigure(1, weight = 0)
    
    self.rowconfigure(0, weight = 1)
    self.rowconfigure(1, minsize = 50)
    self.rowconfigure(2, minsize = 50)
    
    Tkinter.Button(self, text = _("Start new game"   ), command = self.on_new_game ).grid(column = 0, row = 1, sticky = "NSEW")
    Tkinter.Button(self, text = _("Join network game"), command = self.on_join_game).grid(column = 0, row = 2, sticky = "NSEW")
    Tkinter.Button(self, text = _("Options"          ), command = self.on_option   ).grid(column = 0, row = 3, sticky = "NSEW")
    Tkinter.Button(self, text = _("References"       ), command = self.on_info     ).grid(column = 0, row = 4, sticky = "NSEW")
    Tkinter.Button(self, text = _("Credits"          ), command = self.on_credits  ).grid(column = 0, row = 5, sticky = "NSEW")
    Tkinter.Button(self, text = _("Quit"             ), command = self.on_quit     ).grid(column = 0, row = 6, sticky = "NSEW")
    self.wm_protocol("WM_DELETE_WINDOW", self.on_quit)
    
    new_game_options = Tkinter.Frame(self)
    new_game_options.grid(column = 1, row = 1, sticky="NSEW")
    new_game_options.columnconfigure(0, weight = 1)
    new_game_options.columnconfigure(1, weight = 0)
    new_game_options.columnconfigure(2, weight = 0)
    new_game_options.columnconfigure(3, weight = 0)
    
    Tkinter.Label(new_game_options, anchor="e", text = _("Choose level")).grid(column = 0, row = 0, sticky = "NSEW")
    self.level = Tkinter.StringVar()
    self.level.set("mission-1")
    
    levels = map(lambda level_name: level_name[6:], filter(lambda world_name: world_name and world_name.startswith("level-"), soya.soya3d.World.availables()))
    Tkinter.OptionMenu(new_game_options, self.level, *levels).grid(column = 1, row = 0, columnspan = 3, sticky = "NSEW")
    
    Tkinter.Label(new_game_options, anchor="e", text = _("You are")).grid(column = 0, row = 1, sticky="NSEW")
    
    var = Tkinter.StringVar()
    var.set(str(globdef.NAME))
    self.name = Tkinter.Entry(new_game_options, textvariable = var, width = 10, justify = "right")
    self.name.grid(column = 1, row = 1, sticky="NSEW")
    
    Tkinter.Label(new_game_options, text = "@" + socket.gethostname() + ":").grid(column = 2, row = 1, sticky = "NSEW")
    
    self.port = Tkinter.StringVar()
    self.port.set(str(globdef.PORT))
    Tkinter.Entry(new_game_options, textvariable = self.port, width = 5).grid(column = 3, row = 1)
    
    join_game_options = Tkinter.Frame(self)
    join_game_options.grid(column = 1, row = 2, sticky="NSEW")
    join_game_options.columnconfigure(0, weight = 1)
    join_game_options.columnconfigure(1, weight = 1)
    join_game_options.columnconfigure(2, weight = 0)
    join_game_options.columnconfigure(3, weight = 0)
    
    Tkinter.Label(join_game_options, anchor="e", text = _("Join at (host or IP:port)")).grid(column = 0, row = 1, sticky="NSEW")
    
    self.parrain_host = Tkinter.StringVar()
    self.parrain_host.set(str(globdef.PARRAIN_HOST))
    Tkinter.Entry(join_game_options, textvariable = self.parrain_host, width = 18, justify = "right").grid(column = 1, row = 1, sticky="NSEW")
    
    Tkinter.Label(join_game_options, text = ":").grid(column = 2, row = 1, sticky="NSEW")
    
    self.parrain_port = Tkinter.StringVar()
    self.parrain_port.set(globdef.PARRAIN_PORT)
    Tkinter.Entry(join_game_options, textvariable = self.parrain_port, width = 5).grid(column = 3, row = 1, sticky="NSEW")
    
    Tkinter.Label(self, text = _("Slune version %s") % globdef.VERSION).grid(column = 1, row = 6, sticky="NSEW")
    
    character_options = Tkinter.Frame(self)
    character_options.grid(column = 1, row = 3, sticky="NSEW")
    character_options.columnconfigure(0, weight = 0)
    character_options.columnconfigure(1, weight = 1)
    character_options.columnconfigure(2, weight = 0)
    character_options.columnconfigure(3, weight = 1)
    
    Tkinter.Label(character_options, anchor = "e", text = _("Character")).grid(column = 0, row = 0, sticky="NSEW")
    var = Tkinter.StringVar()
    var.set(globdef.CHARACTER)
    Tkinter.OptionMenu(character_options, var, command = self.on_character, *globdef.CHARACTERS).grid(column = 1, row = 0, sticky = "NSEW")
    
    Tkinter.Label(character_options, anchor = "e", text = _("Vehicle")).grid(column = 2, row = 0, sticky="NSEW")
    var = Tkinter.StringVar()
    for text, level in globdef.VEHICLES.items():
      if level == globdef.VEHICLE:
        var.set(text)
        break
    Tkinter.OptionMenu(character_options, var, command = self.on_vehicle, *globdef.VEHICLES.keys()).grid(column = 3, row = 0, sticky = "NSEW")
    
    difficulty_options = Tkinter.Frame(self)
    difficulty_options.grid(column = 1, row = 4, sticky="NSEW")
    difficulty_options.columnconfigure(0, weight = 0)
    difficulty_options.columnconfigure(1, weight = 1)
    
    Tkinter.Label(difficulty_options, anchor = "e", text = _("Difficulty level")).grid(column = 0, row = 0, sticky="NSEW")
    var = Tkinter.StringVar()
    for text, level in globdef.DIFFICULTIES.items():
      if level == globdef.DIFFICULTY:
        var.set(text)
        break
    Tkinter.OptionMenu(difficulty_options, var, _("Newbie"), _("Hacker"), _("Guru"), command = self.on_difficulty).grid(column = 1, row = 0, sticky = "NSEW")
    
    x = self.winfo_screenwidth () / 2 - 385
    y = self.winfo_screenheight() / 2 - 300
    self.wm_geometry("+%s+%s" % (x, y))
    
  def on_new_game(self):
    self.read_params()
    
    self.lower()
    
    import slune.player
    soya.init(width = globdef.SCREEN_WIDTH, height = globdef.SCREEN_HEIGHT)
    soya.set_quality(globdef.QUALITY)
    if globdef.FULLSCREEN: soya.toggle_fullscreen()
    r = slune.player.start_new_game("level-" + self.level.get())
    if globdef.FULLSCREEN: soya.toggle_fullscreen()
    
    if r:
      if os.path.exists(os.path.join(soya3d.World.PATH, "level-" + r[0] + ".data")):
        self.level.set(r[0])
        
    self.tkraise()
    
  def on_join_game(self):
    self.read_params()
    if (globdef.PARRAIN_HOST == "") and (globdef.PORT == globdef.PARRAIN_PORT):
      import tkMessageBox
      tkMessageBox.showerror(_("Network error!"), _("__networkbadconfig__"))
      return
    
    self.lower()
    
    import slune.player
    soya.init(width = globdef.SCREEN_WIDTH, height = globdef.SCREEN_HEIGHT)
    soya.set_quality(globdef.QUALITY)
    if globdef.FULLSCREEN: soya.toggle_fullscreen()
    slune.player.join_network_game()
    if globdef.FULLSCREEN: soya.toggle_fullscreen()
    
    #soya.set_video(640, 480, 0, 0)
    #soya.minimize()
    
    self.tkraise()
    
  def on_option(self):
    self.read_params()
    
    import slune.gui_option
    slune.gui_option.OptionScreen()
    
  def on_info(self): info()
    
  
  def on_credits(self):
    pass
  
  def on_quit(self):
    self.read_params()
    globdef.generate_dot_slune()
    import sys; sys.exit()
    
  def read_params(self):
    globdef.NAME         =     self.name        .get()
    globdef.PORT         = int(self.port        .get())
    globdef.PARRAIN_HOST =     self.parrain_host.get()
    globdef.PARRAIN_PORT = int(self.parrain_port.get())
    
  def on_difficulty(self, difficulty): globdef.DIFFICULTY = globdef.DIFFICULTIES[difficulty]
  
  def on_character (self, character ): globdef.CHARACTER  = character
  
  def on_vehicle   (self, vehicle   ): globdef.VEHICLE    = globdef.VEHICLES[vehicle]


def info():
  f = Tkinter.Toplevel()
  f.wm_title(_("Slune info sources"))
  t = Tkinter.Text(f, background="white")
  t.tag_configure("link", foreground="blue", font = "Courier -11 underline")
  t["font"] = "Courier -16"
  t.pack()
  text = _("__info__")
  for line in text.split("\n"):
    for word in line.split(" "):
      if word.startswith("http://"):
        t.insert("end", word, ("link", word))
        def browse(event, url = word):
          import webbrowser
          webbrowser.open(url)
        t.tag_bind(word, "<Button-1>", browse)
      else: t.insert("end", word)
      t.insert("end", " ")
    t.insert("end", "\n")
