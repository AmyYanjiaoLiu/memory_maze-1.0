import pygame
from game_manager import GameManager
from ui_manager import UIManager

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Memory Maze")
clock = pygame.time.Clock()
FPS = 60

# Game state control
game_state = 'menu'
game_manager = None
start_level = 1
running = True
showing_menu_rules = False  # NEW: rule popup toggle for menu

# UIManager instance
ui = UIManager(screen)

while running:
    screen.fill((20, 20, 40))

    # ──────────────── MAIN MENU ────────────────
    if game_state == 'menu':
        button_rects = ui.draw_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if showing_menu_rules:
                close_rect = ui.draw_game_rule_popup()
                if ui.handle_close_button_click(event, close_rect):
                    showing_menu_rules = False
            else:
                result = ui.handle_menu_events(event)
                if result == 'start':
                    game_state = 'difficulty'
                    pygame.event.clear()
                elif result == 'exit':
                    running = False
                elif result == 'rule':
                    showing_menu_rules = True

        if showing_menu_rules:
            ui.draw_game_rule_popup()

        pygame.display.flip()

    # ──────────────── DIFFICULTY SELECTION ────────────────
    elif game_state == 'difficulty':
        ui.draw_difficulty_popup()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            selection = ui.handle_difficulty_selection(event)
            if selection:
                if selection == 'easy':
                    start_level = 1
                elif selection == 'normal':
                    start_level = 7
                elif selection == 'hard':
                    start_level = 13
                game_manager = GameManager(screen, start_level)
                game_state = 'playing'
                pygame.event.clear()
        pygame.display.flip()

    # ──────────────── PLAYING ────────────────
    elif game_state == 'playing':
        buttons = game_manager.update()  # returns menu_btn, rule_btn, close_btn (rule_btn no longer drawn)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Only handle menu button in gameplay now
            if buttons["menu_btn"] and ui.handle_top_button_click(event, buttons["menu_btn"]):
                game_state = 'menu'
                pygame.event.clear()
                continue

            if not game_manager.showing_rules:
                result = game_manager.handle_input(event)
                if result == 'game_over':
                    game_state = 'game_over'
                elif result == 'menu':
                    game_state = 'menu'

        pygame.display.flip()

    # ──────────────── GAME OVER ────────────────
    elif game_state == 'game_over':
        game_manager.draw_game_over()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 300 <= x <= 500 and 350 <= y <= 410:
                    game_state = 'menu'
                    pygame.event.clear()
        pygame.display.flip()

    clock.tick(FPS)

pygame.quit()