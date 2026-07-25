import pygame
import random
import json
import numpy as np

from card import Card
from painting import Painting



class Game:

    def __init__(self):

        self.current_screen = "welcome"
        self.current_level = 1
        self.painting = Painting()
        self.painting.load_level(self.current_level)

        self.painting.load_image()

        self.unlocked_levels = 1
        self.game_completed = False

        self.completed_levels = set()

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
        self.card_images = []
        self.selected_cards = []
        self.waiting = False

        self.matches = 0
        self.attempts = 0
        self.score = 0

        self.wait_start = 0

        self.wait_time = 700

        self.start_time = 0

        self.elapsed_time = 0

        try:

            with open("scores.json", "r") as file:

                self.scores = json.load(file)

        except (FileNotFoundError, ValueError):
                print("scores.json missing or corrupted. Creating a new one.")
                self.scores = {
                    "1": {"attempts": None, "time": None},
                    "2": {"attempts": None, "time": None},
                    "3": {"attempts": None, "time": None},
                    "4": {"attempts": None, "time": None},
                    "5": {"attempts": None, "time": None},
                }
                self.save_scores()


        self.new_record = False

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

    def create_card_images(self):

        self.card_images = []

        image = self.painting.image

        image_width = image.get_width()
        image_height = image.get_height()

        piece_width = image_width // 4
        piece_height = image_height // 2

        for row in range(2):

            for column in range(4):

                x = column * piece_width
                y = row * piece_height

                piece = image.subsurface(
                    (x, y, piece_width, piece_height)
                )
                piece = pygame.transform.scale(
                    piece,
                    (120, 120)
                )

                self.card_images.append(piece)

        duplicate_images = []

        for piece in self.card_images:

            duplicate_images.append(piece)
            duplicate_images.append(piece)

        self.card_images = duplicate_images

    def initialize_cards(self):
        self.cards = []
        self.create_card_images()

        card_names = [1,1, 2,2, 3,3, 4,4, 5,5, 6,6, 7,7, 8,8]

        for index in range(16):
            card = Card(card_names[index])
            card.set_image(self.card_images[index])
            card.width = 120
            card.height = 120
            self.cards.append(card)

        random.shuffle(self.cards)

        start_x = 180
        start_y = 120
        gap = 20
        index = 0

        for row in range(4):
            for column in range(4):
                self.cards[index].x = start_x + column * (120 + gap)
                self.cards[index].y = start_y + row * (120 + gap)
                index += 1

    def reset_game(self):

        self.selected_cards = []

        self.matches = 0
        self.attempts = 0
        self.score = 0

        self.painting.reset()

        self.initialize_cards()
        self.start_time = pygame.time.get_ticks()
        self.new_record = False


    def start(self):

        self.painting.load_image()
        self.initialize_cards()
        self.start_time = pygame.time.get_ticks()
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

                #welcom screen

                if self.current_screen == "welcome":

                    if self.start_button.collidepoint(mouse):

                        self.current_screen = "levels"

                    elif self.score_button.collidepoint(mouse):

                        self.current_screen = "scoreboard"

                    elif self.how_button.collidepoint(mouse):

                        self.current_screen = "how"

                    elif self.player_button.collidepoint(mouse):

                        self.current_screen = "statistics"

                #level select screen

                elif self.current_screen == "levels":

                    if self.back_button.collidepoint(mouse):

                        print("Level clicked")

                        self.current_screen = "welcome"

                    else:

                        for i in range(len(self.level_buttons)):

                            button = self.level_buttons[i]

                            if button.collidepoint(mouse):

                                #locked level
                                if i + 1 > self.unlocked_levels:
                                    return

                                self.current_level = i + 1

                                self.painting.load_level(self.current_level)

                                self.painting.load_image()

                                self.initialize_cards()

                                self.start_time = pygame.time.get_ticks()

                                self.elapsed_time = 0

                                self.current_screen = "game"

                #game scrren

                elif self.current_screen == "game":

                    if self.back_button.collidepoint(mouse):

                        self.current_screen = "levels"

                    else:

                        self.select_card(mouse)

                #scrreboard screen

                elif self.current_screen == "scoreboard":

                    if self.back_button.collidepoint(mouse):

                        self.current_screen = "welcome"

                #how to play scrren

                elif self.current_screen == "how":

                    if self.back_button.collidepoint(mouse):

                        self.current_screen = "welcome"


                elif self.current_screen == "statistics":

                    if self.back_button.collidepoint(mouse):

                        self.current_screen = "welcome"

                #level complete screen

                elif self.current_screen == "complete":

                    if self.next_button.collidepoint(mouse):

                        if self.current_level < 5:

                            self.current_level += 1

                        self.reset_game()

                        self.elapsed_time = 0

                        self.current_screen = "levels"
                            

    def select_card(self, mouse):

        if self.waiting:
            return

        for card in self.cards:

            if card.is_clicked(mouse):

                if card.get_matched():

                    return

                if card.get_flipped():

                    return

                if len(self.selected_cards) == 2:

                    self.waiting = True

                    self.wait_start = pygame.time.get_ticks()

                    return

                card.flip()

                self.selected_cards.append(card)

                if len(self.selected_cards) == 2:

                    self.waiting = True

                    self.wait_start = pygame.time.get_ticks()

                break

    def update(self):

        if self.current_screen == "game":

            self.elapsed_time = (
                pygame.time.get_ticks() - self.start_time
            ) // 1000

        if self.waiting:

            current_time = pygame.time.get_ticks()

            if current_time - self.wait_start >= self.wait_time:

                self.check_match()


    def check_match(self):

        first = self.selected_cards[0]
        second = self.selected_cards[1]

        print("Checking", first.get_name(), second.get_name())

        if first.get_name() == second.get_name():

            first.match()
            second.match()

            self.matches += 1
            self.score += 10

            self.painting.restore_part()

            if self.painting.is_completed():

                self.game_completed = True

                self.completed_levels.add(self.current_level)

                print("Completed levels so far:", self.completed_levels)

                level = str(self.current_level)

                self.new_record = False

                best_attempts = self.scores[level]["attempts"]
                best_time = self.scores[level]["time"]

                if best_attempts is None or self.attempts < best_attempts:

                    self.scores[level]["attempts"] = self.attempts
                    self.new_record = True

                if best_time is None or self.elapsed_time < best_time:

                    self.scores[level]["time"] = self.elapsed_time
                    self.new_record = True

                self.save_scores()

                if self.current_level == self.unlocked_levels:

                    if self.unlocked_levels < 5:
                        self.unlocked_levels += 1

                self.current_screen = "complete"

        else:

            first.hide()
            second.hide()

        self.attempts += 1

        self.selected_cards = []

        self.waiting = False


    def save_scores(self):

        try:

            with open("scores.json", "w") as file:

                json.dump(
                    self.scores,
                    file,
                    indent=4
                )

        except OSError:

            print("Could not save scores. Check file permissions.")


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

        elif self.current_screen == "scoreboard":
            self.draw_scoreboard_screen()

        elif self.current_screen == "how":
            self.draw_how_screen()

        elif self.current_screen == "statistics":
            self.draw_statistics_screen()


    def calculate_statistics(self):

        times = []
        attempts = []

        for level in self.scores:

            data = self.scores[level]

            if data["time"] is not None:

                times.append(data["time"])

            if data["attempts"] is not None:

                attempts.append(data["attempts"])

        levels_finished = len(times)

        if levels_finished > 0:

            total_time = int(np.sum(times))
            average_time = float(np.mean(times))
            average_time = int(average_time * 10) / 10
            best_time = int(np.min(times))

            total_attempts = int(np.sum(attempts))
            average_attempts = float(np.mean(attempts))
            average_attempts = int(average_attempts * 10) / 10
            best_attempts = int(np.min(attempts))

        else:

            total_time = 0
            average_time = 0
            best_time = None

            total_attempts = 0
            average_attempts = 0
            best_attempts = None

        stats = {

            "levels_finished": levels_finished,
            "total_time": total_time,
            "average_time": average_time,
            "best_time": best_time,
            "total_attempts": total_attempts,
            "average_attempts": average_attempts,
            "best_attempts": best_attempts,

        }

        return stats


    def draw_statistics_screen(self):

        stats = self.calculate_statistics()

        title_font = pygame.font.SysFont(None, 60)

        title = title_font.render(
            "Statistics",
            True,
            (40, 40, 40)
        )

        self.screen.blit(title, (380, 50))

        font = pygame.font.SysFont(None, 34)

        if stats["levels_finished"] > 0:

            best_time_text = str(stats["best_time"]) + " s"
            best_attempts_text = str(stats["best_attempts"])

        else:

            best_time_text = "-"
            best_attempts_text = "-"

        lines = [

            "Levels completed: " + str(stats["levels_finished"]) + " / 5",

            "Unique levels finished: " + str(len(self.completed_levels)),

            "Total time played: " + str(stats["total_time"]) + " s",

            "Average time: " + str(stats["average_time"]) + " s",

            "Best time: " + best_time_text,

            "Total attempts: " + str(stats["total_attempts"]),

            "Average attempts: " + str(stats["average_attempts"]),

            "Best attempts: " + best_attempts_text,

        ]

        y = 160

        for line in lines:

            text = font.render(line, True, (60, 60, 60))

            self.screen.blit(text, (220, y))

            y += 50

        self.draw_back_button()


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

            (self.score_button, "Best score"),

            (self.player_button, "Statistics")

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

        for i in range(len(self.level_buttons)):

            button = self.level_buttons[i]

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

    def draw_complete_screen(self):

        title_font = pygame.font.SysFont(None, 60)

        title = title_font.render(
            "Congratulations!",
            True,
            (40, 40, 40)
        )

        self.screen.blit(title, (300, 120))

        font = pygame.font.SysFont(None, 35)

        message = font.render(
            "You completed the painting!",
            True,
            (60, 60, 60)
        )

        self.screen.blit(message, (300, 200))

        time_taken = font.render(
            "Time : " + str(self.elapsed_time) + " seconds",
            True,
            (60, 60, 60)
        )

        self.screen.blit(
            time_taken,
            (360, 250)
        )

        if self.new_record:

            record_font = pygame.font.SysFont(None, 45)

            record_text = record_font.render(
                "NEW RECORD!",
                True,
                (200, 50, 50)
            )

            self.screen.blit(
                record_text,
                (365, 300)
            )

        pygame.draw.rect(
            self.screen,
            (90, 120, 80),
            self.next_button,
            border_radius=10
        )

        text = font.render(
            "Next Level",
            True,
            (255, 255, 255)
        )

        text_rect = text.get_rect(
            center=self.next_button.center
        )

        self.screen.blit(text, text_rect)


    def draw_scoreboard_screen(self):

        title_font = pygame.font.SysFont(None, 60)

        title = title_font.render(
            "Best Scores",
            True,
            (40, 40, 40)
        )

        self.screen.blit(title, (360, 50))

        font = pygame.font.SysFont(None, 35)

        level = font.render(
            "Level",
            True,
            (40,40,40)
        )

        attempts = font.render(
            "Attempts",
            True,
            (40,40,40)
        )

        time = font.render(
            "Time",
            True,
            (40,40,40)
        )

        self.screen.blit(level, (180,150))
        self.screen.blit(attempts, (420,150))
        self.screen.blit(time, (700,150))

        y = 220

        for i in range(1,6):

            level_key = str(i)

            if level_key in self.scores:

                data = self.scores[level_key]

            else:

                data = {"attempts": None, "time": None}


            if data["attempts"] is None:

                attempt_text = "-"

            else:

                attempt_text = str(data["attempts"])

            if data["time"] is None:

                time_text = "-"

            else:

                time_text = str(data["time"]) + " s"

            level_text = font.render(

                str(i),

                True,

                (40,40,40)

            )

            attempt_render = font.render(

                attempt_text,

                True,

                (40,40,40)

            )

            time_render = font.render(

                time_text,

                True,

                (40,40,40)

            )

            self.screen.blit(level_text, (200,y))
            self.screen.blit(attempt_render, (450,y))
            self.screen.blit(time_render, (710,y))

            y += 70

        self.draw_back_button()


    def draw_how_screen(self):

        title_font = pygame.font.SysFont(None, 60)

        title = title_font.render(
            "How To Play",
            True,
            (40, 40, 40)
        )

        self.screen.blit(title, (340, 50))

        font = pygame.font.SysFont(None, 32)

        instructions = [

            "1. Choose any unlocked level.",

            "2. Click two cards to reveal them.",

            "3. Match both pieces of the painting.",

            "4. Match all 8 pairs to finish the level.",

            "5. Fewer attempts = Better score.",

            "6. Faster time = Better record.",

            "7. Beat your best score to get NEW RECORD!"

        ]

        y = 150

        for line in instructions:

            text = font.render(
                line,
                True,
                (50, 50, 50)
            )

            self.screen.blit(
                text,
                (120, y)
            )

            y += 55

        self.draw_back_button()

    def draw_game_screen(self):

        for card in self.cards:

            card.draw(self.screen)

        font = pygame.font.SysFont(None, 32)

        level_text = font.render(
            "Level " + str(self.current_level),
            True,
            (40, 40, 40)
        )
        self.screen.blit(level_text, (20, 90))

        attempts_text = font.render(
            "Attempts: " + str(self.attempts),
            True,
            (40, 40, 40)
        )
        self.screen.blit(attempts_text, (740, 20))

        time_text = font.render(
            "Time: " + str(self.elapsed_time) + "s",
            True,
            (40, 40, 40)
        )
        self.screen.blit(time_text, (740, 60))

        self.draw_back_button()