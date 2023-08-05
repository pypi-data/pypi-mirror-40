color_tab = {
    'black': (0, 0, 0),
    'white': (1, 1, 1),
    'red': (1, 0, 0),
    'green': (0, 1, 0),
    'blue': (0, 0, 1),
    'grey': (0.5, 0.5, 0.5),
}


class Color:
    def __init__(self, col):
        self.r = 0.0
        self.g = 0.0
        self.b = 0.0
        if isinstance(col, str):
            self.r, self.g, self.b = color_tab[col]
        elif isinstance(col, Color):
            self.r = col.r
            self.g = col.g
            self.b = col.b
        elif isinstance(col, tuple):
            self.r = col[0]
            self.g = col[1]
            self.b = col[2]
        elif isinstance(col, float):
            self.r = col
            self.g = col
            self.b = col

    def hashtag(self):
        r = hex(int(255*self.r))[2:]
        g = hex(int(255*self.g))[2:]
        b = hex(int(255*self.b))[2:]
        if len(r) != 2:
            r = '0' + r
        if len(g) != 2:
            g = '0' + g
        if len(b) != 2:
            b = '0' + b
        return '#{}{}{}'.format(r, g, b)
