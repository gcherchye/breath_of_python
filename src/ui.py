"""docstring"""
from __future__ import absolute_import

import pygame

from .player import Player
from .config import config


class UI:
    """Handles the user interface elements for the game

    Attributes:
        display_surface (pygame.Surface): The display surface for the UI.
        font (pygame.Font): The font used for UI text.
        health_bar_rect (pygame.Rect): The rectangle representing the health bar.
        energy_bar_rect (pygame.Rect): The rectangle representing the energy bar.
        weapon_graphics (list): List of weapon images for display.
    """

    def __init__(self) -> None:
        """Initializes the UI"""
        # General
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(config.ui_font, config.ui_font_size)

        # Bar setup
        self.health_bar_rect = pygame.Rect(
            10,
            10,
            config.health_bar_width,
            config.bar_height
        )
        self.energy_bar_rect = pygame.Rect(
            10,
            34,
            config.energy_bar_width,
            config.bar_height
        )

        # Convert weapon dict
        self.weapon_graphics = []
        for weapon in config.weapon_data.values():
            img_path = weapon['graphic']
            weapon_img = pygame.image.load(img_path).convert_alpha()

            self.weapon_graphics.append(weapon_img)

    def show_bar(
            self,
            current_amount: int,
            max_amount: int,
            bg_rect: pygame.Rect,
            color: str
        ) -> None:
        """Displays a bar with specified parameters

        Args:
            current_amount (int): Current value of the bar.
            max_amount (int): Maximum value of the bar.
            bg_rect (pygame.Rect): Background rectangle for the bar.
            color (str): Color of the bar.
        """
        # Draw the background
        pygame.draw.rect(self.display_surface, config.ui_bg_color, bg_rect)

        # Converting stat to pixel
        ratio = current_amount / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # Drawing the bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, config.ui_border_color, bg_rect, 3)

    def show_exp(self, exp: float) -> None:
        """Displays the experience points on the UI

        Args:
            exp (int): The experience points to display.
        """
        text_surf = self.font.render(str(int(exp)), False, config.text_color)
        x_pos = self.display_surface.get_size()[0] - 20
        y_pos = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright=(x_pos, y_pos))

        pygame.draw.rect(self.display_surface, config.ui_bg_color, text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, config.ui_border_color, text_rect.inflate(20, 20), 3)

    def selection_box(self, left, top, has_switched) -> pygame.Rect:
        """Creates a selection box at specified coordinates

        Args:
            left (int): X-coordinate of the box.
            top (int): Y-coordinate of the box.
            has_switched (bool): Indicates if the selection has switched.

        Returns:
            pygame.Rect: The created rectangle for the selection box.
        """
        bg_rect = pygame.Rect(left, top, config.item_box_size, config.item_box_size)
        pygame.draw.rect(self.display_surface, config.ui_bg_color, bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface, config.ui_border_color_active, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, config.ui_border_color, bg_rect, 3)

        return bg_rect

    def weapon_overlay(self, weapon_index: int, has_switched: bool) -> None:
        """Displays the weapon overlay on the UI

        Args:
            weapon_index (int): Index of the weapon image to display.
            has_switched (bool): Indicates if the weapon has switched.
        """
        bg_rect = self.selection_box(10, 630, has_switched)
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)

        self.display_surface.blit(self.weapon_graphics[weapon_index], weapon_rect)

    def display(self, player: Player) -> None:
        """Displays the UI elements based on player data

        Args:
            player (Player): The player object containing necessary data.
        """
        self.show_bar(
            player.health,
            player.stats['health'],
            self.health_bar_rect,
            config.health_color
        )
        self.show_bar(
            player.energy,
            player.stats['energy'],
            self.energy_bar_rect,
            config.energy_color
        )

        self.show_exp(player.exp)

        self.weapon_overlay(player.weapon_index, not player.can_switch_weapon)
        #self.selection_box(80, 635) # magic
