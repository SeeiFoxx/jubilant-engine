import pygame

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
largeur = 1920
hauteur = 1080
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Jeu sur la Blockchain")

# Couleurs
blanc = (255, 255, 255)
noir = (0, 0, 0)
or_ = 


# Police de caractères
police = pygame.font.SysFont(None, 40)

# Définitions
definitions = {
    "1": "Test1",
    "2": "Test2",
    "3": "test3"
}

# Variables
page = 0
continuer = True

# Boucle de jeu
while continuer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                page -= 1
                if page < 0:
                    page = len(definitions) - 1
            elif event.key == pygame.K_RIGHT:
                page += 1
                if page >= len(definitions):
                    page = 0
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if bouton_precedent_rect.collidepoint(event.pos):
                page -= 1
                if page < 0:
                    page = len(definitions) - 1
            elif bouton_suivant_rect.collidepoint(event.pos):
                page += 1
                if page >= len(definitions):
                    page = 0

    # Affichage des textes
    fenetre.fill(noir)
    titre = police.render(list(definitions.keys())[page], True, or_)
    definition = police.render(list(definitions.values())[page], True, or_)
    fenetre.blit(titre, (100, 100))
    fenetre.blit(definition, (100, 200))

    # Affichage des boutons
    bouton_precedent = police.render("Précédent", True, noir)
    bouton_suivant = police.render("Suivant", True, noir)
    bouton_precedent_rect = pygame.Rect(100, hauteur - 100, bouton_precedent.get_width() + 10, bouton_precedent.get_height() + 10)
    bouton_suivant_rect = pygame.Rect(largeur - bouton_suivant.get_width() - 100, hauteur - 100, bouton_suivant.get_width() + 10, bouton_suivant.get_height() + 10)
    pygame.draw.rect(fenetre, or_, bouton_precedent_rect, 0, 10)
    fenetre.blit(bouton_precedent, (bouton_precedent_rect.x + 5, bouton_precedent_rect.y + 5))
    pygame.draw.rect(fenetre, or_, bouton_suivant_rect, 0, 10)
    fenetre.blit(bouton_suivant, (bouton_suivant_rect.x + 5, bouton_suivant_rect.y + 5))

    # Rafraîchissement de la fenêtre
    pygame.display.flip()

# Fermeture de Pygame
pygame.quit()
