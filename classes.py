# -*- coding: utf-8 -*-

#importation des modules 
import pandas

#creation de la classe mere 
class Joueur:
    
    #constructeur 
    def __init__(self, prenom, nom, poste, equipe):
        self.prenom=prenom
        self.nom=nom
        self.poste=poste
        self.equipe=equipe
    
    #affichage des champs 
    def __str__(self):
        print(self.prenom + " " + self.nom + " est un "+ str(self.getType()) + " au poste de " + self.poste + " dans l'équipe " + self.equipe)
    
    #type de joueur
    def getType(self):
        pass


### Classe fille Handball ###    
class Handballeur(Joueur):
    
    #constructeur 
    def __init__(self,prenom,nom,poste,equipe,NombreMatch):
        Joueur.__init__(self, prenom, nom, poste, equipe)
        self.NombreMatch=NombreMatch        
    
    def getType(self):
        return "Handballeur"


### Classe fille Goal Handball ###    
class Goal_Handballeur(Handballeur):
    
    #constructeur 
    def __init__(self,prenom,nom,poste,equipe,NombreMatch,concedes,arretes):
        Handballeur.__init__(self, prenom, nom, poste, equipe, NombreMatch)
        self.concedes=concedes
        self.arretes=arretes
        
     #affichage des champs
    def __str__(self):
        Joueur.__str__(self)
        return(self.prenom + " " + self.nom + " à réalisé en moyenne par match lors de la saison " + str(round(self.arretes/self.NombreMatch)) + " " + "arrets et a concedé en moyenne "  + str(round(self.concedes/self.NombreMatch)) + " buts pour un total de " + str(self.NombreMatch)+ " matchs")
        
        
### Classe fille attaquant Handball ###
class Attaquant_Handballeur(Handballeur):
    
    #constructeur 
    def __init__(self,prenom,nom,poste,equipe,NombreMatch,assist,but):
        Handballeur.__init__(self, prenom, nom, poste, equipe, NombreMatch)
        self.assist=assist
        self.but=but
     
    #affichage des champs
    def __str__(self):
        Joueur.__str__(self)
        return(self.prenom + " " + self.nom + " à réalisé en moyenne par match lors de la saison " + str(round(self.but/self.NombreMatch, 2)) + " buts et "  + str(round(self.assist/self.NombreMatch)) + " assistances, pour un total de " + str(self.NombreMatch)+ " matchs")
    
    
#Classe fille basketball
class Basketteur(Joueur):
    
    #constructeur 
    def __init__(self,prenom,nom,poste,equipe,points,NombreRebond,TempsJoue):
        Joueur.__init__(self, prenom, nom, poste, equipe)
        self.points=points
        self.NombreRebond=NombreRebond
        self.TempsJoue=TempsJoue
    
    #fonction qui determine le type de joueur 
    def getType(self):
        return "Basketteur"
    
    #affichage des champs
    def __str__(self):
        Joueur.__str__(self)
        return(self.prenom + " " + self.nom + " à réalisé en moyenne par match lors de la saison " + str(self.points) + " " + "points, "  + str(self.NombreRebond) + " " +"rebons, pour une durée moyenne sur le terrain de " + str(self.TempsJoue)+ " "  +"min")


#classe contenant les fonction permettant l'analyse des basketteur
class BasketballAnalyse:
    
    #fonction pour obtenir le maximum de la variable pts filtre par la position des joueurs sur le terrain
    def maxPoints(self,position,B):

        filtre=B[ B['position'] == position ] #filtrage dans le dataframe
        max_=max(filtre.pts)
    
        return max_
    
    
    #Fonction pour selectioner les joueurs pour composer la team
    def ProPlayerBask(self,B,collectBasketteur,canvas):
         
            canvas.delete("all") #on efface le contenu du canvas 

            liste= ["C","F","F-C","G","G-F"] #liste des position 
            liste_joueur = []
            liste_points=[]
            liste_texte=[]
            for i in liste:
                    
                maxpoints = self.maxPoints(i, B) #on recupere la plus grosse moyenne  à l'aide de la fct
                dfJoueur = B[ B['pts'] == maxpoints ] #on filtre sur B
               
                    
                liste_joueur.append(dfJoueur.iloc[0,33]) #ajout dans la liste de joueurs
            
                liste_points.append(dfJoueur.iloc[0,18])#ajout dans la liste des points
            
                liste_texte.append("\n Sélection du joueur au poste " + str(i) + " :\n" + str(collectBasketteur[dfJoueur.iloc[0,32]])) #insertion de texte dans la liste 
              
            canvas.create_text(480, 60, font=("Purisa", 35), text= "Sélection des joueurs") #creation du titre 

            label = canvas.create_text(460,200,font=("Purisa", 10),text=liste_texte) #on place les infos dans la canvas
                
            moy_Points = (liste_points[0]+liste_points[1]+liste_points[2]+liste_points[3]+liste_points[4])/5
            moy_Points = round(moy_Points,2)
            
            #creation d'un dataframe pandas pour afficher les joueurs selectionnes
            AffichageJoueur=pandas.DataFrame(liste_joueur)
            AffichageJoueur.columns=["Joueurs"]
            AffichageJoueur["Points moyens"]= liste_points
            AffichageJoueur=AffichageJoueur.sort_values(by=['Points moyens'],ascending=False) #on trie les données
            
            texte2='\n Liste des joueurs de l\'équipe :\n \n' + str(AffichageJoueur) + "\n \n Moyennes des points de l\'équipe : " + str(moy_Points) +" points"
            label2=canvas.create_text(470,400,font=("Purisa", 10),text=texte2) #on place les infos dans la canvas 
            
    #fonction pour creer une team aleatoire
    def CompoAleatoireBask(self,B,collectBasketteur,canvas):
            
            canvas.delete("all") #on efface le contenu du canvas 
             
            liste= ["C","F","F-C","G","G-F"] #liste des position 
            liste_joueur = []
            liste_points= []
            liste_texte=[]
            for i in liste:
                    
                dfJoueurAlea = B[ B['position'] == i ].sample() #on prend une ligne au hasard dans la df filtre par la position 
            
                liste_joueur.append(dfJoueurAlea.iloc[0,33]) #ajout dans la liste de joueurs
                    
                liste_points.append(dfJoueurAlea.iloc[0,18]) #ajout dans la liste des points
                
                liste_texte.append("\n Selection du joueur au poste " + str(i) + " :\n" + str(collectBasketteur[dfJoueurAlea.iloc[0,32]]))
                
            canvas.create_text(480, 60, font=("Purisa", 35), text= "Sélection des joueurs") #insertion du titre 

            label = canvas.create_text(460,200,font=("Purisa", 10),text=liste_texte) #insertion des infos dans le canvas 

            moy_Points = (liste_points[0]+liste_points[1]+liste_points[2]+liste_points[3]+liste_points[4])/5
            moy_Points = round(moy_Points,2)
            
             #creation d'un dataframe pandas pour afficher les joueurs selectionnes
            AffichageJoueur=pandas.DataFrame(liste_joueur)
            AffichageJoueur.columns=["Joueurs"]
            AffichageJoueur["Points moyens"]= liste_points
            AffichageJoueur=AffichageJoueur.sort_values(by=['Points moyens'],ascending=False) #on trie les données 
        
           
            texte2='\n Liste des joueurs : \n \n' + str(AffichageJoueur) + "\n \n Moyennes des points de l\'équipe : " + str(moy_Points) + " points"
            label2=canvas.create_text(470,400,font=("Purisa", 10),text=texte2) #insertion des infos dans le canvas
            
        
    # fonctions qui insert les graphiques dans le canvas 
    def Graphique(self,canvas,im1,im2,im3,im4):
        
        canvas.delete("all")

        canvas.create_image (250, 160 , image = im1 )

        canvas.create_image ( 650 ,160 , image = im2 )

        canvas.create_image ( 650 , 450 , image = im3  )
        
        canvas.create_image ( 250 , 450 , image = im4  )

        
#classe contenant les fonction permettant l'analyse des handballeur
class HandballAnalyse:
    
    #fonction pour obtenir le maximum de la variable mean_goals filtre par la position des joueurs sur le terrain
    def maxBut(self,position,H):

        filtre=H[H['type'] == position] #filtrage dans le dataframe
        max_=max(filtre.mean_goals)
    
        return max_
    
    #fonction pour obtenir le ratio arrets/concedes maximum des gardien
    def maxRatio(self,H):

        filtre=H[(H['type'] == "G") & (H['games_played'] > 5)] #filtrage dans le dataframe
        max_=max(filtre.Ratio_saved_conceded)
    
        return max_
    
    #Fonction pour selectioner les joueurs pour composer la team
    def ProPlayerHand(self,H,collectHandballeur,canvas):
         
            canvas.delete("all") #on efface le contenu du canvas 

            liste= ['LB', 'LW', 'RW', 'RB', 'CB', 'P'] #liste des position 
            liste_joueur = []
            liste_points=[]
            liste_texte=[]
            for poste in liste:                    
                maxBut = HandballAnalyse().maxBut(poste, H) #on recupere la plus grosse moyenne à l'aide de la fct
                dfJoueur = H[ H['mean_goals'] == maxBut ] #on filtre sur H
                
                liste_joueur.append(dfJoueur.iloc[0,1]) #ajout dans la liste de joueurs
                liste_points.append(maxBut)#ajout dans la liste des points
                liste_texte.append("\n Sélection du joueur au poste " + str(poste) + " :\n" + str(collectHandballeur[dfJoueur.index[0]])) #insertion de texte dans la liste 
            
            maxRatio = HandballAnalyse().maxRatio(H) #on recupere la plus grosse moyenne à l'aide de la fct
            dfJoueur = H[ H['Ratio_saved_conceded'] == maxRatio ] #on filtre sur H
            liste_joueur.append(dfJoueur.iloc[0,1]) #ajout dans la liste de joueurs
            liste_points.append(maxRatio)#ajout dans la liste des points
            liste_texte.append("\n Sélection du joueur au poste G :\n" + str(collectHandballeur[dfJoueur.index[0]])) #insertion de texte dans la liste
            
            canvas.create_text(480, 60, font=("Purisa", 35), text= "Sélection des joueurs") #creation du titre 

            label = canvas.create_text(460,200,font=("Purisa", 10),text=liste_texte) #on place les infos dans la canvas
            
            import numpy as np
            moy_Points = np.mean(liste_points[:-1])
            moy_Points = round(moy_Points,2)
            
            #creation d'un dataframe pandas pour afficher les joueurs selectionnes
            AffichageJoueur=pandas.DataFrame(liste_joueur)
            AffichageJoueur.columns=["Joueurs"]
            AffichageJoueur["Points moyens"]= liste_points
            AffichageJoueur=AffichageJoueur.sort_values(by=['Points moyens'],ascending=False) #on trie les données
            
            texte2='\n Liste des joueurs de l\'équipe :\n \n' + str(AffichageJoueur) + "\n \n Moyennes des buts de l\'équipe : " + str(moy_Points) +" buts"
            label2=canvas.create_text(470,430,font=("Purisa", 10),text=texte2) #on place les infos dans la canvas 
            
    #fonction pour creer une team aleatoire
    def CompoAleatoireHand(self,H,collectHandballeur,canvas):
            
            canvas.delete("all") #on efface le contenu du canvas 
             
            liste= ['LB', 'LW', 'RW', 'RB', 'CB', 'P', 'G'] #liste des position 
            liste_joueur = []
            liste_points= []
            liste_texte=[]
            for poste in liste:
                    
                dfJoueurAlea = H[ H['type'] == poste ].sample() #on prend une ligne au hasard dans la df filtre par la position 
            
                liste_joueur.append(dfJoueurAlea.iloc[0,1]) #ajout dans la liste de joueurs
                liste_points.append(dfJoueurAlea.iloc[0,27])#ajout dans la liste des points
                liste_texte.append("\n Sélection du joueur au poste " + str(poste) + " :\n" + str(collectHandballeur[dfJoueurAlea.index[0]])) #insertion de texte dans la liste 
            
                
            canvas.create_text(480, 60, font=("Purisa", 35), text= "Sélection des joueurs") #insertion du titre 

            label = canvas.create_text(460,200,font=("Purisa", 10),text=liste_texte) #insertion des infos dans le canvas 

            import numpy as np
            moy_Points = np.mean(liste_points[:-1])
            moy_Points = round(moy_Points,2)
            
             #creation d'un dataframe pandas pour afficher les joueurs selectionnes
            AffichageJoueur=pandas.DataFrame(liste_joueur)
            AffichageJoueur.columns=["Joueurs"]
            AffichageJoueur["Points moyens"]= liste_points
            AffichageJoueur=AffichageJoueur.sort_values(by=['Points moyens'],ascending=False) #on trie les données 
        
           
            texte2='\n Liste des joueurs : \n \n' + str(AffichageJoueur) + "\n \n Moyennes des buts de l\'équipe : " + str(moy_Points) + " buts"
            label2=canvas.create_text(470,430,font=("Purisa", 10),text=texte2) #insertion des infos dans le canvas
            
        
    # fonctions qui insert les graphiques dans le canvas 
    def Graphique(self,canvas,im1,im2,im3,im4):
        
        canvas.delete("all")

        canvas.create_image (250, 160 , image = im1 )

        canvas.create_image ( 650 ,160 , image = im2 )

        canvas.create_image ( 650 , 450 , image = im3  )
        
        canvas.create_image ( 250 , 450 , image = im4  )