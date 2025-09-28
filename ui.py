import gradio as gr
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

games = pd.read_csv("games_cleaned.csv", index_col="appid")
games["max_cover"] = games["header_image"]
titles = games["name"].to_dict()

embeddings = np.load("embeddings.npy")
appids = np.load("appids.npy")

# Funzione di raccomandazione
def recommend_from_multiple_ui(user_games, top_k=5):
    if not user_games:
        return [], gr.update(visible=False)

    # Converti titoli selezionati -> appid
    user_appids = []
    for t in user_games:
        found = [k for k, v in titles.items() if v.lower() == t.lower()]
        if found:
            user_appids.append(found[0])

    if not user_appids:
        return [], gr.update(visible=False)

    # Profilo utente = media degli embedding
    idxs = [np.where(appids == a)[0][0] for a in user_appids]
    user_profile = np.mean([embeddings[i] for i in idxs], axis=0)

    sims = cosine_similarity([user_profile], embeddings)[0]
    ranking = np.argsort(sims)[::-1]

    exclude = set(user_appids)
    results = [
        (games.loc[appids[i], "max_cover"], f"{titles[appids[i]]} — {sims[i]:.2f}")
        for i in ranking if appids[i] not in exclude
    ][:top_k]

    # Se ci sono risultati, rendi la gallery visibile
    return results, gr.update(visible=bool(results))



# Interfaccia Gradio

choices = list(titles.values())

with gr.Blocks() as demo:
    gr.Markdown("# 🎮 Game Recommender")
    gr.Markdown("### In questa pagina avrai a disposizione un sistema di raccomandazione dove, inserendo i giochi a cui hai giocato, otterrai 5 giochi che potrebbero interessarti!")
    gr.Markdown("### 💡 Pro Tip: più ne inserisci più i suggerimenti sono accurati!")

    # Dropdown searchable di default
    user_input = gr.Dropdown(
        choices=choices,
        multiselect=True,
        label="Inserisci i giochi che hai giocato e ti sono piaciuti:"
    )

    # Bottone raccomandazioni
    recommend_btn = gr.Button("Cerca giochi adatti a me!")

    # Gallery dei consigliaiti
    rec_gallery = gr.Gallery(
        label="Ti potrebbero piacere",
        columns=5,
        rows=1,
        height="auto",
        show_label=True,
        visible=False
    )

    # Evento click
    recommend_btn.click(
        fn=recommend_from_multiple_ui,
        inputs=user_input,
        outputs=[rec_gallery, rec_gallery]
    )

if __name__ == "__main__":
    demo.launch(share=True)
