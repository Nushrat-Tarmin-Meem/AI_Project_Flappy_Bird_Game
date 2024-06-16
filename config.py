import components
import pygame

win_height = 800
win_width = 864
window = pygame.display.set_mode((win_width, win_height))

ground = components.Ground(win_width)
pipes = []