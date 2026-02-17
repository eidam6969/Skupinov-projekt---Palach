import pygame
import sys
from main import start_game 

# 1. Základní inicializace
pygame.init()
WIDTH, HEIGHT = 1300, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moje Menu")

# 2. Barvy a písma
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
font = pygame.font.SysFont('Arial', 40)
small_font = pygame.font.SysFont('Arial', 30)

# 3. Načtení pozadí (pokud soubor chybí, program nespadne)
try:
    background = pygame.image.load('menu.png')
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
except Exception as e:
    print(f"Varování: menu.png nenalezeno ({e}). Používám černé pozadí.")
    background = None

def draw_text(text, x, y, color=WHITE, center=False):
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
        screen.fill(BLACK)
        
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
            line_surf = small_font.render(line, True, WHITE)
            screen.blit(line_surf, (WIDTH // 2 - 150, 200 + (i * 40)))

        # Tlačítko ZPĚT
        btn_back = pygame.Rect(WIDTH // 2 - 100, 650, 200, 50)
        pygame.draw.rect(screen, GRAY, btn_back)
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
        pygame.draw.rect(screen, BLACK, btn_start)
        pygame.draw.rect(screen, BLACK, btn_settings)
        pygame.draw.rect(screen, BLACK, btn_close)

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

if __name__ == "__main__":
    main_menu()