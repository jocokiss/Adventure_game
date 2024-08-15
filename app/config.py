from dotenv import dotenv_values

from app.utilities import ArgParser


class Config:
    def __init__(self):
        self.args = ArgParser().run()
        self.screen_width = int(self.args.screen_width)
        self.screen_height = int(self.args.screen_height)
        self.zoom_factor = int(self.args.zoom_factor)
        self.tile_size = int(self.args.tile_size) * self.zoom_factor
        self.map_location = self.args.map_location
        self.movement_speed = int(self.args.movement_speed)
