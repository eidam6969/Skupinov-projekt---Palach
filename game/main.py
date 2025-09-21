import pygame
import random
from settings import *
from player import *
from invader import *
from bullet import *
from bullet_invader import *

pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invaders")

running = True
clock = pygame.time.Clock()
game_over = False
font = pygame.font.SysFont(None, 36)

score = 0

try:
    with open("highscore.txt", "r") as f:
        highscore = int(f.read())
except:
    highscore = 0

player = Player()
player_group = pygame.sprite.Group()
player_group.add(player)

enemy_speed = 2
enemies_group = create_enemies(3, 6)

bullets_group = pygame.sprite.Group()
invader_bullets = pygame.sprite.Group()

INVADER_SHOOT_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(INVADER_SHOOT_EVENT, 1200)

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect)
                bullets_group.add(bullet)
        if event.type == INVADER_SHOOT_EVENT and not game_over:
            if len(enemies_group) > 0:
                shooter = random.choice(enemies_group.sprites())
                bullet = BulletInvader(shooter.rect)
                invader_bullets.add(bullet)

    screen.fill(black)

    if pygame.sprite.groupcollide(player_group, enemies_group, True, True):
        game_over = True

    if pygame.sprite.groupcollide(player_group, invader_bullets, True, True):
        game_over = True

    if not game_over:
        keys = pygame.key.get_pressed()
        player_group.update(keys)
        enemies_group.update()
        bullets_group.update()
        invader_bullets.update()

    player_group.draw(screen)
    enemies_group.draw(screen)
    bullets_group.draw(screen)
    invader_bullets.draw(screen)

    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (10, 10))

    highscore_text = font.render(f"Highscore: {highscore}", True, yellow)
    screen.blit(highscore_text, (10, 40))

    hits = pygame.sprite.groupcollide(bullets_group, enemies_group, True, True)
    if len(enemies_group) == 0 and not game_over:
        enemy_speed += 0.2
        enemies_group = create_enemies(3, 6, speed=enemy_speed)
    if hits:
        score += 10

    if game_over:
        screen.fill(black)
        game_over_text = font.render("GAME OVER", True, red)
        screen.blit(game_over_text, (screen_width // 2 - 80, screen_height // 2))
        score_text = font.render(f"Score: {score}", True, white)
        screen.blit(score_text, (screen_width // 2 - 55, screen_height // 2 + 40))

    pygame.display.flip()

if score > highscore:
    with open("highscore.txt", "w") as f:
        f.write(str(score))

pygame.quit()
