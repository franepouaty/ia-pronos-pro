import streamlit as st
import requests
import json

# Récupération de votre clé Gemini sécurisée
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

st.set_page_config(page_title="IA Pronos Final", page_icon="⚽", layout="wide")

# Style CSS pour une lisibilité parfaite et de beaux affichages
st.markdown("""
    <style>
    .main-title { font-size:36px !important; font-weight: bold; color: #1E3A8A; text-align: center; }
    .section-title { font-size:24px !important; font-weight: bold; color: #2563EB; margin-top: 20px; }
    .report-box { font-size:18px !important; line-height: 1.6 !important; background-color: #F3F4F6; padding: 20px; border-radius: 12px; color: #1F2937; }
    .bar-container { background-color: #E5E7EB; border-radius: 8px; padding: 3px; margin-bottom: 10px; }
    .bar-fill { height: 20px; border-radius: 6px; text-align: right; padding-right: 10px; color: white; font-weight: bold; line-height: 20px; }
    </style>
    """, unsafe_allowed_html=True)

st.markdown('<p class="main-title">⚽ Assistant de Pronostics Spécial IA</p>', unsafe_allowed_html=True)

# 🏆 SECTION 1 : SELECTION DU CHAMPIONNAT
st.markdown('<p class="section-title">🏆 Choix de la Compétition</p>', unsafe_allowed_html=True)
championnats = ["Ligue 1 (France)", "Premier League (Angleterre)", "La Liga (Espagne)", "Serie A (Italie)", "Bundesliga (Allemagne)", "Ligue des Champions"]
choix_champ = st.selectbox("Sélectionnez le championnat à analyser :", championnats)

# ⚔️ SECTION 2 : SAISIE DES EQUIPES
st.markdown('<p class="section-title">⚔️ Les Clubs Face-à-Face</p>', unsafe_allowed_html=True)
col_e1, col_e2 = st.columns(2)
with col_e1:
    eq_dom = st.text_input("🏠 Équipe à Domicile", "Paris SG")
with col_e2:
    eq_ext = st.text_input("🚀 Équipe à l'Extérieur", "Marseille")

# 🔮 BOUTON D'ACTION
if st.button("🔮 Générer l'Analyse Complète"):
    with st.spinner("L'IA prépare les statistiques et l'analyse..."):
        try:
            # Connexion directe à Gemini
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
            
            # Extraction propre du texte reçu de l'API
            texte_recu = res['candidates'][0]['content']['parts'][0]['text']
            clean_json = texte_recu.strip().replace("```json", "").replace("```", "")
            data = json.loads(clean_json)
            
            # --- FORME RECENTE ---
            st.markdown('<p class="section-title">📊 Dynamique de Forme Récente</p>', unsafe_allowed_html=True)
            st.info(f"🏠 Derniers matchs de **{eq_dom}** : `{data['forme_domicile']}` | 🚀 Derniers matchs de **{eq_ext}** : `{data['forme_exterieur']}`")
                
            # --- TABLEAU DES JOUEURS ---
            st.markdown('<p class="section-title">🏃‍♂️ Comportement et Statistiques des Joueurs</p>', unsafe_allowed_html=True)
            table_data = [
                {"Équipe": eq_dom, "Joueur": data['j_dom_nom'], "Buts": data['j_dom_buts'], "Tirs Cadrés": data['j_dom_tirs'], "Fautes": data['j_dom_fautes'], "Cartons": data['j_dom_cartons']},
                {"Équipe": eq_ext, "Joueur": data['j_ext_nom'], "Buts": data['j_ext_buts'], "Tirs Cadrés": data['j_ext_tirs'], "Fautes": data['j_ext_fautes'], "Cartons": data['j_ext_cartons']}
            ]
            st.table(table_data)
                
            # --- GRAPHIQUE HTML PROPRE ---
            st.markdown('<p class="section-title">📈 Probabilités du Match</p>', unsafe_allowed_html=True)
            st.markdown(f"""
                <p>Victoire {eq_dom} ({data['p_dom']}%)</p>
                <div class="bar-container"><div class="bar-fill" style="width: {data['p_dom']}%; background-color: #10B981;">{data['p_dom']}%</div></div>
                <p>Match Nul ({data['p_nul']}%)</p>
                <div class="bar-container"><div class="bar-fill" style="width: {data['p_nul']}%; background-color: #F59E0B;">{data['p_nul']}%</div></div>
                <p>Victoire {eq_ext} ({data['p_ext']}%)</p>
                <div class="bar-container"><div class="bar-fill" style="width: {data['p_ext']}%; background-color: #EF4444;">{data['p_ext']}%</div></div>
            """, unsafe_allowed_html=True)
            
            # --- RAPPORT TEXTE ---
            st.markdown('<p class="section-title">🧠 Rapport Stratégique Rédigé par l\'IA</p>', unsafe_allowed_html=True)
            prompt_texte = f"Rédige une analyse détaillée en français pour le match {eq_dom} contre {eq_ext}. Explique la physionomie probable du match, l'importance des tirs cadrés et des cartons à venir, puis propose un score exact."
            payload_txt = {"contents": [{"parts": [{"text": prompt_texte}]}]}
            res_txt = requests.post(url_gemini, json=payload_txt).json()
            texte_final = res_txt['candidates'][0]['content']['parts'][0]['text']
            
            st.markdown(f'<div class="report-box">{texte_final.replace("\n", "<br>")}</div>', unsafe_allowed_html=True)
            
        except Exception as e:
            st.error("Une petite erreur de synchronisation avec l'IA. Veuillez cliquer à nouveau sur le bouton pour générer.")
