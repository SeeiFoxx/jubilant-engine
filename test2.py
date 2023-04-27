import pygame
import time
import math

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
largeur = 800
hauteur = 600
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Console")

# Couleurs
blanc = (255, 255, 255)
noir = (0, 0, 0)

# Police de caractères
police = pygame.font.SysFont(None, 30)

# Console
console = ""
console_output = ""
texte_console_output = ""

# Curseur
curseur = "_"
curseur_visible = True
curseur_timer = time.time()

# Effet de bloom
bloom_intensity = 0.5
continuer = True
# Boucle de jeu
while continuer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                console = console[:-1]
            elif event.key == pygame.K_RETURN:
                if console == "help":
                    console_output = "Liste des commandes disponibles :\n- help : affiche la liste des commandes disponibles\n- clear : efface la console\n- exit : ferme la console"
                elif console == "clear":
                    console_output = ""
                elif console == "exit":
                    pygame.quit()
                else:
                    console_output = "Commande inconnue. Tapez 'help' pour voir la liste des commandes disponibles."
                console = ""
            else:
                console += event.unicode
    
    # Effets graphiques
    temps = pygame.time.get_ticks()
    effet_1 = (int(128 * math.sin(temps / 500)) + 128, int(128 * math.sin(temps / 1000)) + 128, int(128 * math.sin(temps / 1500)) + 128)
    effet_2 = (255 - effet_1[0], 255 - effet_1[1], 255 - effet_1[2])
    effet_3 = (255, 255, 255)
    
    # Affichage du fond d'écran
    fenetre.fill(noir)
    
    # Bloom
    for i in range(1, 10):
        pygame.draw.circle(fenetre, (int(effet_1[0] * bloom_intensity / i), int(effet_1[1] * bloom_intensity / i), int(effet_1[2] * bloom_intensity / i)), (400, 300), i * 10)
    pygame.draw.rect(fenetre, blanc, (50, 50, 700, 500), 5)
    pygame.draw.rect(fenetre, blanc, (50, 560, 700, 30), 5)

    # Affichage du texte de la console
    texte_console = police.render("admin@pycoin-services: # " + console, True, blanc)
    fenetre.blit(texte_console, (30, 30))
    
    # Affichage du texte de sortie de console
    texte_console_output = police.render(console_output, True, blanc)
    fenetre.blit(texte_console_output, (30, 80))
    
    # Affichage du curseur clignotant
    if temps % 1000 < 500:
        curseur = police.render("_", True, blanc)
        fenetre.blit(curseur, (30 + texte_console.get_width(), 30))
    
    # Rafraîchissement de la fenêtre
    pygame.display.flip()
    
# Fermeture de Pygame
pygame.quit()