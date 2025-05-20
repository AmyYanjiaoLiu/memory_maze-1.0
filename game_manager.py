import pygame
from maze import Maze
from player import Player
from ui_manager import UIManager
from config import DARK_BLUE

class GameManager:
    def __init__(self, screen, start_level=1):
        self.screen = screen
        self.ui = UIManager(screen)
        self.level = start_level
        self.lives = 3
        self.score = 0
        self.phase = "memorize"
        self.memorize_timer = 3000
        self.last_phase_change = pygame.time.get_ticks()

        self.player = Player()
        self.maze = Maze(self.level)
        self.maze.generate()
        self.player.reset_position()

        self.level_complete_time = None
        self.showing_rules = False  # NEW: Rule popup flag

    def handle_input(self, event):
        if self.showing_rules:
            return None  # Block input while game rule is shown

        if event.type == pygame.KEYDOWN and self.phase == "navigate":
            if event.key == pygame.K_UP:
                self.player.move("up", self.maze.rows, self.maze.cols)
            elif event.key == pygame.K_DOWN:
                self.player.move("down", self.maze.rows, self.maze.cols)
            elif event.key == pygame.K_LEFT:
                self.player.move("left", self.maze.rows, self.maze.cols)
            elif event.key == pygame.K_RIGHT:
                self.player.move("right", self.maze.rows, self.maze.cols)
            elif event.key == pygame.K_SPACE:
                return self.handle_selection()
        return None

    def handle_selection(self):
        x, y = self.player.get_position()
        symbol = self.maze.grid[x][y]

        if symbol:
            if symbol.found:
                self.ui.render_feedback("Already revealed")
                return None
            else:
                symbol.found = True
                self.maze.revealed_cells[(x, y)] = 'correct'
                self.score += 1
                self.ui.render_feedback("Correct!")
        else:
            if (x, y) not in self.maze.revealed_cells:
                self.maze.revealed_cells[(x, y)] = 'wrong'
                self.lives -= 1
                self.ui.render_feedback("Wrong!")

        if self.lives == 0:
            return 'game_over'

        if self.maze.all_symbols_found() and self.level_complete_time is None:
            self.level_complete_time = pygame.time.get_ticks()

        return None

    def update(self):
        self.screen.fill(DARK_BLUE)

        if self.phase == "memorize":
            self.maze.draw(self.screen, reveal=True)
            if pygame.time.get_ticks() - self.last_phase_change > self.memorize_timer:
                self.phase = "navigate"
            else:
                font = pygame.font.Font(None, 36)
                msg = font.render("Memorize the symbols...", True, (255, 255, 255))
                msg_rect = msg.get_rect(center=(400, 550))
                self.screen.blit(msg, msg_rect)
        elif self.level_complete_time is None:
            self.maze.draw(self.screen, reveal=False)
            self.player.draw(self.screen, self.maze.rows, self.maze.cols)
        else:
            self.maze.draw(self.screen, reveal=False)
            font = pygame.font.Font(None, 48)
            msg = font.render(f"Great job! Moving to Level {self.level + 1}...", True, (0, 255, 0))
            msg_rect = msg.get_rect(center=(400, 580))
            self.screen.blit(msg, msg_rect)

            if pygame.time.get_ticks() - self.level_complete_time > 3000:
                self.start_next_level()

        self.ui.render_score(self.score)
        self.ui.render_level(self.level)
        self.ui.render_lives(self.lives)

        # Top-right buttons
        menu_btn = self.ui.draw_top_menu_button()
        rule_btn = None

        self.ui.update_feedback()

        close_btn = None
        if self.showing_rules:
            close_btn = self.ui.draw_game_rule_popup()

        return {
            "menu_btn": menu_btn,
            "rule_btn": rule_btn,
            "close_btn": None
        }

    def handle_button_clicks(self, event, menu_btn, rule_btn, close_btn):
        if self.ui.handle_top_button_click(event, menu_btn):
            return 'menu'
        elif self.ui.handle_top_button_click(event, rule_btn):
            self.showing_rules = True
        elif close_btn and self.ui.handle_close_button_click(event, close_btn):
            self.showing_rules = False
        return None

    def start_next_level(self):
        self.level += 1
        self.lives = 3
        self.maze = Maze(self.level)
        self.maze.generate()
        self.player.reset_position()
        self.phase = "memorize"
        self.last_phase_change = pygame.time.get_ticks()
        self.level_complete_time = None

    def draw_game_over(self):
        font = pygame.font.Font(None, 60)
        text = font.render("Game Over", True, (255, 100, 100))
        text_rect = text.get_rect(center=(400, 250))
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (100, 200, 200), (300, 350, 200, 60), border_radius=12)
        restart_font = pygame.font.Font(None, 40)
        restart_text = restart_font.render("Start Again", True, (0, 0, 0))
        restart_rect = restart_text.get_rect(center=(400, 380))
        self.screen.blit(restart_text, restart_rect)