import pygame
from settings import *

invader_bullet_image = None

#načtení objektu kulky invadera, rychlosti objektu a směru
class BulletInvader(pygame.sprite.Sprite):
    def __init__(self, invader_rect, speed = 2):
        super().__init__()
        global invader_bullet_image
        if invader_bullet_image is None:
            invader_bullet_image = pygame.image.load("game/img/green_dot.png").convert_alpha()
            invader_bullet_image = pygame.transform.scale(invader_bullet_image, (14, 14))
        self.image = invader_bullet_image
        self.rect = self.image.get_rect()
        self.rect.centerx = invader_rect.centerx
        self.rect.top = invader_rect.bottom
        self.speed = speed
        
#vymazání objektu po úniku z obrazu
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.kill()
