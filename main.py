# -*- coding: utf-8 -*-
import pandas
import json
import matplotlib.pyplot as plt
import seaborn as sns
import re
from classes import Basketteur, BasketballAnalyse, Attaquant_Handballeur, Goal_Handballeur, HandballAnalyse
from tkinter import *


'''
#Bascket
#url 
URL="https://www.balldontlie.io/api/v1/season_averages?player_ids[]=2"

#boucle pour récupérer les résultats en moyennes des joueurs en saison 
for i in numpy.arange(start=50,stop=100,step=1):
    URL = URL + "&player_ids[]=" + str(i)
    r = requests.get(URL) #on recupere les reponses 
    files = r.json()

#convertir json to dataframe
df = json_normalize(files['data']) #Results contain the required data
print(df)


liste=list()

#boucle pour obtenir des infos sur les joueurs
#on réutilise les player_id recupere precedement 
for i in df["player_id"]:
    url = "https://www.balldontlie.io/api/v1/players/" + str(i)
    contents = requests.get(url) #on recupere les reponses 
    files2 = contents.json()
    liste.append(files2)

#mise en forme sous dataframe
df2 = pandas.DataFrame(liste)
#concatener les 2 df en fonction du player_id
Bascket10 = pandas.merge(df, df2, how="right", left_on="player_id", right_on="id")
#exporter en csv
Bascket10.to_csv("Bascket10.csv",index=False)



#importation des fichiers pour les concatener
Bascket1= pandas.read_csv("Bascket1.csv", sep=",")
Bascket2= pandas.read_csv("Bascket2.csv", sep=",")
Bascket3= pandas.read_csv("Bascket3.csv", sep=",")
Bascket4= pandas.read_csv("Bascket4.csv", sep=",")
Bascket5= pandas.read_csv("Bascket5.csv", sep=",")
Bascket6= pandas.read_csv("Bascket6.csv", sep=",")
Bascket7= pandas.read_csv("Bascket7.csv", sep=",")
Bascket8= pandas.read_csv("Bascket8.csv", sep=",")
Bascket9= pandas.read_csv("Bascket9.csv", sep=",")
Bascket10= pandas.read_csv("Bascket10.csv", sep=",")



#concatener les fichiers
B2=pandas.concat([Bascket1,Bascket2])
B3=pandas.concat([Bascket3,Bascket4])
B = pandas.concat([B2,B3])
B = pandas.concat([B,Bascket5])
B = pandas.concat([B,Bascket6])
B = pandas.concat([B,Bascket7])
B = pandas.concat([B,Bascket8])
B = pandas.concat([B,Bascket9])
B = pandas.concat([B,Bascket10])

#supprimer les doublons selon la colonne id_player
B.drop_duplicates(subset ="player_id", keep = 'first', inplace=True)

#exporter en csv
B.to_csv("JoueurBascket.csv",index=False)
'''
#impoerter le fichier
B= pandas.read_csv("JoueurBascket.csv", sep=",")


nom_equipe=[]
#boucle pour recuperer les noms d'équipe des joueurs 
for line in B["team"]: 
    
   #remplace toutes le occurences de guillmet simples par guillemet doubles
   p = re.compile('(?<!\\\\)\'')
   line = p.sub('\"', line)
   
   #lire les données json
   data_dic=json.loads(line)
   #on récupère juste le nom complet
   name=data_dic["full_name"]
   #on insert dans une liste 
   nom_equipe.append(name)

#mettre la liste sous forme de dataframe
N_equipe=pandas.DataFrame(nom_equipe)
N_equipe.columns=["Team_name"] #nommer la colonne 
N_equipe["player_id"]=B["player_id"] #on ajoute la colonne player_id

#On concate B avec N_equipe en fonction de player_id pour avoir Team_name dans B 
B=pandas.merge(B, N_equipe, how="right", left_on="player_id", right_on="player_id")


#recodage de la variable min 
temps_recod = []
for line in B["min"]:
    
    index_=line.index(":") #trouver l'index des ":"
    apres_index = line[index_+1:5] #isoler la chaine après ":"
    
    avant_index = line[0:index_] #isoler la chaine avant ":"
    
    #on arrondi le temps selon si les secondes sont supérieures ou inférieures a 30
    apres_index = int(apres_index)
    if apres_index > 30 :
        
        temps_recod.append(int(avant_index)+1)
    else:
        
        temps_recod.append(int(avant_index))
        

#mettre la liste sous forme de dataframe
Temps_recod=pandas.DataFrame(temps_recod)
Temps_recod.columns=["Temps_recod(min)"] #nommer la colonne
Temps_recod["player_id"]=B["player_id"] #on ajoute la colonne player_id

#On concate B avec N_equipe en fonction de player_id pour avoir Team_name dans B 
B=pandas.merge(B, Temps_recod, how="right", left_on="player_id", right_on="player_id")

#on trie selon valeur selon player_id
B=B.sort_values(by=['player_id'])

#creation d'index 
liste_indice=[]
for i in range(len(B)):
    liste_indice.append(i)

B["index"]= liste_indice #creation de la variable index et insertion des indexs  

B["full_name"]= B.first_name +" " + B.last_name #ajout de d'une colonne full_name composé du prenom et nom



#utilisation des joueurs dans la classe Basket et insertion dans une liste d'objet
collectBasketteur=[]
for i in range(0,len(B)):
    
    prenom=B.iloc[i,23]
    nom=B.iloc[i,26]
    poste=B.iloc[i,27]
    equipe=B.iloc[i,30]
    points=B.iloc[i,18]
    NombreRebond=B.iloc[i,12]
    TempsJoue=B.iloc[i,3]
    a=Basketteur(prenom,nom,poste,equipe,points, NombreRebond, TempsJoue)
    collectBasketteur.append(a) #insertion dans la liste
    
print(collectBasketteur[10])

##################################Handball##################################################

### Requetage via API ###

'''
import http.client, json, time, pandas as pd
conn = http.client.HTTPSConnection("api.sportradar.us")  #connection a l'API'
key = 'y6ffnnuc73bux4nxk2edxsn4' #cle pour les requetes
conn.request("GET", "/handball/trial/v2/fr/seasons.json?api_key="+key) #Obtention des differente saison dispo
res = conn.getresponse()
data = res.read()
data=json.loads(data)
#On prend la ligue 'sr:season:77385' qui represente la ligue des champions 20/21, sr:competition:30

conn = http.client.HTTPSConnection("api.sportradar.us")
key = 'y6ffnnuc73bux4nxk2edxsn4'
conn.request("GET", "/handball/trial/v2/fr/seasons/sr:season:77385/competitors.json?api_key="+key) #obtention des equipe de la competition
res = conn.getresponse()
data = res.read()
data=json.loads(data)

equipes = data["season_competitors"]

players_stats = []
players_profile = []
for equipe in equipes: #Pour chaque equipe
    
    equipe_id = equipe["id"]
    equipe_name = equipe["name"]
    
    conn = http.client.HTTPSConnection("api.sportradar.us")
    key = 'y6ffnnuc73bux4nxk2edxsn4'
    conn.request("GET", "/handball/trial/v2/en/seasons/sr:season:77385/competitors/"+equipe_id+"/statistics.json?api_key="+key) #Obtention des stats des joueurs
    res = conn.getresponse()
    data = res.read()
    
    stat_equipe=json.loads(data)
    stat_players = stat_equipe["statistics"]["players"]
    players_stats += stat_players
    
    time.sleep(1)
    conn = http.client.HTTPSConnection("api.sportradar.us")
    key = 'y6ffnnuc73bux4nxk2edxsn4'
    conn.request("GET", "/handball/trial/v2/en/competitors/"+equipe_id+"/profile.json?api_key="+key) #Obtention des profil des joueurs
    res = conn.getresponse()
    data = res.read()
    time.sleep(1)
    
    profile_equipe=json.loads(data)
    profil_players = profile_equipe["players"]
    for player in profil_players:
        player["equipe"] = equipe_name #Ajout du nom d'equipe
    
    players_profile += profil_players

players_profile = pd.DataFrame(players_profile)
players_stats = pd.DataFrame(players_stats)
players_profile_stat = pd.merge(players_profile, players_stats, on=["id","name"]) #Jointure des 2 tableau
temp = pd.json_normalize(players_profile_stat['statistics']) #gestion des statistique
players_profile_stat = players_profile_stat.drop(columns=['statistics'])
players_profile_stat = pd.concat([players_profile_stat, temp], 1)

players_profile_stat.to_csv("handball.csv") #export pour simplifier l'analyse'
'''

### Traitement avec les classes ###

H = pandas.read_csv("handball.csv", sep=",", index_col=0) #Recuperation des donnees stockees
name = H["name"].str.split(',', expand=True) #Separation des noms
name.columns=["nom", "prenom"]
H = pandas.concat([H, name], 1)
H["Ratio_saved_conceded"] = round(H.saves/H.goals_conceded, 4) #Ajout de la colonne ratio arrets sur buts concedes
H["mean_goals"] = round(H.goals_scored/H.games_played, 2) #Ajout de la colonne but moyen par match
HA = H[ H['type'] != 'G' ]
HG = H[ H['type'] == 'G' ]

from classes import Basketteur, Attaquant_Handballeur, Goal_Handballeur
collectHandballeur=[]

for index, row in H.iterrows(): #On boucle sur le tableau H
    #Ajout des joeurs dans la collection selon leur poste
    if row['type'] == "G":
        i = Goal_Handballeur(row['prenom'],row['nom'],row['type'],row['equipe'],row['games_played'],row['goals_conceded'],row['saves'])
    else:
        i = Attaquant_Handballeur(row['prenom'],row['nom'],row['type'],row['equipe'],row['games_played'],row['assists'],row['goals_scored'])
    collectHandballeur.append(i) #insertion dans la liste
    
print(collectHandballeur[10])

#######################################Analyse generale#####################################

####Creation de boxplots

from PIL import Image, ImageTk

#Basket
Boxplot_points = sns.boxplot(x="pts", data=B,showfliers=False) #boxplot des points 
Boxplot_points.set_title("Points moyens des joueurs durant la saison")
Boxplot_points.set_xlabel('Nombre de points moyens')
plt.savefig("Boxplot_points.png") #enregistrement de l'image
im1 = Image.open('Boxplot_points.png') #importation de l'image
im1 = im1.resize((350, 280), Image.ANTIALIAS) #redimenssion de l'image
plt. clf()

Boxplot_rebond = sns.boxplot(x="reb", data=B,showfliers=False) #boxplot des rebonds
Boxplot_rebond.set_title("Rebons moyens du ballon que les joueurs réalisent durant la saison")
Boxplot_rebond.set_xlabel('Nombre de rebons moyens')
plt.savefig("Boxplot_rebond.png") #enregistrement de l'image
im2 = Image.open('Boxplot_rebond.png') #importation de l'image
im2 = im2.resize((350, 280), Image.ANTIALIAS) #redimenssion de l'image
plt. clf()

Boxplot_min = sns.boxplot(x="Temps_recod(min)", data=B) #boxplot du temps
Boxplot_min.set_title("Temps moyens sur le terrains des joueurs durant la saison")
Boxplot_min.set_xlabel('Temps moyens en min')
plt.savefig("Boxplot_min.png") #enregistrement de l'image
im3 = Image.open('Boxplot_min.png') #importation de l'image
im3 = im3.resize((350, 280), Image.ANTIALIAS) #redimenssion de l'image
plt. clf()

Boxplot_turnover = sns.boxplot(x="turnover", data=B,showfliers=False) #boxplot du temps
Boxplot_turnover.set_title("Perte de balle moyenne des joueurs durant la saison")
Boxplot_turnover.set_xlabel('perte de balle moyenne ')
plt.savefig("Boxplot_turnover.png") #enregistrement de l'image
im4 = Image.open('Boxplot_turnover.png') #importation de l'image
im4 = im4.resize((350, 280), Image.ANTIALIAS) #redimenssion de l'image
plt. clf()

#Hand
Boxplot_buts = sns.boxplot(x="mean_goals", data=HA,showfliers=False) #boxplot des buts moyen 
Boxplot_buts.set_title("Buts moyens des joueurs durant la competition")
Boxplot_buts.set_xlabel('Nombre de buts moyens')
plt.savefig("Boxplot_buts.png") #enregistrement de l'image
im5 = Image.open('Boxplot_buts.png') #importation de l'image
im5 = im5.resize((350, 280), Image.ANTIALIAS) #redimenssion de l'image
plt. clf()

Boxplot_ratio = sns.boxplot(x="Ratio_saved_conceded", data=HG,showfliers=False) #boxplot des ratio
Boxplot_ratio.set_title("Ratio de but sauves et concedes par les gardiens")
Boxplot_ratio.set_xlabel('Ratio des gardiens')
plt.savefig("Boxplot_ratio.png") #enregistrement de l'image
im6 = Image.open('Boxplot_ratio.png') #importation de l'image
im6 = im6.resize((350, 280), Image.ANTIALIAS) #redimenssion de l'image
plt. clf()

Boxplot_total = sns.boxplot(x="goals_scored", data=HA,showfliers=False) #boxplot des buts
Boxplot_total.set_title("Nombre de but total des joueurs durant la saison")
Boxplot_total.set_xlabel('Total de but')
plt.savefig("Boxplot_total.png") #enregistrement de l'image
im7 = Image.open('Boxplot_total.png') #importation de l'image
im7 = im7.resize((350, 280), Image.ANTIALIAS) #redimenssion de l'image
plt. clf()

Boxplot_assist = sns.boxplot(x="assists", data=HA,showfliers=False) #boxplot des assist
Boxplot_assist.set_title("Nombre d'assists total des joueurs durant la saison")
Boxplot_assist.set_xlabel("Total d'assist")
plt.savefig("Boxplot_assist.png") #enregistrement de l'image
im8 = Image.open('Boxplot_assist.png') #importation de l'image
im8 = im8.resize((350, 280), Image.ANTIALIAS) #redimenssion de l'image
plt. clf()

#Creation d'une fenetre tkinter pour visualiser les resultats 

root= Tk() #initialisation
root.title("Analyse Sportive") 
canvas= Canvas(root,width=900, height=600,bg = "white") #creation du canvas pour placer le code/graphique
canvas.pack() #mise en place dans la fenetre

#on les transforme en image pouvant se mettre dans tkinter
i1 = ImageTk.PhotoImage ( im1 )
i2 = ImageTk.PhotoImage ( im2 )
i3 = ImageTk.PhotoImage ( im3 )
i4 = ImageTk.PhotoImage ( im4 )
i5 = ImageTk.PhotoImage ( im5 )
i6 = ImageTk.PhotoImage ( im6 )
i7 = ImageTk.PhotoImage ( im7 )
i8 = ImageTk.PhotoImage ( im8 )


#Boutons qui permettent d'executer les fonctions
bouton_EquipeAlea_basket=Button(root, text= "Equipe aleatoire basket", width = 20, command=lambda:BasketballAnalyse().CompoAleatoireBask(B, collectBasketteur,canvas)).pack(side=LEFT)
bouton_MeilEquipe_basket=Button(root, text= "Meilleure equipe basket", width = 20, command=lambda:BasketballAnalyse().ProPlayerBask(B, collectBasketteur,canvas)).pack(side=LEFT)
bouton_Graph_basket=Button(root, text= "Graphiques basket", width = 20, command=lambda:BasketballAnalyse().Graphique(canvas,i1,i2,i3,i4)).pack(side=LEFT)

bouton_EquipeAlea_hand=Button(root, text= "Equipe aleatoire handball", width = 20, command=lambda:HandballAnalyse().CompoAleatoireHand(H, collectHandballeur,canvas)).pack(side=LEFT)
bouton_MeilEquipe_hand=Button(root, text= "Meilleure equipe handball", width = 20, command=lambda:HandballAnalyse().ProPlayerHand(H, collectHandballeur,canvas)).pack(side=LEFT)
bouton_Graph_hand=Button(root, text= "Graphiques handball", width = 20, command=lambda:HandballAnalyse().Graphique(canvas,i5,i6,i7,i8)).pack(side=LEFT)

bouton_quitter= Button(root, text="quitter",width = 20, command=root.quit()).pack(side=RIGHT)

root.mainloop() #lancement de l'interphace

