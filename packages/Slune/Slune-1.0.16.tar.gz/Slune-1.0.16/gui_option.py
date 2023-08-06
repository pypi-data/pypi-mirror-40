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

import Tkinter
import slune.globdef as globdef

QUALITY_LOW    = _("Low"   ).encode("latin")
QUALITY_MEDIUM = _("Medium").encode("latin")
QUALITY_HIGH   = _("High"  ).encode("latin")

class OptionScreen(Tkinter.Toplevel):
  def __init__(self):
    Tkinter.Toplevel.__init__(self)
    self.wm_title(_("Slune options"))
    
    self.columnconfigure(0, weight = 1)
    self.columnconfigure(1, weight = 1)
    
    Tkinter.Label(self, wraplength = 300, text = _("__warning_need_restart__")).grid(column = 0, row = 0, columnspan = 2, sticky = "NSEW")
    
    Tkinter.Label(self, anchor="e", text = _("Fullscreen")).grid(column = 0, row = 1, sticky = "NSEW")
    self.fullscreen = Tkinter.BooleanVar()
    self.fullscreen.set(globdef.FULLSCREEN)
    Tkinter.Checkbutton(self, variable = self.fullscreen).grid(column = 1, row = 1, sticky = "NSEW")
    
    Tkinter.Label(self, anchor="e", text = _("Resolution")).grid(column = 0, row = 2, sticky = "NSEW")
    
    self.resa = Tkinter.Listbox(self, height = 5)
    resas = ("640x480", "800x600", "1024x768", "1152x864", "1400x1050")
    self.resa.insert(0, *resas)
    i = 0
    for i in range(len(resas)):
      if resas[i] == "%sx%s" % (globdef.SCREEN_WIDTH, globdef.SCREEN_HEIGHT):
        self.resa.selection_set(i)
        break
    self.resa.grid(column = 1, row = 2, sticky = "NSEW")
    
    Tkinter.Label(self, anchor="e", text = _("Graphic quality")).grid(column = 0, row = 3, sticky = "NSEW")
    self.quality = Tkinter.StringVar()
    self.quality.set({ 0 : QUALITY_LOW, 1 : QUALITY_MEDIUM, 2 : QUALITY_HIGH }[globdef.QUALITY])
    Tkinter.OptionMenu(self, self.quality, QUALITY_LOW, QUALITY_MEDIUM, QUALITY_HIGH).grid(column = 1, row = 3, sticky = "NSEW")
    
    Tkinter.Label(self, anchor="e", text = _("Max vision distance")).grid(column = 0, row = 4, sticky = "NSEW")
    self.max_vision = Tkinter.StringVar()
    self.max_vision.set(str(globdef.MAX_VISION))
    Tkinter.Entry(self, textvariable = self.max_vision).grid(column = 1, row = 4, sticky = "NSEW")
    
    Tkinter.Label(self, anchor="e", text = _("Music")).grid(column = 0, row = 5, sticky = "NSEW")
    self.music = Tkinter.BooleanVar()
    self.music.set(globdef.MUSIC)
    Tkinter.Checkbutton(self, variable = self.music).grid(column = 1, row = 5, sticky = "NSEW")
    
    Tkinter.Label(self, anchor="e", text = _("Sound")).grid(column = 0, row = 6, sticky = "NSEW")
    self.sound = Tkinter.BooleanVar()
    self.sound.set(globdef.SOUND)
    Tkinter.Checkbutton(self, variable = self.sound).grid(column = 1, row = 6, sticky = "NSEW")
    
    Tkinter.Label(self, anchor="e", text = _("Async load music")).grid(column = 0, row = 7, sticky = "NSEW")
    self.async_load_music = Tkinter.BooleanVar()
    self.async_load_music.set(globdef.ASYNC_LOAD_MUSIC)
    Tkinter.Checkbutton(self, variable = self.async_load_music).grid(column = 1, row = 7, sticky = "NSEW")
    
    Tkinter.Label(self, anchor="e", text = _("Race laps number")).grid(column = 0, row = 8, sticky = "NSEW")
    self.race_nb_laps = Tkinter.StringVar()
    self.race_nb_laps.set(str(globdef.RACE_NB_LAPS))
    Tkinter.Entry(self, textvariable = self.race_nb_laps).grid(column = 1, row = 8, sticky = "NSEW")
    
    Tkinter.Label(self, anchor="e", text = _("Opponents")).grid(column = 0, row = 9, sticky = "NSEW")
    self.race_nb_opponents = Tkinter.StringVar()
    self.race_nb_opponents.set(str(globdef.RACE_NB_OPPONENTS))
    Tkinter.Entry(self, textvariable = self.race_nb_laps).grid(column = 1, row = 9, sticky = "NSEW")
    
    #Tkinter.Label(self, anchor="e", text = _("Speed")).grid(column = 0, row = 10, sticky = "NSEW")
    #self.speed = Tkinter.StringVar()
    #self.speed.set(str(globdef.SPEED))
    #Tkinter.Entry(self, textvariable = self.speed).grid(column = 1, row = 10, sticky = "NSEW")
    
    Tkinter.Button(self, text = _("Ok"    ), command = self.on_ok    ).grid(column = 0, row = 10, sticky = "NSEW")
    Tkinter.Button(self, text = _("Cancel"), command = self.on_cancel).grid(column = 1, row = 10, sticky = "NSEW")
    
  def on_ok(self):
    import py2play.idler
    
    globdef.FULLSCREEN = self.fullscreen.get()
    try:
      resa = self.resa.get(self.resa.curselection()[0])
    except IndexError: pass
    else:
      globdef.SCREEN_WIDTH         = int(resa[: resa.find("x")])
      globdef.SCREEN_HEIGHT        = int(resa[resa.find("x") + 1:])
    globdef.QUALITY                = { QUALITY_LOW : 0, QUALITY_MEDIUM : 1, QUALITY_HIGH : 2 }[self.quality.get()]
    try: globdef.MAX_VISION        = float(self.max_vision.get())
    except: pass
    globdef.MUSIC                  = self.music.get()
    globdef.SOUND                  = self.sound.get()
    globdef.ASYNC_LOAD_MUSIC       = self.async_load_music.get()
    try: globdef.RACE_NB_LAPS      = int(self.race_nb_laps.get())
    except: pass
    try: globdef.RACE_NB_OPPONENTS = int(self.race_nb_opponents.get())
    except: pass
    #try: globdef.SPEED             = py2play.idler.SPEED = float(self.speed.get())
    #except: pass
    
    globdef.generate_dot_slune()
    self.withdraw()
    
    import soya
    if soya.inited:
      soya.set_quality(globdef.QUALITY)
      soya.set_video(globdef.SCREEN_WIDTH, globdef.SCREEN_HEIGHT, 0, 1)
      
  def on_cancel(self): self.withdraw()
  
