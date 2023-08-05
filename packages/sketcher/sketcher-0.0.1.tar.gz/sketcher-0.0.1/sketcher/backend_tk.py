from .backend_base import CanvasBackend
import tkinter as tk


class Backend(CanvasBackend):
    def __init__(self):
        CanvasBackend.__init__(self)
        self.win = tk.Tk()
        self.can = tk.Canvas(self.win)
        self.user_loop = None

    def init(self):
        self.can.configure(
            width=self.size[0],
            height=self.size[1],
            background=self.back_color.hashtag()
        )
        self.can.pack()

    def start(self, setup, loop):
        setup()
        self.user_loop = loop
        self.win.after(int(1000*self.frame), self.loop)
        self.win.mainloop()

    def loop(self):
        self.user_loop()
        self.win.after(int(1000*self.frame), self.loop)

    def clear(self):
        self.can.delete('all')

    def set_fill(self, yes):
        self.fill = yes

    def set_stroke(self, yes):
        self.stroke = yes

    def get_mouse_state(self):
        pass

    def get_keyboard_state(self):
        pass

    def set_size(self, w, h):
        self.size = (w, h)
        self.can.configure(width=w, height=h)

    def set_background(self, color):
        self.back_color = color

    def draw_shape(self, shape):
        pass

    def draw_point(self, x, y):
        fill = self.stroke_color.hashtag() if self.stroke else ''
        self.can.create_line(x, y, x, y, fill=fill)

    def draw_line(self, x1, y1, x2, y2):
        fill = self.stroke_color.hashtag() if self.stroke else ''
        self.can.create_arc(x1, y1, x2, y2, fill=fill)

    def draw_rectangle(self, x, y, w, h):
        fill = self.fill_color.hashtag() if self.fill else ''
        outline = self.stroke_color.hashtag() if self.stroke else ''
        self.can.create_rectangle(x, y, x+w, y+h, fill=fill, outline=outline)

    def draw_ellipse(self, x, y, a, b):
        x0 = x - a/2
        x1 = x + a/2
        y0 = y - b/2
        y1 = y + b/2
        fill = self.fill_color.hashtag() if self.fill else ''
        outline = self.stroke_color.hashtag() if self.stroke else ''
        self.can.create_oval(x0, y0, x1, y1, fill=fill, outline=outline)

    def draw_text(self, x, y, text, **kwargs):
        pass
