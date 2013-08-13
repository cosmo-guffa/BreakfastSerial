#!/usr/bin/env python
"""
Changes the color of an LED using the GTK color picker.
Requires pygtk.
Use circuit from Example 3, Sparkfun Inventors Guide : http://ardx.org/src/guide/2/ARDX-EG-01.pdf
"""

# example colorsel.py
from BreakfastSerial import RGBLed, Arduino

board = Arduino()
led = RGBLed(board, { "red": 9, "green": 10, "blue": 11 })
import pygtk
pygtk.require('2.0')
import gtk

class ColorSelectionExample:
    # Color changed handler
    def color_changed_cb(self, widget):
        # Get drawingarea colormap
        colormap = self.drawingarea.get_colormap()

        # Get current color
        c = self.colorseldlg.colorsel.get_current_color()
        colorTuple = (c.red_float*255, c.green_float*255, c.blue_float*255)
        print str(colorTuple)
        led.setColor(colorTuple)

        # Set window background color
        self.drawingarea.modify_bg(gtk.STATE_NORMAL, c)

    # Drawingarea event handler
    def area_event(self, widget, event):
        handled = False

        # Check if we've received a button pressed event
        if event.type == gtk.gdk.BUTTON_PRESS:
            handled = True

            # Create color selection dialog
            if self.colorseldlg == None:
                self.colorseldlg = gtk.ColorSelectionDialog(
                    "Select background color")

            # Get the ColorSelection widget
            colorsel = self.colorseldlg.colorsel

            colorsel.set_previous_color(self.color)
            colorsel.set_current_color(self.color)
            colorsel.set_has_palette(True)

            # Connect to the "color_changed" signal
            colorsel.connect("color_changed", self.color_changed_cb)
            # Show the dialog
            response = self.colorseldlg.run()

            if response -- gtk.RESPONSE_OK:
                self.color = colorsel.get_current_color()
            else:
                self.drawingarea.modify_bg(gtk.STATE_NORMAL, self.color)

            self.colorseldlg.hide()

        return handled

    # Close down and exit handler
    def destroy_window(self, widget, event):
        gtk.main_quit()
        return True

    def __init__(self):
        self.colorseldlg = None
        # Create toplevel window, set title and policies
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title("Color selection test")
        window.set_resizable(True)

        # Attach to the "delete" and "destroy" events so we can exit
        window.connect("delete_event", self.destroy_window)
  
        # Create drawingarea, set size and catch button events
        self.drawingarea = gtk.DrawingArea()

        self.color = self.drawingarea.get_colormap().alloc_color(0, 65535, 0)

        self.drawingarea.set_size_request(200, 200)
        self.drawingarea.set_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.drawingarea.connect("event",  self.area_event)
  
        # Add drawingarea to window, then show them both
        window.add(self.drawingarea)
        self.drawingarea.show()
        window.show()
  
def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    ColorSelectionExample()
    main()
