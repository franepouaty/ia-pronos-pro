import streamlit as st
import requests

# Récupération de votre clé Gemini sécurisée
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

st.set_page_config(page_title="IA Pronos Final", page_icon="⚽", layout="wide")

st.title("⚽ Assistant de Pronostics Spécial IA")
st.write("Analyse automatique basée sur les connaissances en temps réel de l'IA Google Gemini.")

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
    with st.spinner("L'IA Gemini rédige votre rapport d'expert..."):
        try:
            # Nouvelle URL 2026 utilisant le modèle mis à jour gemini-1.5-flash
            url_gemini = f"https://googleapis.com{GEMINI_API_KEY}"
            
            prompt_texte = f"""
            Tu es un expert mondial en pronostics de football. Analyse le match : {eq_dom} contre {eq_ext} dans le championnat {choix_champ}.
            Rédige un rapport complet, très aéré et ultra-lisible en français contenant obligatoirement :
            
            1. 📊 ÉTAT DE FORME RÉCENT : Donne la forme simulée des 5 derniers matchs pour chaque équipe (Victoires, Nuls, Défaites).
            2. 🏃‍♂️ STATISTIQUES DES JOUEURS CLÉS : Cite les vrais joueurs actuels de ces clubs capables de marquer, de cadrer des tirs, ou risquant de commettre des fautes et prendre des cartons.
            3. 📈 PROBABILITÉS DU MATCH : Donne une estimation claire en pourcentages de chance (Victoire Domicile %, Match Nul %, Victoire Extérieur %).
            4. 🎯 PRONOSTIC FINAL : Donne ton avis d'expert avec un score exact probable argumenté.
            """
            
            payload = {"contents": [{"parts": [{"text": prompt_texte}]}]}
            res = requests.post(url_gemini, json=payload).json()
            
            # Lecture sécurisée selon la structure du nouveau modèle
            texte_final = res['candidates'][0]['content']['parts'][0]['text']
            
            # Affichage du rapport
            st.subheader("🧠 Rapport Stratégique de l'IA")
            st.text_area(label="Analyse détaillée générée :", value=texte_final, height=450)
            
            st.success("🎯 Analyse terminée avec succès !")
            
        except Exception as e:
            st.error("Problème de validation de la clé. Assurez-vous que le texte dans vos Secrets Streamlit est exactement : GEMINI_API_KEY = \"votre_cle\" sans espaces superflus.")
