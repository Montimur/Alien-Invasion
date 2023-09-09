from game.settings import Settings


class GameStats:

    def __init__(self, settings: Settings):
        self.settings = settings
        self.ships_left = self.settings.ship_limit
        self.game_active = False
        self.score = 0
        self.high_score = 0

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
