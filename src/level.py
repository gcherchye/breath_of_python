"""Level management class"""
from __future__ import absolute_import

import random

import pygame

from .config import config
from .enemy import Enemy
from .player import Player
from .tile import Tile
from .ui import UI
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
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # Vars
        self._create_map()

        # User Interface
        self.user_interface = UI()

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
            'object': import_csv_layout('lib/data/map_Objects.csv'),
            'entities': import_csv_layout('lib/data/map_Entities.csv')
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
                                groups=[
                                    self.visible_sprites,
                                    self.obstacle_sprites,
                                    self.attackable_sprites
                                ],
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

                        if style == 'entities':
                            if col == config.player_tile_id:
                                self.player = Player(
                                    pos=(x_pos, y_pos),
                                    groups=[self.visible_sprites],
                                    obstacles=self.obstacle_sprites,
                                    create_attack=self.create_attack,
                                    destroy_attack=self.destroy_attack,
                                    create_magic=self.create_magic
                                )
                            else:
                                if col == '390':
                                    monster_name = 'bamboo'
                                elif col == '391':
                                    monster_name = 'spirit'
                                elif col == '392':
                                    monster_name = 'raccoon'
                                else:
                                    monster_name = 'squid'
                                Enemy(
                                    monster_name=monster_name,
                                    pos=(x_pos, y_pos),
                                    groups=[self.visible_sprites, self.attackable_sprites],
                                    obstacles=self.obstacle_sprites
                                )



    def create_attack(self) -> None:
        """Creates an attack for the player

        Initiates the creation of an attack object for the player.
        """
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def create_magic(self, style: str, strenght: int, cost: int) -> None:
        """Create a magic attack for the player

        Args:
            style (str): The style of magic used
            strenght (int): The strenght of the spell
            cost (int): The energy cost of the spell
        """
        print(style)
        print(strenght)
        print(cost)

    def destroy_attack(self) -> None:
        """Destroys the current attack object

        Destroys the current attack object if it exists.
        """
        if self.current_attack:
            self.current_attack.kill()

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(
                    sprite=attack_sprite,
                    group=self.attackable_sprites,
                    dokill=True
                )
            if collision_sprites:
                for target_sprite in collision_sprites:
                    target_sprite.kill()

    def run(self) -> None:
        """Runs the game loop, updating and drawing game elements

        Updates and draws the visible sprites in the game.
        """
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.user_interface.display(self.player)


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
    
    def enemy_update(self, player):
        enemy_sprites = [
            sprite for sprite in self.sprites() \
                if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy'
        ]

        for enemy in enemy_sprites:
            enemy.enemy_update(player)
