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

    # colors
    water_color = '#71ddee'
    ui_bg_color = '#222222'
    ui_border_color = '#111111'
    text_color = '#EEEEEE'
    health_color = 'red'
    energy_color = 'blue'
    ui_border_color_active = 'gold'

    # Time config
    fps = 60

    # Player config
    player_img_path = 'lib/images/player/'
    player_animation_speed = 0.15
    player_attack_cooldown = 400
    player_stats = {
        'health': 100,
        'energy': 60,
        'attack': 10,
        'magic': 4,
        'speed': 5
    }
    switch_duration_cooldown = 200

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

    # Magic config
    magic_data = {
        'flame': {'strenght': 5, 'cost': 20, 'graphic': 'lib/images/particles/flame/fire.png'},
        'heal': {'strenght': 20, 'cost': 10, 'graphic': 'lib/images/particles/heal/heal.png'}
    }

    # User Interface
    bar_height = 20
    health_bar_width = 200
    energy_bar_width = 140
    item_box_size = 80
    ui_font = 'lib/images/font/joystix.ttf'
    ui_font_size = 18
    weapon_box_top_left = (10, 630)
    magic_box_top_left = (80, 635)
