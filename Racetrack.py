from src.fltk import *
from time import sleep
import src.fltk
from collections import deque

def dessine_case():
    """
    Dessine les cases du plateau de jeu en fonction des caractères dans la variable globale `piste`.

    Les couleurs sont définies par les caractères suivants:
    - '>': Gris
    - '*': Bleu
    - '#': Vert

    Returns:
        None
    """
    couleur = {'>': '#808080', '*': '#0000FF', '#': '#008000'}
    for y in range(len(piste)):
        for x in range(len(piste[y])):
            caractere = piste[y][x]
            if caractere in couleur:
                abscisse_centre = x * taille_case + taille_case // 2
                ordonnee_centre = y * taille_case + taille_case // 2
                rayon = taille_case // 2 + 4.5
                cercle(abscisse_centre, ordonnee_centre, rayon, remplissage=couleur[caractere], couleur=couleur[caractere])

def dessine_grille():
    """
    Dessine une grille sur le plateau de jeu.

    La grille est composée de lignes noires qui séparent chaque case.

    Returns:
        None
    """
    demi_case = taille_case / 2
    nb_colonnes = largeur_plateau
    nb_lignes = hauteur_plateau

    for x in range(nb_colonnes + 1):
        ligne((x * taille_case) + demi_case, 0, (x * taille_case) + demi_case, hauteur_plateau * taille_case, couleur='black')

    for y in range(nb_lignes + 1):
        ligne(0, (y * taille_case) + demi_case, largeur_plateau * taille_case, (y * taille_case) + demi_case, couleur='black')

def vitesse(trajectoire):
    """
    Calcule la vitesse basée sur les deux dernières positions de la trajectoire.

    Args:
        trajectoire (list): Liste de tuples représentant les positions (x, y).

    Returns:
        tuple: Un tuple (dx, dy) représentant la vitesse en x et y.
    """
    if len(trajectoire) < 2: 
        return (0, 0) 
    x1, y1 = trajectoire[-2] 
    x2, y2 = trajectoire[-1] 
    dx = x2 - x1  
    dy = y2 - y1
    return (dx, dy) 

def verif_collision_souple(debut, fin):
    """
    Vérifie s'il y a une collision souple entre le point de départ et le point d'arrivée.

    Args:
        debut (tuple): Tuple (x, y) représentant la position de départ.
        fin (tuple): Tuple (x, y) représentant la position d'arrivée.

    Returns:
        bool: True si aucune collision, False sinon.
    """
    x1, y1 = debut
    x2, y2 = fin
    if piste[y2][x2] == '#':
        return False
    return True

def verif_collision_strict(debut, fin):
    """
    Vérifie s'il y a une collision stricte entre le point de départ et le point d'arrivée.

    Args:
        debut (tuple): Tuple (x, y) représentant la position de départ.
        fin (tuple): Tuple (x, y) représentant la position d'arrivée.

    Returns:
        bool: True si aucune collision, False sinon.
    """
    x1, y1 = debut
    x2, y2 = fin
    dx = abs(x2 - x1)
    dy = -abs(y2 - y1) 
    sx = 1 if x1 < x2 else -1 
    sy = 1 if y1 < y2 else -1
    err = dx + dy 
    while True:
        if piste[y1][x1] == '#':  
            return False
        if x1 == x2 and y1 == y2: 
            break
        e2 = 2 * err  
        if e2 >= dy:
            err += dy
            x1 += sx
        if e2 <= dx:  
            err += dx  
            y1 += sy
    return True

def options(trajectoire):
    """
    Génère les options de mouvement valides pour la trajectoire actuelle.
    Args:
        trajectoire (list): Liste de tuples représentant les positions (x, y).

    Returns:
        list: Liste de tuples (x, y) représentant les positions valides."""
    positions_valides = []
    if not trajectoire:
        positions_valides = [(x, y) for y, lig in enumerate(piste) for x, char in enumerate(lig) if char == '>']
    else:
        derniere_position = trajectoire[-1] 
        v = vitesse(trajectoire)
        point_principal = (derniere_position[0] + v[0], derniere_position[1] + v[1])
        for dx in range(-1, 2): 
            for dy in range(-1, 2):
                px, py = point_principal[0] + dx, point_principal[1] + dy
                if 0 <= px < len(piste[0]) and 0 <= py < len(piste): 
                    if souple:
                        if verif_collision_souple(derniere_position, (px, py)):
                            positions_valides.append((px, py))
                    else:
                        if verif_collision_strict(derniere_position, (px, py)):
                            positions_valides.append((px, py))
    return positions_valides

def dessine_options(options):
    """
    Dessine les options de mouvement valides sur le plateau de jeu.

    Args:
        options (list): Liste de tuples (x, y) représentant les positions valides.

    Returns:
        None
    """
    for x, y in options:
        cercle(x * taille_case + taille_case // 2, y * taille_case + taille_case // 2, taille_case // 4, remplissage='white', couleur='black')

def couleur_vitesse(longueur_segment, longueur_max):
    """
    Génère une couleur basée sur la vitesse du segment de la trajectoire.

    Args:
        longueur_segment (float): Longueur du segment actuel.
        longueur_max (float): Longueur maximale des segments de la trajectoire.

    Returns:
        str: Une chaîne de caractères représentant la couleur en format hexadécimal."""
    proportion = min(1, longueur_segment / longueur_max) 
    rouge = int(proportion * 255)
    bleu = int((1 - proportion) * 255)
    return f'#{rouge:02X}00{bleu:02X}'

def dessine_trajectoire(trajectoire):
    """
    Dessine la trajectoire actuelle sur le plateau de jeu.

    Args:
        trajectoire (list): Liste de tuples représentant les positions (x, y).

    Returns:
        None"""
    if len(trajectoire) < 2:
        return
    longueurs = [
        ((trajectoire[i][0] - trajectoire[i - 1][0]) ** 2 + (trajectoire[i][1] - trajectoire[i - 1][1]) ** 2) ** 0.5
        for i in range(1, len(trajectoire))
        if (trajectoire[i][0] - trajectoire[i - 1][0]) ** 2 + (trajectoire[i][1] - trajectoire[i - 1][1]) ** 2 > 0
    ]
    longueur_max = max(longueurs) if longueurs else 1

    for i in range(1, len(trajectoire)):
        x1, y1 = trajectoire[i - 1]
        x2, y2 = trajectoire[i]
        longueur_segment = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        couleur = couleur_vitesse(longueur_segment, longueur_max) if longueur_segment > 0 else '#0000FF'  # Default to blue for no movement
        ligne(x1 * taille_case + taille_case // 2, y1 * taille_case + taille_case // 2,
              x2 * taille_case + taille_case // 2, y2 * taille_case + taille_case // 2,
              couleur=couleur, epaisseur=3)
        cercle(x2 * taille_case + taille_case // 2, y2 * taille_case + taille_case // 2, taille_case // 5, remplissage=couleur, couleur=couleur)

def charger(fichier):
    """
    Charge une piste de jeu depuis un fichier texte.

    Args:
        fichier (str): Le chemin vers le fichier texte contenant la piste.

    Returns:
        list: Une liste de listes représentant la piste de jeu.
    """
    with open(fichier, 'r') as file:
        piste = []
        for line in file:
            line = line.strip() 
            if any(char not in '.#>*' for char in line):
                return None
            piste.append(list(line))
        return piste

def afficher_piste_txt(piste, taille_case):
    """
    Affiche la piste de jeu, les options et la trajectoire pour une piste texte.

    Args:
        piste (list): Une liste de listes représentant la piste de jeu.
        taille_case (int): La taille de chaque case sur le plateau.

    Returns:
        tuple: La trajectoire initiale (liste vide) et les options valides.
    """
    efface_tout()
    trajectoire = []
    options_valides = options(trajectoire)
    dessine_case()
    dessine_grille()
    dessine_trajectoire(trajectoire)
    dessine_options(options_valides)
    mise_a_jour()
    return trajectoire, options_valides

def afficher_piste_img(piste, taille_case, im):
    """
    Affiche la piste de jeu, les options et la trajectoire pour une piste image.
    Args:
        piste (list): Une liste de listes représentant la piste de jeu.
        taille_case (int): La taille de chaque case sur le plateau.
        im (str): Le chemin vers l'image de la piste.
    Returns:
        tuple: La trajectoire initiale (liste vide) et les options valides.
    """
    efface_tout()
    image(400, 400, im, largeur=800, hauteur=800, ancrage='center')
    trajectoire = []
    options_valides = options(trajectoire)
    dessine_grille()
    dessine_trajectoire(trajectoire)
    dessine_options(options_valides)
    mise_a_jour()
    return trajectoire, options_valides

def on_backspace():
    """
    Gère l'action de suppression de la dernière position de la trajectoire.

    Returns:
        None
    """
    global trajectoire, options_valides
    if in_game and trajectoire:
        trajectoire.pop()
        options_valides = options(trajectoire)
        efface_tout()
        dessine_case()
        dessine_grille()
        dessine_trajectoire(trajectoire)
        dessine_options(options_valides)
        mise_a_jour()

def on_escape():
    """
    Gère l'action de retour au menu principal depuis le jeu.
    Returns:
        None
    """
    global menu, in_game, manuel, largeur_plateau, hauteur_plateau
    if in_game:
        menu = True
        in_game = False
        manuel = False
        largeur_plateau = 60
        hauteur_plateau = 30
        redimensionne_fenetre(taille_case * largeur_plateau, taille_case * hauteur_plateau)

def afficher_victoire():
    """
    Affiche le message de victoire lorsque le joueur atteint la fin de la piste.
    Returns:
        None
    """
    global in_game
    efface_tout()
    image(600, 300, "assets/Background2.png", ancrage='center')
    texte(largeur_plateau * taille_case // 2, hauteur_plateau * taille_case // 2, "Victoire !", taille=27, couleur='#f7e552', ancrage='center')
    texte(largeur_plateau * taille_case // 2, hauteur_plateau * taille_case // 2 + 30, "Cliquez pour revenir au menu principal", taille=12, couleur='white', ancrage='center')
    mise_a_jour()
    while True:
        ev = donne_ev()
        ty = type_ev(ev)
        if ty == 'ClicGauche':
            in_game = False
            break
        elif ty == 'Quitte':
            exit(0)
        mise_a_jour()

def verifier_victoire(position):
    """
    Vérifie si la position actuelle est une position de victoire.
    Args:
        position (tuple): Tuple (x, y) représentant la position actuelle.
    Returns:
        bool: True si la position est une position de victoire, False sinon.
    """
    x, y = position
    return piste[y][x] == '*'

def recherche_profondeur_iterative(trajectoire_init):
    stack = [(trajectoire_init, set())]
    compteur = 0  
    while stack:
        trajectoire, visite = stack.pop()
        position = trajectoire[-1]
        config = (position, vitesse(trajectoire))
        if config in visite:
            continue
        visite.add(config)
        compteur += 1
        if compteur % 500 == 0:
            efface_tout()
            dessine_case()
            dessine_grille()
            dessine_trajectoire(trajectoire)
            dessine_options(options(trajectoire))
            mise_a_jour()
        if verifier_victoire(position):
            return trajectoire
        for option in options(trajectoire):
            nouvelle_trajectoire = trajectoire + [option]
            stack.append((nouvelle_trajectoire, visite.copy()))
    return None

def trouver_trajectoire_gagnante():
    """
    Initialise et lance la recherche de la trajectoire gagnante.
    Returns:
        None
    """
    global trajectoire
    trajectoire = [(depart_x, depart_y)]
    solution = recherche_profondeur_iterative(trajectoire)
    if solution:
        print("Trajectoire gagnante trouvée :", solution)
        trajectoire = solution
        dessine_trajectoire(trajectoire)
        mise_a_jour()
    else:
        print("Aucune trajectoire gagnante trouvée")

def recherche_largeur(trajectoire):
    """
    Recherche une trajectoire gagnante en utilisant l'algorithme de parcours en largeur (BFS).
    Args:
        trajectoire (list): Liste contenant la position de départ [(x, y)].
        
    Returns:
        list: La trajectoire gagnante si elle existe, sinon None.
    """
    queue = deque()
    queue.append((trajectoire.copy(), vitesse(trajectoire)))
    visite = set()
    while queue:
        current_traj, current_vitesse = queue.popleft()
        position = current_traj[-1]
        config = (position, current_vitesse)
        if config in visite:
            continue
        visite.add(config)
        if piste[position[1]][position[0]] == '*':  
            return current_traj
        for option in options(current_traj):
            new_traj = current_traj + [option]
            queue.append((new_traj, vitesse(new_traj)))
    return None

def trouver_trajectoire_largeur():
    """
    Initialise et lance la recherche en largeur.
    """
    global trajectoire
    trajectoire = [(depart_x, depart_y)]
    print("Début de la recherche en largeur...")
    solution = recherche_largeur(trajectoire)
    if solution:
        print("Trajectoire trouvée :", solution)
        trajectoire = solution
        dessine_trajectoire(trajectoire)
        mise_a_jour()
    else:
        print("Aucune trajectoire trouvée.")

if __name__ == "__main__":
    taille_case = 20
    souple = False
    strict = False
    largeur_plateau = 60
    hauteur_plateau = 30
    depart_x, depart_y = 1, 1
    menu = True
    regle = False
    how_to_play = False
    manuel = False
    profondeur = False
    largeur = False
    jouer = True
    in_game = False
    trajectoire = []
    cree_fenetre(largeur_plateau * taille_case, hauteur_plateau * taille_case)
    while jouer:
        while menu:
            efface_tout()
            image(600, 300, "assets/interface.png", ancrage='center')
            image(55, 50, "assets/regle.png", largeur=80, hauteur=80, ancrage='center')
            texte(55, 100, "Règles", police='jumble', ancrage='center', couleur='white')
            rectangle(230, 350, 400, 400, remplissage="#29C230")
            centre_x = (230 + 400) / 2
            centre_y = (350 + 400) / 2
            texte(centre_x, centre_y, "Manuel", police='jumble', ancrage='center', couleur='white')
            rectangle(760, 350, 990, 450, remplissage="#29C230")
            centre_x = (760 + 990) / 2
            centre_y = (350 + 400) / 2
            texte(centre_x, centre_y, "Recherche", police='jumble', ancrage='center', couleur='white')
            texte(centre_x, 410, "en profondeur", police='jumble', ancrage='center', couleur='white')
            rectangle(515, 500, 685, 590, remplissage="#29C230")
            centre_x = (515 + 685) / 2
            centre_y = (500 + 550) / 2
            texte(centre_x, centre_y, "Recherche", police='jumble', ancrage='center', couleur='white')
            texte(centre_x, 560, "en largeur", police='jumble', ancrage='center', couleur='white')
            rectangle(1000, 20, 1190, 60, remplissage="#EC9033")
            centre_x = (1000 + 1190) / 2
            centre_y = (20 + 60) / 2
            texte(centre_x, centre_y, "How to play", police='jumble', ancrage='center', couleur='white')
            rectangle(540, 250, 660, 300, remplissage="#FF0000")
            texte(600, 275, "Quitter", police='jumble', ancrage='center', couleur='white')

            ev = donne_ev()
            ty = type_ev(ev)
            if ty == 'Quitte':
                jouer = False
                menu = False
                manuel = False
                break
            elif ty == 'ClicGauche':
                if 10 <= abscisse(ev) <= 100 and 10 <= ordonnee(ev) <= 100:
                    regle = True
                    menu = False
                elif 230 <= abscisse(ev) <= 400 and 350 <= ordonnee(ev) <= 400:
                    manuel = True
                    menu = False
                elif 780 <= abscisse(ev) <= 970 and 350 <= ordonnee(ev) <= 450:
                    profondeur = True
                    menu = False
                elif 540 <= abscisse(ev) <= 660 and 250 <= ordonnee(ev) <= 300:
                    jouer = False   
                    menu = False
                elif 1000 <= abscisse(ev) <= 1190 and 20 <= ordonnee(ev) <= 60:
                    how_to_play= True   
                    menu = False
                elif 515 <= abscisse(ev) <= 685 and 500 <= ordonnee(ev) <= 590:
                    largeur = True
                    menu = False
            mise_a_jour()
        while how_to_play:
            image(600,300,'assets/how_to_play.png',largeur=1200, hauteur=600, ancrage = "center") 
            image(1035,515,'assets/btm.png',largeur=120, hauteur=60, ancrage = "center") 
            mise_a_jour()
            ev = donne_ev()
            ty = type_ev(ev)
            if ty == 'Quitte':
                jouer = False
                break
            elif ty == 'ClicGauche':
                if 970 <= abscisse(ev) <= 1100 and 480 <= ordonnee(ev) <= 550:
                    menu = True
                    how_to_play = False
        while regle:
            efface_tout()
            image(600, 300, "assets/Background.png", ancrage='center')
            rectangle(160, 110, 415, 370, couleur='green',remplissage="white")
            image(290, 250, "assets/règles souples.png", largeur=250, hauteur=250, ancrage='center')
            rectangle(780, 110, 1035, 370, couleur='green',remplissage="white")
            image(910, 250, "assets/règles strictes.png", largeur=250, hauteur=250, ancrage='center')

            if souple == False:
                rectangle(170, 40, 410, 90, couleur='red')
                texte(185, 50, "Règles souples", couleur='darkred', police='benguiat', taille="22")
            elif souple:
                rectangle(170, 40, 410, 90, couleur='green')
                texte(185, 50, "Règles souples", couleur='darkgreen', police='benguiat', taille="22")

            if strict == False:
                rectangle(805, 40, 1040, 90, couleur='red')
                texte(820, 50, "Règles strictes", couleur='darkred', police='benguiat', taille="22")
            elif strict:
                rectangle(805, 40, 1040, 90, couleur='green')
                texte(820, 50, "Règles strictes", couleur='darkgreen', police='benguiat', taille="22")
            image(605,550,'assets/btm.png',largeur=120, hauteur=60, ancrage = "center") 

            ev = donne_ev()
            ty = type_ev(ev)
            if ty == 'Quitte':
                jouer = False
                regle = False
                manuel = False
                break
            elif ty == 'ClicGauche':
                if 170 <= abscisse(ev) <= 400 and 40 <= ordonnee(ev) <= 90:
                    souple = not souple
                    if souple:
                        strict = False
                elif 800 <= abscisse(ev) <= 1025 and 40 <= ordonnee(ev) <= 90:
                    strict = not strict
                    if strict:
                        souple = False
                elif 540 <= abscisse(ev) <= 670 and 525 <= ordonnee(ev) <= 575:
                    regle = False
                    menu = True
                    continue
            mise_a_jour()

        while manuel:
            efface_tout()
            image(600, 300, "assets/Background.png", ancrage='center')
            texte(550, 30, "Pistes", couleur='white', police='benguiat', taille="30")
            image(605,555,'assets/btm.png',largeur=120, hauteur=60, ancrage = "center")  
            rectangle(30, 150, 230, 350, couleur='green',remplissage="white")
            image(130, 250, "assets/map1.png",largeur=170, hauteur=150, ancrage='center')
            rectangle(260, 150, 460, 350, couleur='green',remplissage="white")
            image(360, 250, "assets/map2.png",largeur=170, hauteur=150, ancrage='center')
            rectangle(490, 150, 690, 350, couleur='green',remplissage="white")
            image(590, 250, "assets/map3.png",largeur=170, hauteur=150, ancrage='center')
            rectangle(720, 150, 920, 350, couleur='green',remplissage="white")
            image(820, 250, "assets/map4.png", largeur=170, hauteur=150, ancrage='center')
            rectangle(950, 150, 1150, 350, couleur='green',remplissage="white")
            image(1050, 250, "assets/map6.png", largeur=170, hauteur=150, ancrage='center')
            mise_a_jour()

            ev = donne_ev()
            ty = type_ev(ev)
            if ty == 'Quitte':
                jouer = False
                regle = False
                manuel = False
                break
            elif ty == 'ClicGauche':
                x, y = abscisse(ev), ordonnee(ev)
                if 540 <= x <= 670 and 525 <= y <= 575:
                    manuel = False
                    menu = True
                    continue
                elif 30 <= x <= 230 and 150 <= y <= 350:
                    piste = charger('assets/map_mini.txt')
                    if piste:
                        largeur_plateau = len(piste[0])
                        hauteur_plateau = len(piste)
                        for y, l in enumerate(piste):
                            for x, char in enumerate(l):
                                if char == '>':
                                    depart_x, depart_y = x, y
                        redimensionne_fenetre(taille_case * largeur_plateau, taille_case * hauteur_plateau)
                        trajectoire, options_valides = afficher_piste_txt(piste, taille_case)
                        manuel = False
                        menu = False
                        in_game = True
                elif 260 <= x <= 460 and 150 <= y <= 350:
                    piste = charger('assets/map_test.txt')
                    if piste:
                        largeur_plateau = len(piste[0])
                        hauteur_plateau = len(piste)
                        for y, l in enumerate(piste):
                            for x, char in enumerate(l):
                                if char == '>':
                                    depart_x, depart_y = x, y
                        redimensionne_fenetre(taille_case * largeur_plateau, taille_case * hauteur_plateau)
                        trajectoire, options_valides = afficher_piste_txt(piste, taille_case)
                        manuel = False
                        menu = False
                        in_game = True
                elif 490 <= x <= 690 and 150 <= y <= 350:
                    piste = charger('assets/map2.txt')
                    if piste:
                        largeur_plateau = len(piste[0])
                        hauteur_plateau = len(piste)
                        for y, l in enumerate(piste):
                            for x, char in enumerate(l):
                                if char == '>':
                                    depart_x, depart_y = x, y
                        redimensionne_fenetre(taille_case * largeur_plateau, taille_case * hauteur_plateau)
                        trajectoire, options_valides = afficher_piste_txt(piste, taille_case)
                        manuel = False
                        menu = False
                        in_game = True
                elif 720 <= x <= 920 and 150 <= y <= 350:
                    piste = charger('assets/map1.txt')
                    if piste:
                        largeur_plateau = len(piste[0])
                        hauteur_plateau = len(piste)
                        for y, l in enumerate(piste):
                            for x, char in enumerate(l):
                                if char == '>':
                                    depart_x, depart_y = x, y
                        redimensionne_fenetre(taille_case * largeur_plateau, taille_case * hauteur_plateau)
                        trajectoire, options_valides = afficher_piste_txt(piste, taille_case)
                        manuel = False
                        menu = False
                        in_game = True
                elif 950 <= x <= 1150 and 150 <= y <= 350:
                    piste = charger('assets/map3.txt')
                    if piste:
                        largeur_plateau = len(piste[0])
                        hauteur_plateau = len(piste)
                        for y, l in enumerate(piste):
                            for x, char in enumerate(l):
                                if char == '>':
                                    depart_x, depart_y = x, y
                        redimensionne_fenetre(taille_case * largeur_plateau, taille_case * hauteur_plateau)
                        trajectoire, options_valides = afficher_piste_txt(piste, taille_case )
                        manuel = False
                        menu = False
                        in_game = True

        while profondeur:
            efface_tout()
            image(600, 300, "assets/Background.png", ancrage='center')
            texte(550, 30, "Pistes", couleur='white', police='benguiat', taille="30")
            image(605,555,'assets/btm.png',largeur=120, hauteur=60, ancrage = "center")  
            rectangle(30, 150, 230, 350, couleur='green',remplissage="white")
            image(130, 250, "assets/map1.png",largeur=170, hauteur=150, ancrage='center')
            rectangle(260, 150, 460, 350, couleur='green',remplissage="white")
            image(360, 250, "assets/map2.png",largeur=170, hauteur=150, ancrage='center')
            rectangle(490, 150, 690, 350, couleur='green',remplissage="white")
            image(590, 250, "assets/map3.png",largeur=170, hauteur=150, ancrage='center')
            rectangle(720, 150, 920, 350, couleur='green',remplissage="white")
            image(820, 250, "assets/map4.png", largeur=170, hauteur=150, ancrage='center')
            rectangle(950, 150, 1150, 350, couleur='green',remplissage="white")
            image(1050, 250, "assets/map6.png", largeur=170, hauteur=150, ancrage='center')
            mise_a_jour()

            ev = donne_ev()
            ty = type_ev(ev)
            if ty == 'Quitte':
                jouer = False
                profondeur = False
                manuel = False
                break
            elif ty == 'ClicGauche':
                x, y = abscisse(ev), ordonnee(ev)
                if 540 <= x <= 670 and 525 <= y <= 575:
                    profondeur = False
                    menu = True
                    continue
                elif 0 <= x <= 170 and 80 <= y <= 250:
                    piste = charger('assets/map_mini.txt')
                    if piste:
                        largeur_plateau = len(piste[0])
                        hauteur_plateau = len(piste)
                        for y, l in enumerate(piste):
                            for x, char in enumerate(l):
                                if char == '>':
                                    depart_x, depart_y = x, y
                        redimensionne_fenetre(taille_case * largeur_plateau, taille_case * hauteur_plateau)
                        trajectoire, options_valides = afficher_piste_txt(piste, taille_case)
                        profondeur = False
                        in_game = True
                        trouver_trajectoire_gagnante()
                elif 260 <= x <= 460 and 150 <= y <= 350:
                    piste = charger('assets/map_test.txt')
                    if piste:
                        largeur_plateau = len(piste[0])
                        hauteur_plateau = len(piste)
                        for y, l in enumerate(piste):
                            for x, char in enumerate(l):
                                if char == '>':
                                    depart_x, depart_y = x, y
                        redimensionne_fenetre(taille_case * largeur_plateau, taille_case * hauteur_plateau)
                        trajectoire, options_valides = afficher_piste_txt(piste, taille_case)
                        profondeur = False
                        in_game = True
                        trouver_trajectoire_gagnante()
                elif 490 <= x <= 690 and 150 <= y <= 350:
                    piste = charger('assets/map2.txt')
                    if piste:
                        largeur_plateau = len(piste[0])
                        hauteur_plateau = len(piste)
                        for y, l in enumerate(piste):
                            for x, char in enumerate(l):
                                if char == '>':
                                    depart_x, depart_y = x, y
                        redimensionne_fenetre(taille_case * largeur_plateau, taille_case * hauteur_plateau)
                        trajectoire, options_valides = afficher_piste_txt(piste, taille_case)
                        profondeur = False
                        in_game = True
                        trouver_trajectoire_gagnante()
                
                elif 720 <= x <= 920 and 150 <= y <= 350:
                    piste = charger('assets/map1.txt')
                    if piste:
                        largeur_plateau = len(piste[0])
                        hauteur_plateau = len(piste)
                        for y, l in enumerate(piste):
                            for x, char in enumerate(l):
                                if char == '>':
                                    depart_x, depart_y = x, y
                        redimensionne_fenetre(taille_case * largeur_plateau, taille_case * hauteur_plateau)
                        trajectoire, options_valides = afficher_piste_txt(piste, taille_case)
                        profondeur = False
                        in_game = True
                        trouver_trajectoire_gagnante()
                elif 950 <= x <= 1150 and 150 <= y <= 350:
                    piste = charger('assets/map3.txt')
                    if piste:
                        largeur_plateau = len(piste[0])
                        hauteur_plateau = len(piste)
                        for y, l in enumerate(piste):
                            for x, char in enumerate(l):
                                if char == '>':
                                    depart_x, depart_y = x, y
                        redimensionne_fenetre(taille_case * largeur_plateau, taille_case * hauteur_plateau)
                        trajectoire, options_valides = afficher_piste_txt(piste, taille_case)
                        profondeur = False
                        in_game = True
                        trouver_trajectoire_gagnante()

            mise_a_jour()

        while largeur:
            efface_tout()
            image(600, 300, "assets/Background.png", ancrage='center')
            texte(550, 30, "Pistes", couleur='white', police='benguiat', taille="30")
            image(605,555,'assets/btm.png',largeur=120, hauteur=60, ancrage = "center")  
            rectangle(30, 150, 230, 350, couleur='green',remplissage="white")
            image(130, 250, "assets/map1.png",largeur=170, hauteur=150, ancrage='center')
            rectangle(260, 150, 460, 350, couleur='green',remplissage="white")
            image(360, 250, "assets/map2.png",largeur=170, hauteur=150, ancrage='center')
            rectangle(490, 150, 690, 350, couleur='green',remplissage="white")
            image(590, 250, "assets/map3.png",largeur=170, hauteur=150, ancrage='center')
            rectangle(720, 150, 920, 350, couleur='green',remplissage="white")
            image(820, 250, "assets/map4.png", largeur=170, hauteur=150, ancrage='center')
            rectangle(950, 150, 1150, 350, couleur='green',remplissage="white")
            image(1050, 250, "assets/map6.png", largeur=170, hauteur=150, ancrage='center')
            mise_a_jour()
            ev = donne_ev()
            ty = type_ev(ev)

            if ty == 'Quitte':
                jouer = False
                largeur = False
                manuel = False
                break
            elif ty == 'ClicGauche':
                x, y = abscisse(ev), ordonnee(ev)
                if 540 <= x <= 670 and 525 <= y <= 575:
                    largeur = False
                    menu = True
                    continue
                elif 0 <= x <= 170 and 80 <= y <= 250:
                    piste = charger('assets/map_mini.txt')
                    if piste:
                        largeur_plateau = len(piste[0])
                        hauteur_plateau = len(piste)
                        for y, l in enumerate(piste):
                            for x, char in enumerate(l):
                                if char == '>':
                                    depart_x, depart_y = x, y
                        redimensionne_fenetre(taille_case * largeur_plateau, taille_case * hauteur_plateau)
                        trajectoire, options_valides = afficher_piste_txt(piste, taille_case)
                        largeur = False
                        in_game = True
                        trouver_trajectoire_largeur()

                elif 260 <= x <= 460 and 150 <= y <= 350:
                    piste = charger('assets/map_test.txt')
                    if piste:
                        largeur_plateau = len(piste[0])
                        hauteur_plateau = len(piste)
                        for y, l in enumerate(piste):
                            for x, char in enumerate(l):
                                if char == '>':
                                    depart_x, depart_y = x, y
                        redimensionne_fenetre(taille_case * largeur_plateau, taille_case * hauteur_plateau)
                        trajectoire, options_valides = afficher_piste_txt(piste, taille_case)
                        largeur = False
                        in_game = True
                        trouver_trajectoire_largeur()
                elif 490 <= x <= 690 and 150 <= y <= 350:
                    piste = charger('assets/map2.txt')
                    if piste:
                        largeur_plateau = len(piste[0])
                        hauteur_plateau = len(piste)
                        for y, l in enumerate(piste):
                            for x, char in enumerate(l):
                                if char == '>':
                                    depart_x, depart_y = x, y
                        redimensionne_fenetre(taille_case * largeur_plateau, taille_case * hauteur_plateau)
                        trajectoire, options_valides = afficher_piste_txt(piste, taille_case)
                        largeur = False
                        in_game = True
                        trouver_trajectoire_largeur()
                elif 720 <= x <= 920 and 150 <= y <= 350:
                    piste = charger('assets/map1.txt')
                    if piste:
                        largeur_plateau = len(piste[0])
                        hauteur_plateau = len(piste)
                        for y, l in enumerate(piste):
                            for x, char in enumerate(l):
                                if char == '>':
                                    depart_x, depart_y = x, y
                        redimensionne_fenetre(taille_case * largeur_plateau, taille_case * hauteur_plateau)
                        trajectoire, options_valides = afficher_piste_txt(piste, taille_case)
                        largeur = False
                        in_game = True
                        trouver_trajectoire_largeur()
                elif 950 <= x <= 1150 and 150 <= y <= 350:
                    piste = charger('assets/map3.txt')
                    if piste:
                        largeur_plateau = len(piste[0])
                        hauteur_plateau = len(piste)
                        for y, l in enumerate(piste):
                            for x, char in enumerate(l):
                                if char == '>':
                                    depart_x, depart_y = x, y
                        redimensionne_fenetre(taille_case * largeur_plateau, taille_case * hauteur_plateau)
                        trajectoire, options_valides = afficher_piste_txt(piste, taille_case)
                        largeur = False
                        in_game = True
                        trouver_trajectoire_largeur()

            mise_a_jour()
        while not menu and jouer and in_game:
            ev = donne_ev()
            ty = type_ev(ev)
            if ty == 'Quitte':
                jouer = False
                break
            elif ty == 'ClicGauche':
                x, y = abscisse(ev), ordonnee(ev)
                col, lig = x // taille_case, y // taille_case
                if (col, lig) in options_valides:
                    trajectoire.append((col, lig))
                    if verifier_victoire((col, lig)):
                        afficher_victoire()
                        menu = True
                        manuel = False
                        largeur_plateau = 60
                        hauteur_plateau = 30
                        redimensionne_fenetre(taille_case * largeur_plateau, taille_case * hauteur_plateau)
                    else:
                        options_valides = options(trajectoire)
                        efface_tout()
                        dessine_case()
                        dessine_grille()
                        dessine_trajectoire(trajectoire)
                        dessine_options(options_valides)
                else:
                    pass
            elif ty == 'Touche':
                if touche(ev) == 'BackSpace':
                    on_backspace()
                elif touche(ev) == 'Escape':
                    on_escape()
            mise_a_jour()
    ferme_fenetre()

