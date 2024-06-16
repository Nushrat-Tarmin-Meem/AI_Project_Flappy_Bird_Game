import brain
import random
import pygame
import config

class Player:
    def __init__(self):
        # Bird
        self.x, self.y = 50, 200
        self.image = pygame.image.load('.\\Images\\bird1.png')  # Load the image
       # self.image = pygame.transform.scale(self.image, (20, 20))  # Scale the image if necessary
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.vel = 0
        self.flap = False
        self.alive = True
        self.lifespan = 0

        # AI
        self.decision = None
        self.vision = [0.5, 1, 0.5]
        self.fitness = 0
        self.inputs = 3
        self.brain = brain.Brain(self.inputs)
        self.brain.generate_net()

    # Game related functions
    def draw(self, window):
        window.blit(self.image, self.rect)  # Use blit to draw the image at the rect position

    def ground_collision(self, ground):
        return pygame.Rect.colliderect(self.rect, ground)

    def sky_collision(self):
        return bool(self.rect.y < 30)

    def pipe_collision(self):
        for p in config.pipes:
            if pygame.Rect.colliderect(self.rect, p.top_rect) or pygame.Rect.colliderect(self.rect, p.bottom_rect):
                return True
        return False

    def update(self, ground):
        if not (self.ground_collision(ground) or self.pipe_collision()):
            # Gravity
            self.vel += 0.25
            self.rect.y += self.vel
            if self.vel > 5:
                self.vel = 5
            # Increment lifespan
            self.lifespan += 1
        else:
            self.alive = False
            self.flap = False
            self.vel = 0

    def bird_flap(self):
        if not self.flap and not self.sky_collision():
            self.flap = True
            self.vel = -5
        if self.vel >= 3:
            self.flap = False

    @staticmethod
    def closest_pipe():
        for p in config.pipes:
            if not p.passed:
                return p


    # AI related functions
    # AI related functions
    def look(self):
        if config.pipes:
            # Determine vision based on distance to pipes
            closest_pipe = self.closest_pipe()  # Correct the method name here

            # Line to top pipe
            self.vision[0] = max(0, self.rect.center[1] - closest_pipe.top_rect.bottom) / 500

            # Line to mid pipe
            self.vision[1] = max(0, closest_pipe.x - self.rect.center[0]) / 500

            # Line to bottom pipe
            self.vision[2] = max(0, closest_pipe.bottom_rect.top - self.rect.center[1]) / 500

    def think(self):
        self.decision = self.brain.feed_forward(self.vision)
        if self.decision > 0.73:
            self.bird_flap()

    def calculate_fitness(self):
        self.fitness = self.lifespan

    def clone(self):
        clone = Player()
        clone.fitness = self.fitness
        clone.brain = self.brain.clone()
        clone.brain.generate_net()
        return clone
