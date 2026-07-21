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
        
        def initialize_cards(self):
           self.cards = []

        card_names = [
            "A","A",
            "B","B",
            "C","C",
            "D","D",
            "E","E",
            "F","F",
            "G","G",
            "H","H"
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
 