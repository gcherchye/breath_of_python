"""Level management class"""
from __future__ import absolute_import

import random

import pygame

from .config import config
from .player import Player
from .tile import Tile
from .utils import import_csv_layout, import_image_from_folder



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
        layouts = {
            'boundary': import_csv_layout('lib/data/map_FloorBlocks.csv'),
            'grass': import_csv_layout('lib/data/map_Grass.csv'),
            'object': import_csv_layout('lib/data/map_Objects.csv')
        }

        graphics = {
            'grass': import_image_from_folder('lib/images/grass'),
            'objects': import_image_from_folder('lib/images/objects')
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x_pos = col_index * config.tilesize
                        y_pos = row_index * config.tilesize

                        if style == 'boundary':
                            Tile(
                                pos=(x_pos, y_pos),
                                groups=[self.obstacle_sprites],
                                sprite_type='invisible'
                            )

                        if style == 'grass':
                            Tile(
                                pos=(x_pos, y_pos),
                                groups=[self.visible_sprites, self.obstacle_sprites],
                                sprite_type='grass',
                                surface=random.choice(graphics['grass'])
                            )

                        if style == 'object':
                            Tile(
                                pos=(x_pos, y_pos),
                                groups=[self.visible_sprites, self.obstacle_sprites],
                                sprite_type='object',
                                surface=graphics['objects'][int(col)]
                            )


        self.player = Player(
            (2000, 1430),
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

        # Creating the floor
        self.floor_surf = pygame.image.load('lib/images/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        """docstring"""
        # Getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # Drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        # Drawing all the other elements
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
