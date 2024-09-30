import streamlit as st
import requests

api_url = "http://127.0.0.1:8000"

# Fonction pour faire la prédiction à partir d'une image
def predict_image(image):
    # Code pour appeler l'API et faire la prédiction
    # Remplacer cette partie par votre propre code pour l'appel à l'API
    # et le traitement de la réponse
    prediction = "Fertile"  # Exemple de prédiction
    return prediction

# Fonction pour faire la prédiction à partir des valeurs saisies
def predict_values(values):
    response = requests.post(f"{api_url}/predict/", json=values)

    if response.status_code == 200:
        prediction = response.json()["prediction"]
        return prediction
    else:
        # Gérer les cas d'erreur
        return None

# Page d'accueil
def home():
    st.markdown(
        """
        <div style="font-size: 30px; font-weight: bold; color: skyblue; text-align: center;">
        Bienvenue dans notre application pour prédire la qualité du sol.
        </div>
        """,
        unsafe_allow_html=True
    )
    # Insérer une image de fond d'écran
    st.image("./images/fond_ecran.jpg", use_column_width=True)

# def home():
#     st.markdown(
#         """
#         <style>
#         # {
#             background-image: url('./images/fond_ecran2.jpg');
#             background-size: cover;
#             background-position: center;
#             height: 100vh;
#             width: 100vw;
#             display: flex;
#             justify-content: center;
#             align-items: center;
#         }
#         </style>
#         """,
#         unsafe_allow_html=True
#     )
#     st.markdown(
#         """
#         <div style="font-size: 30px; font-weight: bold; color: skyblue; text-align: center;">
#         Bienvenue dans notre application pour prédire la qualité du sol.
#         </div>
#         """,
#         unsafe_allow_html=True
#     )

    


# Page pour la prédiction à partir d'une image
def image_prediction():
    st.title("Prédiction à partir d'une image")
    uploaded_image = st.file_uploader("Charger une image ou prendre une photo")
    if uploaded_image is not None:
        image = uploaded_image.read()
        st.image(image, caption='Image chargée', use_column_width=True)
        if st.button('Prédire'):
            prediction = predict_image(image)
            st.write('La qualité du sol est :', prediction)

# Page pour la prédiction à partir des valeurs saisies
def values_prediction():
    st.title("Prédiction à partir des valeurs saisies")
    st.write("Veuillez saisir les valeurs pour les différents caractéristiques du sol")
    elements = [
    "Ratio_Nitrogen",
    "Ratio_Phosphorous",
    "Ratio_Potassium",
    "Soil_acidity_pH",
    "Electrical_conductivity",
    "Organic_carbon",
    "Sulfur",
    "Zinc",
    "Iron",
    "Copper",
    "Manganese",
    "Boron"
    ]

    features = [
    "Ratio of Nitrogen (NH4+)",
    "Ratio of Phosphorous (P)",
    "Ratio of Potassium (K)",
    "Soil acidity (pH)",
    "Electrical conductivity",
    "Organic carbon",
    "Sulfur (S)",
    "Zinc (Zn)",
    "Iron (Fe)",
    "Copper (Cu)",
    "Manganese (Mn)",
    "Boron (B)"]

    values = {}
    for ftr, elm in zip(features, elements):
        values[f"{elm}"] = st.text_input(f"{ftr}")
    if st.button('Prédire'):
        prediction = predict_values(values)
        st.write('La qualité du sol est :', prediction)

# Navigation entre les pages
def main():
    pages = {
        "Accueil": home,
        "Prédiction à partir d'une image": image_prediction,
        "Prédiction à partir des valeurs saisies": values_prediction
    }

    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Aller à", list(pages.keys()))

    page = pages[selection]
    page()

if __name__ == "__main__":
    main()
