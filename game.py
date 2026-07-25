import pygame
import random
import json
import numpy as np

from card import Card
from painting import Painting



class Game:

    def __init__(self):

        #screen/level state
        self.current_screen = 'welcome'
        self.current_level = 1
        self.painting = Painting()
        self.painting.load_level(self.current_level)
        self.unlocked_levels = 1

        #next level button
        self.next_button = pygame.Rect(350, 450,300, 60)

        pygame.init()

        #window setup
        self.width = 1000
        self.height = 700
        self.title = "Memory Museum"
        self.background_color = (230, 225, 215)

        self.screen = pygame.display.set_mode(
        (self.width, self.height)
        )

        #background images
        self.welcome_background = self.load_background("welcome_screen.jpg")
        self.levels_background = self.load_background("level_screen.jpg")
            
        pygame.display.set_caption(self.title)

        self.clock = pygame.time.Clock()
        self.fps = 60

        self.running = True

        #card matching state
        self.cards = []
        self.card_images = []
        self.selected_cards = []
        self.waiting = False

        self.attempts = 0

        self.wait_start = 0
        self.wait_time = 700

        #timer state
        self.start_time = 0
        self.elapsed_time = 0

        #load scores from file, handle missing/corrupted file
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

        self.completed_levels = set()


        #locked level click feedback
        self.lock_message_time = 0
        self.lock_message_duration = 1200

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

        #test button
        self.test_button = pygame.Rect(860, 640, 120, 40)

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
                self.card_images.append(piece)

    #8 pairs suffle
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

        #4x4 grid
        card_size = 120
        gap = 20
        grid_width = 4 * card_size + 3 * gap

        start_x = (self.width - grid_width) // 2
        start_y = 140

        index = 0

        for row in range(4):
            for column in range(4):
                self.cards[index].x = start_x + column * (card_size + gap)
                self.cards[index].y = start_y + row * (card_size + gap)
                index += 1

    #reset game
    def reset_game(self):

        self.selected_cards = []

        self.attempts = 0

        self.waiting = False

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

                        self.current_screen = "welcome"

                    else:

                        for i in range(len(self.level_buttons)):

                            button = self.level_buttons[i]

                            if button.collidepoint(mouse):

                                #locked level
                                if i + 1 > self.unlocked_levels:
                                    self.lock_message_time = pygame.time.get_ticks()
                                    break

                                self.current_level = i + 1

                                self.painting.load_level(self.current_level)

                                self.painting.load_image()

                                self.reset_game()

                                self.elapsed_time = 0

                                self.current_screen = "game"
                                break

                #game screen

                elif self.current_screen == "game":

                    if self.back_button.collidepoint(mouse):

                        self.current_screen = "levels"


                    #test button
                    # elif self.test_button.collidepoint(mouse):

                    #     self.test_complete_level()

                    else:

                        self.select_card(mouse)

                #scoreboard screen

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
    #flips card
        if self.waiting:
            return

        for card in self.cards:

            if card.is_clicked(mouse):

                if card.get_matched():

                    return

                if card.get_flipped():

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

        if first.get_name() == second.get_name():

            first.match()
            second.match()

            self.painting.restore_part()

            if self.painting.is_completed():


                self.completed_levels.add(self.current_level)

                level = str(self.current_level)

                self.new_record = False

                #updates best score

                best_attempts = self.scores[level]["attempts"]
                best_time = self.scores[level]["time"]

                if best_attempts is None or self.attempts < best_attempts:

                    self.scores[level]["attempts"] = self.attempts
                    self.new_record = True

                if best_time is None or self.elapsed_time < best_time:

                    self.scores[level]["time"] = self.elapsed_time
                    self.new_record = True

                self.save_scores()

                #unlock next level
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

        if self.current_screen == "welcome" and self.welcome_background is not None:
            self.screen.blit(self.welcome_background, (0, 0))

        elif self.current_screen == "levels" and self.levels_background is not None:
            self.screen.blit(self.levels_background, (0, 0))

        else:
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

        #title
        title_font = pygame.font.SysFont(None, 60)

        title = title_font.render(
            "Statistics",
            True,
            (40, 40, 40)
        )

        title_rect = title.get_rect(center=(self.width // 2, 55))
        self.screen.blit(title, title_rect)

        subtitle_font = pygame.font.SysFont(None, 26)

        subtitle = subtitle_font.render(
            "Your progress across all levels",
            True,
            (110, 100, 90)
        )

        subtitle_rect = subtitle.get_rect(center=(self.width // 2, 90))
        self.screen.blit(subtitle, subtitle_rect)

        if stats["levels_finished"] > 0:
            best_time_text = str(stats["best_time"]) + " s"
            best_attempts_text = str(stats["best_attempts"])
        else:
            best_time_text = "-"
            best_attempts_text = "-"

        stat_cards = [

            ("Levels Finished", str(len(self.completed_levels)) + " / 5"),
            ("Total Time Played", str(stats["total_time"]) + " s"),
            ("Total Attempts", str(stats["total_attempts"])),
            ("Best Time", best_time_text),
            ("Best Attempts", best_attempts_text),
            ("Average Time", str(stats["average_time"]) + " s"),
            ("Average Attempts", str(stats["average_attempts"])),
        ]

        columns = 2
        card_width = 440
        card_height = 100
        gap_x = 20
        gap_y = 20

        grid_width = columns * card_width + gap_x
        start_x = (self.width - grid_width) // 2
        start_y = 130

        label_font = pygame.font.SysFont(None, 26)
        value_font = pygame.font.SysFont(None, 42)

        for index in range(len(stat_cards)):

            label, value = stat_cards[index]

            row = index // columns
            column = index % columns

            card_x = start_x + column * (card_width + gap_x)
            card_y = start_y + row * (card_height + gap_y)

            card_rect = pygame.Rect(card_x, card_y, card_width, card_height)

            #card background
            pygame.draw.rect(
                self.screen,
                (250, 247, 240),
                card_rect,
                border_radius=12
            )

            #card border accent
            pygame.draw.rect(
                self.screen,
                (196, 148, 62),
                card_rect,
                width=2,
                border_radius=12
            )

            label_text = label_font.render(label, True, (120, 105, 90))
            label_rect = label_text.get_rect(
                center=(card_rect.centerx, card_rect.y + 28)
            )
            self.screen.blit(label_text, label_rect)

            value_text = value_font.render(value, True, (60, 40, 20))
            value_rect = value_text.get_rect(
                center=(card_rect.centerx, card_rect.y + 68)
            )
            self.screen.blit(value_text, value_rect)

        self.draw_back_button()


    def draw_welcome_screen(self):
        #title

        title_font_name = "Castellar"

        title_font = pygame.font.SysFont(title_font_name, 65)

        title = title_font.render("Memory Museum", True,(60, 40, 20))

        self.screen.blit(title, (180, 140))

        

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

        level_font_name = "Felix Titling"

        title_font = pygame.font.SysFont(level_font_name,55)

        title = title_font.render("Select Level", True,(255, 255, 255))

        self.screen.blit(title, (320, 65))

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

        time_since_click = pygame.time.get_ticks() - self.lock_message_time

        if time_since_click < self.lock_message_duration:

            message_font = pygame.font.SysFont(None, 60)

            message = message_font.render(
                "That level is locked!",
                True,
                (255, 255, 255)
            )

            message_rect = message.get_rect(
                center=(self.width // 2, 640)
            )

            self.screen.blit(message, message_rect)
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

        title_rect = title.get_rect(center=(self.width // 2, 45))
        self.screen.blit(title, title_rect)

        #show the completed painting

        painting_image = pygame.transform.scale(
            self.painting.image,
            (240, 240)
        )

        image_rect = painting_image.get_rect(
            center=(self.width // 2, 200)
        )

        self.screen.blit(painting_image, image_rect)

        font = pygame.font.SysFont(None, 35)

        message = font.render(
            "You completed the painting!",
            True,
            (60, 60, 60)
        )

        message_rect = message.get_rect(center=(self.width // 2, 345))
        self.screen.blit(message, message_rect)

        time_taken = font.render(
            "Time : " + str(self.elapsed_time) + " seconds",
            True,
            (60, 60, 60)
        )

        time_rect = time_taken.get_rect(center=(self.width // 2, 380))
        self.screen.blit(time_taken, time_rect)


        attempts_taken = font.render(
            "Attempts : " + str(self.attempts),
            True,
            (60, 60, 60)
        )

        attempts_rect = attempts_taken.get_rect(center=(self.width // 2, 420))
        self.screen.blit(attempts_taken, attempts_rect)

        if self.new_record:

            record_font = pygame.font.SysFont(None, 45)

            record_text = record_font.render(
                "NEW RECORD!",
                True,
                (0, 128, 0)
            )

            record_rect = record_text.get_rect(center=(self.width // 2, 600))
            self.screen.blit(record_text, record_rect)

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

        title_rect = title.get_rect(center=(self.width // 2, 55))
        self.screen.blit(title, title_rect)

        #header bar
        header_rect = pygame.Rect(180, 130, 640, 50)

        pygame.draw.rect(
            self.screen,
            (120, 90, 60),
            header_rect,
            border_radius=10
        )

        header_font = pygame.font.SysFont(None, 30)

        level_header = header_font.render("Level", True, (255, 255, 255))
        self.screen.blit(level_header, (270, 145))

        attempts_header = header_font.render("Attempts", True, (255, 255, 255))
        self.screen.blit(attempts_header, (460, 145))

        time_header = header_font.render("Time", True, (255, 255, 255))
        self.screen.blit(time_header, (720, 145))

        #rows
        font = pygame.font.SysFont(None, 32)

        y = 180

        for i in range(1, 6):

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

            row_rect = pygame.Rect(180, y, 640, 60)

            if i % 2 == 0:
                row_color = (250, 247, 240)
            else:
                row_color = (240, 235, 224)

            pygame.draw.rect(self.screen, row_color, row_rect)

            level_text = font.render(str(i), True, (60, 40, 20))
            self.screen.blit(level_text, (280, y + 15))

            attempt_render = font.render(attempt_text, True, (60, 40, 20))
            self.screen.blit(attempt_render, (460, y + 15))

            time_render = font.render(time_text, True, (60, 40, 20))
            self.screen.blit(time_render, (720, y + 15))

            y += 60

        #border around whole table
        table_rect = pygame.Rect(180, 130, 640, 350)

        pygame.draw.rect(
            self.screen,
            (196, 148, 62),
            table_rect,
            width=2,
            border_radius=8
        )

        self.draw_back_button()


    def draw_how_screen(self):

        title_font = pygame.font.SysFont(None, 60)

        title = title_font.render(
            "How To Play",
            True,
            (40, 40, 40)
        )

        title_rect = title.get_rect(center=(self.width // 2, 55))
        self.screen.blit(title, title_rect)

        instructions = [
            "1. Choose any unlocked level.",
            "2. Click two cards to reveal them.",
            "3. Match both pieces of the painting.",
            "4. Match all 8 pairs to finish the level.",
            "5. Fewer attempts = Better score.",
            "6. Faster time = Better record.",
            "7. Beat your best score to get NEW RECORD!"
        ]

        font = pygame.font.SysFont(None, 30)

        y = 130

        for line in instructions:

            row_rect = pygame.Rect(150, y, 700, 55)

            pygame.draw.rect(
                self.screen,
                (250, 247, 240),
                row_rect,
                border_radius=10
            )

            text = font.render(line, True, (60, 40, 20))
            self.screen.blit(text, (175, y + 15))

            y += 65

        self.draw_back_button()

    def draw_game_screen(self):

        for card in self.cards:
            card.draw(self.screen)

        #level title, centered at the top
        title_font = pygame.font.SysFont(None, 48)

        title_text = title_font.render(
            "Level " + str(self.current_level) + ": " + self.painting.get_name(),
            True,
            (40, 40, 40)
        )

        title_rect = title_text.get_rect(
            center=(self.width // 2, 45)
        )

        self.screen.blit(title_text, title_rect)

        #attempts and timer, top right corner
        font = pygame.font.SysFont(None, 32)

        attempts_text = font.render(
            "Attempts: " + str(self.attempts),
            True,
            (40, 40, 40)
        )

        attempts_rect = attempts_text.get_rect(
            topright=(self.width - 20, 20)
        )

        self.screen.blit(attempts_text, attempts_rect)

        time_text = font.render(
            "Time: " + str(self.elapsed_time) + "s",
            True,
            (40, 40, 40)
        )

        time_rect = time_text.get_rect(
            topright=(self.width - 20, 55)
        )

        self.screen.blit(time_text, time_rect)

        # #test button
        # pygame.draw.rect(
        #     self.screen,S
        #     (180, 40, 40),
        #     self.test_button,
        #     border_radius=8
        # )

        # test_font = pygame.font.SysFont(None, 26)

        # test_label = test_font.render(
        #     "TEST",
        #     True,
        #     (255, 255, 255)
        # )

        # test_rect = test_label.get_rect(
        #     center=self.test_button.center
        # )

        # self.screen.blit(test_label, test_rect)

        self.draw_back_button()

    def load_background(self, filename):

        try:
            image = pygame.image.load("assets/images/" + filename)
            image = pygame.transform.scale(image, (self.width, self.height))
            return image

        except pygame.error:
            print("Could not load", filename)
            return None


    #test
    def test_complete_level(self):

        self.attempts = 100
        self.elapsed_time = 150
        self.new_record = False

        self.completed_levels.add(self.current_level)

        if self.current_level == self.unlocked_levels:
            if self.unlocked_levels < 5:
                self.unlocked_levels += 1

        self.current_screen = "complete"