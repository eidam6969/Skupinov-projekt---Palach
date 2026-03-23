import mysql.connector
from pripojeni import *
import pygame
import random
import sys
from settings import *
from player import *
from invader import *
from bullet import *
from bullet_invader import *

pygame.init()
clock = pygame.time.Clock()

game_over_font = pygame.font.SysFont(None, 50)
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 30)

INVADER_SHOOT_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(INVADER_SHOOT_EVENT, 1200)

screen = pygame.display.set_mode((WIDTH, HEIGHT))



try:
    background = pygame.image.load('menu.png')
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
except Exception as e:
    print(f"Varování: menu.png nenalezeno ({e}). Používám černé pozadí.")
    background = None

def draw_text(text, x, y, color = white, center=False):
    # Tady bereme tu globální 'screen' definovanou nahoře
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    if center:
        text_rect.center = (x, y)
        screen.blit(text_obj, text_rect)
    else:
        screen.blit(text_obj, (x, y))

def settings_menu():

    settings_running = True
    
    while settings_running:
        screen.fill(black)
        
        draw_text("NASTAVENÍ", WIDTH // 2, 100, center=True)
        
        # Nějaký text, aby to tam nebylo prázdné
        info_text = [
            "Hlasitost: 80%",
            "Obtížnost: Normální",
            "Rozlišení: 1300x800",
            "Ovládání: Mezerník = Střelba",
            "",
            "Tady můžeš mít další řádky nastavení...",
            "KrKuLaLi.cz"

        ]
        
        for i, line in enumerate(info_text):
            line_surf = small_font.render(line, True, white)
            screen.blit(line_surf, (WIDTH // 2 - 150, 200 + (i * 40)))

        # Tlačítko ZPĚT
        btn_back = pygame.Rect(WIDTH // 2 - 100, 650, 200, 50)
        pygame.draw.rect(screen, gray, btn_back)
        draw_text("ZPĚT", WIDTH // 2, 675, center=True)

        m_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_back.collidepoint(m_pos):
                    settings_running = False # Tohle nás vrátí do main_menu loopu

        pygame.display.update()

def main_menu():
    # Použijeme globální screen, abychom ji mohli přenastavit po návratu ze hry
    global screen
    
    while True:
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((30, 30, 30))

        m_pos = pygame.mouse.get_pos()

        # Definice tlačítek
        btn_start = pygame.Rect(460, 450, 383, 83)
        btn_settings = pygame.Rect(460, 560, 383, 83)
        btn_close = pygame.Rect(460, 670, 383, 83)

        # Vykreslení
        pygame.draw.rect(screen, black, btn_start)
        pygame.draw.rect(screen, black, btn_settings)
        pygame.draw.rect(screen, black, btn_close)

        draw_text("START", WIDTH // 2, 490, center=True)
        draw_text("SETTINGS", WIDTH // 2, 605, center=True)
        draw_text("CLOSE", WIDTH // 2, 705, center=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if btn_start.collidepoint(m_pos):
                        start_game()
                        # Po skončení hry vynutíme návrat k rozlišení menu
                        screen = pygame.display.set_mode((WIDTH, HEIGHT))
                    
                    if btn_settings.collidepoint(m_pos):
                        settings_menu()
                    
                    if btn_close.collidepoint(m_pos):
                        pygame.quit()
                        sys.exit()

        pygame.display.update()

# Připojení k DB ponecháme globálně
mydb = mysql.connector.connect(
    host = HOST,
    user = USER,
    password = PASSWORD,
    database = DATABASE
)

def get_highscore_from_db():
    try:
        cursor = mydb.cursor()
        cursor.execute("SELECT MAX(score) FROM Skore_space_invaders")
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result[0] is not None else 0
    except Exception as e:
        print(f"Chyba při načítání highscore z DB: {e}")
        return 0

def start_game():    
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Reset proměnných při každém novém startu
    running = True
    game_over = False
    score = 0
    user_name = ""
    name_entered = False
    current_enemy_speed = 1         #zmenit
    highscore = get_highscore_from_db()

    # Re-inicializace objektů pro novou hru
    player = Player()
    player_group = pygame.sprite.Group(player)
    enemies_group = create_enemies(3, 6)
    bullets_group = pygame.sprite.Group()
    invader_bullets = pygame.sprite.Group()

    while running:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False # Ukončí funkci a vrátí se do menu
        
            if not game_over:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    bullets_group.add(Bullet(player.rect))

                if event.type == INVADER_SHOOT_EVENT:
                    if enemies_group:
                        shooter = random.choice(enemies_group.sprites())
                        invader_bullets.add(BulletInvader(shooter.rect, speed=current_enemy_speed + 0.3))

            elif game_over and not name_entered:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        final_name = user_name.strip() if user_name.strip() else "test"
                        try:
                            cursor_db = mydb.cursor()
                            sql = "INSERT INTO Skore_space_invaders (jmeno, score) VALUES (%s, %s)"
                            val = (final_name, score)
                            cursor_db.execute(sql, val)
                            mydb.commit()
                            cursor_db.close()
                            name_entered = True
                        except Exception as e:
                            print(f"Chyba při zápisu do DB: {e}")

                    elif event.key == pygame.K_BACKSPACE:
                        user_name = user_name[:-1]
                    else:
                        if len(user_name) < 15 and event.unicode.isprintable():
                            user_name += event.unicode

        # --- LOGIKA A VYKRESLOVÁNÍ (MUSÍ BÝT UVNITŘ WHILE RUNNING) ---
        if not game_over:
            screen.fill(black)
            
            # Kolize
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

            screen.blit(font.render(f"Score: {score}", True, white), (10, 10))
            screen.blit(font.render(f"Highscore: {highscore}", True, yellow), (10, 40))

            hits = pygame.sprite.groupcollide(bullets_group, enemies_group, True, True)
            if hits: 
                score += 10
            
            if not enemies_group:
                current_enemy_speed += 0.5
                enemies_group = create_enemies(3, 6, speed=current_enemy_speed)

        else:
            # GAME OVER OBRAZOVKA
            screen.fill(black)
            screen.blit(game_over_font.render("GAME OVER", True, red), (screen_width // 2 - 105, screen_height // 2 - 110))
            screen.blit(font.render(f"Tvoje skóre: {score}", True, white), (screen_width // 2 - 80, screen_height // 2 - 75))
            screen.blit(font.render("Zadej jméno a stiskni ENTER:", True, yellow), (screen_width // 2 - 160, screen_height // 2))

            cursor_blink = "|" if (pygame.time.get_ticks() // 500) % 2 == 0 else ""
            name_surface = font.render(user_name + (cursor_blink if not name_entered else ""), True, white)
            input_rect = pygame.Rect(screen_width // 2 - 110, screen_height // 2 + 40, 220, 40)
            pygame.draw.rect(screen, white, input_rect, 2)
            screen.blit(name_surface, (input_rect.x + 10, input_rect.y + 5))

            if name_entered:
                screen.blit(font.render("ULOŽENO! (Zavři křížkem pro Menu)", True, (0, 255, 0)), (screen_width // 2 - 190, screen_height // 2 + 100))

        pygame.display.flip()

# Spuštění
if __name__ == "__main__":
    try:
        main_menu()
    finally:
        mydb.close()
        pygame.quit()