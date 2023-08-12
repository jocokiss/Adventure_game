from app.classes.player import Player

class Rouge(Player):
    def __init__(self):
        super().__init__()
        self.combo_points = {'count': 0}

    def add_combo_points(self, points_to_add):
        self.combo_points['count'] += points_to_add
        if self.combo_points['count'] >= 5:
            self.combo_points['count'] = 5

    def spend_combo_points(self, points_to_spend):
        pass
