"""Level management class"""
from __future__ import absolute_import

import random

import pygame

from .config import config
from .player import Player
from .tile import Tile
from .utils import import_csv_layout, import_image_from_folder
from .weapon import Weapon


class Level:
    """Manages the level and its elements in the game"""

    def __init__(self) -> None:
        """Initializes the Level class

        Sets up the game display surface, sprite groups, configuration, and initializes the map.
        """
        # Get the game display surface
        self.display_surface = pygame.display.get_surface()

        # Sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # Config
        self.config = config

        # Attack sprites
        self.current_attack = None

        # Vars
        self._create_map()

    def _create_map(self) -> None:
        """Creates the game map based on imported layouts and graphics

        Reads layouts from CSV files and generates tiles based on different styles (boundary, grass,
        and object). Creates tiles according to the layout data and assigns them to corresponding
        sprite groups.

        It also initiate the Player.
        """
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
            self.obstacle_sprites,
            self.create_attack,
            self.destroy_attack
        )

    def create_attack(self) -> None:
        """Creates an attack for the player

        Initiates the creation of an attack object for the player.
        """
        self.current_attack = Weapon(self.player, [self.visible_sprites])

    def destroy_attack(self) -> None:
        """Destroys the current attack object

        Destroys the current attack object if it exists.
        """
        if self.current_attack:
            self.current_attack.kill()

    def run(self) -> None:
        """Runs the game loop, updating and drawing game elements

        Updates and draws the visible sprites in the game.
        """
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group):
    """A specialized sprite group for managing depth sorting in the game."""

    def __init__(self) -> None:
        """Initializes the YSortCameraGroup class

        Sets up the camera group and initializes floor-related variables.
        """
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # Creating the floor
        self.floor_surf = pygame.image.load('lib/images/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player) -> None:
        """Draws game elements with depth sorting

        Draws elements based on their vertical position to create a depth effect. It draws the
        floor, aligns the camera to the player's position, and draws other elements with respect
        to their vertical positions.
        """
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
