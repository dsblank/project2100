from __future__ import print_function, division, with_statement

from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import Gdk

import cairo
import time
import sys
import random

class Project2100():
    def __init__(self, glade_file=None):
        self.shapes = []
        self.new_shapes = []
        self.is_fullscreen = False
        self.double_buffer = None

        if glade_file:
            self.builder = Gtk.Builder()
            self.glade_file = glade_file
            self.builder.add_from_file(self.glade_file)
            # Get objects
            self.window = self.builder.get_object("window")
            self.builder.connect_signals(self)
        else:
            self.window = Gtk.Window()
        self.window.connect("key-press-event", self.on_win_key_press_event)
        self.window.connect("window-state-event", self.on_window_state_event)
        self.window.connect("destroy", self.close_window)
        self.window.show()

    def close_window(self, widget=None):
        Gtk.main_quit()

    def fullscreen_mode(self):
        if self.is_fullscreen:
            self.window.unfullscreen()
        else:
            self.window.fullscreen()

    def on_win_key_press_event(self, widget, ev):
        key = Gdk.keyval_name(ev.keyval)
        if key == "f":
            self.fullscreen_mode()
        elif key == "q":
            self.close_window()
        elif key == "u":
            self.redraw()

    def on_window_state_event(self, widget, ev):
        self.is_fullscreen = bool(ev.new_window_state & Gdk.WindowState.FULLSCREEN)

    def on_draw(self, widget, cr):
        """Throw double buffer into widget drawable"""
        db = self.double_buffer
        if db is None:
            print('Invalid double buffer')
            return False
        #new things to draw?
        if self.new_shapes:
            cc = cairo.Context(db)
            cc.scale(db.get_width(), db.get_height())
            for shape in self.new_shapes:
                shape.draw(cc)
            db.flush()
            # move to shape to be able to redraw after resize/etc
            #self.shapes.extend(self.new_shapes)
            while self.new_shapes: 
                self.new_shapes.pop()
        # Now refresh window:
        cr.set_source_surface(db, 0.0, 0.0)
        cr.paint()
        return False

    def on_configure(self, widget, event, data=None):
        """Configure the double buffer based on size of the widget"""
        # Destroy previous buffer
        if self.double_buffer is not None:
            self.double_buffer.finish()
            self.double_buffer = None
        # Create a new buffer
        self.double_buffer = cairo.ImageSurface(\
                cairo.FORMAT_ARGB32,
                widget.get_allocated_width(),
                widget.get_allocated_height()
            )
        # Initialize the buffer
        self.redraw_everything()
        return False

    def redraw_everything(self):
        """Draw something into the buffer"""
        db = self.double_buffer
        if db is not None:
            # Create cairo context with double buffer as is DESTINATION
            cc = cairo.Context(db)
            # Scale to device coordenates
            cc.scale(db.get_width(), db.get_height())
            # Draw a white background
            cc.set_source_rgb(1, 1, 1)
            for shape in self.shapes:
                shape.draw(cc)
            # Flush drawing actions
            db.flush()
        else:
            print('Invalid double buffer')

    def background(self):
        self.new_shapes.append( Rectangle(random.random(), random.random(), 0.1, 0.1))
        self.redraw()
        return True

    def redraw(self):
        self.window.queue_draw()

class Rectangle():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.line_width = 1.0
        self.color = (0, 0, 0)

    def draw(self, canvas):
        print("Rectangle", self.x, self.y, self.width, self.height)
        line_width, notused = canvas.device_to_user(self.line_width, 0.0)
        canvas.rectangle(self.x, self.y, self.width, self.height)
        canvas.set_line_width(line_width)
        canvas.set_source_rgb(*self.color)
        canvas.stroke()

if __name__ == "__main__":
    app = Project2100('project2100.glade')
    GLib.timeout_add(100, app.background, priority=100)
    Gtk.main()
