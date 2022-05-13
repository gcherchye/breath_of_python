"""Level management class"""
from __future__ import absolute_import

import pygame


from .config import config
from .player import Player
from .tile import Tile



class Level:
    """Level management class"""

    def __init__(self) -> None:
        # Get the game display surface
        self.display_surface = pygame.display.get_surface()

        # Sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # Config
        self.config = config

        # Vars
        self._create_map()

    def _create_map(self):
        for row_index, row in enumerate(config.world_map):
            for col_index, col in enumerate(row):
                x_pos = col_index * config.tilesize
                y_pos = row_index * config.tilesize

                if col == 'x':
                    Tile((x_pos, y_pos), [self.visible_sprites, self.obstacle_sprites])
                if col == 'p':
                    self.player = Player(
                        (x_pos, y_pos),
                        [self.visible_sprites],
                        self.obstacle_sprites
                    )

    def run(self) -> None:
        """Update and draw the game"""
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group):
    """docstring"""

    def __init__(self) -> None:
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        """docstring"""
        # Getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
