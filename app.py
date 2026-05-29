import streamlit as st
import google.generativeai as genai
import pandas as pd
import plotly.express as px
import json

# Récupération automatique de votre clé Gemini qui fonctionne
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)

st.set_page_config(page_title="IA Pronos Expert", page_icon="⚽", layout="wide")

# Style pour rendre les textes ultra-lisibles
st.markdown("""
    <style>
    .main-title { font-size:38px !important; font-weight: bold; color: #1E3A8A; text-align: center; }
    .section-title { font-size:24px !important; font-weight: bold; color: #2563EB; margin-top: 25px; }
    .report-box { font-size:18px !important; line-height: 1.6 !important; background-color: #F3F4F6; padding: 25px; border-radius: 12px; color: #1F2937; }
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
    with st.spinner("L'IA analyse le match, prépare les graphiques et les statistiques..."):
        try:
            # Demande structurée à l'IA pour créer les statistiques
            prompt_data = f"""
            Donne les statistiques estimées actuelles pour le match {eq_dom} vs {eq_ext} ({choix_champ}) au format JSON strict. 
            Renvoie UNIQUEMENT l'objet JSON ci-dessous, sans aucune phrase autour, sans balise de code markdown.
            {{
                "forme_domicile": "WWDLW",
                "forme_exterieur": "LDWLW",
                "pourcentage_domicile": 55,
                "pourcentage_nul": 25,
                "pourcentage_exterieur": 20,
                "joueurs_cle_domicile": [
                    {{"nom": "Joueur A", "buts": 12, "tirs_cadres": 24, "fautes": 8, "cartons": 1}}
                ],
                "joueurs_cle_exterieur": [
                    {{"nom": "Joueur B", "buts": 9, "tirs_cadres": 18, "fautes": 14, "cartons": 4}}
                ]
            }}
            Donne de vrais noms de joueurs actuels de ces clubs et des statistiques cohérentes.
            """
            
            model = genai.GenerativeModel('gemini-pro')
            reponse_data = model.generate_content(prompt_data)
            
            clean_json = reponse_data.text.strip().replace("```json", "").replace("```", "")
            data = json.loads(clean_json)
            
            # --- AFFICHAGE DE LA FORME RECENTE ---
            st.markdown('<p class="section-title">📊 Dynamique de Forme Récente</p>', unsafe_allowed_html=True)
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                st.info(f"Derniers matchs de **{eq_dom}** : `{data['forme_domicile']}` (W=Victoire, D=Nul, L=Défaite)")
            with col_f2:
                st.info(f"Derniers matchs de **{eq_ext}** : `{data['forme_exterieur']}`")
                
            # --- TABLEAUX DES JOUEURS CLÉS ---
            st.markdown('<p class="section-title">🏃‍♂️ Comportement et Statistiques des Joueurs</p>', unsafe_allowed_html=True)
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                st.write(f"**Joueurs clés - {eq_dom}**")
                st.dataframe(pd.DataFrame(data['joueurs_cle_domicile']), use_container_width=True)
            with col_t2:
                st.write(f"**Joueurs clés - {eq_ext}**")
                st.dataframe(pd.DataFrame(data['joueurs_cle_exterieur']), use_container_width=True)
                
            # --- GRAPHIQUE DES POURCENTAGES ---
            st.markdown('<p class="section-title">📈 Probabilités du Match</p>', unsafe_allowed_html=True)
            df_chart = pd.DataFrame({
                'Issue du match': [f"Victoire {eq_dom}", 'Match Nul', f"Victoire {eq_ext}"],
                'Chances (%)': [data['pourcentage_domicile'], data['pourcentage_nul'], data['pourcentage_exterieur']]
            })
            fig = px.bar(df_chart, x='Issue du match', y='Chances (%)', color='Issue du match', text='Chances (%)',
                         color_discrete_sequence=['#10B981', '#F59E0B', '#EF4444'])
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            # --- RAPPORT TEXTE GLOBAL ---
            st.markdown('<p class="section-title">🧠 Rapport Stratégique Rédigé par l\'IA</p>', unsafe_allowed_html=True)
            prompt_texte = f"Rédige une analyse détaillée en français pour le match {eq_dom} contre {eq_ext}. Explique la physionomie probable du match, l'importance des tirs cadrés et des cartons à venir, puis propose un score exact."
            reponse_texte = model.generate_content(prompt_texte)
            st.markdown(f'<div class="report-box">{reponse_texte.text.replace("\n", "<br>")}</div>', unsafe_allowed_html=True)
            
        except Exception as e:
            st.error("L'IA met à jour les données. Veuillez recliquer sur le bouton pour afficher le résultat.")
