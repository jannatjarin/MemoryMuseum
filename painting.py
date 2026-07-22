class Painting:

    def __init__(self):
        self.total_parts = 16
        self.restored_parts = 0

    def restore_part(self):
        if self.restored_parts < self.total_parts:
            self.restored_parts +=1
    def get_percentage(self):

        return (

            self.restored_parts

            /

            self.total_parts

        ) * 100

    def get_progress(self):
        return self.restored_parts

    def is_completed(self):
        return self.restored_parts == self.total_parts

    def reset(self):
        self.restored_parts= 0