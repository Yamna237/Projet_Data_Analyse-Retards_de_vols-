# README - Projet de Data Analyse sur les Retards de Vols ✈️

---

## 📌 Nom du projet

**Analyse exploratoire des retards de vols (Flight Delay Analysis)**

---

## 🎯 Objectif

Ce projet vise à analyser un grand volume de données liées aux vols aériens, en particulier les retards.  
L’objectif est d’identifier les facteurs influents, visualiser la distribution des retards et proposer des pistes d'optimisation.

---

## 🛠️ Étapes réalisées

1. Chargement du dataset CSV (plusieurs millions de lignes)  
2. Nettoyage :  
   - Suppression des doublons  
   - Suppression/remplacement des valeurs manquantes  
   - Transformation des types de données (dates, numériques, catégories)  
3. Exploration des variables :  
   - Distribution des retards  
   - Comparaison selon la distance, la compagnie, l'année, l’aéroport, etc.  
4. Visualisations avancées :  
   - Histogrammes des retards  
   - Boxplots par distance ou compagnie  
   - Barplots des retards par années  
   - Scatterplots (distance vs temps de vol...)  
5. Analyse de corrélations :  
   - Relation entre distance et retards  
   - Relation entre la distance de vol et le temps de vol  

---

## 💻 Technologies utilisées

- Python 3.8 (Spyder)  
- Pandas  
- NumPy  
- Matplotlib / Seaborn  

---

## 📊 Dataset

- **Format** : CSV (compressé)  
- **Source** : [Kaggle - Flight Delay Dataset](https://www.kaggle.com/datasets/patrickzel/flight-delay-and-cancellation-dataset-2019-2023)  
- **Taille** : ~3 millions de lignes  
- **Colonnes principales** :  
  - `flight_date`, `airline`, `origin`, `destination`  
  - `distance`, `dep_delay`, `arr_delay`  
  - `scheduled_time`, `actual_time`  

---

## 📝 Auteur

**Nom** : MOTCHIEMIEN YAMNA RIGOBERT  
**Email** : yamnamotchiemien@yahoo.com  
**Date** : 24/06/2025  

---

## 💡 Remarques

- Des optimisations mémoire ont été nécessaires pour charger le jeu de données.  
- Le traitement a été réalisé étape par étape via Spyder.  
- Projet adapté pour démontrer une compétence réelle en nettoyage, visualisation et structuration de données massives.
