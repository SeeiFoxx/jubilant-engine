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
        self.historique_prix = [int(prix_init)] * 60
        # Défini une première fois car on en a besoin pour dériver des prix plus tard
        self.prix = int(prix_init)
        # Faire varier le prix 60 fois pour que on ait une vraie charte au début
        for i in range(60):
        	self.faire_varier_prix()
        # Le prix initial de la monnaie, formé à partir de l'historique des prix initiaux
        self.prix = int(self.historique_prix[-1])
        # Le nombre d'unités de cette monnaie que l'on a, initialisé à 0
        self.portefeuille = 0
        # Le nombre d'unités de cette monnaie que le portefeuille des utilisateurs des services pycoins a actuellement.
        # Initialisé à un nombre aléatoire entre 1 000 et 1 000 000.
        self.portefeuille_pycoin = int(randint(10, 1000))
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
                ('Réglementation favorable', True),
                ('Attaque informatique', False),
            ]
        # Sinon, c'est une crypto qui subit une déflation (fixée à 0.1 = 10% par 50
        # tours soit 0.2% par tour pour des raisons de simplicité, négative car l'inflation est enlevée)
        else:
            self.inflation = -0.1
            # Évènements de crypto (un peu exotiques...)
            self.events = [
                ('Réglementation favorable', True),
                ('Réglementation défavorable', False),
                ('Ton cousin Kevin en a acheté', False),
                ('Décision judiciaire favorable', True),
                ('Décision judiciaire défavorable', False),
                ('Elon Musk Tweete', True),
                ('POV tes parents découvrent ton wallet de 200K et tu dois tout vendre comme une certaine personne dans ce groupe', False),
                ('Innovation technologique de fou', True),
                ('Abdelmajid pirate Kyian et prends tout son argent', True),
                ('Kyian a ligoté Abdelmajid dans sa cave, il peut plus trader', False),
                ('Romain fait un trading copy de mon compte', True),
                ('Hugo vends des dessins de qualité en NFT', True)
            ]

    # Méthode pour acheter
    def acheter(self, monnaie2 , quantite):
        quantite = int(quantite)
        # Le prix total de l'achat en dollars
        prix_total_achat = int(quantite * self.prix)
        # On checke si on a assez de l'autre monnaie pour acheter
        if prix_total_achat > int(monnaie2.portefeuille * monnaie2.prix):
            # Si ce n'est pas le cas, on retourne False.
            return(False)
        # On enlève le montant de monnaie dans le portefeuille de la monnaie qu'on vends pour acheter la nouvelle monnaie
        monnaie2.portefeuille -= int(prix_total_achat / monnaie2.prix)
        # On ajoute la nouvelle monnaie achetée dans le portefeuille correspondant.
        self.portefeuille += quantite
        # On retourne True pour signaler que l'opération s'est bien passée.
        return(True)
    
    # Méthode pour vendre
    def vendre(self, monnaie2, quantite):
        quantite = int(quantite)
        # Checke si on a assez de monnaie pour mener à bien la transaction
        if self.portefeuille < quantite:
            return(False)
        # On calcule le prix total de la vente
        prix_total_vente = int(quantite * self.prix)
        # On enlève les coins vendus du portefeuille de cette monnaie
        self.portefeuille -= quantite
        # On mets les coins achetés dans le portefeuille de l'autre monnaie
        monnaie2.portefeuille += int(prix_total_vente / monnaie2.prix)
    
    # S'occupe de faire varier le prix d'une monnaie en fonction de sa volatilité
    def faire_varier_prix(self):
        # Si on a une volatilité (pas une fiat mdr) et que la monnaie n'est pas morte
        if self.volatilite > 0 and self.prix != 0:
            variation = random.uniform(-(self.volatilite), (self.volatilite))
            nouveau_prix = int(self.prix * (1 + variation))
            # Si le prix tombe à 0, on considère que la monnaie est morte et on liquide tous les wallets.
            if (int(nouveau_prix) == 0) or (int(nouveau_prix) < 0):
                self.emprunte = 0
                self.prix = 0
                self.portefeuille = 0
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
        montant = int(montant)
        if montant > monnaie.portefeuille_pycoin:
            # On retourne False pour montrer que la transaction a échoué
            return(False)
        # Si on a assez s'argent, on autorise le prêt
        else:
            monnaie.portefeuille_pycoin -= montant
            monnaie.portefeuille += montant
            monnaie.emprunte += montant
            # On retourne true pour montrer que la transaction a été validée
            return(True)
        
	# Méthode pour rembourser un emprunt
    def remboursement(self, monnaie, montant):
        montant = int(montant)
        # Si on rends plus que ce qu'on a emprunté, ça crashe
        if int(monnaie.emprunte) > montant:
            return(False)
        # Si on a pas le montant
        elif monnaie.portefeuille < montant:
            return(False)
        else:
            monnaie.emprunt -= montant
            monnaie.portefeuille_pycoin += montant
            monnaie.portefeuille -= montant
            return(True)


    # Les gouvernements police tourner la planche à billet, c'est l'heure de l'inflation!
    # Cette fonction enlève un au décompte de l'inflation qui arrive une fois tous les 50 tours.
    def money_printer_go_brr(self):
        # C'est l'heure de l'inflation !!!
        if self.inflation_countdown == 0:
            # On applique le changement de prix
            nouveau_prix = int(self.prix * (1 - self.inflation))
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
            randomnumber = randint(0, len(self.events)-1)
            evenement = self.events[randomnumber]
            # Si la variation doit être positive, on fait varier le prix aléatoirement
            # dans le positif entre 0 et 10%
            if evenement[1] == True:
                self.prix += self.prix * (randint(0, 10)/100)
            else:
                self.prix -= self.prix * (randint(0, 10)/100)
            # Applique le prix dans l'historique
            self.historique_prix.pop(0)
            self.historique_prix.append(self.prix)
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
def draw_chart(screen, chart):
    global blanc
    for i in range(len(chart) - 1):
        pygame.draw.line(screen, blanc, (i * 10 + 100, fenetre[0] - chart[i] - 100), ((i + 1) * 10 + 100, fenetre[0] - chart[i + 1] - 100))


# Définition de la fonction pour dessiner l'écran du joueur
def draw_player_screen(screen):
    # affiche le menu de gauche avec les portefeuilles
    pygame.draw.rect(screen, blanc, [fenetre[0]-450, 0, 450, fenetre[1]])
    text1 = police.render('Nom_crypto :', True, noir)
    screen.blit(text1, [fenetre[0]-440, 25])
    text2 = police.render('Solde Pycoin | Solde Perso | Solde Emprunté', True, noir)
    screen.blit(text2, [fenetre[0]-440, 50])
    text3 = police.render('Wallet Pycoin | Wallet Perso | Wallet Emprunté', True, noir)
    screen.blit(text3, [fenetre[0]-440, 75])
    # Affiche le solde et le nombre de coins dans les portefeuilles de toutes les monnaies,
    # à la fois dans le portefeuille de pycoin, et le portefeuille personnel et de ce qu'on a emprunté
    i = 0
    for monnaie in liste_monnaies:
        text_ = police.render(monnaie.nom_court + " :", True, noir)
        text = police.render(str(monnaie.portefeuille_pycoin * monnaie.prix) + "$ " + str(monnaie.portefeuille * monnaie.prix) + "$ " + str(monnaie.emprunte * monnaie.prix) + "$ ", True, noir)
        text2 = police.render(str(monnaie.portefeuille_pycoin) + " " + monnaie.nom_court + " " + str(monnaie.portefeuille) + " " + monnaie.nom_court + " " + str(monnaie.emprunte) + " " + monnaie.nom_court, True, noir)
        screen.blit(text_, [fenetre[0]-440, 125 + i * 30])
        i += 1
        screen.blit(text, [fenetre[0]-440, 125 + i * 30])
        i += 1
        screen.blit(text2, [fenetre[0]-440, 125 + i * 30])
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
    somme_monnaie_crypto_empruntee = 0
    for crypto in liste_monnaies[2:]:
        somme_monnaie_crypto_empruntee += crypto.prix * crypto.emprunte
    somme_monnaie_fiat_empruntee = Dollar.emprunte + (Euro.emprunte * Euro.prix)
    total_emprunte = somme_monnaie_crypto_empruntee + somme_monnaie_fiat_empruntee
    # Affichage des totaux
    text = police.render('Total Crypto: ' + str(somme_monaie_crypto_pycoin) + "$ " + str(somme_monaie_crypto) + "$  " + str(monnaie.emprunte) + '$', True, noir)
    screen.blit(text, [fenetre[0]-440, 100 + i * 50])
    i += 1
    text = police.render('Total Fiat: ' + str(somme_monnaie_fiat_pycoin) + '$ ' + str(somme_monnaie_fiat) + '$ ' + str(somme_monnaie_fiat_empruntee) + '$ ', True, noir)
    screen.blit(text, [fenetre[0]-440, 100 + i * 50])
    i += 1
    text = police.render('Total: ' + str(total_pycoin) + '$ ' + str(total) + '$ ' + str(total_emprunte) + '$ ', True, noir)
    screen.blit(text, [fenetre[0]-440, 100 + i * 50])


# Temporaire, a effacer une fois le programme confirmé
def main_menu_init_temp():
    global noir, blanc, or_, police, fenetre, liste_monnaies, current_crypto, screen
    # Initialisation de Pygame
    pygame.init()

    # Définition des couleurs
    noir = (0, 0, 0)
    blanc = (255, 255, 255)
    or_ = (228, 192, 27)

    # Définition des dimensions de la fenêtre de jeu
    fenetre = (1920, 1080)
    screen = pygame.display.set_mode(fenetre)


def FTX_scenario():
    global blanc, noir, or_, police, fenetre, screen
     # Chargement des images
    images = [pygame.image.load("image1.png"), pygame.image.load("image2.png"), pygame.image.load("image3.png")]
    # Choix aléatoire d'une image
    image_index = random.randint(0, 2)
    image = images[image_index]
    # Création du texte
    text = police.render("Bravo, vous avez perdu! Vous avez les qualités pour diriger un exchange et finir en prison tout comme Sam Bankman Fried!", True, blanc)
    text_rect = text.get_rect()
    text_rect.center = (fenetre[0] // 2, fenetre[1] // 3)
    # Création des boutons
    quit_button = pygame.Rect(fenetre[0] // 4, fenetre[1] // 2, 100, 50)
    replay_button = pygame.Rect((3 * fenetre[0]) // 4, fenetre[1] // 2, 100, 50)
    # Création des boutons
    quit_button = pygame.Rect(fenetre[0] // 4, fenetre[1] // 2, 100, 50)
    replay_button = pygame.Rect((3 * fenetre[0]) // 4, fenetre[1] // 2, 100, 50)
    # Boucle principale du programme
    continuer = True
    while continuer:
        # Gestion des événements
        for event in pygame.event.get():
            # On quitte si l'utilisateur veut quitter
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                # On quitte si l'utilisateur veut quitter
                mouse_pos = pygame.mouse.get_pos()
                if quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    exit()
                # Bouton rejouer cliqué, on relance le main menu
                elif replay_button.collidepoint(mouse_pos):
                    main_menu_init()
                    main_menu()
        # Effacement de l'écran
        screen.fill(noir)
        # Affichage du texte et de l'image
        screen.blit(text, text_rect)
        screen.blit(image, (fenetre[0] // 2 - image.get_width() // 2, text_rect.bottom + 50))
        # Affichage des boutons
        pygame.draw.rect(screen, blanc, quit_button)
        quit_text = police.render("Quitter", True, noir)
        quit_text_rect = quit_text.get_rect()
        quit_text_rect.center = quit_button.center
        screen.blit(quit_text, quit_text_rect)
        pygame.draw.rect(screen, blanc, replay_button)
        replay_text = police.render("Rejouer", True, noir)
        replay_text_rect = replay_text.get_rect()
        replay_text_rect.center = replay_button.center
        screen.blit(replay_text, replay_text_rect)
        # Mise à jour de l'affichage
        pygame.display.update()




# Initialise le menu principal
def main_menu_init():
    # Importe les variables
    global noir, blanc, or_, police, fenetre, liste_monnaies, current_crypto, screen, chart, clock, continuer, police_bouton, liste_boutons, liste_boutons_rect
    global Dollar, Euro, Bitcoin, Ethereum, Litecoin, Dogecoin, Shiba, IOTA, Ergo, Isotopec 
    # Définition de la police de caractères
    police = pygame.font.Font('police.ttf', 25)
    police_bouton = pygame.font.Font('police.ttf', 35)
    # Création de toutes les cryptomononnaies
    Dollar = Monnaie("Dollar", "USD", 1, 0)
    Euro = Monnaie("Euro", "EUR", 1.2, 0)
    Bitcoin = Monnaie("Bitcoin", "BTC", 50000, 0.2)
    Ethereum = Monnaie("Ethereum", "ETH", 2000, 0.7)
    Litecoin = Monnaie("Litecoin", "LTC", 1000, 0.1)
    Dogecoin = Monnaie("Dogecoin", "DOGE", 2500, 0.4)
    Shiba = Monnaie("Shiba", "INU", 1500, 0.3)
    IOTA = Monnaie("IOTA", "IOTA", 4600, 0.3)
    Ergo = Monnaie("Ergo", "ERGO", 3400, 0.2)
    Isotopec = Monnaie("Isotopec", "ISO", 10000, 0.2)
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
    # Définit les boutons pour switcher (sur le graphe) entre différentes cryptomonnaies à gauche de l'écran
    usd_bouton = police_bouton.render(Dollar.nom_court+str(" : ")+str(Dollar.prix)+" $", True, blanc)
    usd_bouton_rect = pygame.Rect(10, (1 * 75), usd_bouton.get_width() + 10, usd_bouton.get_height() + 10)
    eur_bouton = police_bouton.render(Euro.nom_court+str(" : ")+str(Euro.prix)+" $", True, blanc)
    eur_bouton_rect = pygame.Rect(10, (2 * 75), eur_bouton.get_width() + 10, eur_bouton.get_height() + 10)
    btc_bouton = police_bouton.render(Bitcoin.nom_court+str(" : ")+str(Bitcoin.prix)+" $", True, blanc)
    btc_bouton_rect = pygame.Rect(10, (3 * 75), btc_bouton.get_width() + 10, btc_bouton.get_height() + 10)
    eth_bouton = police_bouton.render(Ethereum.nom_court+str(" : ")+str(Ethereum.prix)+" $", True, blanc)
    eth_bouton_rect = pygame.Rect(10, (4 * 75), eth_bouton.get_width() + 10, eth_bouton.get_height() + 10)
    ltc_bouton = police_bouton.render(Litecoin.nom_court+str(" : ")+str(Litecoin.prix)+" $", True, blanc)
    ltc_bouton_rect = pygame.Rect(10, (5 * 75), ltc_bouton.get_width() + 10, ltc_bouton.get_height() + 10)
    doge_bouton = police_bouton.render(Dogecoin.nom_court+str(" : ")+str(Dogecoin.prix)+" $", True, blanc)
    doge_bouton_rect = pygame.Rect(10, (6 * 75), doge_bouton.get_width() + 10, doge_bouton.get_height() + 10)
    shib_bouton = police_bouton.render(Shiba.nom_court+str(" : ")+str(Shiba.prix)+" $", True, blanc)
    shib_bouton_rect = pygame.Rect(10, (7 * 75), shib_bouton.get_width() + 10, shib_bouton.get_height() + 10)
    iota_bouton = police_bouton.render(IOTA.nom_court+str(" : ")+str(IOTA.prix)+" $", True, blanc)
    iota_bouton_rect = pygame.Rect(10, (8 * 75), iota_bouton.get_width() + 10, iota_bouton.get_height() + 10)
    ergo_bouton = police_bouton.render(Ergo.nom_court+str(" : ")+str(Ergo.prix)+" $", True, blanc)
    ergo_bouton_rect = pygame.Rect(10, (9 * 75), ergo_bouton.get_width() + 10, ergo_bouton.get_height() + 10)
    iso_bouton = police_bouton.render(Isotopec.nom_court+str(" : ")+str(Isotopec.prix)+" $", True, blanc)
    iso_bouton_rect = pygame.Rect(10, (10 * 75), iso_bouton.get_width() + 10, iso_bouton.get_height() + 10)
    liste_boutons = [usd_bouton, eur_bouton, btc_bouton, eth_bouton, ltc_bouton, doge_bouton, shib_bouton, iota_bouton, ergo_bouton, iso_bouton]
    liste_boutons_rect = [usd_bouton_rect, eur_bouton_rect, btc_bouton_rect, eth_bouton_rect, ltc_bouton_rect, doge_bouton_rect, shib_bouton_rect, iota_bouton_rect, ergo_bouton_rect, iso_bouton_rect]


# Définition de la fonction principale
def main_menu():
    global noir, blanc, or_, police, fenetre, liste_monnaies, current_crypto, screen, chart, clock, continuer, police_bouton, liste_boutons, liste_boutons_rect
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
                for i in range(len(liste_boutons_rect)):
                    # Si l'utilisateur clique sur un bouton de monnaie, on passe à cette monnaie
                    if liste_boutons_rect[i].collidepoint(event.pos):
                        current_crypto = liste_monnaies[i]
                        chart = current_crypto.historique_prix
                        chart[-1] = current_crypto.prix
        # Réinitialise l'écran
        screen.fill(noir)
        # Variable qui checke si un ftx scenario est possible
        FTX_scenario_ok = 1
        # Mise à jour du prix de chaque monnaie, de l'inflation et des évènements
        for monnaie in liste_monnaies:
            monnaie.faire_varier_prix()
            monnaie.money_printer_go_brr()
            event = monnaie.evenement_aleatoire()
            # Si toutes les monnaies ne se sont pas crashées, on ne conduit pas un FTX Scenario ending
            if int(monnaie.prix) > 0:
                FTX_scenario_ok = 0
            # Si un évènement a eu lieu, affiche une notification
            if event != False:
                notification = police.render("Évènement sur "+str(monnaie.nom_court)+":\n"+str(event[0])+"\nInfluence + "+str(event[1] * 100)+" %.", True, or_)
                notification_rect = pygame.Rect(int((fenetre[0] - notification.get_width()) / 2), 25, notification.get_width() + 25, notification.get_height() + 25)
                pygame.draw.rect(screen, blanc, notification_rect, 0, 25)
                screen.blit(notification, (notification_rect.x + 5, notification_rect.y + 5))
                # Attends trois secondes, puis la notification disparait
                pygame.time.wait(3000)
        # On fait u FTX ending si possible
        if FTX_scenario_ok == 1:
            FTX_scenario()
        # Affichage de l'interface utilisateur gauche
        pygame.draw.rect(screen, noir, [0, 0, 250, 1080])
        # Affiche le sélecteur de cryptos pour vendre
        # Options pour le sélecteur
        options = [monnaie.nom for monnaie in liste_monnaies]
        # Position du sélecteur
        selector_x = fenetre[0] - 200
        selector_y = 50
        # Position des boutons
        button_x = fenetre[0]  - 200
        button_y1 = 200
        button_y2 = 300
        # Taille des boutons
        button_width = 150
        button_height = 50
        pygame.draw.rect(screen, or_, (selector_x, selector_y, 150, 50))
        selector = police.render("Crypto à vendre", True, blanc)
        screen.blit(selector, (selector_x + 25, selector_y + 10))
        # Affichage des options dans le sélecteur
        for i, option in enumerate(options):
            option_y = selector_y + 50 + (i * 25)
            pygame.draw.rect(screen, noir, (selector_x, option_y, 150, 25))
            text = police.render(option, True, or_)
            screen.blit(text, (selector_x + 10, option_y + 5))
        # Affichage des boutons vendre et acheter
        pygame.draw.rect(screen, (255, 0, 0), (button_x, button_y1, button_width, button_height))
        text = police.render("Vendre", True, blanc)
        screen.blit(text, (button_x + 25, button_y1 + 10))
        pygame.draw.rect(screen, (0, 255, 0), (button_x, button_y2, button_width, button_height))
        text = police.render("Acheter", True, blanc)
        screen.blit(text, (button_x + 25, button_y2 + 10))
        # Regénère le bouton avec le bon prix de la monnaie
        for i in range(len(liste_boutons)):
            liste_boutons[i] = police_bouton.render(liste_monnaies[i].nom_court+str(" : ")+str(liste_monnaies[i].prix)+" $", True, blanc)
        # Affcihe tous les boutons avec les prix des cryptos
        for i in range(len(liste_boutons_rect)):
            # Définition du bouton et du rectangle de position du bouton
            bouton = liste_boutons[i]
            bouton_rect = liste_boutons_rect[i]
            # Affichage du rectangle et du bouton
            pygame.draw.rect(screen, noir, bouton_rect, 0, 10)
            screen.blit(bouton, (bouton_rect.x + 5, bouton_rect.y + 5))
        # Mise à jour du graphe
        chart.pop(0)
        chart.append(current_crypto.prix)
        # Dessin de l'écran de jeu
        draw_chart(screen, chart)
        draw_player_screen(screen)

        # Actualisation de la fenêtre de jeu
        pygame.display.update()

        # Limite de rafraîchissement de la fenêtre de jeu
        clock.tick(0.3)

    # Fermeture de Pygame
    pygame.quit()

main_menu_init_temp()
main_menu_init()
main_menu()
