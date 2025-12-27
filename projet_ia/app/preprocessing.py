# app/preprocessing.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, mutual_info_regression


# app/preprocessing.py

import pandas as pd
from sklearn.preprocessing import OrdinalEncoder


MUTUAL_FEATURES = [
    'Event_Type',
    'Venue_Capacity',
    'Marketing_Budget',
    'Pre_sale_Tickets',
    'Expected_Attendance',
    'Historical_Attendance_Similar_Events',
    'Venue_Rental_Cost',
    'Staff_Cost',
    'Stage_and_Equipment_Cost',
    'Permits_and_Licenses_Cost'
]

# Valeurs par défaut pour TOUTES les colonnes non-MUTUAL
DEFAULT_NON_MUTUAL = {
    "Price_per_Ticket": 40,
    "Nearby_Events": 1,
    "Competition_Level": "Medium",
    "Season": "Summer",
    "Location": "DefaultCity",
    "Weather_Forecast": "Sunny",
    "Indoor_Outdoor": "Indoor",
    "Day_of_week": "Monday",
    "Date": "2024-01-01"
}


# -----------------------
# PREPROCESS COMPLET
# -----------------------
def full_preprocess(X):
    X = X.copy()

    # Convert Date
    if "Date" in X.columns:
        X["Date"] = pd.to_datetime(X["Date"])
        X["Date"] = (X["Date"] - pd.Timestamp("1970-01-01")).dt.days

    # Frequency encoding
    for col in ['Location', 'Season', 'Weather_Forecast']:
        if col in X.columns:
            counts = X[col].value_counts()
            X[col] = X[col].map(counts)

    # One-hot
    if "Indoor_Outdoor" in X.columns:
        X = pd.get_dummies(X, columns=["Indoor_Outdoor"], drop_first=True)

    # Ordinal encoders
    if "Competition_Level" in X.columns:
        enc_comp = OrdinalEncoder(categories=[["Low", "Medium", "High"]])
        X["Competition_Level"] = enc_comp.fit_transform(X[["Competition_Level"]])

    if "Day_of_week" in X.columns:
        enc_day = OrdinalEncoder(categories=[[
            "Monday", "Tuesday", "Wednesday", "Thursday",
            "Friday", "Saturday", "Sunday"
        ]])
        X["Day_of_week"] = enc_day.fit_transform(X[["Day_of_week"]])

    return X


# -----------------------
# PREPROCESS POUR API
# -----------------------
def preprocess_input(df):
    df = df.copy()

    # Ajouter valeurs par défaut pour TOUTES les colonnes NON-MUTUAL
    for col, val in DEFAULT_NON_MUTUAL.items():
        if col not in df.columns:
            df[col] = val

    # Appliquer preprocess complet
    df = full_preprocess(df)

    # S'assurer que toutes les colonnes MUTUAL existent
    for col in MUTUAL_FEATURES:
        if col not in df.columns:
            df[col] = 0   # par sécurité

    #  Retourner uniquement les colonnes MUTUAL
    return df[MUTUAL_FEATURES]
