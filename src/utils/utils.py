"""Common utilitary function for the whole application"""
from __future__ import absolute_import

from csv import reader
from os import listdir
from os.path import isfile, join
from typing import List

import pygame


def import_csv_layout(path: str) -> List[List[int]]:
    """Import a csv floor data file and read it

    Args:
        path (str): The path of the needed floor data file

    Returns:
        List[List[int]]: The values of the data file as a list of row, each row being a list of int
    """
    terrain_map = []

    with open(path, encoding='cp1252') as level_map:
        layout = reader(level_map, delimiter=',')

        for row in layout:
            terrain_map.append(row)

    return terrain_map


def import_image_from_folder(path: str) -> List[pygame.Surface]:
    """Import all the image in a folder as a surface

    Args:
        path (str): The path of the folder conatining the image to load

    Returns:
        List[pygame.Surface]: The list containing all the surfaces of the loaded image
    """
    img_files = [f'{path}/{f}' for f in listdir(path) if isfile(join(path, f))]
    return [pygame.image.load(img_path).convert_alpha() for img_path in img_files]
