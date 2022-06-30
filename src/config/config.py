"""Config file for the game"""
from __future__ import absolute_import

from dataclasses import dataclass

import pygame


@dataclass
class Configuration:
    """Global configuration class"""
    # Screen config
    width = 1280
    height = 720
    tilesize = 64

    # Time config
    fps = 60

    # Player config
    player_img_path = 'lib/images/player/'
    player_animation_speed = 0.15
    player_speed = 5
    player_attack_cooldown = 400

    # Weapons config
    weapon_data = {
        'sword': {
            'cooldown': 100,
            'damage': 15,
            'graphic': 'lib/images/weapons/sword/full.png'
        },
        'lance': {
            'cooldown': 400,
            'damage': 30,
            'graphic': 'lib/images/weapons/lance/full.png'
        },
        'axe': {
            'cooldown': 300,
            'damage': 20,
            'graphic': 'lib/images/weapons/axe/full.png'
        },
        'rapier': {
            'cooldown': 50,
            'damage': 8,
            'graphic': 'lib/images/weapons/rapier/full.png'
        },
        'sai': {
            'cooldown': 80,
            'damage': 10,
            'graphic': 'lib/images/weapons/sai/full.png'
        }
    }

    weapon_horizon_offset = pygame.math.Vector2(0, 16)
    weapon_vertical_offset = pygame.math.Vector2(-10, 0)
