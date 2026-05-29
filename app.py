import streamlit as st
import requests

# Récupération sécurisée de votre clé ChatGPT
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="IA Pronos ChatGPT", page_icon="⚽", layout="wide")
st.title("⚽ Assistant de Pronostics Spécial ChatGPT")
st.write("Analyse automatique et rapports d'experts rédigés en direct par l'IA d'OpenAI.")

# 🏆 CHOIX DE LA COMPÉTITION
st.subheader("🏆 Choix de la Compétition")
championnats = ["Ligue des Champions 🇪🇺", "Ligue 1 (France) 🇫🇷", "Premier League (Angleterre) 🏴\u200d󠁧󠁢󠁥󠁮󠁧󠁿", "La Liga (Espagne) 🇪🇸", "Serie A (Italie) 🇮🇹"]
choix_champ = st.selectbox("Sélectionnez votre championnat :", championnats)

# 📅 GRILLE DES MATCHS
st.subheader("📅 Grille des vrais matchs de la semaine")

def obtenir_matchs(nom_championnat):
    matchs_actuels = {
        "Ligue des Champions 🇪🇺": ["Real Madrid 🆚 Man. City", "Bayern Munich 🆚 Paris SG", "FC Barcelone 🆚 Arsenal", "Inter Milan 🆚 Liverpool"],
        "Ligue 1 (France) 🇫🇷": ["Paris SG 🆚 Marseille", "Monaco 🆚 Lyon", "Lille 🆚 Lens", "Rennes 🆚 Nice"],
        "Premier League (Angleterre) 🏴\u200d󠁧󠁢󠁥󠁮󠁧󠁿": ["Man. United 🆚 Liverpool", "Arsenal 🆚 Chelsea", "Man. City 🆚 Tottenham"],
        "La Liga (Espagne) 🇪🇸": ["Real Madrid 🆚 FC Barcelone", "Atlético Madrid 🆚 Séville"],
        "Serie A (Italie) 🇮🇹": ["Inter Milan 🆚 AC Milan", "Juventus 🆚 AS Rome"]
    }
    return matchs_actuels.get(nom_championnat, ["Match 1 🆚 Match 2"])

liste_matchs = obtenir_matchs(choix_champ)
match_choisi = st.selectbox("👉 Choisissez un match de la grille à analyser :", liste_matchs)

if match_choisi and st.button("🔮 Lancer l'Analyse par ChatGPT"):
    with st.spinner("ChatGPT examine l'historique et rédige votre rapport..."):
        try:
            # Paramétrage de la requête officielle OpenAI (Format standard)
            url_openai = "https://openai.com"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {OPENAI_API_KEY}"
            }
            
            prompt_systeme = "Tu es un expert mondial en pronostics de football et statistiques sportives. Tu rédiges en français."
            prompt_utilisateur = f"""
            Fais une analyse statistique et un pronostic pour le match : {match_choisi} dans la compétition {choix_champ}.
            Rédige un rapport complet, très aéré, espacé avec des puces contenant :
            1. 📊 ÉTAT DE FORME : Une estimation logique de la forme des deux équipes sur leurs 5 derniers matchs.
            2. 🏃‍♂️ COMPORTEMENT DES JOUEURS CLÉS : Quels joueurs actuels de ces clubs sont les plus dangereux (buteurs, tirs cadrés) ou agressifs (fautes, cartons) ?
            3. 📈 PROBABILITÉS EN % : Donne un pourcentage précis pour la Victoire Domicile, le Nul et la Victoire Extérieur.
            4. 🎯 PRONOSTIC FINAL : Propose un score exact probable argumenté.
            """
            
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": prompt_systeme},
                    {"role": "user", "content": prompt_utilisateur}
                ],
                "temperature": 0.7
            }
            
            # Envoi à OpenAI
            reponse = requests.post(url_openai, json=payload, headers=headers).json()
            
            # Extraction du texte rédigé par ChatGPT
            analyse_chatgpt = reponse['choices'][0]['message']['content']
            
            # Affichage du rapport
            st.markdown("---")
            st.subheader(f"🧠 Rapport Stratégique de l'IA — {match_choisi}")
            st.info(analyse_chatgpt)
            st.success("🎯 Pronostic généré avec succès par ChatGPT !")
            
        except Exception as e:
            st.error("Une erreur est survenue lors de la communication avec ChatGPT. Vérifiez que votre clé est bien collée et créditée de 5$.")
