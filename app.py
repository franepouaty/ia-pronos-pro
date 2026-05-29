import streamlit as st
import requests
from datetime import datetime

# Récupération automatique de votre clé sécurisée
FOOTBALL_API_KEY = st.secrets["FOOTBALL_API_KEY"]

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': FOOTBALL_API_KEY
}

st.set_page_config(page_title="IA Pronos Pro", page_icon="⚽", layout="wide")
st.title("⚽ Sélection des Équipes en Temps Réel")

# Détermination automatique de la saison de football en cours
annee_actuelle = datetime.now().year

# Liste filtrée des grands championnats
options_championnats = {
    "Ligue 1 (France)": 61,
    "Premier League (Angleterre)": 39,
    "La Liga (Espagne)": 140,
    "Serie A (Italie)": 135,
    "Bundesliga (Allemagne)": 78
}

choix_utilisateur = st.selectbox("🏆 Choisissez votre championnat :", list(options_championnats.keys()))
id_championnat = options_championnats[choix_utilisateur]

# --- FONCTION POUR CHARGER LES ÉQUIPES ET LES LOGOS ---
@st.cache_data(ttl=3600)
def charger_equipes(ligue, annee):
    # Requête pour récupérer les clubs de la saison en cours
    url = f"https://api-sports.io{ligue}&season={annee}"
    res = requests.get(url, headers=headers).json()
    
    # Sécurité : si la saison n'a pas encore de données, on prend la saison précédente
    if not res.get('response'):
        url = f"https://api-sports.io{ligue}&season={annee-1}"
        res = requests.get(url, headers=headers).json()
        
    return {item['team']['name']: {"id": item['team']['id'], "logo": item['team']['logo']} for item in res.get('response', [])}

try:
    # Téléchargement des équipes du championnat sélectionné
    dict_equipes = charger_equipes(id_championnat, annee_actuelle)
    liste_equipes = sorted(list(dict_equipes.keys()))

    # Affichage des deux listes de sélection côte à côte
    st.subheader("⚔️ Configuration de l'affrontement")
    col1, col2 = st.columns(2)
    
    with col1:
        eq_dom = st.selectbox("🏠 Équipe Domicile", liste_equipes, index=0)
        # Affichage du logo de l'équipe domicile
        st.image(dict_equipes[eq_dom]['logo'], width=100)
        
    with col2:
        eq_ext = st.selectbox("🚀 Équipe Extérieur", liste_equipes, index=min(1, len(liste_equipes)-1))
        # Affichage du logo de l'équipe extérieur
        st.image(dict_equipes[eq_ext]['logo'], width=100)

except Exception as e:
    st.error("Impossible de charger les équipes. Vérifiez que votre FOOTBALL_API_KEY est bien configurée dans les Secrets Streamlit.")
