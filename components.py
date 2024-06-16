import pygame
import random


class Ground:
    ground_level = 768

    def __init__(self, win_width):
        self.x, self.y = 0, Ground.ground_level
        self.rect = pygame.Rect(self.x, self.y, win_width, 5)

    def draw(self, window):
        pygame.draw.rect(window, (255, 255, 255), self.rect)



class Pipes:
    width = 70
    opening = 300
    pipe_image_path = '.\\Images\\pipe.png'  # Path to your pipe image

    def __init__(self, win_width):
        self.x = win_width
        self.bottom_height = random.randint(150, 300)  # Adjust range as necessary for your game
        self.top_height = 768 - self.bottom_height - self.opening
        self.image = pygame.image.load(Pipes.pipe_image_path)
        #self.image = pygame.transform.scale(self.image, (self.width, 800))  # Assuming pipe image needs to be scaled
        
        # Create flipped version for top pipe
        self.top_image = pygame.transform.flip(self.image, False, True)
        
        # Set initial positions for rects, they will be updated in draw()
        self.bottom_rect = self.image.get_rect(midtop=(self.x, 768 - self.bottom_height))
        self.top_rect = self.top_image.get_rect(midbottom=(self.x, self.top_height))

        self.passed = False
        self.off_screen = False

    def draw(self, window):
        # Update rect positions
        self.bottom_rect.x = self.top_rect.x = self.x
        
        # Blit the images instead of drawing rects
        window.blit(self.image, self.bottom_rect)
        window.blit(self.top_image, self.top_rect)

    def update(self):
        self.x -= 4  # Update this to your game's pipe speed
        if self.x + self.width <= 50:
            self.passed = True
        if self.x <= -self.width:
            self.off_screen = True












