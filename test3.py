import pygame
import random
from random import randint

# Classe Monnaie, utilisée pour gérer les monnaies et les cryptomonnaies
class Monnaie:
    # Contruscteur qui définit toutes les variables
    def __init__(self, nom, nom_court, prix_init, volatilite):
        # Le nom de la monnaie
        self.nom = nom
        # Le nom de la monnaie mais en raccourci, pour une fois que vous êtes intimes
        self.nom_court = nom_court
        # La volatilité de la monnaie, en fonction de son type (fiat, crypto) et de son risque.
        self.volatilite = float(volatilite)
        # Un historique des prix est créé pour une visualisation facile.
        self.historique_prix = [prix_init] * 60
        # Défini une première fois car on en a besoin pour dériver des prix plus tard
        self.prix = prix_init
        # Faire varier le prix 60 fois pour que on ait une vraie charte au début
        for i in range(60):
        	self.faire_varier_prix()
        # Le prix initial de la monnaie, formé à partir de l'historique des prix initiaux
        self.prix = float(self.historique_prix[-1])
        # Le nombre d'unités de cette monnaie que l'on a, initialisé à 0
        self.portefeuille = 0
        # Le nombre d'unités de cette monnaie que le portefeuille des utilisateurs des services pycoins a actuellement.
        # Initialisé à un nombre aléatoire entre 1 000 et 1 000 000.
        self.portefeuille_pycoin = int(randint(1000, 1000000))
        # Par défaut, il reste 50 tours avant que l'inflation soit prise en compte.
        self.inflation_countdown = 50
        # Par défaut, il reste 20 tours avant un évènement
        self.event_countdown = 20
        # Le nombre de cryptos empruntées au services pycoin. Lors de l' "emprunt" les cryptos passent en douce du
        # compte des services pycoin à mon compte personnel, étant au passage ajoutées dans cette balance pour être
        # séparées de profits que je ferai avec ces emprunts plus tard.
        self.emprunte = 0
        # Si la volatilité est à 0, c'est une fiat qui subit l'inflation (fixée à 0.07% pour des raisons de simplicité)
        if volatilite == 0:
            self.inflation = 0.07
            # Évènements de fiat
            self.events = [
                ('Réglementation favorable', 0.1),
                ('Attaque informatique', -0.2),
            ]
        # Sinon, c'est une crypto qui subit une déflation (fixée à 0.1 = 10% par 50
        # tours soit 0.2% par tour pour des raisons de simplicité)
        else:
            self.inflation = -0.1
            # Évènements de crypto (un peu exotiques...)
            self.events = [
                ('Réglementation favorable', 0.3),
                ('Réglementation défavorable', -0.1),
                ('Ton cousin Kevin en a acheté', -0.6),
                ('Décision judiciaire favorable', 0.4),
                ('Décision judiciaire défavorable', -0.15),
                ('Elon Musk Tweete', 2),
                ('POV tes parents découvrent ton wallet de 200K et tu dois tout vendre comme une certaine personne dans ce groupe', -0.7),
                ('Innovation technologique de fou', 0.3),
                ('Abdelmajid pirate Kyian et prends tout son argent', 0.5),
                ('Kyian a ligoté Abdelmajid dans sa cave, il peut plus trader', -0.15),
                ('Romain fait un trading copy de mon compte', 0.2),
                ('Hugo vends des dessins de qualité en NFT', 0.45)
            ]

    # Méthode pour acheter
    def acheter(self, monnaie2 , quantite):
        # Le prix total de l'achat en dollars
        prix_total_achat = quantite * self.prix
        # On checke si on a assez de l'autre monnaie pour acheter
        if prix_total_achat > monnaie2.portefeuille * monnaie2.prix:
            # Si ce n'est pas le cas, on retourne False.
            return(False)
        # On enlève le montant de monnaie dans le portefeuille de la monnaie qu'on vends pour acheter la nouvelle monnaie
        monnaie2.portefeuille -= prix_total_achat / monnaie2.prix
        # On ajoute la nouvelle monnaie achetée dans le portefeuille correspondant.
        self.portefeuille += quantite
        # On retourne True pour signaler que l'opération s'est bien passée.
        return(True)
    
    # Méthode pour vendre
    def vendre(self, monnaie2, quantite):
        # Checke si on a assez de monnaie pour mener à bien la transaction
        if self.portefeuille < quantite:
            return(False)
        # On calcule le prix total de la vente
        prix_total_vente = quantite * self.prix
        # On enlève les coins vendus du portefeuille de cette monnaie
        self.portefeuille -= quantite
        # On mets les coins achetés dans le portefeuille de l'autre monnaie
        monnaie2.portefeuille += prix_total_vente/ monnaie2.prix
    
    # S'occupe de faire varier le prix d'une monnaie en fonction de sa volatilité
    def faire_varier_prix(self):
        # Si on a une volatilité (pas une fiat mdr) et que la monnaie n'est pas morte
        if self.volatilite > 0 and self.prix != 0:
            variation = random.uniform(-self.volatilite, self.volatilite)
            nouveau_prix = self.prix * (1 + variation)
            # Si le prix tombe à 0.00000 quelque chose, on considère que la monnaie est morte et on liquide tous les wallets.
            if round(nouveau_prix, 5) == 0:
                self.prix = 0
                self.portefeuille = 0
                self.emprunt = 0
                self.portefeuille_pycoin = 0
            else:
                self.historique_prix.pop(0)
                self.historique_prix.append(nouveau_prix)
                self.prix = nouveau_prix
    
    # Méthode pour emprunter
    def emprunt(self, monnaie, montant):
        # Vérifie que les comptes pycoin ont assez d'argent,
        # pas comme la plateforme FTX qui avait un "bug" dans laquelle les mecs piochaient en illimité,
        # aucune limite sur les "prêts" de leur propre exchange sur leurs comptes (ceux de Alameda Research,
        # leur entreprise perso quoi). Oui, on plagie les mecs qui ont fait faillite.
        # Si on a pas assez de coins,
        if montant > monnaie.portefeuille_pycoin:
            # On retourne False pour montrer que la transaction a échoué
            return(False)
        # Si on a assez s'argent, on autorise le prêt
        else:
            monnaie.portefeuille_pycoin -= int(montant)
            monnaie.portefeuille += int(montant)
            monnaie.emprunte += int(montant)
            # On retourne true pour montrer que la transaction a été validée
            return(True)
        
	# Méthode pour rembourser un emprunt
    def remboursement(self, monnaie, montant):
        # Si on rends plus que ce qu'on a emprunté, ça crashe
        if int(monnaie.emprunte) > int(montant):
            return(False)
        # Si on a pas le montant
        elif monnaie.portefeuille < montant:
            return(False)
        else:
            monnaie.emprunt -= int(montant)
            monnaie.portefeuille_pycoin += int(montant)
            monnaie.portefeuille -= int(montant)
            return(True)


    # Les gouvernements police tourner la planche à billet, c'est l'heure de l'inflation!
    # Cette fonction enlève un au décompte de l'inflation qui arrive une fois tous les 50 tours.
    def money_printer_go_brr(self):
        # C'est l'heure de l'inflation !!!
        if self.inflation_countdown == 0:
            # On applique le changement de prix
            nouveau_prix = self.prix * (1 - self.inflation)
            # Applique le prix
            self.historique_prix.pop(0)
            self.historique_prix.append(nouveau_prix)
            self.prix = nouveau_prix
            # Nouveau compteur
            self.inflation_countdown = 50
        # Sinon, on enlève juste un à l' "inflation countdown"
        else:
            self.inflation_countdown -= 1

    # Éxécute un évènement aléatoire tous les 20 tours
    def evenement_aleatoire(self):
        if self.event_countdown == 0:
            # Choisit un évènement au hasard
            evenement = random.choices(self.evenements, [p for e, p in self.evenements])[0]
            variation = evenement[1]
            # Calcule le nouveau prix après l'évènement
            nouveau_prix = self.prix * (1 + variation)
            # Applique le prix
            self.historique_prix.pop(0)
            self.historique_prix.append(nouveau_prix)
            self.prix = nouveau_prix
            # Nouveau compteur
            self.event_countdown = 20
            # Retourne l'évènement joué
            return(evenement)
        # Sinon, on enlève 1 au compteur.
        else:
            self.event_countdown -= 1
            # Retourne false pour faire savoir qu'aucun eévènement n'a eu lieu
            return(False)

# Définition de la fonction pour dessiner la charte de trading
def draw_chart(screen, chart, color):
    for i in range(len(chart) - 1):
        pygame.draw.line(screen, color, (i * 10 + 100, fenetre[0] - chart[i] - 100), ((i + 1) * 10 + 100, fenetre[0] - chart[i + 1] - 100))


# Définition de la fonction pour dessiner l'écran du joueur
def draw_player_screen(screen):
    # affiche le menu de gauche avec les portefeuilles
    pygame.draw.rect(screen, blanc, [fenetre[1] - 300, 0, 300, fenetre[0]])
    text1 = police.render('Solde ...', True, noir)
    screen.blit(text1, [fenetre[1] - 280, 25])
    text2 = police.render('Pycoin | Perso | Emprunté', True, noir)
    screen.blit(text2, [fenetre[1] - 280, 50])
    # Affiche le solde de toutes les monnaies, à la fois dans le portefeuille de pycoin, et le portefeuille personnel
    i = 0
    for monnaie in liste_monnaies:
        text = police.render(str(monnaie.portefeuille_pycoin) + "$ " + str(monnaie.portefeuille) + "$ " + str(monnaie.emprunte), True, noir)
        screen.blit(text, [fenetre[1] - 280, 100 + i * 50])
        i += 1
    # Calcul de la somme des monnaies des cryptomonnaies, des fiat et du total, à la fois pycoin et perso et emprunté de pycoin
    somme_monaie_crypto = 0
    for crypto in liste_monnaies[2:]:
        somme_monaie_crypto += crypto.prix * crypto.portefeuille
    somme_monaie_crypto_pycoin = 0
    for crypto in liste_monnaies[2:]:
        somme_monaie_crypto_pycoin += crypto.prix * crypto.portefeuille_pycoin
    somme_monnaie_fiat = Dollar.portefeuille + (Euro.portefeuille * Euro.prix)
    somme_monnaie_fiat_pycoin = Dollar.portefeuille_pycoin + (Euro.portefeuille_pycoin * Euro.prix)
    total = somme_monaie_crypto + somme_monnaie_fiat
    total_pycoin = somme_monaie_crypto_pycoin + somme_monnaie_fiat_pycoin
    somme_monaie_crypto_empruntee = 0
    for crypto in liste_monnaies[2:]:
        somme_monaie_crypto_empruntee += crypto.prix * crypto.emprunte
    somme_monnaie_fiat_empruntee = Dollar.emprunte + (Euro.emprunte * Euro.prix)
    total_emprunte = somme_monnaie_crypto_empruntee + somme_monnaie_fiat_empruntee
    # Affichage des totaux
    text = police.render('Total Crypto: ' + str(somme_monaie_crypto_pycoin) + "$ " + str(somme_monaie_crypto) + "$  " + str(monnaie.emprunte) + '$', True, noir)
    screen.blit(text, [fenetre[1] - 280, 100 + i * 50])
    i += 1
    text = police.render('Total Fiat: ' + str(somme_monnaie_fiat_pycoin) + '$ ' + str(somme_monnaie_fiat) + '$ ' + str(somme_monnaie_fiat_empruntee) + '$ ', True, noir)
    screen.blit(text, [fenetre[1] - 280, 100 + i * 50])
    i += 1
    text = police.render('Total: ' + str(total_pycoin) + '$ ' + str(total) + '$ ' + str(total_emprunte) + '$ ', True, noir)
    screen.blit(text, [fenetre[1] - 280, 100 + i * 50])


# Temporaire, a effacer une fois le programme confirmé
def main_menu_init_temp():
    global noir, blanc, or_, police, fenetre, liste_monnaies, current_crypto, screen
    # Initialisation de Pygame
    pygame.init()

    # Définition des couleurs
    noir = (0, 0, 0)
    blanc = (255, 255, 255)
    or_ = blanc

    # Définition des dimensions de la fenêtre de jeu
    fenetre = (1920, 1080)
    screen = pygame.display.set_mode(fenetre)

# Initialise le menu principal
def main_menu_init():
    # Importe les variables
    global noir, blanc, or_, police, fenetre, liste_monnaies, current_crypto, screen, chart, clock, continuer
    global Dollar, Euro, Bitcoin, Ethereum, Litecoin, Dogecoin, Shiba, IOTA, Ergo, Isotopec 
    # Définition de la police de caractères
    police = pygame.font.Font('police.ttf', 25)
    # Création de toutes les cryptomononnaies
    Dollar = Monnaie("Dollar", "USD", 1, 0)
    Euro = Monnaie("Euro", "EUR", 1.2, 0)
    Bitcoin = Monnaie("Bitcoin", "BTC", 50000, 0.2)
    Ethereum = Monnaie("Ethereum", "ETH", 2000, 0.7)
    Litecoin = Monnaie("Litecoin", "LTC", 100, 1.4)
    Dogecoin = Monnaie("Dogecoin", "DOGE", 0.2, 5)
    Shiba = Monnaie("Shiba", "INU", 0.02, 50)
    IOTA = Monnaie("IOTA", "IOTA", 2.6, 2.3)
    Ergo = Monnaie("Ergo", "ERGO", 14, 1.7)
    Isotopec = Monnaie("Isotopec", "ISO", 0.009, 2.7)
    # Création de la liste des monnaies
    liste_monnaies = [Dollar, Euro, Bitcoin, Ethereum, Litecoin, Dogecoin, Shiba, IOTA, Ergo, Isotopec]
    # Cyrpto dont le grpahe est actuellement affiché
    current_crypto = Bitcoin
    # Définition des variables pour la charte de trading
    chart = current_crypto.historique_prix
    chart[-1] = current_crypto.prix
    # Boucle du jeu
    continuer = True
    # Impote l'horloge
    clock = pygame.time.Clock()


# Définition de la fonction principale
def main_menu():
    global noir, blanc, or_, police, fenetre, liste_monnaies, current_crypto, screen, chart, clock, continuer
    global Dollar, Euro, Bitcoin, Ethereum, Litecoin, Dogecoin, Shiba, IOTA, Ergo, Isotopec
    # Boucle du jeu
    while continuer:
        # Gestion des événements
        for event in pygame.event.get():
            # Si l'utilisateur veut quitter, on quitte
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                # Si l'utilisateur clique sur un bouton de monnaie, on passe à cette monnaie
                if X:
                    current_crypto = X
                    chart = current_crypto.historique_prix
                    chart[-1] = current_crypto.prix
        # Mise à jour du prix de chaque monnaie, de l'inflation et des évènements
        for monnaie in liste_monnaies:
            monnaie.faire_varier_prix()
            monnaie.money_printer_go_brr()
            event = monnaie.evenement_aleatoire() 
            # Si un évènement a eu lieu,
            if event != False:
                notification = police.render("Évènement sur "+str(monnaie.nom_court)+":\n"+str(event[0])+"\nInfluence + "+str(event[1] * 100)+" %.", True, noir)
                notification_rect = pygame.Rect(int((fenetre[0] - notification.get_width()) / 2), 25, notification.get_width() + 25, notification.get_height() + 25)
                pygame.draw.rect(screen, or_, notification_rect, 0, 25)
                screen.blit(notification, (notification_rect.x + 5, notification_rect.y + 5))
                # Attends trois secondes, puis la notification disparait
                pygame.time.wait(3000)
        # Affichage de l'interface utilisateur droite
        pygame.draw.rect(screen, blanc, [0, 0, 100, fenetre[0]])
        # Affichage des boutons des monnaies dans la barre
        i = 0
        for monnaie in liste_monnaies:
            monnaie_bouton = police.render(monnaie.nom_court, True, or_)
            monnaie_bouton_rect = pygame.Rect(10, (50 + i * 50), monnaie_bouton.get_width() + 10, monnaie_bouton.get_height() + 10)
            pygame.draw.rect(screen, noir, monnaie_bouton_rect, 0, 10)
            screen.blit(monnaie_bouton, (monnaie_bouton_rect.x + 5, monnaie_bouton_rect.y + 5))
            i += 1
       
        # Mise à jour du graphe
        chart.pop(0)
        chart.append(current_crypto.prix)
        # Dessin de l'écran de jeu
        screen.fill(noir)
        draw_chart(screen, chart, or_)
        draw_player_screen(screen)

        # Actualisation de la fenêtre de jeu
        pygame.display.flip()

        # Limite de rafraîchissement de la fenêtre de jeu
        clock.tick(0.3)

    # Fermeture de Pygame
    pygame.quit()

main_menu_init_temp()
main_menu_init()
main_menu()
