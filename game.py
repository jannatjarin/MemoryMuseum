import pygame

from card import Card
from painting import Painting


class Game:

    def __init__(self):

        pygame.init()

        self.width = 1000
        self.height = 700
        self.title = "Memory Museum"

        self.background_color = (230, 225, 215)

        self.screen = pygame.display.set_mode(
            (self.width, self.height)
        )

        pygame.display.set_caption(self.title)

        self.clock = pygame.time.Clock()
        self.fps = 60

        self.running = True

        self.cards = []
        self.selected_cards = []

        self.matches = 0
        self.attempts = 0
        self.score = 0

        self.painting = Painting()

        self.current_screen = "welcome"

        #welcome screen buttons
        self.start_button = pygame.Rect(350, 250, 300, 60)

        self.how_button = pygame.Rect(350, 330, 300, 60)

        self.score_button = pygame.Rect(350, 410, 300, 60)

        self.player_button = pygame.Rect(350, 490, 300, 60)

        #level buttons

        self.level_buttons = []

        for i in range(5):

            button = pygame.Rect(350, 180 + i * 90, 300, 60)

            self.level_buttons.append(button)

    def initialize_cards(self):

        self.cards = []

        card_names = [
            "A", "A",
            "B", "B",
            "C", "C",
            "D", "D",
            "E", "E",
            "F", "F",
            "G", "G",
            "H", "H"
        ]

        for name in card_names:
            card = Card(name)
            self.cards.append(card)

    def reset_game(self):

        self.selected_cards = []

        self.matches = 0
        self.attempts = 0
        self.score = 0

        self.painting.reset()

        self.initialize_cards()

    def start(self):
        self.initialize_cards()
        while self.running:
            self.handle_events()
            self.update()
            self.draw()

            pygame.display.flip()

            self.clock.tick(self.fps)

        pygame.quit()

    def handle_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()

                if self.current_screen == "welcome":
                    if self.start_button.collidepoint(mouse):
                        self.current_screen = "levels"

                elif self.current_screen == "levels":
                    for button in self.level_buttons:
                        if button.collidepoint(mouse):
                            self.current_screen = "game"

    def update(self):

        pass

    def draw(self):

        self.screen.fill(self.background_color)
        if self.current_screen == "welcome":
            self.draw_welcome_screen()

        elif self.current_screen == "levels":
            self.draw_level_screen()

        elif self.current_screen == "game":
            self.draw_game_screen()

    def draw_welcome_screen(self):
        #title

        title_font = pygame.font.SysFont(None, 72)

        title = title_font.render("Memory Museum", True,(60, 40, 20))

        self.screen.blit(title, (300, 90))

        #subtitle
        subtitle_font = pygame.font.SysFont(None,36)

        subtitle = subtitle_font.render(
            "Explore the world's greatest paintings",
            True,
            (90, 80, 70)
        )

        self.screen.blit(subtitle, (280, 160))

        button_font = pygame.font.SysFont(None,36)

        buttons = [

            (self.start_button, "Start Game"),

            (self.how_button, "How To Play"),

            (self.score_button, "Scoreboard"),

            (self.player_button, "Create Player")

        ]

        for button, text in buttons:

            pygame.draw.rect(
                self.screen,
                (120, 90, 60),
                button,
                border_radius=10
            )

            label = button_font.render(text,True,(255, 255, 255))

            label_rect = label.get_rect(
                center=button.center
            )

            self.screen.blit(label,label_rect)

    def draw_level_screen(self):

        title_font = pygame.font.SysFont(None,64)

        title = title_font.render("Select Level", True,(60, 40, 20))

        self.screen.blit(title, (340, 50))

        button_font = pygame.font.SysFont(None,36)

        for i, button in enumerate(self.level_buttons):

            pygame.draw.rect(
                self.screen,
                (100, 100, 150),
                button,
                border_radius=10
            )

            text = button_font.render(
                "Level " + str(i + 1),
                True,
                (255, 255, 255)
            )

            text_rect = text.get_rect(
                center=button.center
            )

            self.screen.blit(text,text_rect)

    def draw_game_screen(self):

        title_font = pygame.font.SysFont(None,50)

        title = title_font.render(
            "Level 1",
            True,
            (50, 50, 50)
        )

        self.screen.blit(title,(430, 20))

        start_x = 180
        start_y = 120

        card_width = 120
        card_height = 120

        gap = 20

        index = 0

        font = pygame.font.SysFont(None, 40)

        for row in range(4):

            for column in range(4):

                x = start_x + column * (card_width + gap)

                y = start_y + row * (card_height + gap)

                pygame.draw.rect(

                    self.screen,

                    (110, 90, 70),

                    (x, y, card_width, card_height),

                    border_radius=8

                )

                font = pygame.font.SysFont(None,40)

                text = font.render(
                    str(index + 1),
                    True,
                    (255, 255, 255)
                )
                
                self.screen.blit(text, (x + 50, y + 40))

                index += 1