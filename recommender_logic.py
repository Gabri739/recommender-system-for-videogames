import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Carica dati all'import del modulo (una sola volta)
games = pd.read_csv("games_cleaned.csv", index_col="appid")
games["max_cover"] = games["header_image"]
titles = games["name"].to_dict()

embeddings = np.load("embeddings.npy")
appids = np.load("appids.npy")

# Crea dizionari di lookup per prestazioni O(1)
appid_to_idx = {appid: idx for idx, appid in enumerate(appids)}
title_to_appid = {v.lower(): k for k, v in titles.items()}
all_titles_sorted = sorted(titles.values())


def search_games(query, max_results=50):

    if not query or len(query) < 2:
        return []

    query_lower = query.lower()
    matches = [title for title in all_titles_sorted if query_lower in title.lower()]

    return matches[:max_results]


def get_recommendations(game_titles, top_k=5):

    if not game_titles:
        raise ValueError("Nessun gioco fornito")

    # Converti titoli -> appids
    user_appids = [
        title_to_appid[game.lower()]
        for game in game_titles
        if game.lower() in title_to_appid
    ]

    if not user_appids:
        raise ValueError("Nessun gioco valido trovato")

    # Trova indici degli embedding
    idxs = [appid_to_idx[a] for a in user_appids if a in appid_to_idx]

    if not idxs:
        raise ValueError("Impossibile trovare gli embeddings per i giochi selezionati")

    # Calcola profilo utente come media degli embeddings
    user_profile = np.mean([embeddings[i] for i in idxs], axis=0)

    # Calcola similarità con tutti i giochi
    sims = cosine_similarity([user_profile], embeddings)[0]
    ranking = np.argsort(sims)[::-1]

    # Escludi i giochi già selezionati
    exclude = set(user_appids)
    results = []

    for i in ranking:
        if appids[i] not in exclude and len(results) < top_k:
            try:
                game_data = games.loc[appids[i]]
                cover = game_data["max_cover"]
                title = titles[appids[i]]
                similarity_score = sims[i]

                info = f"{title}\n : {similarity_score:.1%}"
                results.append((cover, info))
            except:
                continue

    if not results:
        raise ValueError("Non sono stati trovati giochi da raccomandare")

    return results