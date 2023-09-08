class Settings:

    def __init__(self):
        self.target_width = 25
        self.target_height = 150
        self.target_color = (255, 0, 0)
        self.target_speed_factor = 1.0

        self.screen_width = 1200
        self.screen_height = 800
        self.background_color = (100, 100, 230)
        self.ship_speed_factor = 1.5

        self.bullet_speed_factor = 3.0
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

        self.speedup_factor = 1.1

    def initialize_default_speed_settings(self):
        self.target_speed_factor = 1.0

    def increase_speed(self):
        self.target_speed_factor *= self.speedup_factor
