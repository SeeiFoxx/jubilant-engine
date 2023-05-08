import pygame
import random

# Initialisation de Pygame
pygame.init()

# Définition des couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Définition des dimensions de la fenêtre de jeu
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Définition de la police de caractères
FONT = pygame.font.SysFont('Calibri', 25, True, False)

# Définition des variables pour la cryptomonnaie
CRYPTOS = {
    'Bitcoin': {
        'price': 50000,
        'color': RED
    },
    'Ethereum': {
        'price': 3000,
        'color': BLUE
    },
    'Dogecoin': {
        'price': 0.50,
        'color': GREEN
    }
}
current_crypto = 'Bitcoin'

# Définition des variables pour le joueur
fiat_balance = 10000
crypto_balance = {
    'Bitcoin': 0,
    'Ethereum': 0,
    'Dogecoin': 0
}

# Définition de la fonction pour dessiner la charte de trading
def draw_chart(screen, chart, color):
    for i in range(len(chart) - 1):
        pygame.draw.line(screen, color, (i * 10 + 100, SCREEN_HEIGHT - chart[i] - 100), ((i + 1) * 10 + 100, SCREEN_HEIGHT - chart[i + 1] - 100))

# Définition de la fonction pour mettre à jour la charte de trading
def update_chart(chart, price):
    chart.pop(0)
    chart.append(price)

# Définition de la fonction pour dessiner l'écran du joueur
def draw_player_screen(screen):
    pygame.draw.rect(screen, WHITE, [SCREEN_WIDTH - 300, 0, 300, SCREEN_HEIGHT])
    text = FONT.render('Solde Fiat: ' + str(fiat_balance) + ' $', True, BLACK)
    screen.blit(text, [SCREEN_WIDTH - 280, 50])
    text = FONT.render('Solde Crypto: ', True, BLACK)
    screen.blit(text, [SCREEN_WIDTH - 280, 100])
    i = 0
    for crypto in crypto_balance:
        text = FONT.render(crypto + ': ' + str(crypto_balance[crypto]), True, CRYPTOS[crypto]['color'])
        screen.blit(text, [SCREEN_WIDTH - 280, 150 + i * 50])
        i += 1

# Définition de la fonction pour dessiner le menu
def draw_menu(screen):
    pygame.draw.rect(screen, WHITE, [0, 0, 100, SCREEN_HEIGHT])
    i = 0
    for crypto in CRYPTOS:
        text = FONT.render(crypto, True, CRYPTOS[crypto]['color'])
        screen.blit(text, [10, 50 + i * 50])
        i += 1

# Définition de la fonction principale
def main():
    # Initialisation de la fenêtre de jeu
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption('Simulateur d\'achat et de vente de cryptomonnaie')

    # Définition des variables pour la charte de trading
    chart = [random.randint(500, 600) for _ in range(60)]
    current_price = CRYPTOS[current_crypto]['price']
    chart[-1] = current_price

    # Boucle de jeu
    done = False
    clock = pygame.time.Clock()

    while not done:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if pos[0] < 100:
                    i = pos[1] // 50
                    current_crypto = list(CRYPTOS.keys())[i]
                    current_price = CRYPTOS[current_crypto]['price']
                    chart[-1] = current_price

        # Mise à jour de la charte de trading
        update_chart(chart, current_price)
        current_price += random.uniform(-5, 5)

        # Dessin de l'écran de jeu
        screen.fill(BLACK)
        draw_chart(screen, chart, CRYPTOS[current_crypto]['color'])
        draw_player_screen(screen)
        draw_menu(screen)

        # Actualisation de la fenêtre de jeu
        pygame.display.flip()

        # Limite de rafraîchissement de la fenêtre de jeu
        clock.tick(60)

    # Fermeture de Pygame
    pygame.quit()

main()
