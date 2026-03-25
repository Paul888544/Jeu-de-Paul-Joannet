#puissance 4
from tkinter import *
import pygame
from random import*

couleur = ["green", "blue", "red", "brown", "black", "pink", "purple", "yellow", "grey"]
grille = [[ ' ' for i in range(7)] for j in range(7)]
couleur_joueuro = 0
couleur_joueurx = 2

joueur = True

colonne = [0, 0, 0, 0, 0, 0, 0, 0]

hauteur = len(grille)
largeur = len(grille[0])

victoire = False





def afficheur(grille):
    for col in grille:
        print(col)
    print('\n')


def faire_tomber_piece(chaine):
    global grille, joueur, colonne, victoire
    if sum(colonne) >= 42:
        victoire = True
        print("Toutes les colonnes sont pleines, il y a égalité")
        print('\n')
        label.config(text="Toutes les colonnes sont pleines, il y a égalité")
    if victoire:
        print("Quelqu'un a gagné, bien joué !")
        print('\n')
        label.config(text="Quelqu'un a gagné, bien joué !")
    elif int(chaine) > 6:
        print("le chiffre est trop grand")
        print('\n')
        label.config(text="le chiffre est trop grand")
    elif colonne[int(chaine)] >= 6:
        print("la colonne est pleine")
    else:
        if joueur == True:
            grille[5-colonne[int(chaine)]][int(chaine)] = 'O'
            joueur = False
            colonne[int(chaine)] = colonne[int(chaine)]+1
            label.config(text="Au joueur X")
        else:
            grille[5-colonne[int(chaine)]][int(chaine)] = 'X'
            joueur = True
            colonne[int(chaine)] = colonne[int(chaine)]+1
            label.config(text="Au joueur O")
        afficheur(grille)
        for i in range(hauteur):
            for j in range(largeur):
                if grille[i][j] == 'X':
                     txt = canevas.create_text(j*50+25, i*50+25, text=grille[i][j], font="Arial 2", fill=couleur[couleur_joueurx])
                     disque = canevas.create_oval(j*50+5, i*50+5, j*50+45, i*50+45, fill=couleur[couleur_joueurx])
                elif grille[i][j] =='O':
                    txt = canevas.create_text(j*50+25, i*50+25, text=grille[i][j], font="Arial 2", fill=couleur[couleur_joueuro])
                    disque = canevas.create_oval(j*50+5, i*50+5, j*50+45, i*50+45,  fill=couleur[couleur_joueuro])
                else:
                    txt = canevas.create_text(j*50+25, i*50+25, text=grille[i][j], font= "Arial 28", fill="black")
        test()
def reset():
    global grille, joueur, canevas, colonne, victoire
    grille = [[' ' for i in range(7)] for j in range(7)]
    afficheur(grille)
    draw(canevas)
    joueur = True
    colonne = [0, 0, 0, 0, 0, 0, 0, 0]
    canevas.create_rectangle(0, 0, 350, 350, fill="pink")
    for i in range(hauteur):
        canevas.create_line(50+50*i,0,50+50*i,300, fill="black", width=5)
        canevas.create_line(0,50+50*i, 350,50+50*i, fill="black", width=5)
        for j in range(largeur):
            txt = canevas.create_text(j*50+25, i*50+25, text=grille[i][j], font="Arial 28", fill="black")
    victoire = False
    label.config(text="Puissance 4")

def draw(canevas):
    global grille

    for i in range(hauteur):
        canevas.create_line(50+50*i,0,50+50*i,350,fill="black", width=5)
        canevas.create_line(0,50+50*i,350,50+50*i, fill="black", width=5)
        for j in range(largeur):
            txt = canevas.create_text(j*50+25,i*50+25, text=grille[i][j], font="Arial 28" , fill="black")


def test():
    global grille, canevas, colonne, joueur, victoire
    for i in range(hauteur):
        for j in range(largeur-3):
            if grille[i][j] != ' ' and grille[i][j] == grille[i][j+1] and grille[i][j+1] == grille[i][j+2] and grille[i][j+2] == grille[i][j+3]:
                if joueur:
                    print("Bien joué le joueur 1 a gagné")
                    label.config(text="Bien joué le joueur 1 a gagné")
                    canevas.create_line(j*50+25, i*50+25, (j+3)*50+25, i*50+25, fill="red", width=5)
                else:
                    print("Bien joué le joueur 2 a gagné")
                    label.config(text="Bien joué le joueur 2 a gagné")
                    canevas.create_line(j*50+25, i*50+25, (j+3)*50+25, i*50+25, fill="red", width=5)
                victoire = True
            else:
                pass
    for i in range(4, hauteur-1):
        for j in range(largeur):
            if grille[i][j] != ' ' and grille[i][j] == grille[i-1][j] == grille[i-2][j] and grille[i-2][j] == grille[i-3][j]:
                if joueur:
                    print("Bien joué le joueur 1 a gagné")
                    label.config(text="Bien joué le joueur 1 a gagné")
                    canevas.create_line(j*50+25, i*50+25, j*50+25, (i-3)*50+25, fill="blue", width=5)
                else:
                    print("Bien joué le joueur 2 a gagné")
                    label.config(text="Bien joué le joueur 2 a gagné")
                    canevas.create_line(j*50+25, i*50+25, j*50+25, (i-3)*50+25, fill="red", width=5)
                victoire = True
            else:
                pass
            
    for i in range(4, hauteur):
        for j in range(largeur-3):
            if grille[i][j] != ' ' and grille[i][j] == grille[i-1][j+1] and grille[i-1][j+1] == grille[i-2][j+2] and grille[i-2][j+2] == grille[i-3][j+3]:
                if joueur:
                    print("Bien joué le joueur 1 a gagné")
                    label.config(text="Bien joué le jouer 1 a gagné")
                    canevas.create_line(j*50+25, i*50+25, (j+3)*50+25, (i-3)*50+25, fill="red", width=5)
                else:
                    print("Bien joué le joueur 2 a gagné")
                    label.config(text="Bien joué le joueur 2 a gagné")
                    canevas.create_line(j*50+25, i*50+25, (j+3)*50+25, (i-3)*50+25, fill="red", width=5)
                victoire = True
        else:
            pass
    for i in range(1, hauteur-3):
        for j in range(largeur-3):
            if grille[i][j] != ' ' and grille[i][j] == grille[i+1][j+1] and grille[i+1][j+1] == grille[i+2][j+2] and grille[i+2][j+2] == grille[i+3][j+3]:
                if joueur:
                    print("Bien joué le joueur 1 a gagné")
                    label.config(text="Bien joué le joueur 1 a gagné")
                    canevas.create_line(j*50+25, i*50+25, (j+3)*50+25, (i+3)*50+25, fill="red", width=5)
                else:
                    print("Bien joué le joueur 2 a gagné")
                    label.config(text="Bien joué le joueur 2 a gagné")
                    canevas.create_line(j*50+25, i*50+25, (j+3)*50+25, (i+3)*50+25, fill="red", width=5)
                victoire = True
            else:
                pass

def changer_couleur():
    global couleur_joueurx, couleur_joueuro
    draw(canevas)
    couleur_joueurx = randint(1, 9)
    couleur_joueuro = randint(1, 9)


def piece1():
    faire_tomber_piece(0)

def piece2():
    faire_tomber_piece(1)

def piece3():
    faire_tomber_piece(2)

def piece4():
    faire_tomber_piece(3)

def piece5():
    faire_tomber_piece(4)

def piece6():
    faire_tomber_piece(5)

def piece7():
    faire_tomber_piece(6)

pygame.mixer.init()

#pygame.mixer.Channel(0).play(pygame.mixer.Sound('Bolero-Ravel.mp3'), loops=42)


fenetre = Tk()
fenetre.geometry('450x560')
fenetre.title("Puissance 4")

canevas = Canvas(fenetre, width=450 , height=450, bg='pink')
canevas.pack()


bouton2 = Button(fenetre, text = "Rejouer", command = reset)
bouton2.pack()

bouton3 = Button(fenetre, text = "1", font="Arial 29", command = piece1)
bouton3.place(x = 0, y = 300, width = 50, height = 50)

bouton4 = Button(fenetre, text = "2", font="Arial 29", command = piece2)
bouton4.place(x = 50, y = 300, width = 50, height = 50)

bouton5 = Button(fenetre, text = "3", font="Arial 29", command = piece3)
bouton5.place(x = 100, y = 300, width = 50, height = 50)

bouton6 = Button(fenetre, text = "4", font="Arial 29", command = piece4)
bouton6.place(x = 150, y = 300, width = 50, height = 50)

bouton7 = Button(fenetre, text = "5", font="Arial 29", command = piece5)
bouton7.place(x = 200, y = 300, width = 50, height = 50)

bouton8 = Button(fenetre, text = "6", font="Arial 29", command = piece6)
bouton8.place(x = 250, y = 300, width = 50, height = 50)

bouton9 = Button(fenetre, text = "7", font="Arial 29", command = piece7)
bouton9.place(x = 300, y = 300, width = 50, height = 50)

bouton10 = Button(fenetre, text = "couleur", command = changer_couleur)
bouton10.pack()

label = Label(fenetre, text="Puissance 4")
label.pack()

afficheur(grille)

draw(canevas)

