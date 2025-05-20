import pygame
from config import SCREEN_WIDTH

class UIManager:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.feedback_timer = 0
        self.feedback_message = ""

        heart = pygame.image.load("assets/icons/redheart.png").convert_alpha()
        self.heart_img = pygame.transform.scale(heart, (24, 24))

        close = pygame.image.load("assets/icons/red_x.png").convert_alpha()
        self.close_img = pygame.transform.scale(close, (20, 20))

    # ───────────────────────────────
    # Game HUD
    # ───────────────────────────────
    def render_score(self, score):
        text = self.font.render(f"Score: {score}", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

    def render_level(self, level):
        text = self.font.render(f"Level: {level}", True, (255, 255, 255))
        self.screen.blit(text, (10, 45))

    def render_lives(self, lives):
        label_font = pygame.font.Font(None, 28)
        anchor_x = SCREEN_WIDTH - 300
        anchor_y = 15

        label = label_font.render("Remaining Lives:", True, (255, 255, 255))
        self.screen.blit(label, (anchor_x, anchor_y))

        label_width = label.get_width()
        spacing_after_label = 30
        spacing_between_hearts = 30

        for i in range(lives):
            heart_x = anchor_x + label_width + spacing_after_label + i * spacing_between_hearts
            self.screen.blit(self.heart_img, (heart_x, anchor_y - 2))

    def render_feedback(self, message, duration=1500):
        self.feedback_message = message
        self.feedback_timer = pygame.time.get_ticks() + duration

    def update_feedback(self):
        if self.feedback_message:
            current_time = pygame.time.get_ticks()
            if current_time < self.feedback_timer:
                text = self.font.render(self.feedback_message, True, (255, 215, 0))
                text_rect = text.get_rect(center=(400, 550))
                self.screen.blit(text, text_rect)
            else:
                self.feedback_message = ""

    # ───────────────────────────────
    # Top Button (Main Menu only now)
    # ───────────────────────────────
    def draw_top_menu_button(self):
        rect = pygame.Rect(SCREEN_WIDTH - 150, 50, 130, 40)
        pygame.draw.rect(self.screen, (150, 150, 255), rect, border_radius=8)
        font = pygame.font.Font(None, 28)
        label = font.render("Main Menu", True, (0, 0, 0))
        self.screen.blit(label, label.get_rect(center=rect.center))
        return rect

    def handle_top_button_click(self, event, rect):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect.collidepoint(event.pos):
                return True
        return False

    # ───────────────────────────────
    # Main Menu UI
    # ───────────────────────────────
    def draw_menu(self):
        font_big = pygame.font.Font(None, 80)
        font_small = pygame.font.Font(None, 48)
        mouse_x, mouse_y = pygame.mouse.get_pos()

        title = font_big.render("Memory Maze", True, (255, 255, 100))
        title_shadow = font_big.render("Memory Maze", True, (0, 0, 0))
        self.screen.blit(title_shadow, title.get_rect(center=(402, 152)))
        self.screen.blit(title, title.get_rect(center=(400, 150)))

        buttons = [
            {"text": "Start Game", "rect": pygame.Rect(300, 250, 200, 60), "color": (100, 200, 100)},
            {"text": "Exit Game", "rect": pygame.Rect(300, 350, 200, 60), "color": (200, 100, 100)},
            {"text": "Game Rule", "rect": pygame.Rect(300, 450, 200, 60), "color": (255, 200, 150)}
        ]

        for btn in buttons:
            rect = btn["rect"]
            hover = rect.collidepoint(mouse_x, mouse_y)
            color = tuple(min(255, c + 30) if hover else c for c in btn["color"])
            pygame.draw.rect(self.screen, color, rect, border_radius=12)
            text = font_small.render(btn["text"], True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

        return [btn["rect"] for btn in buttons]

    def handle_menu_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if 300 <= x <= 500:
                if 250 <= y <= 310:
                    return 'start'
                elif 350 <= y <= 410:
                    return 'exit'
                elif 450 <= y <= 510:
                    return 'rule'
        return None

    # ───────────────────────────────
    # Game Rule Popup (shared)
    # ───────────────────────────────
    def draw_game_rule_popup(self):
        popup_rect = pygame.Rect(100, 100, 600, 300)
        pygame.draw.rect(self.screen, (255, 255, 255), popup_rect, border_radius=12)
        pygame.draw.rect(self.screen, (0, 0, 0), popup_rect, 3, border_radius=12)

        font = pygame.font.Font(None, 28)
        paragraph = (
            "At the start of each level, you’ll be shown the locations of various symbols for a few seconds. "
            "Once they disappear, you’ll need to navigate the maze using the arrow keys and select the correct "
            "symbol positions by pressing the spacebar. Each correct selection reveals a symbol permanently, "
            "but selecting an incorrect cell will cost you a life. You begin each level with three lives. "
            "The maze size and difficulty increase as you progress through the levels."
        )

        wrapped_lines = self.wrap_text(paragraph, font, max_width=popup_rect.width - 40)
        for i, line in enumerate(wrapped_lines):
            text_surface = font.render(line, True, (0, 0, 0))
            self.screen.blit(text_surface, (popup_rect.left + 20, popup_rect.top + 30 + i * 30))

        # Draw close button
        close_rect = pygame.Rect(popup_rect.right - 30, popup_rect.top + 10, 20, 20)
        self.screen.blit(self.close_img, close_rect)
        return close_rect

    def handle_close_button_click(self, event, close_rect):
        if event.type == pygame.MOUSEBUTTONDOWN and close_rect.collidepoint(event.pos):
            return True
        return False

    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "

        if current_line:
            lines.append(current_line.strip())

        return lines
    
    def draw_difficulty_popup(self):
        font = pygame.font.Font(None, 48)
        prompt = font.render("Select Difficulty", True, (255, 255, 255))
        self.screen.blit(prompt, prompt.get_rect(center=(400, 180)))

        options = [
            {"text": "Easy", "rect": pygame.Rect(300, 230, 200, 60), "color": (120, 200, 120)},
            {"text": "Normal", "rect": pygame.Rect(300, 310, 200, 60), "color": (220, 220, 120)},
            {"text": "Hard", "rect": pygame.Rect(300, 390, 200, 60), "color": (200, 120, 120)},
        ]

        mouse_x, mouse_y = pygame.mouse.get_pos()

        for opt in options:
            rect = opt["rect"]
            hover = rect.collidepoint(mouse_x, mouse_y)
            color = tuple(min(255, c + 30) if hover else c for c in opt["color"])
            pygame.draw.rect(self.screen, color, rect, border_radius=12)

            text = font.render(opt["text"], True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

    def handle_difficulty_selection(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if 300 <= x <= 500:
                if 230 <= y <= 290:
                    return 'easy'
                elif 310 <= y <= 370:
                    return 'normal'
                elif 390 <= y <= 450:
                    return 'hard'
        return None