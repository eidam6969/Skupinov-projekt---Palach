import pygame
import random
from settings import *
#load in
class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed=2):
        super().__init__()
        self.image = pygame.image.load("game/img/invader.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(50, 150)
        self.speed = speed

#pohyb ze strany na stranu
    def update(self):
        self.rect.x += self.speed
        if self.rect.right >= screen_width:
            self.speed *= -1
            self.rect.right = screen_width - 1
            self.rect.y += 40
            
        elif self.rect.left <= 0:
            self.speed *= -1
            self.rect.left = 1
            self.rect.y += 40
#mřížové seskupení invaderů
def create_enemies(rows, cols, x_spacing=50, y_spacing=40, start_x=0, start_y=0, speed=2):
    enemies_group = pygame.sprite.Group()
    for row in range(rows):
        for col in range(cols):
            enemy = Enemy(speed)
            enemy.rect.x = start_x + col * x_spacing
            enemy.rect.y = start_y + row * y_spacing
            enemies_group.add(enemy)
    return enemies_group
