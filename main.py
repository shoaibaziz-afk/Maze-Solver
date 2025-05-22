from tkinter import Tk, BOTH, Canvas
import time

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
    def __init__(self, win):
        self.has_top_wall = True
        self.has_right_wall = True
        self.has_left_wall = True
        self.has_bottom_wall = True
        self.__x1 = -1
        self.__x2 = -1
        self.__y1 = -1
        self.__y2 = -1
        self.__win = win
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
        if self.has_right_wall:
            p1 = Point(self.__x2, self.__y1)
            p2 = Point(self.__x2, self.__y2)
            line = Line(p1, p2)
            self.__win.draw_line(line, "black")
        if self.has_left_wall:
            p1 = Point(self.__x1, self.__y1)
            p2 = Point(self.__x1, self.__y2)
            line = Line(p1, p2)
            self.__win.draw_line(line, "black")
        if self.has_bottom_wall:
            p1 = Point(self.__x1, self.__y2)
            p2 = Point(self.__x2, self.__y2)
            line = Line(p1, p2)
            self.__win.draw_line(line, "black")
             
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
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win):
        self.__cells = []
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self.__create_cells()
        
    def __create_cells(self):
        self.__cells = []
        for i in range(self.__num_cols):
            column = []
            self.__cells.append(column)
            for j in range(self.__num_rows):
                x = self.__x1 + (i * self.__cell_size_x)
                y = self.__y1 + (j * self.__cell_size_y)
                new_cells = Cell(self.__win)
                column.append(new_cells)
                self.__draw_cell(i, j)
        
    def __draw_cell(self, i, j):
        x1 = self.__x1 + (i * self.__cell_size_x)
        y1 = self.__y1 + (j * self.__cell_size_y)
        x2 = x1 + self.__cell_size_x
        y2 = y1 + self.__cell_size_y
        cell = self.__cells[i][j]
        cell.draw(x1, y1, x2, y2)
        self._animate()
        
    def _animate(self):
        self.__win.redraw()
        time.sleep(0.02)
        
        
if __name__ == "__main__":
    win = Window(800, 600)
    point_1 = Point(100, 100)
    point_2 = Point(200, 200)
    cell = Cell(win)
    maze = Maze(50, 50, 10, 14, 50, 50, win)
    # x1, y1, x2, y2 = 0, 0, 20, 20
    # while x1 <= 780 and x2 <= 800 and y1 <= 580 and y2 <= 600:
    #     cell.draw(x1, y1, x2, y2)
    #     x1 += 20
    #     y1 += 20
    #     x2 += 20
    #     y2 += 20
    # line = Line(point_1, point_2)
    # win.draw_line(line, "black")
    win.wait_for_close()