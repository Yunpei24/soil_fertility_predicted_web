from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import os

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

columns_name = ['N', 'P', 'K', 'pH', 'EC', 'OC', 'S', 'Zn', 'Fe', 'Cu', 'Mn', 'B']

# Définition du modèle Pydantic pour les données d'entrée
class InputData(BaseModel):
    Ratio_Nitrogen: int
    Ratio_Phosphorous: float
    Ratio_Potassium: float
    Soil_acidity_pH: float
    Electrical_conductivity: float
    Organic_carbon: float
    Sulfur: float
    Zinc: float
    Iron: float
    Copper: float
    Manganese: float
    Boron: float
# Fonction pour transformer les données d'entrée
def transform_features(features):
    """
    Transforme les caractéristiques en prenant le logarithme base 10 si la caractéristique est numérique.
    
    Args:
    - features : DataFrame contenant les caractéristiques à transformer
    
    Returns:
    - transformed_features : DataFrame contenant les caractéristiques transformées
    """
    def log_transform(x):
        if np.issubdtype(x.dtype, np.number):
            return np.log10(x)
        else:
            return x
    
    transformed_features = features.apply(log_transform)
    return transformed_features

# Fonction d'interprétation de la prédiction
def interpretation_predict(x):
    if x == 0:
        return "Sol Non fertile"
    elif x == 1:
        return "Sol Moyennement fertile"
    elif x == 2:
        return "Sol Très fertile"
    else:
        return None

# Répertoire où se trouve le fichier
directory = "./models/"

# Nom du fichier
# filename = "random_forest_pkl.pkl"

# Construire le chemin complet du fichier
# file_path = os.path.join(directory, filename)

# Charger le modèle sauvegardé
model = joblib.load('./models/random_forest_pkl.pkl')

# Créer une instance FastAPI
app = FastAPI()

# Endpoint pour les prédictions
@app.post("/predict/")
def predict(data: InputData):
    # Transformer les données d'entrée en un tableau NumPy 2D avec une seule ligne
    input_features = np.array([[getattr(data, element) for element in elements]])
    df_input_features = pd.DataFrame(input_features, columns=columns_name)
    input_features_transformer = transform_features(df_input_features)

    # Faire la prédiction avec le modèle chargé
    prediction = model.predict(input_features_transformer)

    int_predict = interpretation_predict(prediction[0])

    # Renvoyer la prédiction
    return JSONResponse(content={"prediction": int_predict})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)