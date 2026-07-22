class Card:
    def __init__(self, card_name):
     self.card_name = card_name
     self.is_flipped = False
     self.is_matched = False

     def flip(self):
      self.is_flipped = True
    def hide(self):
     self.is_flipped = False
     def match(self):
      self.is_matched = True
      
      def get_name(self):
       return self.card_name
      def get_flipped(self):
       return self.is_flipped
    def get_matched(self):
     return self.is_matched
 