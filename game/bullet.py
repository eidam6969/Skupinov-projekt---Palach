import pygame
from settings import *

bullet_image = None

#načtení objektu kulky hráče, rychlosti objektu a směru
class Bullet(pygame.sprite.Sprite):
    def __init__(self, player_rect):
        super().__init__()
        global bullet_image
        if bullet_image is None:
            bullet_image = pygame.image.load("game/img/red_dot.png").convert_alpha()
            bullet_image = pygame.transform.scale(bullet_image, (14, 14))
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.centerx = player_rect.centerx
        self.rect.bottom = player_rect.top - 20
        self.speed = 5
        
#vymazání objektu po úniku z obrazu
    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()
