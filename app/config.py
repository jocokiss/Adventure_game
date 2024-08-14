from dotenv import dotenv_values

from app.utilities import ArgParser


class Config:
    def __init__(self):
        self.args = ArgParser().run()
        self.screen_width = self.args.screen_width
        self.screen_height = self.args.screen_height
        self.tile_size = self.args.tile_size
        self.map_location = self.args.map_location
        self.movement_speed = self.args.movement_speed
