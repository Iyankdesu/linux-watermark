#!/usr/bin/env python
# -.- encoding: utf-8 -.-

'''
Dependences: python-gobject
'''

import os
import ctypes
import platform
import logging
import signal

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Pango
import cairo


def set_name(new_name):
    if platform.system() != 'Linux':
        logging.warning('Rename process:Unsupported platform')
    try:
        libc = ctypes.CDLL('libc.so.6')
        libc.prctl(15, new_name, 0, 0, 0)
        return True
    except:
        logging.warning("Rename process failed :PID: " + repr(os.getpid()))
    return False


class WaterMark(Gtk.Window):

    def __init__(self):
        super(WaterMark, self).__init__()
        self.setup()
        self.init_ui()

    def setup(self):
        self.set_app_paintable(True)
        self.set_type_hint(Gdk.WindowTypeHint.DOCK)
        self.set_keep_below(True)

        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual and screen.is_composited():
            self.set_visual(visual)

    def init_ui(self):

        self.connect("draw", self.on_draw)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.box.set_homogeneous(False)
        self.add(self.box)

        label_atas = Gtk.Label()
        text = "Activate Linux" #Change this
        label_atas.set_text(text)
        fd = Pango.FontDescription("Arial 15")
        label_atas.set_alignment(0, 1)
        label_atas.modify_font(fd)
        label_atas.modify_fg(Gtk.StateFlags.NORMAL, Gdk.color_parse("#A9A9A9"))
        self.box.pack_start(label_atas, True, True, 0)


        
        label_bawah = Gtk.Label()
        label_bawah.set_text("Go to Settings to activate Linux.") #Change this
        fd = Pango.FontDescription("Arial 10")
        label_bawah.set_alignment(0, 1)
        label_bawah.modify_font(fd)
        label_bawah.modify_fg(Gtk.StateFlags.NORMAL, Gdk.color_parse("#A9A9A9"))
        self.box.pack_start(label_bawah, True, True, 0)
        

        root_win = Gdk.get_default_root_window()
        root_height = root_win.get_height()
        root_width = root_win.get_width()
        logging.info("Desktop-size: " +
                     repr(root_width) + "x" + repr(root_height))

        self.connect("delete-event", Gtk.main_quit)
        self.show_all()
        self.set_keep_above(True)
        self.set_property("skip-taskbar-hint", True)
        w_width, w_height = self.get_size()
        logging.info("Window-size: " + repr(w_width) + "x" + repr(w_height))
        self.move(root_width - w_width - 90, root_height - w_height - 70)


    def on_draw(self, wid, cr):
        cr.set_operator(cairo.OPERATOR_CLEAR)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)


def main():
        logging.basicConfig(level=logging.DEBUG)
        WaterMark()
        Gtk.main()
        

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
