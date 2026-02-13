import pygame
from settings import *
from player import *
#načtení objektu kulky hráče, rychlosti objektu a směru
class Bullet(pygame.sprite.Sprite):
    def __init__(self, player_rect):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)  
        pygame.draw.circle(self.image, (255, 0, 0), (5, 5), 5)
        self.rect = self.image.get_rect()
        self.rect.centerx = player_rect.centerx
        self.rect.bottom = player_rect.top
        self.speed = 5
#vymazání objektu po úniku z obrazu
    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()
