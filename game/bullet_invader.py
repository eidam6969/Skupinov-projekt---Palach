import pygame
from settings import *
from invader import *
#načtení objektu kulky invadera, rychlosti objektu a směru
class BulletInvader(pygame.sprite.Sprite):
    def __init__(self, invader_rect, speed = 2):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)  
        pygame.draw.circle(self.image, (0, 255, 0), (5, 5), 5)
        self.rect = self.image.get_rect()
        self.rect.centerx = invader_rect.centerx
        self.rect.top = invader_rect.bottom
        self.speed = speed
#vymazání objektu po úniku z obrazu
    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()
