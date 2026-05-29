import streamlit as st
import requests
import json

# Récupération de votre clé Gemini sécurisée
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

st.set_page_config(page_title="IA Pronos Final", page_icon="⚽", layout="wide")

st.title("⚽ Assistant de Pronostics Spécial IA")
st.write("Analyse automatique basée sur les connaissances de l'IA Google Gemini.")

# 🏆 SECTION 1 : SELECTION DU CHAMPIONNAT
st.subheader("🏆 Choix de la Compétition")
championnats = ["Ligue 1 (France)", "Premier League (Angleterre)", "La Liga (Espagne)", "Serie A (Italie)", "Bundesliga (Allemagne)", "Ligue des Champions"]
choix_champ = st.selectbox("Sélectionnez le championnat à analyser :", championnats)

# ⚔️ SECTION 2 : SAISIE DES EQUIPES
st.subheader("⚔️ Les Clubs Face-à-Face")
col_e1, col_e2 = st.columns(2)
with col_e1:
    eq_dom = st.text_input("🏠 Équipe à Domicile", "Paris SG")
with col_e2:
    eq_ext = st.text_input("🚀 Équipe à l'Extérieur", "Marseille")

# 🔮 BOUTON D'ACTION
if st.button("🔮 Générer l'Analyse Complète"):
    with st.spinner("L'IA prépare les statistiques et l'analyse..."):
        try:
            url_gemini = f"https://googleapis.com{GEMINI_API_KEY}"
            
            prompt_data = f"""
            Donne les statistiques estimées actuelles pour le match {eq_dom} vs {eq_ext} ({choix_champ}) au format JSON strict. 
            Renvoie UNIQUEMENT l'objet JSON ci-dessous, sans aucune phrase autour, sans balise de code markdown.
            {{
                "forme_domicile": "WWDLW",
                "forme_exterieur": "LDWLW",
                "p_dom": 55,
                "p_nul": 25,
                "p_ext": 20,
                "j_dom_nom": "Joueur A", "j_dom_buts": 12, "j_dom_tirs": 24, "j_dom_fautes": 8, "j_dom_cartons": 1,
                "j_ext_nom": "Joueur B", "j_ext_buts": 9, "j_ext_tirs": 18, "j_ext_fautes": 14, "j_ext_cartons": 4
            }}
            Donne de vrais noms de joueurs actuels de ces clubs et des statistiques cohérentes.
            """
            
            payload = {"contents": [{"parts": [{"text": prompt_data}]}]}
            res = requests.post(url_gemini, json=payload).json()
            
            texte_recu = res['candidates']['content']['parts']['text']
            clean_json = texte_recu.strip().replace("```json", "").replace("```", "")
            data = json.loads(clean_json)
            
            # --- FORME RECENTE ---
            st.subheader("📊 Dynamique de Forme Récente")
            st.info(f"🏠 Derniers matchs de **{eq_dom}** : {data['forme_domicile']} | 🚀 Derniers matchs de **{eq_ext}** : {data['forme_exterieur']}")
                
            # --- TABLEAU DES JOUEURS ---
            st.subheader("🏃‍♂️ Comportement et Statistiques des Joueurs")
            table_data = [
                {"Équipe": eq_dom, "Joueur": data['j_dom_nom'], "Buts": data['j_dom_buts'], "Tirs Cadrés": data['j_dom_tirs'], "Fautes": data['j_dom_fautes'], "Cartons": data['j_dom_cartons']},
                {"Équipe": eq_ext, "Joueur": data['j_ext_nom'], "Buts": data['j_ext_buts'], "Tirs Cadrés": data['j_ext_tirs'], "Fautes": data['j_ext_fautes'], "Cartons": data['j_ext_cartons']}
            ]
            st.table(table_data)
                
            # --- GRAPHIQUE INTEGRÉ STANDARD ---
            st.subheader("📈 Probabilités du Match")
            st.progress(int(data['p_dom']))
            st.write(f"🟢 Chance Victoire **{eq_dom}** : {data['p_dom']}%")
            
            st.progress(int(data['p_nul']))
            st.write(f"🟡 Chance **Match Nul** : {data['p_nul']}%")
            
            st.progress(int(data['p_ext']))
            st.write(f"🔴 Chance Victoire **{eq_ext}** : {data['p_ext']}%")
            
            # --- RAPPORT TEXTE ---
            st.subheader("🧠 Rapport Stratégique Rédigé par l'IA")
            prompt_texte = f"Rédige une analyse détaillée en français pour le match {eq_dom} contre {eq_ext}. Explique la physionomie probable du match, l'importance des tirs cadrés et des cartons à venir, puis propose un score exact."
            payload_txt = {"contents": [{"parts": [{"text": prompt_texte}]}]}
            res_txt = requests.post(url_gemini, json=payload_txt).json()
            texte_final = res_txt['candidates']['content']['parts']['text']
            
            st.text_area(label="Analyse détaillée :", value=texte_final, height=300)
            
        except Exception as e:
            st.error("L'IA se synchronise. Veuillez recliquer sur le bouton pour valider l'affichage.")
