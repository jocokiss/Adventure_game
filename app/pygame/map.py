"""Module that contains the Map class."""


class Map:
    def __init__(self, config):
        self.config = config
        self.npcs = []

    def add_npc(self, npc):
        """Add an NPC to the map."""
        self.npcs.append(npc)

    def update_npcs(self):
        """Update all NPCs on the map."""
        for npc in self.npcs:
            npc.update_movement()
            npc.update()

    def draw_npcs(self):
        """Draw all NPCs on the screen."""
        for npc in self.npcs:
            npc.draw()

    def __draw_tiles(self, layers: set):

        x_pos, y_pos = self.config.calculate_positions()

        for layer in layers:
            for y in range(y_pos[0], y_pos[1]):
                for x in range(x_pos[0], x_pos[1]):
                    gid = layer.data[y][x]
                    if gid:
                        tile = self.config.get_animated_tile(gid, self.config.dt)
                        if tile:
                            # Calculate where to draw the tile on the screen
                            blit_x = (x - x_pos[0]) * self.config.tile_size
                            blit_y = (y - y_pos[0]) * self.config.tile_size
                            self.config.screen.blit(tile, (blit_x, blit_y))

    def render_background(self):
        self.__draw_tiles(self.config.background_layers)

    def render_foreground(self):
        self.__draw_tiles(self.config.foreground_layers)
