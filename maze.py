from cell import Cell
from graphics import Point
import time
import random

class Maze:
    def __init__(
        self, 
        x1, 
        y1, 
        num_rows, 
        num_cols, 
        cell_size_x, 
        cell_size_y, 
        win=None,
        seed=None
        ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win

        if seed:
            random.seed(seed)
        
        self._cells = []
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)

        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        last_x = len(self._cells) - 1
        last_y = len(self._cells[last_x]) - 1

        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[last_x][last_y].has_bottom_wall = False
        self._draw_cell(last_x, last_y)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            to_visit = []
            # down
            if self._num_rows - 1 > j and not self._cells[i][j+1].visited:
                to_visit.append([i, j+1])
            # right
            if self._num_cols - 1 > i and not self._cells[i+1][j].visited:
                to_visit.append([i+1, j])
            # up
            if j > 0 and not self._cells[i][j-1].visited:
                to_visit.append([i, j-1])
            # left
            if i > 0 and not self._cells[i-1][j].visited:
                to_visit.append([i-1, j])

            if len(to_visit) == 0:
                self._draw_cell(i, j)
                return
            else:
                rand_direction = random.choice(to_visit)

                # down
                if rand_direction[1] == j+1:
                    self._cells[i][j].has_bottom_wall = False
                    self._cells[i][j+1].has_top_wall = False
                # top
                if rand_direction[1] == j-1:
                    self._cells[i][j].has_top_wall = False
                    self._cells[i][j-1].has_bottom_wall = False
                # right
                if rand_direction[0] == i+1:
                    self._cells[i][j].has_right_wall = False
                    self._cells[i+1][j].has_left_wall = False
                # left
                if rand_direction[0] == i-1:
                    self._cells[i][j].has_left_wall = False
                    self._cells[i-1][j].has_right_wall = False

                # recursively visit the next cell
                self._break_walls_r(rand_direction[0], rand_direction[1])

    def _reset_cells_visited(self):
        for col in self._cells:
                for cell in col:
                    cell.visited = False

    def solve(self):
        return self._solve_r()

    def _solve_r(self, i=0, j=0):
        self._animate()
        self._cells[i][j].visited =True
        if i == self._num_cols-1 and j == self._num_rows-1:
            return True
        # down
        if self._num_rows - 1 > j and not self._cells[i][j].has_bottom_wall and not self._cells[i][j+1].visited:
            self._cells[i][j].draw_move(self._cells[i][j+1])
            if self._solve_r(i, j+1):
                return True
            self._cells[i][j].draw_move(self._cells[i][j+1], True)
        # right
        if self._num_cols - 1 > i and not self._cells[i][j].has_right_wall  and not self._cells[i+1][j].visited:
            self._cells[i][j].draw_move(self._cells[i+1][j])
            if self._solve_r(i+1, j):
                return True
            self._cells[i][j].draw_move(self._cells[i+1][j], True)
        # up
        if j > 0 and not self._cells[i][j-1].visited:
            self._cells[i][j].draw_move(self._cells[i][j-1])
            if self._solve_r(i, j-1):
                return True
            self._cells[i][j].draw_move(self._cells[i][j-1], True)
        # left
        if i > 0 and not self._cells[i-1][j].visited:
            self._cells[i][j].draw_move(self._cells[i-1][j])
            if self._solve_r(i-1, j):
                return True
            self._cells[i][j].draw_move(self._cells[i-1][j], True)
        return False