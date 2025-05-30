from tkinter import Tk, BOTH, Canvas
import time, random

class Window:
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, width=self.__width, height=self.__height)
        self.__canvas.pack(fill = BOTH, expand = True)
        self.__window_running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        
    def get_width(self):
        return self.__width
    def get_height(self):
        return self.__height
        
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def wait_for_close(self):
        self.__window_running = True
        while self.__window_running:
            self.redraw()
            
    def close(self):
        self.__window_running = False
        
    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)
        
        
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
 
        
class Line:
    def __init__(self, point_1, point_2):
        self.point_1 = point_1
        self.point_2 = point_2
        
    def draw(self, canvas, fill_color):
        canvas.create_line(self.point_1.x, self.point_1.y, self.point_2.x, self.point_2.y, fill = fill_color, width =2)
        
    def set_color(self, color):
        self.color = color
                
class Cell:
    def __init__(self, win = None):
        self.has_top_wall = True
        self.has_right_wall = True
        self.has_left_wall = True
        self.has_bottom_wall = True
        self.__x1 = -1
        self.__x2 = -1
        self.__y1 = -1
        self.__y2 = -1
        self.__win = win
        self.visited = False
        if win:
            self.window_width = self.__win.get_width()
            self.window_height = self.__win.get_height()
        
                
    def draw(self, x1, y1, x2, y2):
        if self.__win is None:
            return
        self.__x1 = x1
        self.__x2 = x2
        self.__y1 = y1
        self.__y2 = y2
        if self.has_top_wall:
            p1 = Point(self.__x1, self.__y1)
            p2 = Point(self.__x2, self.__y1)
            line = Line(p1, p2)
            self.__win.draw_line(line, "black")
        else:
            p1 = Point(self.__x1, self.__y1)
            p2 = Point(self.__x2, self.__y1)
            line = Line(p1, p2)
            self.__win.draw_line(line, "white")
        if self.has_right_wall:
            p1 = Point(self.__x2, self.__y1)
            p2 = Point(self.__x2, self.__y2)
            line = Line(p1, p2)
            self.__win.draw_line(line, "black")
        else:
            p1 = Point(self.__x2, self.__y1)
            p2 = Point(self.__x2, self.__y2)
            line = Line(p1, p2)
            self.__win.draw_line(line, "white")
        if self.has_left_wall:
            p1 = Point(self.__x1, self.__y1)
            p2 = Point(self.__x1, self.__y2)
            line = Line(p1, p2)
            self.__win.draw_line(line, "black")
        else:
            p1 = Point(self.__x1, self.__y1)
            p2 = Point(self.__x1, self.__y2)
            line = Line(p1, p2)
            self.__win.draw_line(line, "white")
        if self.has_bottom_wall:
            p1 = Point(self.__x1, self.__y2)
            p2 = Point(self.__x2, self.__y2)
            line = Line(p1, p2)
            self.__win.draw_line(line, "black")
        else:
            p1 = Point(self.__x1, self.__y2)
            p2 = Point(self.__x2, self.__y2)
            line = Line(p1, p2)
            self.__win.draw_line(line, "white")
             
    def draw_move(self, to_cell, undo = False):
        cell_1_x_center = (self.__x1 + self.__x2) / 2
        cell_1_y_center = (self.__y1 + self.__y2) / 2
        cell_2_x_center = (to_cell.__x1 + to_cell.__x2) / 2
        cell_2_y_center = (to_cell.__y1 + to_cell.__y2) / 2
        current_center = Point(cell_1_x_center, cell_1_y_center)
        to_center = Point(cell_2_x_center, cell_2_y_center)
        color = "gray" if undo else "red"
        line = Line(current_center, to_center)
        line.set_color(color)
        self.__win.draw_line(line, color)
        
        
class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win = None, seed = None):
        self.__cells = []
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self.__create_cells()
        if seed is not None:
            random.seed(seed)
        self.__create_cells()
        self.__break_entrance_and_exit()
        self.__break_walls_r(0, 0)
        self.__reset_cells_visited()
        
    def __create_cells(self):
        self.__cells = []
        for i in range(self.__num_cols):
            column = []
            self.__cells.append(column)
            for j in range(self.__num_rows):
                new_cells = Cell(self.__win)
                column.append(new_cells)        
        for i in range(self.__num_cols):
            for j in range(self.__num_rows):
                self._draw_cell(i,j)
        self.__break_entrance_and_exit()
        
    def _draw_cell(self, i, j):
        x1 = self.__x1 + (i * self.__cell_size_x)
        y1 = self.__y1 + (j * self.__cell_size_y)
        x2 = x1 + self.__cell_size_x
        y2 = y1 + self.__cell_size_y
        cell = self.__cells[i][j]
        cell.draw(x1, y1, x2, y2)
        self._animate()
        
        
    def _animate(self):
        self.__win.redraw()
        time.sleep(0.01)
        
    def __break_entrance_and_exit(self):
        self.__cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self.__cells[self.__num_cols - 1][self.__num_rows - 1].has_bottom_wall = False
        self._draw_cell(self.__num_cols - 1, self.__num_rows - 1)
        
    def __break_walls_r(self, i, j):
        self.__cells[i][j].visited = True
        while True:
            to_visit = []
            if i > 0 and not self.__cells[i-1][j].visited:
                to_visit.append((i-1, j))
            if i < self.__num_cols -1 and not self.__cells[i+1][j].visited:
                to_visit.append((i+1, j))
            if j > 0 and not self.__cells[i][j-1].visited:
                to_visit.append((i, j-1))
            if j < self.__num_rows -1 and not self.__cells[i][j+1].visited:
                to_visit.append((i, j+1))
            
            if len(to_visit) == 0:
                self._draw_cell(i, j)
                return
            
            direction = random.randrange(len(to_visit))
            next_i, next_j = to_visit[direction]
            
            if next_i == i - 1:
                self.__cells[i][j].has_left_wall = False
                self.__cells[next_i][next_j].has_right_wall = False
            if next_i == i + 1:
                self.__cells[i][j].has_right_wall = False
                self.__cells[next_i][next_j].has_left_wall = False
            if next_j == j - 1:
               self.__cells[i][j].has_top_wall = False
               self.__cells[next_i][next_j].has_bottom_wall = False
            if next_j == j + 1:
                self.__cells[i][j].has_bottom_wall = False
                self.__cells[next_i][next_j].has_top_wall = False
            self.__break_walls_r(next_i, next_j)
            
        
        
    def __reset_cells_visited(self):
        for col in self.__cells:
            for cell in col:
                cell.visited = False
                
    def _solve_r(self, i, j):
        self._animate()
        self.__cells[i][j].visited = True
    
        if i == self.__num_cols - 1 and j == self.__num_rows - 1:
            return True
    
        directions = [
            (i-1, j, "left"),
            (i+1, j, "right"), 
            (i, j-1, "up"),
            (i, j+1, "down")
        ]
    
        for new_i, new_j, direction in directions:
            if 0 <= new_i < self.__num_cols and 0 <= new_j < self.__num_rows:
                if ((direction == "left" and not self.__cells[i][j].has_left_wall and not self.__cells[new_i][new_j].visited) or
                    (direction == "right" and not self.__cells[i][j].has_right_wall and not self.__cells[new_i][new_j].visited) or
                    (direction == "up" and not self.__cells[i][j].has_top_wall and not self.__cells[new_i][new_j].visited) or
                    (direction == "down" and not self.__cells[i][j].has_bottom_wall and not self.__cells[new_i][new_j].visited)):
                    
                    self.__cells[i][j].draw_move(self.__cells[new_i][new_j])
                    if self._solve_r(new_i, new_j):
                        return True
                    self.__cells[i][j].draw_move(self.__cells[new_i][new_j], undo=True)
    
        return False

    def solve(self):
        return self._solve_r(0, 0)  
                               
if __name__ == "__main__":
    win = Window(800, 600)
    point_1 = Point(100, 100)
    point_2 = Point(200, 200)
    cell = Cell(win)
    maze = Maze(50, 50, 10, 13, 50, 50, win)
    maze.solve()
    win.wait_for_close()