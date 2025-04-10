import os
import sys
import pygame

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def load_image(name):
    """Load an image with proper path handling for both dev and compiled modes"""
    path = get_resource_path(os.path.join('assets', name))
    print(f"Attempting to load image: {path}")
    print(f"File exists: {os.path.exists(path)}")
    try:
        return pygame.image.load(path)
    except pygame.error as e:
        print(f"Error loading image {name}: {e}")
        # Return a colored surface as fallback for debugging
        surface = pygame.Surface((100, 100))
        surface.fill((255, 0, 0))  # Red
        return surface
def load_sound(name):
    """Load a sound with proper path handling for both dev and compiled modes"""
    path = get_resource_path(os.path.join('assets', name))
    try:
        return pygame.mixer.Sound(path)
    except pygame.error as e:
        print(f"Error loading sound {name}: {e}")
        # You could return a silent sound here
        raise