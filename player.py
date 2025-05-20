import pygame
from config import CELL_SIZE

class Player:
    def __init__(self):
        self.row = 0
        self.col = 0

    def reset_position(self):
        self.row = 0
        self.col = 0

    def move(self, direction, max_rows, max_cols):
        if direction == "up" and self.row > 0:
            self.row -= 1
        elif direction == "down" and self.row < max_rows - 1:
            self.row += 1
        elif direction == "left" and self.col > 0:
            self.col -= 1
        elif direction == "right" and self.col < max_cols - 1:
            self.col += 1

    def get_position(self):
        return self.row, self.col

    def draw(self, screen, maze_rows, maze_cols):
        # Dynamically center player based on maze size
        total_width = maze_cols * CELL_SIZE
        total_height = maze_rows * CELL_SIZE
        offset_x = (800 - total_width) // 2
        offset_y = (600 - total_height) // 2

        x = self.col * CELL_SIZE + offset_x
        y = self.row * CELL_SIZE + offset_y
        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, (0, 255, 0), rect)