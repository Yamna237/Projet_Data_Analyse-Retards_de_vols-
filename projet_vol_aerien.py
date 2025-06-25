# -*- coding: utf-8 -*-
"""
Created on Sun Jun 15 09:36:34 2025

@author: rigobert
"""
#Projet python de DataAnalyse sur les retards de vol d'un aéroport aux états-unis

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

#CHARGEMENT ET PREPARATIONS DES DONNEES
#importation des données
Vol = pd.read_csv("C:/Users/rigobert/Desktop/Dossier DATA_ANALYST/DATA ANALYST/flights_sample_3m.csv")
# Pour inspecter les infos sur nos données:
Vol.info
# inspecter le type de données:
Vol.dtypes
# Visualiser les premières lignes:
Vol.head(5)

#NETTOYAGE DES DONNEES
#Gestion des valeurs manquantes
Vol.isnull().mean()*100  #Taux de valeurs manquantes par colonne

#Pour définir le nombre de lignes et colonnes a visualiser
pd.options.display.max_rows = 5
pd.options.display.max_columns = 32

#Supprimer les colonnes qui ont un taux de 90% de valeurs manquantes 
#Supprimer également les lignes avec plus de 25% de valeurs manquantes
Vol = Vol.dropna(axis=0, thresh =  int(0.75 * Vol.shape[1]))
Vol = Vol.dropna(axis=1, thresh = int(0.9 * len(Vol)))

#Traiter les valeurs manquantes restantes
for col in Vol.columns:
    if Vol[col].dtype in ['int64','float64']:
        Vol[col] = Vol[col].fillna(Vol[col].median())
    elif Vol[col].dtype == 'object':
        Vol[col] = Vol[col].fillna("inconnu")
    elif str(Vol[col].dtype).startswith('datetime'):
        Vol[col] = Vol[col].fillna(method="ffill")
        
#Correction des types
#Date de Vol
Vol["FL_DATE"] = pd.to_datetime(Vol["FL_DATE"],errors = "coerce") 
#Heure prevue de depart
Vol["CRS_DEP_TIME"] =Vol["CRS_DEP_TIME"].astype(str).str.zfill(4)
Vol["CRS_DEP_TIME"]=Vol["CRS_DEP_TIME"].str[:2] +":"+Vol["CRS_DEP_TIME"].str[2:]
Vol["CRS_DEP_TIME"]=pd.to_datetime(Vol["CRS_DEP_TIME"],format = "%H:%M",errors = "coerce")
#Creation d'une colonne pour convertir en min
Vol["CRS_DEP_TIME_min"]=Vol["CRS_DEP_TIME"].dt.hour*60 + Vol["CRS_DEP_TIME"].dt.minute
#Heure réelle de Depart
Vol["DEP_TIME"] = Vol["DEP_TIME"].astype(int)
Vol["DEP_TIME"] =Vol["DEP_TIME"].astype(str).str.zfill(4)
Vol["DEP_TIME"]=Vol["DEP_TIME"].str[:2] +":"+Vol["DEP_TIME"].str[2:]
Vol["DEP_TIME"]=pd.to_datetime(Vol["DEP_TIME"],format = "%H:%M",errors = "coerce")
##Creation d'une colonne pour convertir en min
Vol["DEP_TIME_min"]=Vol["DEP_TIME"].dt.hour*60 + Vol["DEP_TIME"].dt.minute
#Retard au départ
Vol["REAL_DEP_DELAY"] = Vol["CRS_DEP_TIME_min"] - Vol["DEP_TIME_min"]
#Heure prevue d'arrivé
Vol["CRS_ARR_TIME"] =Vol["CRS_ARR_TIME"].astype(str).str.zfill(4)
Vol["CRS_ARR_TIME"]=Vol["CRS_ARR_TIME"].str[:2] +":"+Vol["CRS_ARR_TIME"].str[2:]
Vol["CRS_ARR_TIME"]=pd.to_datetime(Vol["CRS_ARR_TIME"],format = "%H:%M",errors = "coerce")
#Convertion en min
Vol["CRS_ARR_TIME_min"]=Vol["CRS_ARR_TIME"].dt.hour*60 + Vol["CRS_ARR_TIME"].dt.minute
#Heure réelle d'arrivé
Vol["ARR_TIME"] = Vol["ARR_TIME"].astype(int)
Vol["ARR_TIME"] =Vol["ARR_TIME"].astype(str).str.zfill(4)
Vol["ARR_TIME"]=Vol["ARR_TIME"].str[:2] +":"+Vol["ARR_TIME"].str[2:]
Vol["ARR_TIME"]=pd.to_datetime(Vol["ARR_TIME"],format = "%H:%M",errors = "coerce")
##Creation d'une colonne pour convertir en min
Vol["ARR_TIME_min"]=Vol["ARR_TIME"].dt.hour*60 + Vol["ARR_TIME"].dt.minute
#Retard a l'arrivé
Vol["REAL_ARR_DELAY"] = Vol["CRS_ARR_TIME_min"] - Vol["ARR_TIME_min"]
#Analyse de la ponctualité des vols
#Nombre de vols au départ à l'heure,en avance ou en retard
#En avance
Nbr_vol_av_dep = (Vol["REAL_DEP_DELAY"] > 0).sum()
#En retard
Nbr_vol_rtrd_dep = (Vol["REAL_DEP_DELAY"] < 0).sum()
#A l'heure
Nbr_vol_a_lheure_depj = (Vol["REAL_DEP_DELAY"] == 0).sum()

#Nombre de vols à l'arrivée à l'heure,en avance ou en retard
Nbr_vol_av_arr = (Vol["REAL_ARR_DELAY"] > 0).sum()
#En retard
Nbr_vol_rtrd_arr = (Vol["REAL_ARR_DELAY"] < 0).sum()
#A l'heure
Nbr_vol_a_lheure_arr = (Vol["REAL_ARR_DELAY"] == 0).sum()

#Retard Median
Med_Retard_Vol_Depart = Vol["REAL_DEP_DELAY"].median()
Med_Retard_Vol_Arrivee = Vol["REAL_ARR_DELAY"].median()

#Detection des outliers
Q1=Vol["REAL_DEP_DELAY"].quantile(0.75)
Q3=Vol["REAL_DEP_DELAY"].quantile(0.25)
IQR= Q3- Q1
lower_bound = Q1 - 1.5*IQR
upper_bound = Q1 + 1.5*IQR
outliers = Vol[(Vol["REAL_DEP_DELAY"] < lower_bound) | (Vol["REAL_DEP_DELAY"] > upper_bound)]

plt.boxplot(Vol['REAL_DEP_DELAY'].dropna())
plt.title("Boxplot des retards au depart")
plt.ylabel('Minutes')
plt.grid(True)
plt.show()

#Retard median par compagnie au départ
RtdD_Med_Par_Cpgn= Vol.groupby ('AIRLINE')["REAL_DEP_DELAY"].median()
#Retard median par compagnie a l'arrivé
RtdA_Med_Par_Cpgn= Vol.groupby ('AIRLINE')["REAL_ARR_DELAY"].median()

#Retard au depart par aéoroports
RtdD_Med_Par_Aero= Vol.groupby ('ORIGIN_CITY')["DEP_DELAY"].median()

#Retard à l'arrivée par aéoroports
RtdA_Med_Par_Aero= Vol.groupby ('DEST_CITY')["ARR_DELAY"].median()

#creation de la colonne Année
Vol["Année"] = Vol["FL_DATE"].dt.year

#Creation de la cololle Mois
Vol["Mois"] = Vol["FL_DATE"].dt.to_period("M")

#Analyse des temps de vols et des distances parcourues
#Top 20 des Itineraires les plus long
Iti_longs = Vol["DISTANCE"].nlargest(20)
#Top 20 des Itineraires les plus courts
Iti_courts = Vol["DISTANCE"].nsmallest(20)

#CORRELATION ENTRE LA DUREE DE VOL ET LA DISTANCE
Corr_dis_tpsvol = Vol[["AIR_TIME","DISTANCE"]].corr()

#rapport de temps de vol par compagnies
Vol["rapport_tps_vol"] = Vol["ELAPSED_TIME"] - Vol["CRS_ELAPSED_TIME"]
Rprt_diff_vol_par_cpgn= Vol.groupby("AIRLINE")["rapport_tps_vol"].median()

#VISUALISATION
#Nombre de vols en avance au départ par compagnie
Avance_depart =Vol[Vol["REAL_DEP_DELAY"] > 0]
nbr_vol_par_cpgn_DA =Avance_depart.groupby("AIRLINE")["REAL_DEP_DELAY"].count().reset_index()
plt.figure(figsize=(7,7))
sns.barplot(data = nbr_vol_par_cpgn_DA, x ="AIRLINE", y ="REAL_DEP_DELAY")
plt.title("Nombre de vols en avance au départ par compagnie")
plt.xlabel("Compagnies Aériennes")
plt.ylabel("Nombre de vols")
plt.xticks(rotation=90)
plt.yticks(ticks=range(0,300001,50000))
plt.ylim(0,300000)
plt.tight_layout()
plt.savefig("NbreD_vols_avances_cpgn.png")
plt.show

#Nombre de vols a l'heure par au depart compagnie
Ponc_depart =Vol[Vol["REAL_DEP_DELAY"] == 0]
nbr_vol_par_cpgn_DH =Ponc_depart.groupby("AIRLINE")["REAL_DEP_DELAY"].count().reset_index()
plt.figure(figsize=(7,7))
sns.barplot(data = nbr_vol_par_cpgn_DH, x ="AIRLINE", y ="REAL_DEP_DELAY")
plt.title("Nombre de vols à l'heure au départ par compagnie")
plt.xlabel("Compagnies Aériennes")
plt.ylabel("Nombre de vols")
plt.xticks(rotation=90)
plt.yticks(ticks=range(0,50001,10000))
plt.ylim(0,50000)
plt.tight_layout()
plt.savefig("NbreD_vols_a_l'heure_cpgn.png")
plt.show

#Nombre de vols en retard au depart par compagnie
Retard_depart =Vol[Vol["REAL_DEP_DELAY"] < 0]
nbr_vol_par_cpgn_DR =Retard_depart.groupby("AIRLINE")["REAL_DEP_DELAY"].count().reset_index()
plt.figure(figsize=(7,7))
sns.barplot(data = nbr_vol_par_cpgn_DR, x ="AIRLINE", y ="REAL_DEP_DELAY")
plt.title("Nombre de vols en retard au départ par compagnie")
plt.xlabel("Compagnies Aériennes")
plt.ylabel("Nombre de vols")
plt.xticks(rotation=90)
plt.yticks(ticks=range(0,300001,40000))
plt.ylim(0,300000)
plt.tight_layout()
plt.savefig("NbreD_vols_a_retard_cpgn.png")
plt.show

#Nombre de vols en retard a l'arrivée par compagnie
Retard_Arrivée =Vol[Vol["REAL_ARR_DELAY"] < 0]
nbr_vol_par_cpgn_AR =Retard_Arrivée.groupby("AIRLINE")["REAL_ARR_DELAY"].count().reset_index()
plt.figure(figsize=(7,7))
sns.barplot(data = nbr_vol_par_cpgn_AR, x ="AIRLINE", y ="REAL_ARR_DELAY")
plt.title("Nombre de vols en retard a l'arrivée par compagnie")
plt.xlabel("Compagnies Aériennes")
plt.ylabel("Nombre de vols")
plt.xticks(rotation=90)
plt.yticks(ticks=range(0,300001,40000))
plt.ylim(0,300000)
plt.tight_layout()
plt.savefig("NbreA_vols_a_retard_cpgn.png")
plt.show

#Nombre de vols a l'heure a l'arrivée par compagnie
Retard_Arrivée =Vol[Vol["REAL_ARR_DELAY"] == 0]
nbr_vol_par_cpgn_AH =Retard_Arrivée.groupby("AIRLINE")["REAL_ARR_DELAY"].count().reset_index()
plt.figure(figsize=(7,7))
sns.barplot(data = nbr_vol_par_cpgn_AH, x ="AIRLINE", y ="REAL_ARR_DELAY")
plt.title("Nombre de vols a l'heure a l'arrivée par compagnie")
plt.xlabel("Compagnies Aériennes")
plt.ylabel("Nombre de vols")
plt.xticks(rotation=90)
plt.yticks(ticks=range(0,15001,4000))
plt.ylim(0,15000)
plt.tight_layout()
plt.savefig("NbreA_vols_a_l'heure_cpgn.png")
plt.show

#Nombre de vols a l'avance a l'arrivée par compagnie
Retard_Arrivée =Vol[Vol["REAL_ARR_DELAY"] < 0]
nbr_vol_par_cpgn_AA =Retard_Arrivée.groupby("AIRLINE")["REAL_ARR_DELAY"].count().reset_index()
plt.figure(figsize=(7,7))
sns.barplot(data = nbr_vol_par_cpgn_AA, x ="AIRLINE", y ="REAL_ARR_DELAY")
plt.title("Nombre de vols en avance a l'arrivée par compagnie")
plt.xlabel("Compagnies Aériennes")
plt.ylabel("Nombre de vols")
plt.xticks(rotation=90)
plt.yticks(ticks=range(0,300001,40000))
plt.ylim(0,300000)
plt.tight_layout()
plt.savefig("NbreA_vols_a_l'avance_cpgn.png")
plt.show

#NOMBRE DE VOLS A L'HEURE,EN RETARD ET A l'AVANCE PAR ANNEE
#Nombre de vols en avance au départ par année
Avance_depart =Vol[Vol["REAL_DEP_DELAY"] > 0]
nbr_vol_par_An_DA =Avance_depart.groupby("Année")["REAL_DEP_DELAY"].count().reset_index()
plt.figure(figsize=(7,7))
sns.barplot(data = nbr_vol_par_An_DA, x ="Année", y ="REAL_DEP_DELAY")
plt.title("Nombre de vols en avance au départ par Année")
plt.xlabel("Année")
plt.ylabel("Nombre_de_vols")
plt.xticks(rotation=0)
plt.yticks(ticks=range(0,500001,50000))
plt.ylim(0,500000)
plt.tight_layout()
plt.savefig("NbreD_vols_a_l'avance_An.png")
plt.show

#Nombre de vols en retard au départ par année
Avance_depart =Vol[Vol["REAL_DEP_DELAY"] < 0]
nbr_vol_par_An_DR =Avance_depart.groupby("Année")["REAL_DEP_DELAY"].count().reset_index()
plt.figure(figsize=(7,7))
sns.barplot(data = nbr_vol_par_An_DR, x ="Année", y ="REAL_DEP_DELAY")
plt.title("Nombre de vols en retard au départ par Année")
plt.xlabel("Année")
plt.ylabel("Nombre_de_vols")
plt.xticks(rotation=0)
plt.yticks(ticks=range(0,300001,50000))
plt.ylim(0,300000)
plt.tight_layout()
plt.savefig("NbreD_vols_en_retard_An.png")
plt.show

#Nombre de vols a l'heure au départ par année
Avance_depart =Vol[Vol["REAL_DEP_DELAY"] == 0]
nbr_vol_par_An_DH =Avance_depart.groupby("Année")["REAL_DEP_DELAY"].count().reset_index()
plt.figure(figsize=(7,7))
sns.barplot(data = nbr_vol_par_An_DH, x ="Année", y ="REAL_DEP_DELAY")
plt.title("Nombre de vols a l'heure au départ par Année")
plt.xlabel("Année")
plt.ylabel("Nombre_de_vols")
plt.xticks(rotation=0)
plt.yticks(ticks=range(0,50001,10000))
plt.ylim(0,50000)
plt.tight_layout()
plt.savefig("NbreD_vols_a_l'heure_An.png")
plt.show

#Nombre de vols en avance a l'arrivée par année
Avance_Arrivée =Vol[Vol["REAL_ARR_DELAY"] > 0]
nbr_vol_par_An_AA =Avance_Arrivée.groupby("Année")["REAL_ARR_DELAY"].count().reset_index()
plt.figure(figsize=(7,7))
sns.barplot(data = nbr_vol_par_An_AA, x ="Année", y ="REAL_ARR_DELAY")
plt.title("Nombre de vols en avance a l'arrivée par Année")
plt.xlabel("Année")
plt.ylabel("Nombre_de_vols")
plt.xticks(rotation=0)
plt.yticks(ticks=range(0,500001,50000))
plt.ylim(0,500000)
plt.tight_layout()
plt.savefig("NbreA_vols_a_l'avance_An.png")
plt.show

#Nombre de vols en retard a l'arrivée par année
Avance_Arrivée =Vol[Vol["REAL_ARR_DELAY"] < 0]
nbr_vol_par_An_AR =Avance_Arrivée.groupby("Année")["REAL_ARR_DELAY"].count().reset_index()
plt.figure(figsize=(7,7))
sns.barplot(data = nbr_vol_par_An_AR, x ="Année", y ="REAL_ARR_DELAY")
plt.title("Nombre de vols en retard a l'arrivée par Année")
plt.xlabel("Année")
plt.ylabel("Nombre_de_vols")
plt.xticks(rotation=0)
plt.yticks(ticks=range(0,300001,50000))
plt.ylim(0,300000)
plt.tight_layout()
plt.savefig("NbreA_vols_en_retard_An.png")
plt.show

#Nombre de vols a l'heure au départ par année
Avance_Arrivée =Vol[Vol["REAL_ARR_DELAY"] == 0]
nbr_vol_par_An_AH =Avance_Arrivée.groupby("Année")["REAL_DEP_DELAY"].count().reset_index()
plt.figure(figsize=(7,7))
sns.barplot(data = nbr_vol_par_An_DH, x ="Année", y ="REAL_DEP_DELAY")
plt.title("Nombre de vols a l'heure a l'arrivée par Année")
plt.xlabel("Année")
plt.ylabel("Nombre_de_vols")
plt.xticks(rotation=0)
plt.yticks(ticks=range(0,50001,10000))
plt.ylim(0,50000)
plt.tight_layout()
plt.savefig("NbreA_vols_a_l'heure_An.png")
plt.show

#DISTRIBUTION DU RETARD A L'ARRIVEE SELON LA DISTANCE DE VOL
plt.figure(figsize=(8,8))
sns.scatterplot(data=Vol, x="DISTANCE",y="REAL_ARR_DELAY")
plt.title("Distribution du retard en foncetion de la distance")
plt.xlabel("Distances(miles)")
plt.ylabel("Retard(min)")
plt.savefig("Distribution_retard_tps-vol.png")
plt.show

#DISTRIBUTION DU TEMPS A DE VOL SELON LA DISTANCE DE VOL
plt.figure(figsize=(8,8))
sns.scatterplot(data=Vol, x="DISTANCE",y="AIR_TIME")
plt.title("Distribution du temps de vol en foncetion de la distance")
plt.xlabel("Distances(miles)")
plt.ylabel("Temps de vol(min)")
plt.savefig("Distribution_distance-vol_tps-vol.png")
plt.show

#Sauvevegarde du dataset traité
Vol.to_csv("Retard_vols_traité.csv",index=False)



