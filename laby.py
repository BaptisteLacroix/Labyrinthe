from random import choice
from math import sqrt
from tkinter import *

# Class
from typing import List, Tuple


class Graphe:

    def __init__(self, sommets, adjacent):
        self.dico_graphe = {}
        self.couleur = {}
        for i in range(len(sommets)):
            self.dico_graphe[sommets[i]] = adjacent[i]
        for j in range(len(sommets)):
            self.couleur[sommets[j]] = 'white'

    def listes_sommets(self):
        return [i for i in self.dico_graphe]

    def liste_voisins(self, value):
        for i in self.dico_graphe.keys():
            if i == value:
                k = self.dico_graphe.get(value)
                return k


class Pile:

    def __init__(self):
        self.valeurs = []

    def empiler(self, nombre):
        self.valeurs.append(nombre)

    def depiler(self):
        return self.valeurs.pop()

    def est_vide(self):
        if not self.valeurs:
            return True
        return False

    def taille(self):
        return len(self.valeurs)

    def sommet(self):
        if self.valeurs is None:
            return
        return self.valeurs[-1]


# parcours

def dfs_alea2(G, sommet):
    visite = {sommet: None}
    p = Pile()
    p.empiler(sommet)
    while not (p.est_vide()):
        s = p.sommet()
        v = [i for i in G.liste_voisins(s) if i not in visite]
        if v:
            voisin = choice(v)
            visite[voisin] = s
            p.empiler(voisin)
        else:
            p.depiler()
    return visite


# Génération Graphe

def generation_graphe(M):
    liste_sommets = []
    liste_sommets_adjacent = []
    for i in range(len(M)):
        for j in range(len(M[i])):
            liste_sommets.append((i, j))
            if M[i][j] == 1:
                voisin = voisins(M, (i, j))
                liste_sommets_adjacent.append(voisin)
            else:
                liste_sommets_adjacent.append([])
    G = Graphe(liste_sommets, liste_sommets_adjacent)
    return G


def dedale(L: int) -> Graphe:
    liste = generation_graphe([[1 for _ in range(L)] for _ in range(L)])
    parcours = dfs_alea2(liste, (0, 0))  # parcours en profondeur aléatoire avec le père pour chaque sommet
    labyrinthe = [[0 for _ in range(2 * L - 1)] for _ in range(2 * L - 1)]
    # on met les 1 dans labyrinthe qui correspondent aux sommets ayant des voisins
    labyrinthe[0][0] = 1  # on commence par mettre un 1 à l'entrée
    for (i, j) in parcours:
        if (i, j) != (0, 0):
            k, liste = parcours[(i, j)]  # parents de (i,j)
            labyrinthe[2 * k][2 * liste] = 1
            labyrinthe[i + k][j + liste] = 1
    labyrinthe[-1][-1] = 1  # 1 à la sortie
    print(sum([len(i) for i in labyrinthe]))
    return generation_graphe(labyrinthe)


def represente_laby(cavenas, graphe: Graphe):
    size = 1000 / (case * 2 - 1)
    liste_sommets = [i for i in graphe.dico_graphe]
    affichage_sortie_labytinthe_white_recu(graphe, cavenas, liste_sommets, float(size))


def affichage_sortie_labytinthe_white_recu(graphe: Graphe, cavenas: Canvas, liste_sommets: List[Tuple[int, int]],
                                           size: float) -> None:
    if not liste_sommets:
        return
    sommet_actuel = liste_sommets[0]
    if graphe.liste_voisins(sommet_actuel):
        cavenas.create_rectangle(sommet_actuel[1] * size, sommet_actuel[0] * size, sommet_actuel[1] * size + size,
                                 sommet_actuel[0] * size + size, fill='white')
    fen_princ.after(5, lambda: affichage_sortie_labytinthe_white_recu(graphe, cavenas, liste_sommets[1:], size))


# Voisin

# fonction qui retourne la liste des voisins de (i,j) dans une matrice carrée M
def voisins(M, couple: Tuple[int, int]) -> List[Tuple[int, int]]:
    """
    Renvoie la liste des cellules voisines de la cellule (ligne, colonne)
    """
    listeVoisins = []
    i, j = couple[0], couple[1]
    for d in (-1, 1):
        if -1 < i + d < len(M) and M[i + d][j] == 1:  # attention matrice carrée sinon "hauteur"
            listeVoisins.append((i + d, j))
        if -1 < j + d < len(M) and M[i][j + d] == 1:  # attention matrice carrée sinon "largeur"
            listeVoisins.append((i, j + d))
    return listeVoisins


# Chemin et arrivée

def chemin(graphe: Graphe, sommet_depart: Tuple[int, int], sommet_arrive: Tuple[int, int]) -> List[Tuple[int, int]] \
                                                                                              or None:
    parents = dfs_alea2(graphe, sommet_depart)
    if sommet_arrive not in parents:
        print('Pas de chemin')
        return None
    path = []
    courant = sommet_arrive
    while courant is not None:
        path = [courant] + path
        courant = parents[courant]
    return path


def onkeypressed(event):
    if event.keysym == 'r':
        sortie_labyrinthe(monCanvas, G1)
    elif event.keysym == 'z':
        keypressed_up(monCanvas)
    elif event.keysym == 's':
        keypressed_down(monCanvas)
    elif event.keysym == 'q':
        keypressed_left(monCanvas)
    elif event.keysym == 'd':
        keypressed_right(monCanvas)


def sortie_labyrinthe(cavenas: Canvas, graphe: Graphe) -> None:
    end = int(sqrt(len(graphe.dico_graphe))) - 1
    size = 1000 / (case * 2 - 1)
    path = chemin(graphe, (0, 0), (end, end))
    affichage_sortie_labytinthe_blue_recu(cavenas, path, float(size))


def affichage_sortie_labytinthe_blue_recu(cavenas: Canvas, path: List[Tuple[int, int]], size: float) -> None:
    if not path:
        return
    coord_x = path[0][1] * size
    coord_y = path[0][0] * size
    # print("path = ", path)
    cavenas.create_rectangle(coord_x, coord_y, coord_x + size, coord_y + size, fill='blue')
    fen_princ.after(100, lambda: affichage_sortie_labytinthe_blue_recu(cavenas, path[1:], size))


# Main

case = int(input("Saisissez la taille de votre labyrinthe : "))
G1 = dedale(case)

fen_princ = Tk()  # création d'une fenetre
fen_princ.geometry("1000x1000")  # taille de la fenetre : 900x900

monCanvas = Canvas(fen_princ, width=1000, height=1000, bg='black', border=1)  # widget canvas


# il permet de dessiner des formes diverses


def keypressed_right(cavenas):
    pass


def keypressed_left(cavenas):
    pass


def keypressed_up(cavenas):
    pass


def keypressed_down(cavenas):
    pass


fen_princ.bind('<KeyPress-r>', onkeypressed)  # permet d'appeler onkeypressed lors l'appuie sur la touche <r>
fen_princ.bind('<KeyPress-z>', onkeypressed)
fen_princ.bind('<KeyPress-s>', onkeypressed)
fen_princ.bind('<KeyPress-q>', onkeypressed)
fen_princ.bind('<KeyPress-d>', onkeypressed)

monCanvas.pack()  # place le widget dans la fenetre

represente_laby(monCanvas, G1)

fen_princ.mainloop()  # lance le gestionnaire d'événements qui interceptera les actions de l'utilisateur
