import pygame
 
 
class Card:

    def __init__(self, card_name):

        self.card_name = card_name

        self.image = None

        self.back_color = (110, 90, 70)

        self.front_color = (240, 235, 220)

        self.is_flipped = False

        self.is_matched = False

        self.x = 0
        self.y = 0

        self.width = 120
        self.height = 120
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
    def set_image(self, image):
            self.image = image




    
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

        rectangle = pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

        if self.is_flipped or self.is_matched:

            if self.image is not None:

                screen.blit(
                    self.image,
                    rectangle
                )

            else:

                pygame.draw.rect(
                    screen,
                    self.front_color,
                    rectangle,
                    border_radius=8
                )

                font = pygame.font.SysFont(None, 40)

                text = font.render(
                    str(self.card_name),
                    True,
                    (50,50,50)
                )

                text_rect = text.get_rect(
                    center=rectangle.center
                )

                screen.blit(
                    text,
                    text_rect
                )

        else:

            pygame.draw.rect(
                screen,
                self.back_color,
                rectangle,
                border_radius=8
            )