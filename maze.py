import pygame
import random
from config import SYMBOL_TYPES, CELL_SIZE

class Symbol:
    def __init__(self, type_, position, image):
        self.type = type_
        self.position = position
        self.found = False
        self.image = image

    def is_match(self, other):
        return self.type == other.type

class Maze:
    def __init__(self, level):
        # Determine grid size by level
        if level >= 15:
            self.rows, self.cols = 6, 6
        elif level >= 10:
            self.rows, self.cols = 5, 5
        elif level >= 5:
            self.rows, self.cols = 4, 4
        else:
            self.rows, self.cols = 3, 3

        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.symbols = []

        # Load icons
        raw_icon = pygame.image.load("assets/icons/star.png").convert_alpha()
        self.symbol_image = pygame.transform.scale(raw_icon, (32, 32))

        red_x = pygame.image.load("assets/icons/red_x.png").convert_alpha()
        self.wrong_image = pygame.transform.scale(red_x, (32, 32))

        self.revealed_cells = {}

        self.num_pairs = self.get_num_pairs_by_level(level)

    def get_num_pairs_by_level(self, level):
        # Max cells = rows * cols
        # Fill at most 80% of the grid, even if level demands more

        pair_map = {
            1: 2,  2: 2,  3: 3,  4: 3,     # 3x3 (max 7 filled)
            5: 3,  6: 4,  7: 5,  8: 6,  9: 6,     # 4x4 (max 12 filled)
            10: 4, 11: 6, 12: 8, 13: 9, 14: 10,   # 5x5 (max 20 filled)
            15: 6, 16: 8, 17: 10, 18: 12, 19: 13, 20: 14,  # 6x6 (max 28 filled)
        }

        requested_pairs = pair_map.get(level, 4)
        max_cells = self.rows * self.cols
        max_pairs = (int(max_cells * 0.8)) // 2

        return min(requested_pairs, max_pairs, len(SYMBOL_TYPES))

    def generate(self):
        positions = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        random.shuffle(positions)

        max_possible_pairs = len(positions) // 2
        pairs_to_place = min(self.num_pairs, max_possible_pairs)

        for i in range(pairs_to_place):
            symbol_type = SYMBOL_TYPES[i % len(SYMBOL_TYPES)]
            pos1 = positions.pop()
            pos2 = positions.pop()
            s1 = Symbol(symbol_type, pos1, self.symbol_image)
            s2 = Symbol(symbol_type, pos2, self.symbol_image)
            self.symbols.extend([s1, s2])
            self.grid[pos1[0]][pos1[1]] = s1
            self.grid[pos2[0]][pos2[1]] = s2

    def reveal_symbol(self, x, y):
        symbol = self.grid[x][y]
        if symbol and not symbol.found:
            symbol.found = True
            self.revealed_cells[(x, y)] = 'correct'
            return True
        else:
            self.revealed_cells[(x, y)] = 'wrong'
            return False

    def all_symbols_found(self):
        return all(s.found for s in self.symbols)

    def draw(self, screen, reveal=False):
        total_width = self.cols * CELL_SIZE
        total_height = self.rows * CELL_SIZE
        offset_x = (800 - total_width) // 2
        offset_y = (600 - total_height) // 2

        for r in range(self.rows):
            for c in range(self.cols):
                x = c * CELL_SIZE + offset_x
                y = r * CELL_SIZE + offset_y
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, (255, 255, 255), rect, 2)

                symbol = self.grid[r][c]
                if reveal and symbol:
                    screen.blit(symbol.image, (x + 14, y + 14))
                elif (r, c) in self.revealed_cells:
                    state = self.revealed_cells[(r, c)]
                    if state == 'correct' and symbol:
                        screen.blit(symbol.image, (x + 14, y + 14))
                    elif state == 'wrong':
                        screen.blit(self.wrong_image, (x + 14, y + 14))