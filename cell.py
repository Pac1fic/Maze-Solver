from graphics import Line, Point

class Cell:
    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = win
        self.visited = False

    def draw(self, x1, y1, x2, y2):
        if self._win is None:
            return
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        if self.has_left_wall:
            left = Line(
                Point(x1, y1),
                Point(x1, y2)
            )
            self._win.draw_line(left) 
        else:
            left = Line(
                Point(x1, y1),
                Point(x1, y2)
            )
            self._win.draw_line(left, "white")
        
        if self.has_top_wall:
            top = Line(
                Point(x1, y1),
                Point(x2, y1)
            )
            self._win.draw_line(top)
        else:
            top = Line(
                Point(x1, y1),
                Point(x2, y1)
            )
            self._win.draw_line(top, "white")

        if self.has_right_wall:
            right = Line(
                Point(x2, y1),
                Point(x2, y2)
            )
            self._win.draw_line(right)
        else:
            right = Line(
                Point(x2, y1),
                Point(x2, y2)
            )
            self._win.draw_line(right, "white")

        if self.has_bottom_wall:
            bottom = Line(
                Point(x1, y2),
                Point(x2, y2)
            )
            self._win.draw_line(bottom)
        else:
            bottom = Line(
                Point(x1, y2),
                Point(x2, y2)
            )
            self._win.draw_line(bottom, "white")

    def draw_move(self, to_cell, undo=False):
        fill_color = "red"
        if undo:
            fill_color = "gray"

        x_start = (self._x1 + self._x2) // 2
        y_start = (self._y1 + self._y2) // 2
        x_finish = (to_cell._x1 + to_cell._x2) / 2
        y_finish = (to_cell._y1 + to_cell._y2) / 2

        path = Line(
            Point(x_start, y_start),
            Point(x_finish, y_finish),
        )

        self._win.draw_line(path, fill_color)