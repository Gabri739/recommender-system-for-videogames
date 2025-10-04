# 🎮 Game Recommender

**Game Recommender** è un sistema di raccomandazione progettato per consigliare videogiochi sulla base di alcuni titoli forniti in input dall’utente.  
Il sistema si basa sul concetto di **similarità tra videogiochi**, costruito considerando tre fattori principali trasformati in embeddings:

- **Descrizione breve del gioco**  
- **Tags del gioco** (generi e caratteristiche come *FPS, Multiplayer, Co-op, Adventure, Action...*)  
- **Numero totale di recensioni** (come indicatore di popolarità e analisi sociale)

Il database su cui si fonda il progetto è disponibile su Kaggle al seguente link:  https://www.kaggle.com/datasets/artermiloff/steam-games-dataset

In particolare il file usato è: games_march2025_cleaned.csv

## Metodo di raccomandazione
Il sistema cerca di formare un **profilo utente** a partire dai giochi inseriti in input e utilizza la **cosine similarity** per calcolare i titoli più affini a quel profilo.

L’obiettivo di questo progetto è fornire agli utenti uno strumento intuitivo e intelligente per scoprire nuovi videogiochi che potrebbero apprezzare, partendo dai loro gusti personali.
