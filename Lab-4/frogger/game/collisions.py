"""
collisions: frog-vs-vehicle collision detection.
"""

import pygame

CELL_SIZE = 50


def check_collision(frog, vehicles):
    """
    Returns True if the frog is currently hit by any vehicle.
    Uses bounding-box collision detection between the frog and vehicles.
    """
    frog_rect = frog.get_rect(CELL_SIZE)
    for v in vehicles:
        if v.row == frog.row and v.get_rect(CELL_SIZE).colliderect(frog_rect):
            return True
    return False
