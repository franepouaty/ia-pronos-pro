import streamlit as st
import requests
from datetime import datetime

# Récupération de la clé de football uniquement
FOOTBALL_API_KEY = st.secrets["FOOTBALL_API_KEY"]

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': FOOTBALL_API_KEY
}

st.set_page_config(page_title="Pronos Live Réels", page_icon="⚽", layout="wide")
st.title("⚽ Analyseur de Matchs Réels en Temps Réel")
st.write("Cette version affiche la grille des vrais prochains matchs de la semaine.")

# Sélection du championnat
st.subheader("🏆 Choix de la Compétition")
options_championnats = {
    "Ligue 1 (France)": 61,
    "Premier League (Angleterre)": 39,
    "La Liga (Espagne)": 140,
    "Serie A (Italie)": 135,
    "Bundesliga (Allemagne)": 78
}
choix_champ = st.selectbox("Sélectionnez votre championnat :", list(options_championnats.keys()))
id_ligue = options_championnats[choix_champ]
annee_actuelle = datetime.now().year

# --- CHARGEMENT DE LA GRILLE DES MATCHS DE LA SEMAINE ---
st.subheader("📅 Grille des prochains matchs programmés")

@st.cache_data(ttl=1800)
def obtenir_matchs_semaine(ligue, annee):
    # Récupère les 10 prochains vrais matchs de la ligue
    url = f"https://api-sports.io{ligue}&season={annee}&next=10"
    res = requests.get(url, headers=headers).json()
    return res.get('response', [])

try:
    fixtures = obtenir_matchs_semaine(id_ligue, annee_actuelle) or obtenir_matchs_semaine(id_ligue, annee_actuelle - 1)
    
    if fixtures:
        liste_matchs = []
        details_matchs = {}
        
        for f in fixtures:
            titre = f"{f['teams']['home']['name']} 🆚 {f['teams']['away']['name']}"
            liste_matchs.append(titre)
            details_matchs[titre] = {
                "id_home": f['teams']['home']['id'],
                "name_home": f['teams']['home']['name'],
                "id_away": f['teams']['away']['id'],
                "name_away": f['teams']['away']['name']
            }
            
        match_choisi = st.selectbox("👉 Choisissez un vrai match de la grille à analyser :", liste_matchs)
        
        if match_choisi and st.button("🔮 Calculer les Statistiques Réelles & Pronostiquer"):
            data_m = details_matchs[match_choisi]
            
            with st.spinner("Récupération des vrais résultats récents..."):
                # Récupération de la vraie forme
                def get_real_form(team_id):
                    url = f"https://api-sports.io{id_ligue}&season={annee_actuelle}&team={team_id}"
                    r = requests.get(url, headers=headers).json()
                    if not r.get('response') or not r['response'].get('form'):
                        url = f"https://api-sports.io{id_ligue}&season={annee_actuelle-1}&team={team_id}"
                        r = requests.get(url, headers=headers).json()
                    f_str = r.get('response', {}).get('form', 'NNNNN')
                    return f_str[-5:] if f_str else 'NNNNN'
                
                forme_dom = get_real_form(data_m['id_home'])
                forme_ext = get_real_form(data_m['id_away'])
                
                # Affichage des formes réelles
                st.markdown("### 📊 Forme Récente Réelle (5 derniers matchs)")
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"🏠 **{data_m['name_home']}** : `{forme_dom}`")
                with col2:
                    st.info(f"🚀 **{data_m['name_away']}** : `{forme_ext}`")
                
                # Calcul de l'algorithme statistique
                pts_dom = sum([3 if l == 'W' else 1 if l == 'D' else 0 for l in forme_dom]) + 2
                pts_ext = sum([3 if l == 'W' else 1 if l == 'D' else 0 for l in forme_ext])
                total = pts_dom + pts_ext if (pts_dom + pts_ext) > 0 else 1
                
                p_dom = int((pts_dom / total) * 100)
                p_ext = int((pts_ext / total) * 100)
                p_nul = 100 - p_dom - p_ext
                
                # Affichage des probabilités réelles
                st.markdown("### 📈 Probabilités Basées sur les Vrais Résultats")
                st.progress(p_dom)
                st.write(f"🟢 Victoire **{data_m['name_home']}** : {p_dom}%")
                st.progress(p_nul)
                st.write(f"🟡 Match Nul : {p_nul}%")
                st.progress(p_ext)
                st.write(f"🔴 Victoire **{data_m['name_away']}** : {p_ext}%")
                
    else:
        st.error("Aucun match trouvé pour ce championnat. Vérifiez la validité de votre clé de football.")

except Exception as e:
    st.error("Erreur de connexion. Assurez-vous que votre FOOTBALL_API_KEY dans les Secrets Streamlit est valide.")
