class Painting:

    def __init__(self):

        self.level = 1

        self.painting_name = ""

        self.folder_name = ""

        self.total_parts = 16

        self.restored_parts = 0

        self.load_level(1)


    def load_level(self, level):

        self.level = level

        if level == 1:

            self.painting_name = "Starry Night"

            self.folder_name = "starry_night"

        elif level == 2:

            self.painting_name = "Mona Lisa"

            self.folder_name = "mona_lisa"

        elif level == 3:

            self.painting_name = "The Scream"

            self.folder_name = "the_scream"

        elif level == 4:

            self.painting_name = "Girl With A Pearl Earring"

            self.folder_name = "girl_with_pearl"

        elif level == 5:

            self.painting_name = "The Persistence Of Memory"

            self.folder_name = "persistence_memory"

        self.reset()


    def restore_part(self):

        if self.restored_parts < self.total_parts:

            self.restored_parts += 1


    def get_progress(self):

        return self.restored_parts


    def get_percentage(self):

        return int(
            (self.restored_parts / self.total_parts) * 100
        )


    def get_name(self):

        return self.painting_name


    def get_folder(self):

        return self.folder_name


    def is_completed(self):

        return self.restored_parts == self.total_parts


    def reset(self):

        self.restored_parts = 0