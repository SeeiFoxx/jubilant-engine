# Importe pygame pour créer une GUI python et os pour récupérer le chemin
# absolu des fichiers dsous n'importe quel OS
import os
import pygame

# Initialise la fenêtre pygame
pygame.init()

# Crée une fenêtre de 1920 fois 1080 pixels
fenetre = (1920, 1080)
screen = pygame.display.set_mode(fenetre)

# Variable utilisée pour savoir si c'est la première fois qu'on lance le jeu --- A CHANGER APRES AVEC SQL
tutoriel_ = True

# Charge la vidéo de chargement
def chargement():
	global noir
	# Importe la librairie nécessaire pour jouer la vidéo dans pygame
	import moviepy.editor
	# Charge la vidéo
	video = moviepy.editor.VideoFileClip("vid_chargement.gif")
	# Convertit la vidéo en une série d'images
	frames = video.iter_frames()
	# Change le titre et l'icône de la fenêtre
	pygame.display.set_caption('Pycoin - Apprendre la finance de façon ludique')
	icon = pygame.image.load('icon_pygame.ico')
	pygame.display.set_icon(icon)
	# Initialise la clock pour limiter la vitesse de lecture
	clock = pygame.time.Clock()
	# Afficher chaque frame sur pygame
	for frame in frames:
		# Convertit l'image en une surface Pygame
		surface_video = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
		# Affiche la surface de la vidéo sur la surface Pygame principale
		screen.blit(surface_video, (0, 0))
		# Mets à jour les éléments de la fenêtre Pygame
		pygame.display.update()
		# Limite la vitesse de lecture à 60 FPS
		clock.tick(60)


# Lance un écran qui prévient de lancer le jeu en plein écran, monter le son et joue la musique
def musique():
	global blanc, noir
	# La musique est dans le domaine public. L'auteur a renoncé au copyright. 
	# music by Karl Casey @ White Bat Audio https://www.youtube.com/watch?v=rc53oCjqu-U
	# Affiche l'écran pour prévenir du lancement de la musique
	# Mets un arrière plan noir
	screen.fill(noir)
	font = pygame.font.SysFont('police.ttf', 32)
	text_1 = "Ce jeu vous propose une expérience musicale, un casque est recommandé. Si vous ne souhaitez pas entendre la musique, coupez le son."
	text_2 = "Lancement de la musique dans "
	# Affiche le texte centré
	text_surface_1 = font.render(text_1, True, blanc)
	text_surface_2 = font.render(text_2, True, blanc)
	text_rect_1 = text_surface_1.get_rect()
	text_rect_1.center = (fenetre[0] / 2, (fenetre[1] / 2) - 50)
	text_rect_2 = text_surface_2.get_rect()
	text_rect_2.center = (fenetre[0] / 2, fenetre[1] / 2)
	screen.blit(text_surface_1, text_rect_1)
	screen.blit(text_surface_2, text_rect_2)
	# Mets à jour les éléments de la fenêtre Pygame
	pygame.display.update()
	# Fait un décompte de 10 à 0 avant de lancer la musique
	for i in range(10, -1, -1):
		# Met un arrière-plan noir
		screen.fill(noir)
		# Nouveau texte
		text_3 = text_2 + str(i) + " secondes ..."
		# Affiche le texte centré avec le temps restant
		text_surface_2 = font.render(text_3, True, blanc)
		text_rect_2 = text_surface_2.get_rect()
		text_rect_2.center = (fenetre[0] / 2, fenetre[1] / 2)
		screen.blit(text_surface_1, text_rect_1)
		screen.blit(text_surface_2, text_rect_2)
		# Mets à jour les éléments de la fenêtre Pygame
		pygame.display.update()
		# Si le joueur veut quitter le jeu quitte
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
		# Attend une seconde
		pygame.time.wait(1000)
	# Réinitialise l'écran
	screen.fill(noir)
	pygame.display.update()
	# Lance la musique
	pygame.mixer.init()
	pygame.mixer.music.load("music.mp3") 
	pygame.mixer.music.play(-1,0.0)


def choix_tutoriel():
	global noir, blanc, or_
	screen.fill(noir)
	# Initialise l'horloge de Pygame
	clock = pygame.time.Clock()
	# Police de caractères
	font_undertext = pygame.font.Font('police.ttf', 23)
	font_bouton = pygame.font.Font('police.ttf', 55)
	font_title = pygame.font.Font('police.ttf', 45)
	# Boutons
	bouton_debutant = font_bouton.render("Débutant", True, noir)
	bouton_debutant_rect = pygame.Rect(int((fenetre[0] - bouton_debutant.get_width()) / 2), 250, bouton_debutant.get_width() + 10, bouton_debutant.get_height() + 10)
	bouton_apprenti = font_bouton.render("Apprenti", True, noir)
	bouton_apprenti_rect = pygame.Rect(int((fenetre[0] - bouton_apprenti.get_width()) / 2), 400, bouton_apprenti.get_width() + 10, bouton_apprenti.get_height() + 10)
	bouton_confirme = font_bouton.render("Confirmé", True, noir)
	bouton_confirme_rect = pygame.Rect(int((fenetre[0] - bouton_confirme.get_width()) / 2), 550, bouton_confirme.get_width() + 10, bouton_confirme.get_height() + 10)
	bouton_expert = font_bouton.render("Expert", True, noir)
	bouton_expert_rect = pygame.Rect(int((fenetre[0] - bouton_expert.get_width()) / 2), 700, bouton_expert.get_width() + 10, bouton_expert.get_height() + 10)
	pygame.draw.rect(screen, or_, bouton_debutant_rect, 0, 10)
	pygame.draw.rect(screen, or_, bouton_apprenti_rect, 0, 10)
	pygame.draw.rect(screen, or_, bouton_confirme_rect, 0, 10)
	pygame.draw.rect(screen, or_, bouton_expert_rect, 0, 10)
	# Textes
	text_tech_1 = font_title.render("Ce jeu sera assez technique, c'est pourquoi on vous propose un petit tutoriel avant de commencer.", True, blanc)
	text_tech_2 = font_title.render("Choisissez votre niveau en terme de connaissances:", True, blanc)
	text_tech_rect_1 = text_tech_1.get_rect()
	text_tech_rect_1.center = (fenetre[0] / 2, fenetre[1] - 100)
	text_tech_rect_2 = text_tech_2.get_rect()
	text_tech_rect_2.center = (fenetre[0] / 2, fenetre[1] - 105 - text_tech_2.get_width())
	text_debutant = font_undertext.render("C'est quoi la blockchain?", True, blanc)
	text_apprenti = font_undertext.render("J'ai besoin d'éclaircissements.", True, blanc)
	text_confirme = font_undertext.render("Je suis à l'aise.", True, blanc)
	text_expert = font_undertext.render("Le gameplay, directement!", True, blanc)
	text_debutant_rect = text_debutant.get_rect()
	text_debutant_rect.center = (fenetre[0] / 2, bouton_debutant_rect.y + 10 + bouton_debutant.get_height() + text_debutant.get_height())
	text_apprenti_rect = text_apprenti.get_rect()
	text_apprenti_rect.center = (fenetre[0] / 2, bouton_apprenti_rect.y + 10 + bouton_apprenti.get_height() + text_apprenti.get_height())
	text_confirme_rect = text_confirme.get_rect()
	text_confirme_rect.center = (fenetre[0] / 2, bouton_confirme_rect.y + 10 + bouton_confirme.get_height() + text_confirme.get_height())
	text_expert_rect = text_expert.get_rect()
	text_expert_rect.center = (fenetre[0] / 2, bouton_expert_rect.y + 10 + bouton_expert.get_height() + text_expert.get_height())
	continuer = True
	while continuer:
		# Affichage des boutons
		screen.blit(bouton_debutant, (bouton_debutant_rect.x + 5, bouton_debutant_rect.y + 5))
		screen.blit(bouton_apprenti, (bouton_apprenti_rect.x + 5, bouton_apprenti_rect.y + 5))
		screen.blit(bouton_confirme, (bouton_confirme_rect.x + 5, bouton_confirme_rect.y + 5))
		screen.blit(bouton_expert, (bouton_expert_rect.x + 5, bouton_expert_rect.y + 5))
		# Affichage des textes
		screen.blit(text_tech_1, text_tech_rect_1)
		screen.blit(text_tech_2, text_tech_rect_2)
		screen.blit(text_debutant, text_debutant_rect)
		screen.blit(text_apprenti, text_apprenti_rect)
		screen.blit(text_confirme, text_confirme_rect)
		screen.blit(text_expert, text_expert_rect)
		for event in pygame.event.get():
			# Si le joueur veut quitter, le jeu quitte
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			# Si un bouton est cliqué,
			elif event.type == pygame.MOUSEBUTTONDOWN:
				# Pour chaque bouton respectif,
				if bouton_debutant_rect.collidepoint(event.pos):
        			# On arrête le while et on va définir le niveau du joueur
					continuer = False
					niveau = 0
				elif bouton_apprenti_rect.collidepoint(event.pos):
					# On arrête le while et on va définir le niveau du joueur
					continuer = False
					niveau = 1
				elif bouton_confirme_rect.collidepoint(event.pos):
        			# On arrête le while et on va définir le niveau du joueur
					continuer = False
					niveau = 2
				elif bouton_expert_rect.collidepoint(event.pos):
        			# On arrête le while et on va définir le niveau du joueur
					continuer = False
					niveau = 3
		# Rafraîchissement de la fenêtre
		pygame.display.update()
		# Limite de FPS à 60
		clock.tick(60)
	# Une fois la boucle while terminée, on retourne le niveau du joueur
	return(niveau)



# Affiche le tutoriel, optionnellement à une certaine page
def tutoriel(page = 0):
	# Import des couleurs
	global noir, blanc, or_
	# Initialise l'horloge de Pygame
	clock = pygame.time.Clock()
	continuer = True
	# Police de caractères
	font = pygame.font.Font('police.ttf', 25)
	font_title = pygame.font.Font('police.ttf', 45)
	# Titre et contenu des différentes pages
	contenu_pages = {
	"Niveau Grand-mère:": """
Voici une version très simplifiée des concepts nécessaires pour manier le jeu. Vous pourrez toujours revenir à ce tutoriel. Si vous avez aimé le tutoriel une fois terminé, n'hésitez pas à explorer les différents niveaux de difficultés en cliquant sur le bouton "Suivant" en bas à droite pour changer de difficulté. Naviguez entre les pages du tutoriel avec les boutons, ou bien avec les flèches gauche et droite de votre clavier.

Une cryptomonnaie est une forme de monnaie numérique. Cela signifie que vous ne pouvez pas la toucher ou la voir en personne, mais vous pouvez l'utiliser pour acheter des biens et des services en ligne.
C'est comme si vous aviez de l'argent dans un portefeuille électronique sur votre téléphone, mais au lieu d'utiliser des euros ou des dollars, vous utilisez une monnaie numérique spéciale appelée "cryptomonnaie". Il y a plusieurs cryptomonnaies comme le Bitocin, l'Ethereum ou le Litecoin.
La cryptomonnaie fonctionne grâce à une technologie appelée blockchain. C'est un peu comme un grand livre de comptes que tout le monde regarde, où chaque transaction est enregistrée et vérifiée par les autres. Cela rend les transactions très sûres et difficiles à pirater.

Un effet de levier est un outil financier qui permet de multiplier les gains ou les pertes potentiels d'un investissement en utilisant des fonds empruntés. Prenons un exemple simple d'un effet de levier x10: pour acheter une maison à 100 000 euros avec 10 000 euros d'économies, grâce à l'effet de levier, tu pourrais emprunter les 90 000 euros manquants à une banque ou à un investisseur, et ainsi acheter la maison. Le but est ici d'acheter la maison et de la revendre plus tard pour plus cher, générant ainsi des bénéfices. Si tu revends la maison plus tard pour 110 000 euros, tu auras réalisé un gain de 10 000 euros, soit un retour sur investissement de 100% sur les 10 000 eurso misés au départ. Si tu avais acheté la maison sans effet de levier, en utilisant uniquement 10 000 euros, tu n'aurais gagné que 10% de retour sur investissement. Avec un effet de levier x10, on a donc multiplié les profits par 10, mais aussi les pertes potentielles. Le multiplicateur derrière l'effet de levier est donc associé à un certain risque, mais aussi à une augmentation du profit.

Cependant, il est important de comprendre que l'effet de levier fonctionne dans les deux sens : si tu avais acheté la maison à 100 000 euros avec un emprunt de 90 000 euros et que tu avais revendu la maison pour seulement 90 000 euros, tu aurais perdu tes 10 000 euros d'investissement initial, ainsi que les intérêts de l'emprunt, perdant 100% de ton investissement (perte multipliée par 10 aussi). Il est donc important de bien comprendre les risques liés à l'utilisation de l'effet de levier et de ne l'utiliser que si tu es prêt à en assumer les conséquences.
							""",
	"Niveau Apprenti Page 1/2:": """
Le tutoriel peut sembler un peu long, mais accrochez-vous: il a été simplifié au maximum pour vous permettre de saisir en grande partie un sujet très complexe! Ne vous inquiétez pas trop, vous n'avez pas à tout retenir à la lettre, ayez juste une idée de ce qu'est chaque concept avant de commencer. Vous pourrez toujours revenir à ce tutoriel. Si le tutoriel est trop compliqué, ou si vous avez aimé le tutoriel une fois terminé, n'hésitez pas à explorer les différents niveaux de difficultés en cliquant sur le bouton en haut à droite pour changer de difficulté. Naviguez entre les pages du tutoriel avec les boutons, ou bien avec les flèches gauche et droite de votre clavier.

La blockchain est une technologie qui permet de stocker et de transférer des données en toute sécurité, sans avoir besoin d'un intermédiaire. Elle est basée sur un système de blocs liés entre eux par une formule mathématique. Chaque bloc contient des informations et un identifiant unique appelé "hash". Lorsqu'un nouveau bloc est ajouté à la chaîne, il est lié au bloc précédent par son hash. Cela garantit l'intégrité et la sécurité des données, car si un bloc est modifié, tous les blocs suivants doivent également être modifiés pour que la chaîne reste valide.

Par exemple, imaginez que vous voulez transférer de l'argent à un ami. Avec la blockchain, vous pouvez effectuer cette transaction directement, sans passer par une banque ou un tiers de confiance. La transaction est enregistrée dans un bloc, qui est ensuite ajouté à la chaîne. Tout le monde peut voir la transaction, mais personne ne peut la modifier.

Les cryptomonnaies sont des monnaies numériques qui sont basées sur la technologie de la blockchain. Elles sont décentralisées, ce qui signifie qu'elles ne sont contrôlées par aucune autorité centrale, comme une banque centrale. Les transactions sont enregistrées dans la blockchain et sont sécurisées par un système de cryptographie. Les cryptomonnaies les plus connues sont le Bitcoin, l'Ethereum et le Litecoin. Elles sont toutes déflationnistes, c'est à dire qu'elles ont une tendance à se raréfier au cours du temps. Ceci est bien l'inverse de l'inflation, qui fait perdre de la rareté à une monnaie au cours du temps, d'où l'augmentation de prix sur les articles du quotidien. Comme les cryptomonnaies sont limitées en nombre d'unités émises, contrairement aux monnaies centrales, on est surs qu'elles sont déflationnistes, car au cours du temps, on obtient de moins en moins facilement ces cryptomonnaies, ce qui crée leur déflation.

Le portefeuille de cryptomonnaie est un programme informatique qui permet de stocker, d'envoyer et de recevoir des cryptomonnaies. Il est similaire à un compte bancaire, mais sans intermédiaire. On peut aussi recevoir des tokens, qui sont juste des jetons n'étant pas de la crytpomonnaie, un peu comme les jetons pour laver sa voiture qui trainent dans votre portefeuille.

Les noeuds sont des ordinateurs qui participent au réseau de la blockchain. Ils téléchargent et stockent une copie de la blockchain complète, et vérifient chaque transaction pour s'assurer qu'elle est valide. Les noeuds sont essentiels au fonctionnement de la blockchain, car ils garantissent la sécurité et la validité des transactions.

Les mineurs sont des utilisateurs du réseau qui vérifient les transactions et ajoutent de nouveaux blocs à la blockchain. Les mineurs effectuent des calculs complexes pour résoudre des problèmes mathématiques qui permettent de sécuriser le réseau et de valider les transactions. En retour, les mineurs reçoivent des récompenses sous forme de tokens, qui se raréfient au cours du temps, causant la déflation des cryptomonnaies.
						""",
	"Niveau Apprenti Page 2/2:": """
Les logiciels open source sont des programmes informatiques dont le code source est ouvert et disponible pour que tout le monde puisse le voir et le modifier. Les blockchains et les cryptomonnaies sont souvent basées sur des logiciels open source, ce qui permet à la communauté de développeurs de contribuer à l'amélioration et au développement de la technologie.

La décentralisation est un principe fondamental de la blockchain et des cryptomonnaies. Contrairement aux systèmes centralisés, où les données et les décisions sont contrôlées par une seule entité, la blockchain est décentralisée, ce qui signifie qu'elle est répartie sur un grand nombre de noeuds ou d'ordinateurs à travers le monde. Cela rend la blockchain plus résiliente aux attaques et aux pannes, car il n'y a pas de point de défaillance unique. La décentralisation permet également de garantir la sécurité et la transparence des transactions sur la blockchain.

Les transactions sur la blockchain sont des échanges de valeur entre des utilisateurs du réseau. Chaque transaction est vérifiée par des mineurs ou des noeuds pour s'assurer que les fonds sont disponibles et que la transaction est valide. Les transactions sont ensuite ajoutées à un bloc dans la blockchain, ce qui garantit leur immuabilité et leur transparence.

La sécurité de la blockchain est assurée par la cryptographie et la décentralisation. Chaque transaction est cryptée à l'aide d'un algorithme de chiffrement, ce qui la rend pratiquement impossible à falsifier. La décentralisation de la blockchain signifie qu'il n'y a pas de point unique de contrôle, ce qui rend la blockchain plus résistante aux attaques et aux pannes.

Les avantages de la blockchain sont nombreux. Elle permet de réaliser des transactions plus rapidement, plus facilement et à moindre coût que les systèmes traditionnels. Elle offre également une sécurité accrue grâce à la cryptographie et à la décentralisation, ce qui rend les transactions plus fiables et plus transparentes. Enfin, la blockchain peut être utilisée dans une grande variété de domaines, comme les finances, la logistique, l'immobilier, l'assurance, les soins de santé, et bien d'autres encore.

Prenons un exemple simple: pour acheter un livre en ligne, habituellement, on devrait passer par une plateforme comme Amazon, leur donner nos informations personnelles au passage, tout ça pour commander un livre. À contrario, avec la blockchain, on peux acheter directement auprès du propriétaire du livre (ici l'éditeur du livre) sans avoir à passer par un tiers (ici Amazon). La transaction est enregistrée sur la blockchain et on peux suivre le processus en temps réel. De plus, pas besoin de révéler quoi que ce soit à propos de toi! Le vendeur ne saura pas qui tu es.

Les cryptomonnaies sont plus sécurisées, plus rapides et plus transparentes que les monnaies fiat étatiques classiques. Elles permettent également aux utilisateurs de contrôler leur propre argent sans l'intervention d'un tiers.
								""",
	"Niveau Confirmé Page 1/2:": """
Vous pourrez toujours revenir à ce tutoriel. Si le tutoriel est trop compliqué, ou sivous avez aimé le tutoriel une fois terminé, n'hésitez pas à explorer les différents niveaux de difficultés en cliquant sur le bouton en haut à droite pour changer de difficulté. Naviguez entre les pages du tutoriel avec les boutons, ou bien avec les flèches gauche et droite de votre clavier.

Les tokens sont des unités de valeur qui sont échangées sur la blockchain. Ils peuvent être utilisés pour représenter des actifs physiques, comme de l'or ou de l'immobilier, ou des actifs numériques, comme des jetons de jeux vidéo. Les tokens sont créés à l'aide de "smart contracts", qui sont des programmes informatiques qui s'exécutent automatiquement lorsque certaines conditions sont remplies.

Le portefeuille contient une clé privée, qui est utilisée pour signer les transactions, et une clé publique, qui est utilisée pour recevoir des paiements, comme dans les systèmes de chiffrement asymétriques. Le chiffrement asymétrique est une technique de cryptage qui utilise deux clés différentes pour chiffrer et déchiffrer les données. Dans la blockchain, les utilisateurs ont deux clés: une clé publique et une clé privée. La clé publique est visible par tous et permet à d'autres utilisateurs de vous envoyer des fonds. La clé privée, en revanche, doit être gardée secrète et permet de débloquer les fonds que vous avez reçus. Cette méthode de cryptage assure la sécurité de vos fonds sur la blockchain.

Les logiciels open source sont des programmes informatiques dont le code source est ouvert et disponible pour que tout le monde puisse le voir et le modifier. Les blockchains et les cryptomonnaies sont souvent basées sur des logiciels open source, ce qui permet à la communauté de développeurs de contribuer à l'amélioration et au développement de la technologie. Cela permets aussi d'être sûr de la technologie dans laquelle on place son argent, en vérifiant l'abscence de backdoor ou autre activité non désirée.

Le staking est un processus qui permet aux détenteurs de cryptomonnaies de participer au réseau de la blockchain et de gagner des récompenses. En stakant leurs cryptomonnaies, c'est à dire en s'engageant à ne pas toucher à leurs cryptomonnaies en les verrouillant dans des portefeuilles spécifiques, les utilisateurs peuvent aider à sécuriser le réseau et à valider les transactions à la place des mineurs. Dans ce nouveau modèle appelé Proof Of Stake, les stakeurs reçoivent une partie des frais de transaction et des nouvelles cryptomonnaies créées en échange du staking, à la place des mineurs qui existent dans le modèle le plus utilisé, le Proof Of Work. Le POS est souvent bien plus écologique que le POW car il n'engendre pas la dépense énergétique collatérale due au hardware des mineurs.
						""",
	"Niveau Confirmé Page 2/2:": """
Le principe de signature numérique dans la blockchain est également un élément important. La signature numérique est un procédé qui permet d'authentifier la source d'une information ou d'une transaction. Dans la blockchain, chaque transaction est signée avec la clé privée de l'utilisateur. Cette signature numérique garantit l'authenticité de la transaction et empêche toute modification frauduleuse.

Le hash des blocs dans la blockchain est une autre notion clé. Le hash est un algorithme qui prend en entrée des données et génère une empreinte unique de ces données. Dans la blockchain, chaque bloc contient des données sur les transactions récentes, ainsi qu'un hash qui représente l'ensemble de ces données. Ce hash permet de s'assurer que les données du bloc n'ont pas été altérées, car si une seule donnée est modifiée, le hash du bloc entier change également.

Enfin, les smart contracts sont des programmes autonomes qui exécutent automatiquement des conditions prédéfinies lorsqu'elles sont remplies. Ils sont écrits dans un langage de programmation spécifique et sont stockés sur la blockchain. Les smart contracts sont utilisés pour automatiser des processus et garantir l'exécution de contrats sans avoir besoin d'un tiers de confiance. Par exemple, un smart contract peut être utilisé pour automatiser la vente d'un bien lorsque les conditions de paiement sont remplies. C'est ce qui rends la blockchain si versatile et si apte à résoudre n'import quel problème dont l'origine est la confiance mutuelle. Tout cela grâce au pouvoir quasiment magique des mathématiques!

La gouvernance de la blockchain est un élément clé de son fonctionnement. Contrairement aux systèmes traditionnels où il y a un acteur central qui contrôle toutes les actions, la blockchain est décentralisée, ce qui signifie que les utilisateurs ont un certain contrôle sur le système. La gouvernance de la blockchain peut prendre différentes formes selon les protocoles. Par exemple, certains protocoles de blockchain sont gérés par des communautés de développeurs, qui décident des mises à jour et des changements à apporter au protocole. D'autres protocoles peuvent être gérés par des fondations ou des entreprises, qui ont plus de contrôle sur les décisions prises. Quelle que soit la forme de gouvernance, le but est de maintenir le consensus et la stabilité du système.

En ce qui concerne les différentes architectures de la blockchain, il existe deux types principaux : la blockchain publique et la blockchain privée. La blockchain publique est accessible à tous, et n'importe qui peut rejoindre le réseau et participer à la validation des transactions. Cela la rend transparente et résistante à la censure, mais peut également entraîner une moindre confidentialité. La blockchain privée, quant à elle, est limitée à un groupe spécifique de personnes ou d'organisations qui ont été autorisées à y accéder. Cela peut offrir une plus grande confidentialité, mais peut également rendre le système moins résistant à la censure. Il y a également des protocoles de blockchain qui combinent des éléments de ces deux architectures pour créer des réseaux hybrides. Par exemple, certains protocoles peuvent permettre aux utilisateurs de créer des chaînes latérales privées, tout en conservant une chaîne principale publique.
								""",
	}
	# Boucle de jeu, les boutons précédents et suivants s'activent soit quand cliqués
	# soit quand la flèche gauche ou droite est pressée
	while continuer:
		# On surveille les évènements
		for event in pygame.event.get():
			# Si l'utilisateur veut quitter, on quitte
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			# Page précédente ou suivante en fonction de la flèche gauche ou droite si pressée
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					# Sauf pour la première page,
					if page != 0:
						# On va à la page d'avant
						page -= 1
				elif event.key == pygame.K_RIGHT:
					# Pour toutes les pages sauf la dernière,
					if page != len(contenu_pages)-1:
						page += 1
					# Si on est déjà à la dernière page,
					else:
						# On quitte la boucle et continue le jeu après le tutoriel
						continuer = False
			# Si un bouton est cliqué,
			elif event.type == pygame.MOUSEBUTTONDOWN:
				# bouton précédent: page précédente
				if page != 0:
					if bouton_precedent_rect.collidepoint(event.pos):
							page -= 1
				# Bouton suivant: page suivante
				if page != len(contenu_pages)-1:
					if bouton_suivant_rect.collidepoint(event.pos):
							page += 1
				# Bouton quitter: on continue après le tutoriel
				if bouton_quitter_rect.collidepoint(event.pos):
					continuer = False
		screen.fill(noir)
		# Affichage du titre, on récupère la clé qui correspond à la page actuelle
		titre = font_title.render(list(contenu_pages.keys())[page], True, or_)
		screen.blit(titre, (100, 100))
		# Découpe et affichage du texte, on récupère la valeur qui correspond à la page actuelle
		text = list(contenu_pages.values())[page]
		# découpage du texte en mots
		words = text.split()
		# liste pour stocker les lignes de texte
		lines = []
		# initialisation de la première ligne de texte
		line = words[0]
		# ajout des mots à la ligne de texte jusqu'à atteindre la limite de 180 caractères
		for word in words[1:]:
			if len(line + " " + word) < 165:
				line += " " + word
			else:
				lines.append(line)
				line = word
		# ajout de la dernière ligne de texte
		if line:
			lines.append(line)
		# Affichage des lignes de texte
		y = 200
		for line in lines:
			text_surface = font.render(line, True, or_)
			screen.blit(text_surface, (100, y))
			y += text_surface.get_height()
		# Affichage des boutons précédent et suivant qui passent d'une page à l'autre quand cliqués
		# On affiche le bouton précédent pour toutes les pages sauf la première page
		if page != 0:
			bouton_precedent = font.render("Précédent", True, noir)
			bouton_precedent_rect = pygame.Rect(100, fenetre[1] - 100, bouton_precedent.get_width() + 10, bouton_precedent.get_height() + 10)
			pygame.draw.rect(screen, or_, bouton_precedent_rect, 0, 10)
			screen.blit(bouton_precedent, (bouton_precedent_rect.x + 5, bouton_precedent_rect.y + 5))
		# Si le bouton suivant est celui de la dernière page, on le remplace par le texte continuer
		# pour signifier qu'on va quitter le tutoriel.
		if page != len(contenu_pages)-1:
			bouton_suivant = font.render("Suivant", True, noir)
			bouton_suivant_rect = pygame.Rect(fenetre[0] - bouton_suivant.get_width() - 100, fenetre[1] - 100, bouton_suivant.get_width() + 10, bouton_suivant.get_height() + 10)
			pygame.draw.rect(screen, or_, bouton_suivant_rect, 0, 10)
			screen.blit(bouton_suivant, (bouton_suivant_rect.x + 5, bouton_suivant_rect.y + 5))
		# Affichage du bouton quitter
		bouton_quitter = font.render("Quitter le tutoriel", True, noir)
		bouton_quitter_rect = pygame.Rect(fenetre[0] - 105 - (2*bouton_quitter.get_width()), fenetre[1] - 100, bouton_quitter.get_width() + 10, bouton_quitter.get_height() + 10)
		pygame.draw.rect(screen, or_, bouton_quitter_rect, 0, 10)
		screen.blit(bouton_quitter, (bouton_quitter_rect.x + 5, bouton_quitter_rect.y + 5))
		# Rafraîchissement de la fenêtre
		pygame.display.update()
		# Limite de FPS à 60
		clock.tick(60)


# Lance la suite du tutoriel, en fonction du niveau
def tutoriel_suite(niveau = 0):
	# Arrière plan noir
	screen.fill(noir)
	# Charge l'arrière plan
	# Image libre d'utilisation, source: 
	# https://pixabay.com/illustrations/mountains-landscape-sunset-dusk-55067/
	# et https://pixabay.com/vectors/mountains-panorama-forest-mountain-1412683/
	background = pygame.image.load('mountain.png').convert()
	# Affiche un fond noir
	screen.fill(noir)
	# Mets à jour les éléments de la fenêtre pygame
	pygame.display.update()
	# Initialise la clock pour limiter la vitesse de lecture
	clock = pygame.time.Clock()
	# On affiche l'animation
	# Statistiques de l'animation                                                 
	duree_animation = 5                                                           
	fps = 60                                                                      
	total_frames = duree_animation * fps                                      
	for frame in range(total_frames):                                             
		# Calculer la progression du dégradé                                      
		progres = frame / total_frames                                            
		# Affichage d'un rectangle noir                                           
		pygame.draw.rect(screen, noir, (0, 0, 1920, 1080))                        
		# Affichage du blend entre la couleur et l'image d'arrière-plan           
		alpha = int(255 * progres)
		background.set_alpha(alpha)
		screen.blit(background, (0, 0))
		pygame.display.update()
		pygame.time.wait(1000 // fps)
	# On mets le fond d'écran définitif
	screen.blit(background, (0, 0))
	# Pour un niveau débutant,
	if niveau == 0:
		text = "Test niveau 0"
	# Pour un niveau apprenti,
	if niveau == 1:
		text = "2060. Les taux d'inflation des monnaies étatiques (dites fiat) ont fait fuir les populations du monde vers les cryptomonnaies. Ces monnaies digitales, sécurisées et anonymes, qui étaient pour la plupart considérées comme des blagues, deviennent un enjeu majeur au niveau mondial de par leur propriétés déflationnistes par nature. À la tête des fameux Pycoin Services, la plus grade plateforme d'échange anonyme de cryptommonaies, se tient un mystérieux individu: EL. Presque aussi mythique que le grand Satoshi Nakamoto, beaucoup de rumeurs circulent à son sujet. On dit qu'il aurait inventé une intelligence artificielle assez poussée pour l'aider dans la gestion du site, avant d'avoir disparu peu de temps après. Tokyo, 3 heures du matin. Vous êtes réveillé par une notification particulière: votre compte Pycoin vient d'être crédité d'un token inconnu."
	if (niveau == 2) or (niveau == 3):
		text = "2060. Les taux d'inflation des monnaies étatiques (dites fiat) ont fait fuir les populations du monde vers les cryptomonnaies. Ces monnaies digitales, sécurisées et anonymes, qui étaient pour la plupart considérées comme des blagues, deviennent un enjeu majeur au niveau mondial de par leur propriétés déflationnistes par nature. À la tête des fameux Pycoin Services, la plus grade plateforme d'échange anonyme de cryptommonaies, se tient un mystérieux individu: EL. Presque aussi mythique que le grand Satoshi Nakamoto, beaucoup de rumeurs circulent à son sujet. On dit qu'il aurait inventé une intelligence artificielle assez poussée pour l'aider dans la gestion du site, avant d'avoir disparu peu de temps après. Tokyo, 3 heures du matin. Vous êtes réveillé par une notification particulière: votre compte Pycoin vient d'être crédité d'un token inconnu."
	# Défintion de la police de caratères
	font = pygame.font.Font(None, 32)
	# Préparation affichage bouton
	# Image flèche (https://flaticons.net/customize.php?dir=Application&icon=Navigation-Right.png)
	arrow_image = pygame.image.load("arrow.png")
	text_bouton = "[ENTREE] Continuer"
	box_1 = font.render(text_bouton, True, selected_color, selected_bg_color)
	box_1_pos = box_1.get_rect()
	box_1_pos.center = (fenetre[0] / 2, (fenetre[1] / 2) + 300)
	arrow_pos = (box_1_pos[0] - arrow_image.get_width(), box_1_pos[1])
	# découpage du texte en mots
	words = text.split()
	# liste pour stocker les lignes de texte
	lines = []
	# initialisation de la première ligne de texte
	line = words[0]
	# ajout des mots à la ligne de texte jusqu'à atteindre la limite de 180 caractères
	for word in words[1:]:
		if len(line + " " + word) < 165:
			line += " " + word
		else:
			lines.append(line)
			line = word
	# ajout de la dernière ligne de texte
	if line:
		lines.append(line)
	running = True
	while running:
		# Affichage du bouton
		screen.blit(box_1, box_1_pos)
		screen.blit(arrow_image, arrow_pos)
		# Affichage du texte
		y = 500
		for line in lines:
			text_surface = font.render(line, True, blanc)
			text_rect = text_surface.get_rect(center=(fenetre[0] // 2, y + text_surface.get_height() // 2))
			screen.blit(text_surface, text_rect)
			y += 50
		# Quitte si l'utilisateur veut quitter le jeu ou si une touche est pressée
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			elif event.type == pygame.KEYDOWN:
				running = False
		# Mets à jour l'écran et attends la prochaine frame
		pygame.display.update()
		# Limite des FPS à 60
		clock.tick(60)


# Teste si le jeu a été lancé pour la première fois, initialise les variables nécessaires
# et affiche l'écran de chargement
def init():
	# Définition des variables
	global blanc, noir, or_, selected_bg_color, selected_color, unselected_bg_color, unselected_color
	blanc = (255, 255, 255)
	noir = (0, 0, 0)
	or_ = (228, 192, 27)
	# Couleur pour les éléments sélectionnées et non sélectionnées,  couleur d'arrière plan et couleur de texte
	selected_color = noir
	selected_bg_color = or_
	unselected_color = blanc
	unselected_bg_color = noir
	# Affiche l'écran de chargement deux fois, car il est rapide
	for i in range(2):
		chargement()
	# Pendant ce temps, réinitialise l'écran
	screen.fill(noir)
	pygame.display.update()
	# Préviens et lance la musique
	musique()
	# Détecte si le jeu est lancé pour la première fois, si oui affiche le tutoriel
	if tutoriel_:
		# On met sl'écran pour choisir le nieavu de difficulté du tutoriel
		niveau = choix_tutoriel()
		# Si nieavu 0 ou 1, le tutoriel est de ce niveau
		if (niveau == 0) or (niveau == 1):
			tutoriel(niveau)
		# Si niveau confirmé, le tutoriel amène à la troisième page (car le tutoriel apprenti prends deux pages donc 2+1)
		elif niveau == 2:
			tutoriel(3)
		# Pour le niveau 3 expert, pas de tutoriel directement la suite, et pour tous les niveaux la suite aussi
		tutoriel_suite(niveau)
	# Après le tutoriel ou en l'abscence de tutoriel, on lance le menu principal
	main_menu()
	

def main_menu():
	global noir, blanc, or_
	# Initialise la clock pour limiter la vitesse de lecture
	clock = pygame.time.Clock()
	XXXACOMPLETER
	# Limite les fps à 60
	clock.tick(60)


# Initialise le jeu
init()
