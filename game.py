import pygame

from card import Card
from painting import Painting


class Game:

    def __init__(self):
        pygame.init()

        #basic screen
        self.width=1000
        self.height=700
        self.title= "Memory Museum"

        self.background_color =(230, 225, 215)

        self.screen= pygame.display.set_mode(
            (self.width, self.height)
        )

        pygame.display.set_caption(self.title)

        self.clock = pygame.time.Clock()
        self.fps=60

        self.running=True

        self.cards = []
        self.selected_cards = []

        self.matches =0
        self.attempts= 0
        self.score =0

        self.painting = Painting()

        self.current_screen = "welcome"

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

    def update(self):
        pass

    def draw(self):
        self.screen.fill(self.background_color)
        if self.current_screen == "welcome":
            self.draw_welcome_screen()

    def draw_welcome_screen(self):

        #title
        title_font = pygame.font.SysFont(
            None,
            72
        )

        title = title_font.render(
            "Memory Museum",
            True,
            (60, 40, 20)
        )

        title_rect = title.get_rect(
            center=(
                self.width // 2,
                120
            )
        )

        self.screen.blit(
            title,
            title_rect
        )

        #subtitle
        subtitle_font = pygame.font.SysFont(
            None,
            36
        )

        subtitle = subtitle_font.render(
            "Explore the world's greatest paintings",
            True,
            (90, 80, 70)
        )

        subtitle_rect = subtitle.get_rect(
            center=(
                self.width // 2,
                180
            )
        )

        self.screen.blit(
            subtitle,
            subtitle_rect
        )