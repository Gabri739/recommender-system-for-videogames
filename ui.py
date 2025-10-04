import gradio as gr

#import per la logica della raccomandazione
from recommender_logic import search_games as search_games_recommender
from recommender_logic import get_recommendations



#funzione cha chiama la funzione nel back end per trovare i giochi
def search_games(query):

    matches = search_games_recommender(query, max_results=50)

    if matches:
        return gr.update(choices=matches, visible=True, value=None)
    else:
        return gr.update(choices=[], visible=False, value=None)


#aggiunge il game ai game già selezionati
def add_game_to_list(selected_game, current_list):

    if not selected_game or selected_game == "":
        return current_list, "", gr.update(visible=False, value=None)

    if selected_game not in current_list:
        current_list.append(selected_game)

    # Reset del campo di ricerca
    return current_list, "", gr.update(visible=False, value=None)


#chiamata della funzione di raccomandazione presente nel back end
def recommend_from_multiple_ui(user_games):

    if not user_games:
        return [], gr.update(visible=False), gr.update(
            visible=True,
            value="⚠️ Seleziona almeno un gioco per ricevere raccomandazioni!"
        )

    try:
        results = get_recommendations(user_games, top_k=5)
        return results, gr.update(visible=True), gr.update(visible=False)

    except ValueError as e:
        error_msg = f"⚠️ {str(e)}"
        return [], gr.update(visible=False), gr.update(visible=True, value=error_msg)

    except Exception as e:
        error_msg = f"❌ Errore durante il calcolo: {str(e)}"
        print(error_msg)
        return [], gr.update(visible=False), gr.update(visible=True, value=error_msg)


# CSS inline per font uniforme per tutta la pagina di Gradio
custom_css = """
body, body *, input, textarea, select, button, label, .label, option, 
.markdown-text, .prose, p, h1, h2, h3, h4, h5, h6, span, div {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;}"""

# Interfaccia Gradio
with gr.Blocks(theme=gr.themes.Soft(), css=custom_css) as demo:
    gr.Markdown("# 🎮 Game Recommender System")
    gr.Markdown(
        "Cerca e seleziona i giochi che hai giocato e ti sono piaciuti per ricevere 5 raccomandazioni personalizzate."
    )

    with gr.Row():
        gr.Markdown("### 💡 **Pro Tip**: Più giochi inserisci, più accurate saranno le raccomandazioni!")

    with gr.Row():
        with gr.Column(scale=4):
            search_input = gr.Textbox(
                label="Cerca un gioco",
                placeholder="Digita almeno 2 lettere per cercare...",
                interactive=True
            )
            search_results = gr.Radio(
                choices=[],
                label="Risultati della ricerca",
                visible=False,
                interactive=True
            )

    # Lista giochi selezionati
    selected_games = gr.State([])

    games_display = gr.Dropdown(
        choices=[],
        multiselect=True,
        label="✅ Giochi selezionati (deseleziona per rimuovere)",
        info="I tuoi giochi preferiti appariranno qui",
        interactive=True
    )

    # Aggiorna i risultati mentre digiti
    search_input.change(
        fn=search_games,
        inputs=search_input,
        outputs=search_results
    )

    # Aggiungi cliccando direttamente su un risultato
    search_results.change(
        fn=add_game_to_list,
        inputs=[search_results, selected_games],
        outputs=[selected_games, search_input, search_results]
    ).then(
        fn=lambda x: gr.update(choices=x, value=x),
        inputs=selected_games,
        outputs=games_display
    )

    # Rimuovi gioco dalla lista quando viene deselezionato
    games_display.change(
        fn=lambda x: x,
        inputs=games_display,
        outputs=selected_games
    )

    recommend_btn = gr.Button("Trova giochi per me!", variant="primary", size="lg")

    # Messaggio di errore/info
    info_msg = gr.Markdown(visible=False)

    rec_gallery = gr.Gallery(
        label="Ti potrebbero piacere questi giochi",
        columns=5,
        rows=1,
        height="auto",
        show_label=True,
        visible=False,
        object_fit="cover"
    )

    gr.Markdown(
        "---\n"
        "**Come funziona?**\n"
        "1. Cerca un gioco digitando il nome nella casella di ricerca\n"
        "2. Seleziona il gioco dai risultati che appaiono\n"
        "3. Aggiungi i giochi che ti piacciono\n"
        "4. Clicca su 'Trova giochi per me!' per ricevere raccomandazioni personalizzate"
    )

    recommend_btn.click(
        fn=recommend_from_multiple_ui,
        inputs=selected_games,
        outputs=[rec_gallery, rec_gallery, info_msg]
    )

if __name__ == "__main__":
    demo.launch(share=True)