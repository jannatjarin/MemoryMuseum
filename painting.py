import pygame

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

        if level == 1:

            self.painting_name = "Starry Night"
            self.image_file = "starry_night.jpg"

        elif level == 2:

            self.painting_name = "Mona Lisa"
            self.image_file = "mona_lisa.jpg"

        elif level == 3:

            self.painting_name = "The Scream"
            self.image_file = "the_scream.jpg"

        elif level == 4:

            self.painting_name = "Girl with a Pearl Earring"
            self.image_file = "girl_with_pearl.jpg"

        elif level == 5:

            self.painting_name = "The Weeping Memory"
            self.image_file = "the_weeping_woman.jpg"

    def restore_part(self):

        if self.restored_parts < self.total_parts:

            self.restored_parts += 1

    def get_progress(self):

        return self.restored_parts

    def is_completed(self):

        return self.restored_parts == self.total_parts

    def reset(self):

        self.restored_parts = 0

    def get_name(self):

        return self.painting_name

    def get_image_file(self):

        return self.image_file

    def get_level(self):

        return self.current_level

    def load_image(self):

        image_path = "assets/images/" + self.image_file

        self.image = pygame.image.load(image_path)