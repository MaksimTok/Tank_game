import pygame


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 0:
                    border = 1
                else:
                    border = self.cell_size
                pygame.draw.rect(screen, 'white',
                                 pygame.Rect(self.left + j * self.cell_size, self.top + i * self.cell_size,
                                             self.cell_size, self.cell_size), width=border)

    def get_cell(self, mouse_pos):
        for i in range(self.height):
            for j in range(self.width):
                if self.left + j * self.cell_size <= mouse_pos[0] <= \
                        self.left + j * self.cell_size + self.cell_size and \
                        self.top + i * self.cell_size <= mouse_pos[1] <= self.top + i * self.cell_size + self.cell_size:
                    return i, j
        return

    def on_click(self, cell_coords):
        if cell_coords:
            if self.board[cell_coords[0]][cell_coords[1]] == 0:
                self.board[cell_coords[0]][cell_coords[1]] = 1
            else:
                self.board[cell_coords[0]][cell_coords[1]] = 0

    def get_click(self, mouse_pos):
        self.on_click(self.get_cell(mouse_pos))


class Tank:
    pass


class TankType1(Tank):
    pass


class TankType2(Tank):
    pass


class TankType3(Tank):
    pass


class TankType4(Tank):
    pass


class TankType5(Tank):
    pass


class TankType6(Tank):
    pass


class TankType7(Tank):
    pass


class TankType8(Tank):
    pass