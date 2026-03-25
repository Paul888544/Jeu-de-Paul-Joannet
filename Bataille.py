from  random import*
from tkinter import *

class jeu_carte:
    def __init__(self, valeur=None, dico = None, Jeu=None):
        self.valeur = [] if valeur is None else valeur
        for i in range(2, 15):
            self.valeur.append(i)
        self.dico = {} if dico is None else dico
        self.jeu = [] if Jeu is None else Jeu

    def creerjeu(self):
        couleur = ["coeur", "carreaux", "trefle", "pic"]
        for coul in couleur:
            for valeur in self.valeur:
                nom = valeur
                if valeur == 11:
                    nom = "valet"
                    self.dico[str(nom)+" de "+coul] = [11, coul]
                elif valeur == 12:
                    nom = "reine"
                    self.dico[str(nom)+" de "+coul] = [12, coul]
                elif valeur ==13:
                    nom = "roi"
                    self.dico[str(nom)+" de "+coul] = [13, coul]
                elif valeur == 14:
                    nom = "as"
                    self.dico[str(nom)+" de "+coul] = [14, coul]
                else:   
                    self.dico[str(nom)+" de "+coul] = [valeur, coul]
                self.jeu.append(str(nom)+" de "+str(coul))

    def afficher(self):
        ch = ""
        for i in self.jeu:
            ch += str(i)+",  "
        return ch

class distribuer:
    def __init__(self, nb,jeu=None, deck=None):
        self.nb = nb
        self.jeu = [] if jeu is None else jeu
        self.deck = [] if deck is None else deck
    def distri(self):
        carte = 0
        for i in range(self.nb):
            carte = randint(0, len(self.jeu.jeu)-1)
            self.deck.append(self.jeu.jeu[carte])
            self.jeu.jeu.pop(carte)
    def afficherM(self):
        ch=""
        ch2 = ""
        for j in self.deck:
            ch += str(j)+", "
#        for i in self.jeu.jeu:
  #          ch2 += str(i)+", "
        return ch
            
class partie:
    def __init__(self, D1, D2, jeu, pile1=None, pile2=None, transfert1=None, transfert2=None):
        self.D1 = D1.deck
        self.D2 = D2.deck
        self.jeu = jeu
        self.pile1 = [] if pile1 is None else pile1
        self.pile2 = [] if pile2 is None else pile2
        self.transfert1=[] if transfert1 is None else transfert1
        self.transfert2=[] if transfert2 is None else transfert2

    def ellir1(self):
        self.transfert1.append(self.D1[-1])
        self.D1.pop(-1)

    def ellir2(self):
        self.transfert2.append(self.D2[-1])
        self.D2.pop(-1)
    def afficher(self, gagnant, pile):
        ch = "Le "+gagnant+" a gagné, "
        ch2 = ""
        for j in pile:
            ch += str(j)+" "
        """for i in self.D1:
            ch2 += str(i)+", """
        #label.config(text=str(ch))
        print(ch, ch2)

    
    def tour(self):
        a = len(self.pile1)
        b = len(self.pile2)
        if a == 0 and len(self.D1) == 0:
            label.config(text="le joueur 2 a gagné")
            print("le joueur 2 a gagné")
            return 
        if b == 0 and len(self.D2) == 0:
            label.config(text="le joueur 1 a gagné")
            print("le joueur 1 a gagné")
            return
        if len(self.D1) == 0:
            for i in self.pile1:
                self.D1.append(i)
            for i in range(a):
                self.pile1.pop(0)
        if len(self.D2) == 0:
            for i in self.pile2:
                self.D2.append(i)
            for i in range(b):
                self.pile2.pop(0)
        self.ellir1()
        self.ellir2()
        if self.jeu.dico[self.transfert1[-1]][0] > self.jeu.dico[self.transfert2[-1]][0]:
            for i in self.transfert1:
                self.pile1.append(i)
            for j in self.transfert2:
                self.pile1.append(j)
            self.transfert1 = []
            self.transfert2 = []
            return self.afficher("joueur1", self.pile1)
        
        elif self.jeu.dico[self.transfert2[-1]][0] > self.jeu.dico[self.transfert1[-1]][0]:
            for i in self.transfert1:
                self.pile2.append(i)
            for j in self.transfert2:
                self.pile2.append(j)
            self.transfert1 = []
            self.transfert2 = []
            return self.afficher("joueur2", self.pile2)

        else:
            if len(self.D1)-1 == 0:
                for i in self.pile1:
                    self.D1.append(i)
                for i in range(a):
                    self.pile1.pop(0)
            if len(self.D2)-1 == 0:
                for i in self.pile2:
                    self.D2.append(i)
                for i in range(b):
                    self.pile2.pop(0)
            else:
                self.ellir1()
                self.ellir2()
                return self.tour()

def lejeu(D1, D2):
    global P
    if len(D1.deck) == 0 or len(D2.deck) == 0:
        return
    else:
        a = D1.deck[-1]
        b = D2.deck[-1]
        canevas.create_rectangle(300, 400,75, 50, outline="red", fill="white", width=3)
        canevas.create_rectangle(575, 400,350, 50, outline="red", fill="white", width=3)
        label.config(text="a")
        label.config( text="le joueur1 a le "+str(a)+" et le joueur 2 a le "+str(b))
        return "le joueur1 a le "+str(a)+" et le joueur 2 a le "+str(b)




A = jeu_carte()
A.creerjeu()
B = A.afficher()
print(B)
"""B = A.dico["as de trefle"]
print(B)"""


D1 = distribuer( 26, A)
D1.distri()
A1 = D1.afficherM()
D2 = distribuer(26, A)
D2.distri()
A2 = D2.afficherM()
print(A1)
print("llll")
print(A2)

print("llll")
P = partie(D1, D2, A)
P1 = P.tour()
print(P1)

# permet l'appelle de deux fonction
A = None
D1 = None
D2 = None
def regroupe_B1():
    global A, D1, D2
    A = jeu_carte()
    A.creerjeu()
    D1 = distribuer( 4, A)
    D1.distri()
    D2 = distribuer(4, A)
    D2.distri()
    afficher_b2()
    
def regroupe_B2():
    label.pack()
    lejeu(D1, D2)
    afficher_b3()
P = None
def regroupe_B3():
    global P
    if P is None:
        P = partie(D1, D2, A)
    P.tour()
    boucle()
    
#remplace les boutons par le suivant

def afficher_b2():
    fenetre.after(100, label.pack_forget())
    fenetre.after(200, bouton1.pack_forget())
    fenetre.after(300, bouton2.pack())
def afficher_b3():
    fenetre.after(200, bouton2.pack_forget())
    fenetre.after(300, bouton3.pack())
def boucle():
    fenetre.after(200, bouton3.pack_forget())
    fenetre.after(300, bouton2.pack())

def recommence():
    fenetre.after(200, bouton1.pack_forget())
    fenetre.after(200, bouton2.pack_forget())
    fenetre.after(200, bouton3.pack_forget())
    fenetre.after(300, bouton1.pack())



fenetre = Tk()
fenetre.geometry('900x800')
fenetre.title("Bataille")
canevas = Canvas(fenetre, width=650 , height=560, bg='pink')
canevas.pack()

# Créé un nouveau jeu et Distribue
bouton1 = Button(fenetre, text = "Distribuer", command = lambda : regroupe_B1())
bouton1.pack()
# Nous donne les deux cartes
bouton2 = Button(fenetre, text = "prendre carte", command = lambda : regroupe_B2())


bouton3 = Button(fenetre, text = "bataille", command = lambda : regroupe_B3())

bouton4 = Button(fenetre, text = "reset", command = lambda : recommence())
bouton4.place(x = 650, y = 600, width = 50, height = 50)
label = Label(fenetre, text="Le côté gauche est celui du joueur 1 \net le côté droit est celui du joueur 2", font="Arial 14")
label.pack()

