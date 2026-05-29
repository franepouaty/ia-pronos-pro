import streamlit as st
import requests
from datetime import datetime

# Récupération automatique de vos clés sécurisées
FOOTBALL_API_KEY = st.secrets["FOOTBALL_API_KEY"]

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': FOOTBALL_API_KEY
}

st.set_page_config(page_title="IA Pronos Pro", page_icon="⚽", layout="wide")
st.title("⚽ Configuration du Championnat")

# Année dynamique (Saison en cours)
annee_actuelle = datetime.now().year

# Liste filtrée des grands championnats mondiaux
st.subheader("🏆 Sélection de la Compétition")
options_championnats = {
    "Ligue 1 (France)": 61,
    "Premier League (Angleterre)": 39,
    "La Liga (Espagne)": 140,
    "Serie A (Italie)": 135,
    "Bundesliga (Allemagne)": 78
}

choix_utilisateur = st.selectbox("Choisissez votre championnat :", list(options_championnats.keys()))
id_championnat = options_championnats[choix_utilisateur]

st.success(f"Idéal ! Vous avez sélectionné **{choix_utilisateur}** (ID: {id_championnat}) pour la saison {annee_actuelle}.")

