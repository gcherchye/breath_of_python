"""Debugging tool to add debug lmog on the screen"""
from __future__ import absolute_import

import pygame


pygame.init()
font = pygame.font.Font(None,30)

def debug(info: str, y_pos: int= 10, x_pos: int= 10) -> None:
    """Add log on the screen at the designated position

    Args:
        info (str): The log to add on the screen
        y (int, optional): The postion of the log on the y axis. Defaults to 10.
        x (int, optional): The position of the log on the x axis. Defaults to 10.
    """

    display_surface = pygame.display.get_surface()

    debug_surf = font.render(str(info),True,'White')
    debug_rect = debug_surf.get_rect(topleft = (x_pos,y_pos))

    pygame.draw.rect(display_surface,'Black',debug_rect)

    display_surface.blit(debug_surf,debug_rect)
