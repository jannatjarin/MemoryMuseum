import pygame
 
 
class Card:
 
    def __init__(self, card_name, x, y, width, height):
 
        self.card_name = card_name
 
        self.x = x
        self.y = y
 
        self.width = width
        self.height = height
 
        self.is_flipped = False
        self.is_matched = False
 
    def flip(self):
 
        self.is_flipped = True
 
    def hide(self):
 
        self.is_flipped = False
 
    def match(self):
 
        self.is_matched = True
 
    def get_name(self):
 
        return self.card_name
 
    def get_flipped(self):
 
        return self.is_flipped
 
    def get_matched(self):
 
        return self.is_matched
 
    def is_clicked(self, mouse):
 
        mouse_x = mouse[0]
 
        mouse_y = mouse[1]
 
        if (
 
            self.x <= mouse_x <= self.x + self.width
 
            and
 
            self.y <= mouse_y <= self.y + self.height
 
        ):
 
            return True
 
        return False
 
    def draw(self, screen):
 
        if self.is_flipped:
 
            color = (220, 220, 220)
 
        else:
 
            color = (110, 90, 70)
 
        pygame.draw.rect(
 
            screen,
 
            color,
 
            (
 
                self.x,
 
                self.y,
 
                self.width,
 
                self.height
 
            ),
 
            border_radius=8
 
        )
 
        pygame.draw.rect(
 
            screen,
 
            (0, 0, 0),
 
            (
 
                self.x,
 
                self.y,
 
                self.width,
 
                self.height
 
            ),
 
            2,
 
            border_radius=8
 
        )
 
        if self.is_flipped:
 
            font = pygame.font.SysFont(None, 40)
 
            text = font.render(
 
                self.card_name,
 
                True,
 
                (0, 0, 0)
 
            )
 
            text_rect = text.get_rect(
 
                center=(
 
                    self.x + self.width // 2,
 
                    self.y + self.height // 2
 
                )
 
            )
 
            screen.blit(text, text_rect)