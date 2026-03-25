import pyxel
import time
import random
import sys
import os

# script pour le .exe
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)



class Plante:
    temps_variete = [30.0, 45.0, 60.0, 75.0, 90.0, 30.0]
    def __init__(self, x, y, variete=0):
        self.x = x
        self.y = y
        self.variete = variete
        self.croissance = 1
        self.planted_time = time.time()  # Horodatage de plantation
        self.multi_croissance = 1.0   # : multiplicateur de vitesse

    def afficher(self):
        pyxel.blt(self.x, self.y, 0, self.croissance*16, (self.variete+1)*16, 16, 16)
        if self.croissance < 6:
            progress = self.progression()
            bar_width = int(progress * 16)
            # fond de barre
            pyxel.rect(self.x, self.y + 15, 16, 1, 0)
            # barre de progression
            pyxel.rect(self.x, self.y + 15, bar_width, 1, 11)

    def grandir(self):
        if self.croissance >= 6:
            self.croissance = 6
        else:
            self.croissance += 1

    def recolter(self):
        if self.croissance >= 6:
            # recolter la plante
            var_jardin.plantes.remove(self)
            # ajouter deux graines de la même variété à l'inventaire
            if self.variete < 5:
                inventaire[0].append(Graine(self.variete))
                inventaire[0].append(Graine(self.variete))
            # ajouter un fruit de la même variété à l'inventaire
            inventaire[1].append(Fruit(self.variete))

    def update_from_time(self):
        """
        Met à jour la croissance en fonction du temps écoulé depuis planted_time.
        total_seconds: temps total pour aller de stade 1 à stade 6 (défaut 30s).
        """
        adjusted_total_seconds = Plante.temps_variete[self.variete] / self.multi_croissance
        elapsed = time.time() - self.planted_time
        # De 1 -> 6 il y a 5 sauts, donc intervalle par étape
        step = adjusted_total_seconds / 5.0
        new_stage = 1 + int(elapsed // step)
        if new_stage > 6:
            new_stage = 6
        if new_stage < 1:
            new_stage = 1
        self.croissance = new_stage
    
    def progression(self):
        """Retourne la progression totale de la plante (0 -> 1)."""
        total_time = Plante.temps_variete[self.variete] / self.multi_croissance
        elapsed = time.time() - self.planted_time
        progress = elapsed / total_time
        return max(0, min(1, progress))

class Selectionneur:
    def __init__(self):
        self.variete = None
        self.compte = 0

class Jardin:
    def __init__(self):
        self.plantes = []
        places = []
        for y in range(4):
            for x in range(5):
                places.append((48 + x*20, 28 + y*20))
        self.places = places
        self.nb_parcelles = 5   # nombre de parcelles débloquées au début
        
    def afficher_jardin(self):
        for i, place in enumerate(self.places):
            if i < self.nb_parcelles:
                pyxel.blt(place[0], place[1], 0, 0, 0, 16, 16)
            else:
                pyxel.rect(place[0], place[1], 16, 16, 13)  # parcelle verrouillée
        for plante in self.plantes:
            plante.afficher()
    
    def ajouter_plante(self, plante):
        self.plantes.append(plante)

    def mettre_a_jour_croissance(self):
        for plante in self.plantes:
            plante.update_from_time()
    
    def acheter_parcelles(self, nb):
        self.nb_parcelles = min(self.nb_parcelles + nb, len(self.places))

class Graine:
    def __init__(self, variete):
        self.variete = variete

class Fruit:
    def __init__(self, variete):
        self.variete = variete

class App:
    def __init__(self):
        pyxel.init(152, 120, title="Farming Game", quit_key=pyxel.KEY_Q)
        pyxel.load(resource_path("assets.pyxres"))
        pyxel.mouse(True)
        self.selection_marche = Selectionneur()
        self.selection_compost = Selectionneur()
        self.current_screen = "jardin"  # État du menu : "jardin", "marche", "boutique"
        self.selected_graine_variete = None  # None = aucune sélection, sinon 0,1,2...
        self.selected_fruit_variete = None  # None = aucune sélection, sinon 0,1,2...
        self.selected_tool = None  # None, 'arrosoir' ou 'engrais'
        self.prix = [5,10,20,40,80,500]
        self.proba_varietes = [0.42, 0.3, 0.15, 0.08, 0.045, 0.005]
        self.arrosoir_cooldown = 5.0   # secondes entre 2 utilisations
        self.arrosoir_last_use = 0     # dernière utilisation
        pyxel.run(self.update, self.draw)

    def update(self):
        # Mettre à jour la croissance temporelle des plantes (quelque soit le menu)
        var_jardin.mettre_a_jour_croissance()
        if self.current_screen == "jardin":
            self.update_jardin()
        elif self.current_screen == "marche":
            self.update_marche()
        elif self.current_screen == "boutique":
            self.update_boutique()
            
    def update_jardin(self):
        """Mise à jour du jardin"""
        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
            # Récupère les coordonnées de la souris
            mouse_pos = (pyxel.mouse_x, pyxel.mouse_y)
            ###### si la souris est dans la partie droite de l'écran, gérer le clic ######
            if 40 <= mouse_pos[0] < 160:
                ### si la souris est dans la zone du jardin, gérer le clic ###
                if 20 <= mouse_pos[1] < 120:
                    clicked_place = self.place_cliquee(mouse_pos)
                    if clicked_place:
                        self.gere_clic_jardin(clicked_place)
                    else:
                        self.clear_selection()
                ### sinon la souris est dans la zone du menu, alors gérer le clic ###
                else:
                    self.boutons_menu(mouse_pos)
            ###### sinon, gérer le clic dans la partie gauche de l'écran (inventaire) ######
            elif 20 <= mouse_pos[1] < 34: # zone des outils
                self.gere_clic_outils(mouse_pos)
            elif 35 <= mouse_pos[1] < 120: # zone des fruits ou des graines
                if 21 <= mouse_pos[0] < 40: # zone des graines
                    self.gere_clic_inventaire_graines(mouse_pos)

    def update_marche(self):
        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
            mouse_pos = (pyxel.mouse_x, pyxel.mouse_y)

            ### interactions marché
            if 2 <= mouse_pos[0] < 21 and 35 <= mouse_pos[1] < 120:
                self.gere_clic_inventaire_fruit(mouse_pos)

                if self.selected_fruit_variete is not None:
                    max_dispo = sum(
                        1 for f in inventaire[1]
                        if f.variete == self.selected_fruit_variete)

                    if max_dispo > 0:
                        self.selection_marche.variete = self.selected_fruit_variete
                        self.selection_marche.compte = 1
            
            if 46 <= mouse_pos[0] < 54 and 38 <= mouse_pos[1] < 46:
                vente = self.selection_marche
                if vente.variete is not None:
                    max_dispo = sum(1 for f in inventaire[1] if f.variete == vente.variete)
                    vente.compte = min(vente.compte + 1, max_dispo)

            if 46 <= mouse_pos[0] < 54 and 50 <= mouse_pos[1] < 58:
                self.selection_marche.compte = max(1, self.selection_marche.compte-1)

            if 59 <= mouse_pos[0] < 88 and 56 <= mouse_pos[1] < 67:
                self.vendre_fruits()
            
            ###interactions compost
            if 21 <= mouse_pos[0] < 40 and 35 <= mouse_pos[1] < 120:
                self.gere_clic_inventaire_graines(mouse_pos)

                if self.selected_graine_variete is not None:
                    max_dispo = sum(
                        1 for g in inventaire[0]
                        if g.variete == self.selected_graine_variete)

                    if max_dispo > 0:
                        self.selection_compost.variete = self.selected_graine_variete
                        self.selection_compost.compte = 1
            
            if 46 <= mouse_pos[0] < 54 and 80 <= mouse_pos[1] < 88:
                compost = self.selection_compost
                if compost.variete is not None:
                    max_dispo = sum(1 for f in inventaire[0] if f.variete == compost.variete)
                    compost.compte = min(compost.compte + 1, max_dispo)

            if 46 <= mouse_pos[0] < 54 and 90 <= mouse_pos[1] < 98:
                self.selection_compost.compte = max(1, self.selection_compost.compte-1)
            
            if 59 <= mouse_pos[0] < 101 and 96 <= mouse_pos[1] < 107:
                self.composter_graines()


            self.boutons_menu(mouse_pos)

    def update_boutique(self):
        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
            mouse_pos = (pyxel.mouse_x, pyxel.mouse_y)
            x, y = 47, 40
            # PACK 5 graines
            if x <= mouse_pos[0] < x+62 and y <= mouse_pos[1] < y+11:
                self.acheter_pack_graines(5)

            # PACK 10 graines
            if x <= mouse_pos[0] < x+66 and y+15 <= mouse_pos[1] < y+26:
                self.acheter_pack_graines(10)
            
            # ENGRAIS
            if x <= mouse_pos[0] < x+34 and y+30 <= mouse_pos[1] < y+41:
                self.acheter_engrais()

            # PACK 5 parcelles
            if x <= mouse_pos[0] < x+70 and y+45 <= mouse_pos[1] < y+56:
                self.acheter_pack_parcelles(5)

            self.boutons_menu(mouse_pos)
    
    def afficher_panneau(self,x,y,texte):
        longueur = 4*len(texte)
        pyxel.rect(x,y,longueur+5,11,4)
        pyxel.rect(x+1,y+1,longueur+3,9,0)
        pyxel.text(x+3,y+3,texte,7)

    def draw(self):
        pyxel.cls(3)
        self.afficher_menu()
        self.afficher_argent()
        if self.current_screen == "jardin":
            self.draw_jardin()
        elif self.current_screen == "marche":
            self.draw_marche()
        elif self.current_screen == "boutique":
            self.draw_boutique()
    
    def draw_jardin(self):
        pyxel.rect(40, 20, 120, 100, 7)
        var_jardin.afficher_jardin()
        self.afficher_inventaire()
    
    def draw_marche(self):
        pyxel.rect(40, 20, 120, 100, 7)
        self.afficher_inventaire()
        vente = self.selection_marche
        composte = self.selection_compost
        xm,ym = 46,28
        xc,yc = 46,70
        # MARCHE
        if vente.variete is None:
            self.afficher_panneau(xm+6,ym,"Selectionnez un fruit")
        if vente.variete is not None:
            pyxel.rect(xm+47,ym,11,11,4)
            pyxel.blt(xm+48,ym+1,0,0,16+16*vente.variete,8,8) # sprite du fruit
            self.afficher_panneau(xm+13,ym,"Fruit :")
            self.afficher_panneau(xm+13,ym+13,f"quantite:{vente.compte}")
            pyxel.blt(xm,ym+10,0,104,0,8,8) # +
            pyxel.blt(xm,ym+20,0,104,8,8,8) # -
            total = vente.compte * self.prix[vente.variete]
            self.afficher_panneau(xm+45,ym+26,f"prix:{total}")
            self.afficher_panneau(xm+13,ym+26,"VENDRE")
        # COMPOSTE
        if composte.variete is None:
            self.afficher_panneau(xc+6,yc,"Selectionnez une graine")
        if composte.variete is not None:
            pyxel.rect(xc+51,yc,11,11,4)
            pyxel.blt(xc+52,yc+1,0,0,24+16*composte.variete,8,8) # sprite de la graine
            self.afficher_panneau(xc+13,yc,"Graine :")
            self.afficher_panneau(xc+13,yc+13,f"quantite:{composte.compte}")
            pyxel.blt(xc,yc+10,0,104,0,8,8) # +
            pyxel.blt(xc,yc+20,0,104,8,8,8) # -
            total = composte.compte * self.prix[composte.variete]
            #self.afficher_panneau(xc+45,yc+26,f"prix:{total}")
            self.afficher_panneau(xc+13,yc+26,"COMPOSTER")
    
    def draw_boutique(self):
        pyxel.rect(40, 20, 120, 100, 7)
        x, y = 47, 40

        self.afficher_panneau(x, y, "PACK 5 graines")
        pyxel.rect(x+61, y, 11, 11, 4)
        pyxel.blt(x+62, y+2, 0, 112, 0, 8, 8)
        self.afficher_panneau(x+75,y,"20")

        self.afficher_panneau(x, y+15, "PACK 10 graines")
        pyxel.rect(x+65, y+15, 11, 11, 4)
        pyxel.blt(x+66, y+17, 0, 120, 0, 8, 8)
        self.afficher_panneau(x+79,y+15,"35")

        self.afficher_panneau(x, y+30, "ENGRAIS")
        pyxel.rect(x+33, y+30, 11, 11, 4)
        pyxel.blt(x+34, y+32, 0, 80, 8, 8, 8)
        self.afficher_panneau(x+47,y+30,"15")

        self.afficher_panneau(x, y+45, "PACK 5 parcelles")
        pyxel.rect(x+69, y+45, 11, 11, 4)
        pyxel.blt(x+70, y+47, 0, 112, 8, 8, 8)
        self.afficher_panneau(x+83,y+45,"750")

        self.afficher_inventaire()

    def tirer_variete(self):
        r = random.random()
        total = 0
        for i, p in enumerate(self.proba_varietes):
            total += p
            if r <= total:
                return i
        return len(self.proba_varietes) - 1

    def acheter_engrais(self):
        if argent >= 15:
            inventaire_outils['engrais'] += 1
            self.payer(15)
    
    def acheter_pack_parcelles(self, nb_parcelles):
        if argent >= 750:
            var_jardin.acheter_parcelles(nb_parcelles)
            self.payer(750)
    
    def acheter_pack_graines(self, nb_graines):
        cout = 20 if nb_graines == 5 else 35
        if argent >= cout:
            self.ouvrir_pack_graines(nb_graines)
            self.payer(cout)
    
    def ouvrir_pack_graines(self, nb_graines):
        gains = []
        for _ in range(nb_graines):
            variete = self.tirer_variete()
            inventaire[0].append(Graine(variete))
            gains.append(variete)

    def payer(self, montant):
        global argent
        argent -= montant

    def afficher_argent(self):
        x,y = 111,2
        pyxel.blt(x,y,0,96,0,8,8)
        pyxel.text(x+10,y+2,str(argent),7)

    def boutons_menu(self, mouse_pos):
        """Gère les clics sur les boutons du menu"""
        if 2 <= mouse_pos[1] < 18:
            if 40 <= mouse_pos[0] < 60:
                self.current_screen = "jardin"
            elif 64 <= mouse_pos[0] < 84:
                self.current_screen = "marche"
            elif 88 <= mouse_pos[0] < 108:
                self.current_screen = "boutique"

    def place_cliquee(self, mouse_pos):
        for i, place in enumerate(var_jardin.places):
            if i >= var_jardin.nb_parcelles:
                continue
            if (place[0] <= mouse_pos[0] < place[0] + 16 and
                place[1] <= mouse_pos[1] < place[1] + 16):
                return place
        return None

    def gere_clic_jardin(self, place):
        """Gère le clic sur une place du jardin"""
        # Cherche une plante existante à cette place
        plante_existante = self.plante_a_la_place(place)

        if plante_existante:
            # si un outil est sélectionné, appliquer son effet
            if self.selected_tool == "arrosoir":
                current_time = time.time()

                # Vérifier cooldown
                if current_time - self.arrosoir_last_use >= self.arrosoir_cooldown:
                    self.appliquer_outil_sur_plante("arrosoir", plante_existante)
                    self.arrosoir_last_use = current_time
                else:
                    return
                return
            elif self.selected_tool == "engrais":
                # Appliquer l'engrais seulement sur une plante existante
                self.appliquer_outil_sur_plante("engrais", plante_existante)
                inventaire_outils["engrais"] -= 1
                if inventaire_outils["engrais"] <= 0:
                    self.selected_tool = None
                return
            # sinon tenter de récolter
            plante_existante.recolter()
            return
        else:
            # Sinon, créer une nouvelle plante si on a des graines
            if inventaire[0]:
                # Si une variété est sélectionnée, essayer d'en retirer une
                if self.selected_graine_variete is not None:
                    for i, g in enumerate(inventaire[0]):
                        if g.variete == self.selected_graine_variete:
                            graine = inventaire[0].pop(i)
                            var_jardin.ajouter_plante(Plante(place[0], place[1], graine.variete))
                            return
                else:
                    # Sinon, retirer la première graine de l'inventaire
                    graine = inventaire[0].pop(0)
                    var_jardin.ajouter_plante(Plante(place[0], place[1], graine.variete))
                    return
    
    def gere_clic_inventaire_graines(self, mouse_pos):
        """Gère le clic sur les icônes de l'inventaire des graines (slots dynamiques)."""
        varietes = self.get_varietes_inventaire_graines()
        sx, sy = 21, 35
        slot_h = 10
        for i, variete in enumerate(varietes):
            x0 = sx
            y0 = sy + i * slot_h
            if x0 <= mouse_pos[0] < x0 + 8 and y0 <= mouse_pos[1] < y0 + 8:
                # Ne permettre la sélection que si on a au moins une graine de cette variété
                if any(g.variete == variete for g in inventaire[0]):
                    if self.selected_graine_variete == variete:
                        self.clear_selection()
                    else:
                        self.clear_selection()
                        self.selected_graine_variete = variete
                return

    def gere_clic_inventaire_fruit(self, mouse_pos):
        """Gère le clic sur les icônes de l'inventaire des fruits (slots dynamiques)."""
        varietes = self.get_varietes_inventaire_fruits()
        sx, sy = 2, 35
        slot_h = 10
        for i, variete in enumerate(varietes):
            x0 = sx
            y0 = sy + i * slot_h
            if x0 <= mouse_pos[0] < x0 + 8 and y0 <= mouse_pos[1] < y0 + 8:
                # Ne permettre la sélection que si on a au moins un fruit de cette variété
                if any(g.variete == variete for g in inventaire[1]):
                    if self.selected_fruit_variete == variete:
                        self.clear_selection()
                    else:
                        self.clear_selection()
                        self.selected_fruit_variete = variete
                return
            
    def gere_clic_outils(self, mouse_pos):
        """Retourne True si le clic a sélectionné/désélectionné un outil."""
        tx, ty = 2, 22
        for i, outil in enumerate(list(inventaire_outils.keys())):
            x = tx + i * 12
            y = ty
            if x <= mouse_pos[0] < x + 8 and y <= mouse_pos[1] < y + 8:
                if inventaire_outils.get(outil, 0) > 0:
                    if self.selected_tool == outil:
                        self.clear_selection()
                    else:
                        self.clear_selection()
                        self.selected_tool = outil
                return True
        return False
    
    def vendre_fruits(self):
        global argent
        sel = self.selection_marche
        if sel.variete is None:
            return
        fruits_dispo = [f for f in inventaire[1] if f.variete == sel.variete]
        nb = min(sel.compte, len(fruits_dispo))
        sel.compte = nb
        for i in range(nb):
            inventaire[1].remove(fruits_dispo[i])
        argent += nb * self.prix[sel.variete]
        sel.compte = 0
        sel.variete = None

    def composter_graines(self):
        global argent
        sel = self.selection_compost
        if sel.variete is None:
            return
        graines_dispo = [f for f in inventaire[0] if f.variete == sel.variete]
        nb = min(sel.compte, len(graines_dispo))
        sel.compte = nb
        for i in range(nb):
            inventaire[0].remove(graines_dispo[i])
        argent += nb * self.prix[sel.variete] // 3
        sel.compte = 0
        sel.variete = None

    def plante_a_la_place(self, place):
        """Retourne la plante à une position donnée, ou None"""
        for plante in var_jardin.plantes:
            if (plante.x, plante.y) == place:
                return plante
        return None
    
    def appliquer_outil_sur_plante(self, outil, plante_ou_place):
        """
        Effets simples :
        - 'arrosoir' : augmente la croissance d'1 (max 6) et recalcule planted_time
        - 'engrais'  : accélère la vitesse de croissance sur cet emplacement de 50%
        """
        step_seconds = (Plante.temps_variete[plante_ou_place.variete] / plante_ou_place.multi_croissance) / 5.0
        if outil == 'arrosoir':
            plante_ou_place.croissance = min(6, plante_ou_place.croissance + 1)
            # Réajuster planted_time pour que update_from_time reste cohérent
            plante_ou_place.planted_time = time.time() - (plante_ou_place.croissance - 1) * step_seconds
        elif outil == 'engrais':
            # Sauvegarder le stade actuel
            stade_actuel = plante_ou_place.croissance
    
            # Appliquer le multiplicateur
            if plante_ou_place.multi_croissance < 3:
                plante_ou_place.multi_croissance *= 1.5
    
            # Recalculer le temps par étape avec nouvelle vitesse
            new_step = (Plante.temps_variete[plante_ou_place.variete] / plante_ou_place.multi_croissance) / 5.0
    
            # Ajuster planted_time pour garder le même stade
            plante_ou_place.planted_time = time.time() - (stade_actuel - 1) * new_step

    def progression_arrosoir(self):
        elapsed = time.time() - self.arrosoir_last_use
        progress = elapsed / self.arrosoir_cooldown
        return max(0, min(1, progress))

    def afficher_inventaire(self):
        ### Gestion de l'affichage de l'inventaire des graines ###
        # Compter les graines par variété
        compte_graines = {}
        for graine in inventaire[0]:
            compte_graines[graine.variete] = compte_graines.get(graine.variete, 0) + 1

        # Afficher chaque graine avec son compte
        varietes = self.get_varietes_inventaire_graines()
        sx, sy = 21, 35
        slot_h = 10
        for i, variete in enumerate(varietes):
            x = sx
            y = sy + i * slot_h
            count = compte_graines.get(variete, 0)
            # Afficher le sprite de la graine (stage 1, variété)
            if self.selected_graine_variete == variete:
                # Afficher le sprite de sélection
                pyxel.blt(x, y, 0, 8, (variete+1)*16+8, 8, 8)
            else:
                pyxel.blt(x, y, 0, 0, (variete+1)*16+8, 8, 8)
            # Afficher le compte à côté
            pyxel.text(x + 10, y + 2, f"{count}", 0)

        ### Gestion de l'affichage de l'inventaire des fruits ###
        # Compter les fruits par variété
        compte_fruits = {}
        for fruit in inventaire[1]:
            compte_fruits[fruit.variete] = compte_fruits.get(fruit.variete, 0) + 1

        # Afficher chaque fruit avec son compte
        varietes = self.get_varietes_inventaire_fruits()
        fx, fy = 2, 35
        slot_h = 10
        for i, variete in enumerate(varietes):
            x = fx
            y = fy + i * slot_h
            count = compte_fruits.get(variete, 0)
            # Afficher le sprite du fruit (stage 1, variété)
            if self.selected_fruit_variete == variete:
                # Afficher le sprite de sélection
                pyxel.blt(x, y, 0, 8, (variete+1)*16, 8, 8)
            else:
                pyxel.blt(x, y, 0, 0, (variete+1)*16, 8, 8)
            # Afficher le compte à côté
            pyxel.text(x + 10, y + 2, f"{count}", 0)
        
        ### Gestion de l'affichage des outils (pour l'instant : arrosoir et engrais) ###
        x, y = 2, 22
        if inventaire_outils['arrosoir']:
            # Barre de cooldown sous l'arrosoir
            progress = self.progression_arrosoir()
            largeur = int(progress * 8)
            pyxel.rect(x, y + 9, 8, 1, 0)
            # barre (plus elle est remplie, plus c'est prêt)
            pyxel.rect(x, y + 9, largeur, 1, 11)
            if self.selected_tool == 'arrosoir':
                # Afficher le sprite de sélection
                pyxel.blt(x, y, 0, 88, 0, 8, 8)
            else:
                # Afficher le sprite normal
                pyxel.blt(x, y, 0, 80, 0, 8, 8)
        x += 10
        if inventaire_outils['engrais'] > 0:
            if self.selected_tool == 'engrais':
                # Afficher le sprite de sélection
                pyxel.blt(x, y, 0, 88, 8, 8, 8)
            else:
                # Afficher le sprite normal
                pyxel.blt(x, y, 0, 80, 8, 8, 8)
            pyxel.text(x + 10, y + 2, f"x{inventaire_outils['engrais']}", 0)

    def afficher_menu(self):
        # affiche les boutons du menu
        for i in range(3):
            pyxel.blt(40+i*24, 2, 0, i*20+16, 0, 20, 16)

    def get_varietes_inventaire_graines(self):
        """Retourne la liste triée des variétés présentes dans l'inventaire des graines."""
        return sorted({g.variete for g in inventaire[0]})
    
    def get_varietes_inventaire_fruits(self):
        """Retourne la liste triée des variétés présentes dans l'inventaire des fruits."""
        return sorted({g.variete for g in inventaire[1]})
    
    def clear_selection(self):
        """Désélectionne tout."""
        self.selected_graine_variete = None
        self.selected_fruit_variete = None
        self.selected_tool = None

var_jardin = Jardin()
inventaire = [[Graine(0), Graine(0), Graine(1)], [Fruit(0)]]
inventaire_outils = {'arrosoir': 1, 'engrais': 2}
argent = 100

App()
