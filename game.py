import pygame

from card import Card
from painting import Painting


class Game:

    def __init__(self):

        self.current_screen = "welcome"

        self.current_level = 1
        self.unlocked_levels = 1
        self.game_completed = False

        self.next_button = pygame.Rect(
            350,
            450,
            300,
            60
        )

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

        #back button
        self.back_button = pygame.Rect(20, 20, 120, 50)

    def initialize_cards(self):

        self.cards = []

        card_names = [
            1,1,
            2,2,
            3,3,
            4,4,
            5,5,
            6,6,
            7,7,
            8,8,
            9,9,
            10,10,
            11,11,
            12,12,
            13,13,
            14,14,
            15,15,
            16,16,

        ]


        start_x = 180

        start_y = 120

        card_width = 120

        card_height = 120

        gap = 20

        index = 0

        for row in range(4):

            for column in range(4):

                x = start_x + column * (card_width + gap)

                y = start_y + row * (card_height + gap)

                card = Card(card_names[index], x, y, card_width, card_height)

                self.cards.append(card)

                index += 1

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

                #welcome screen
                if self.current_screen == "welcome":

                    if self.start_button.collidepoint(mouse):
                        self.current_screen = "levels"

                #level screen
                elif self.current_screen == "levels":

                    if self.back_button.collidepoint(mouse):
                        self.current_screen = "welcome"

                    else:
                        for i, button in enumerate(self.level_buttons):
                            if button.collidepoint(mouse):
                                if i + 1 <= self.unlocked_levels:
                                    self.current_level = i + 1
                                    self.reset_game()
                                    self.current_screen = "game"

                #game screen
                elif self.current_screen == "game":

                    if self.back_button.collidepoint(mouse):
                        self.current_screen = "levels"

                    else:

                        self.select_card(mouse)

                elif self.current_screen == "complete":

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse = pygame.mouse.get_pos()

                    if self.next_button.collidepoint(mouse):
                        if self.current_level < 5:
                            self.current_level += 1
                            self.reset_game()
                            self.current_screen = "levels"

    def select_card(self, mouse):

        for card in self.cards:

            if card.is_clicked(mouse):

                if card.get_matched():

                    return

                if card.get_flipped():

                    return

                if len(self.selected_cards) == 2:

                    return

                card.flip()

                self.selected_cards.append(card)

                break

    def update(self):

        if len(self.selected_cards) == 2:
            self.check_match()


    def check_match(self):
        first = self.selected_cards[0]
        second = self.selected_cards[1]
        if first.get_name() == second.get_name():
            first.match()
            second.match()
            self.matches += 1
            self.score += 10
            self.painting.restore_part()

            if self.painting.is_completed():
                self.game_completed = True

                if self.current_level == self.unlocked_levels:

                    if self.unlocked_levels < 5:
                        self.unlocked_levels += 1

            self.current_screen = "complete"

        else:
            first.hide()
            second.hide()
        self.attempts += 1

        self.selected_cards.clear()


    

    
    

    def draw(self):

        self.screen.fill(self.background_color)

        if self.current_screen == "welcome":
            self.draw_welcome_screen()

        elif self.current_screen == "levels":
            self.draw_level_screen()

        elif self.current_screen == "game":
            self.draw_game_screen()

        elif self.current_screen == "complete":
            self.draw_complete_screen()

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

            if i + 1 <= self.unlocked_levels:
                color = (100,100,150)
                text = "Level " + str(i+1)
            else:
                color = (150,150,150)
                text = "Locked"

        pygame.draw.rect(
            self.screen,
            color,
            button,
            border_radius=10
        )

        label = button_font.render(
            text,
            True,
            (255,255,255)
        )

        rect = label.get_rect(
            center=button.center
        )

        self.screen.blit(label,rect)
        self.draw_back_button()


    def draw_back_button(self):

        pygame.draw.rect(
            self.screen,
            (120, 90, 60),
            self.back_button,
            border_radius=10
        )

        font = pygame.font.SysFont(None, 30)

        text = font.render(
            "Back",
            True,
            (255, 255, 255)
        )

        self.screen.blit(text, (50, 35))

    def draw_game_screen(self):

        title_font = pygame.font.SysFont(None,50)

        title = title_font.render(
            "Level 1",
            True,
            (50, 50, 50)
        )

        font = pygame.font.SysFont(

            None,

            30

        )

        score = font.render(

            "Score : " + str(self.score),

            True,

            (40,40,40)

        )

        attempts = font.render(

            "Attempts : " + str(self.attempts),

            True,

            (40,40,40)

        )

        matches = font.render(

            "Matches : " + str(self.matches),

            True,

            (40,40,40)

        )
        self.screen.blit(

            score,

            (40,80)

        )

        self.screen.blit(

            attempts,

            (40,120)

        )

        self.screen.blit(

            matches,

            (40,160)

        )
        progress = pygame.font.SysFont(

            None,

            30

        )

        text = progress.render(

            "Painting : "

            +

            str(

                self.painting.get_progress()

            )

            +

            "/16",

            True,

            (40,40,40)

        )

        self.screen.blit(

            text,

            (40,200)

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

                index += 1

        for card in self.cards:

            card.draw(self.screen)

        self.draw_back_button()


    def draw_complete_screen(self):

        title_font = pygame.font.SysFont(None, 60)

        title = title_font.render(

            "Congratulations!",
            True,
            (40,40,40)
        )

        self.screen.blit(title,(300,120))

        font = pygame.font.SysFont(None,35)

        message = font.render(
            "You completed the painting!",
            True,
            (60,60,60)
        )

        self.screen.blit(message,(300,200))

        pygame.draw.rect(

            self.screen,
            (90,120,80),
            self.next_button,
            border_radius=10
        )

        text = font.render(
            "Next Level",
            True,
            (255,255,255)
         )

        text_rect = text.get_rect(

            center=self.next_button.center

        )

        self.screen.blit(text,text_rect)