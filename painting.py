import pygame


LEVELS = {
 
    1: ("Starry Night", "starry_night.jpg"),
    2: ("Mona Lisa", "mona_lisa.jpg"),
    3: ("The Scream", "the_scream.jpg"),
    4: ("Girl with a Pearl Earring", "girl_with_pearl.jpg"),
    5: ("The Weeping Woman", "the_weeping_woman.jpg"),
 
}

class Painting:

    def __init__(self):

        self.current_level = 1

        self.total_parts = 8
        self.restored_parts = 0

        self.painting_name = "Starry Night"

        self.image_file = "starry_night.jpg"

        self.image = None

    def load_level(self, level):

        self.current_level = level

        self.restored_parts = 0

        if level in LEVELS:
 
            name, image_file = LEVELS[level]
 
            self.painting_name = name
            self.image_file = image_file

    def restore_part(self):

        if self.restored_parts < self.total_parts:

            self.restored_parts += 1

    def is_completed(self):

        return self.restored_parts == self.total_parts

    def reset(self):

        self.restored_parts = 0

    def get_name(self):

        return self.painting_name

    def load_image(self):

        image_path = "assets/images/" + self.image_file

        try:

            self.image = pygame.image.load(image_path)

        except pygame.error:

            print("Could not load image:", image_path)

            self.image = pygame.Surface((400, 200))

            self.image.fill((200, 0, 0))