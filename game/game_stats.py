from game.settings import Settings


class GameStats:

    def __init__(self, settings: Settings):
        self.settings = settings
        self.ships_left = self.settings.ship_limit
        self.game_active = True

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
