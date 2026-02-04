import mysql.connector
from pripojeni import *
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

#variablies
running = True
clock = pygame.time.Clock()
game_over = False
game_over_font = pygame.font.SysFont(None, 50)
font = pygame.font.SysFont(None, 36)
score = 0
user_name = ""
name_entered = False
current_enemy_speed = 1

highscore = 

try:
    cursor = mydb.cursor()
    cursor.execute("SELECT MAX(skore) FROM highscores")
    result = cursor.fetchone()
    highscore = result[0] if result[0] is not None else 0
    cursor.close()
except Exception as e:
    print(f"Nepodařilo se načíst highscore: {e}")
    highscore = 0

#inicializace objektu
player = Player()
player_group = pygame.sprite.Group(player)
enemies_group = create_enemies(3, 6)
bullets_group = pygame.sprite.Group()
invader_bullets = pygame.sprite.Group()

#shoot time
INVADER_SHOOT_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(INVADER_SHOOT_EVENT, 1200)

while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if not game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bullets_group.add(Bullet(player.rect))
            
            if event.type == INVADER_SHOOT_EVENT:
                if enemies_group:
                    shooter = random.choice(enemies_group.sprites())
                    invader_bullets.add(BulletInvader(shooter.rect, speed=current_enemy_speed + 0.3))

        #jmeno
        elif game_over and not name_entered:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    final_name = user_name.strip() if user_name.strip() else "test"
                    try:
                        
                        #sql zapis
                        cursor = mydb.cursor()
                        sql = "INSERT INTO highscores (jmeno, skore) VALUES (%s, %s)"
                        val = (final_name, score)
                        cursor.execute(sql, val)
                        mydb.commit() # Důležité pro potvrzení změn v DB
                        cursor.close()
                        
                        
                        
                        print(f"ULOŽENO DO DB: {final_name} : {score}")
                        name_entered = True
                    except Exception as e:
                        print(f"Chyba při zápisu do DB: {e}")

                elif event.key == pygame.K_BACKSPACE:
                    user_name = user_name[:-1]
                else:
                    if len(user_name) < 15 and event.unicode.isprintable():
                        user_name += event.unicode

    #logika
    if not game_over:
        screen.fill(black)
        
        #kolize
        if pygame.sprite.groupcollide(player_group, enemies_group, True, True) or \
           pygame.sprite.groupcollide(player_group, invader_bullets, True, True):
            game_over = True

        keys = pygame.key.get_pressed()
        player_group.update(keys)
        enemies_group.update()
        bullets_group.update()
        invader_bullets.update()

        player_group.draw(screen)
        enemies_group.draw(screen)
        bullets_group.draw(screen)
        invader_bullets.draw(screen)

        #score
        screen.blit(font.render(f"Score: {score}", True, white), (10, 10))
        screen.blit(font.render(f"Highscore: {highscore}", True, yellow), (10, 40))

        hits = pygame.sprite.groupcollide(bullets_group, enemies_group, True, True)
        if hits: score += 10
        
        if not enemies_group:
            current_enemy_speed += 0.5  #enemy speed
            enemies_group = create_enemies(3, 6, speed=current_enemy_speed)

    else:
        #gae over
        screen.fill(black)
        screen.blit(game_over_font.render("GAME OVER", True, red), (screen_width // 2 - 105, screen_height // 2 - 110))
        screen.blit(font.render(f"Tvoje skóre: {score}", True, white), (screen_width // 2 - 80, screen_height // 2 - 75))
        screen.blit(font.render("Zadej jméno a stiskni ENTER:", True, yellow), (screen_width // 2 - 160, screen_height // 2))

        #input box
        cursor_blink = "|" if (pygame.time.get_ticks() // 500) % 2 == 0 else ""
        name_surface = font.render(user_name + (cursor_blink if not name_entered else ""), True, white)
        input_rect = pygame.Rect(screen_width // 2 - 110, screen_height // 2 + 40, 220, 40)
        pygame.draw.rect(screen, white, input_rect, 2)
        screen.blit(name_surface, (input_rect.x + 10, input_rect.y + 5))

        if name_entered:
            screen.blit(font.render("ULOŽENO! (Zavři křížkem)", True, (0, 255, 0)), (screen_width // 2 - 130, screen_height // 2 + 100))

    pygame.display.flip()

#konec
mydb.close()
pygame.quit()