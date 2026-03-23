import pygame
from settings import *
from player import *

#načtení objektu kulky hráče, rychlosti objektu a směru
class Bullet(pygame.sprite.Sprite):
    def __init__(self, player_rect):
        super().__init__()
        self.image = pygame.image.load("game/img/red_dot.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (14, 14))
        self.rect = self.image.get_rect()
        self.rect.centerx = player_rect.centerx
        self.rect.bottom = player_rect.top - 20
        self.speed = 5
        
#vymazání objektu po úniku z obrazu
    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()
