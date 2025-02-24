import streamlit as st
import requests
try:
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    import sys
    sys.exit("Module 'bs4' introuvable. Veuillez installer 'beautifulsoup4' (ajoutez-le à requirements.txt).")
import pandas as pd
import base64
import os
import streamlit.components.v1 as components

# Configuration de la page
st.set_page_config(
    page_title="CoinAfrique Scraper",
    page_icon="👕",
    layout="wide"
)

# Bouton GitHub pour déploiement
github_url = "https://github.com/ton-repo/ton-projet"  # Remplace par le lien réel de ton dépôt GitHub
st.markdown(
    f"""
    <div style="position: absolute; top: 10px; right: 10px;">
        <a href="{github_url}" target="_blank">
            <button style="
                background-color: #333;
                color: white;
                border: none;
                padding: 10px 15px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 5px;
                cursor: pointer;
            ">
                🚀 Déployer sur GitHub
            </button>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

# Style personnalisé pour un design professionnel avec fond réduit pour les titres
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    
    body, .stApp {
        font-family: 'Roboto', sans-serif;
    }
    
    /* Titres principaux avec fond réduit */
    h1, h2 {
         display: inline-block;
         color: #ecf0f1;
         background-color: #2c3e50;
         padding: 5px 10px;
         margin: 10px 0;
         border-radius: 8px;
         font-weight: 700;
    }
    
    /* Style de la barre latérale */
    .css-1d391kg { 
         background-color: #34495e;
         color: #ecf0f1;
         padding: 15px;
         border-radius: 8px;
         margin-bottom: 15px;
    }
    
    /* Boutons avec dégradé et ombre */
    .stButton button {
         background-color: #2980b9;
         background-image: linear-gradient(90deg, #2980b9, #3498db);
         color: #fff;
         border: none;
         padding: 0.6em 1.2em;
         border-radius: 5px;
         font-size: 16px;
         font-weight: 600;
         box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
         transition: background 0.3s ease;
    }
    .stButton button:hover {
         background-image: linear-gradient(90deg, #3498db, #2980b9);
    }
    
    a {
         color: #2980b9;
         font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Définition des chemins des fichiers
PATHS = {
    "vetements": r"C:\Users\broco\Desktop\WorkSpace\Data collection\Mini_projet\coinafrique.csv",
    "chaussures": r"C:\Users\broco\Desktop\WorkSpace\Data collection\Mini_projet\coinafrique_ch.csv",
    "notebooks": [
        r"C:\Users\broco\Desktop\WorkSpace\Data collection\Mini_projet\data1.csv",
        r"C:\Users\broco\Desktop\WorkSpace\Data collection\Mini_projet\data2.csv"
    ],
    "background": r"C:\Users\broco\Desktop\WorkSpace\Data collection\Mini_projet\a-photo-of-clothing-and-shoes-in-a-shopp_1-W09orWT8iO1w3ZqbFwTA_ikM2TsvbSNyBF3K3aGLSNw.jpeg"
}

# Fonction d'arrière-plan
def set_background(image_path):
    try:
        with open(image_path, "rb") as f:
            img_data = f.read()
        b64_img = base64.b64encode(img_data).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url(data:image/jpeg;base64,{b64_img});
                background-size: cover;
                background-position: center;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except Exception as e:
        st.error(f"Erreur de chargement de l'image : {str(e)}")

set_background(PATHS["background"])

# Titre et description de l'application
st.title("🛍️ SCRAPER COINAFRIQUE")
st.markdown("""
**Application de collecte de données pour :**
- Vêtements Homme
- Chaussures Homme

*Par Alexis MANDO NGODJI - Étudiant en L2 Big Data*
""")

# Configuration des catégories pour le scraping
CATEGORIES = {
    "Vêtements Homme": {
        "url": "https://sn.coinafrique.com/categorie/vetements-homme",
        "fichier": PATHS["vetements"]
    },
    "Chaussures Homme": {
        "url": "https://sn.coinafrique.com/categorie/chaussures-homme",
        "fichier": PATHS["chaussures"]
    }
}

# Fonction de scraping sans nettoyage (données brutes)
def scraper_page(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        elements = []
        
        # Recherche des conteneurs d'annonces par classes
        containers = soup.find_all('div', class_='col-lg-4')
        if not containers:
            containers = soup.find_all('div', class_='card')
        
        for item in containers:
            try:
                price_elem = item.find('span', class_='price')
                if not price_elem:
                    price_elem = item.find('div', class_='price')
                price = price_elem.text.strip() if price_elem else "N/A"
                
                loc_elem = item.find('div', class_='location')
                if not loc_elem:
                    loc_elem = item.find('span', class_='location')
                location = loc_elem.text.strip() if loc_elem else "N/A"
                
                img_elem = item.find('img')
                image = img_elem.get('src') if img_elem else None
                
                if "vetements-homme" in url:
                    category = "Vêtements Homme"
                elif "chaussures-homme" in url:
                    category = "Chaussures Homme"
                else:
                    category = "Autre"
                
                elements.append({
                    'Catégorie': category,
                    'Prix': price,
                    'Localisation': location,
                    'Image': image
                })
            except Exception:
                continue
        
        return pd.DataFrame(elements)
    
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {str(e)}")
        return pd.DataFrame()

# Initialisation des variables dans session_state
if "show_google_form" not in st.session_state:
    st.session_state["show_google_form"] = False
if "show_kobo_form" not in st.session_state:
    st.session_state["show_kobo_form"] = False
if "scraped_data_by_page" not in st.session_state:
    st.session_state["scraped_data_by_page"] = {}
if "raw_data_total" not in st.session_state:
    st.session_state["raw_data_total"] = pd.DataFrame()

# Barre latérale pour les paramètres de scraping
with st.sidebar:
    st.header("⚙️ Paramètres de Scraping")
    categorie_scrap = st.selectbox("Choix de la catégorie", list(CATEGORIES.keys()))
    pages = st.slider("Nombre de pages à scraper", 1, 119, 3)
    
    if st.button("Démarrer le scraping"):
        data_by_page = {}
        df_total = pd.DataFrame()
        for page in range(1, pages + 1):
            url_page = f"{CATEGORIES[categorie_scrap]['url']}?page={page}"
            df_page = scraper_page(url_page)
            st.write(f"Page {page} : {len(df_page)} éléments récupérés")
            data_by_page[page] = df_page
            df_total = pd.concat([df_total, df_page], ignore_index=True)
        if not df_total.empty:
            # Sauvegarde du CSV
            df_total.to_csv(CATEGORIES[categorie_scrap]['fichier'], index=False)
            st.session_state.scraped_data_by_page = data_by_page
            st.session_state.raw_data_total = df_total
            st.success(f"✅ {len(df_total)} éléments collectés au total !")
        else:
            st.warning("Aucune donnée n'a été récupérée. Vérifie le sélecteur ou la structure du site.")

# Bouton pour afficher les données brutes complètes dans la zone principale
if not st.session_state.raw_data_total.empty:
    if st.button("Afficher les données brutes complètes"):
        st.subheader("Données brutes complètes")
        st.dataframe(st.session_state.raw_data_total)

# Bouton pour afficher les données scrappées par page dans la zone principale
if st.session_state.scraped_data_by_page:
    if st.button("Afficher les données scrappées par page"):
        for page, df_page in st.session_state.scraped_data_by_page.items():
            with st.expander(f"Page {page} - {len(df_page)} éléments"):
                st.dataframe(df_page)

# Section pour afficher les formulaires d'évaluation via des boutons
st.header("📋 Formulaires d'évaluation")
col1, col2 = st.columns(2)
with col1:
    if st.button("Afficher Google Form"):
         st.session_state["show_google_form"] = not st.session_state["show_google_form"]
with col2:
    if st.button("Afficher Kobo Collect"):
         st.session_state["show_kobo_form"] = not st.session_state["show_kobo_form"]

if st.session_state["show_google_form"]:
     st.subheader("Google Forms")
     components.iframe("https://docs.google.com/forms/d/e/1FAIpQLSfgJgHHC4hcshsTYBJIUd0v93wx2OyZJPKVr8PSTk71E717yw/viewform?embedded=true", height=800)

if st.session_state["show_kobo_form"]:
     st.subheader("Kobo Collect")
     # Hauteur augmentée pour afficher le formulaire Kobo en entier
     components.iframe("https://ee.kobotoolbox.org/x/SZNgvTy0", height=1500)

# Section Données Nettoyées (affichage des fichiers data1.csv et data2.csv)
st.header("🗂️ Données Nettoyées")
option_clean = st.selectbox("Choisissez les données nettoyées à afficher", ["Data1", "Data2"], key="clean_select")
data_files = {
    "Data1": r"C:\Users\broco\Desktop\WorkSpace\Data collection\Mini_projet\data1.csv",
    "Data2": r"C:\Users\broco\Desktop\WorkSpace\Data collection\Mini_projet\data2.csv"
}
selected_file = data_files[option_clean]
st.write(f"Chargement du fichier : {selected_file}")
try:
    df_clean = pd.read_csv(selected_file)
    st.subheader(f"Données Nettoyées - {option_clean}")
    st.dataframe(df_clean)
except Exception as e:
    st.error(f"Erreur lors du chargement des données nettoyées pour {option_clean} : {str(e)}")

# Pied de page
st.markdown("---")
st.markdown("""
**Sources de données :**  
[Vêtements Homme](https://sn.coinafrique.com/categorie/vetements-homme) | 
[Chaussures Homme](https://sn.coinafrique.com/categorie/chaussures-homme)

**Technologies utilisées :**  
Streamlit • BeautifulSoup • Pandas • Requests
""")
