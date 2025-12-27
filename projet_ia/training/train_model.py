# train_model.py
import pandas as pd
import joblib
from sklearn.linear_model import Lasso
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from app.preprocessing import apply_mutual_info

def train_model(train_df, test_df, save_path="models/best_model.pkl"):

    X_train = train_df.drop(columns=["Total_Cost"])
    y_train = train_df["Total_Cost"]

    X_test = test_df.drop(columns=["Total_Cost"])
    y_test = test_df["Total_Cost"]

    # Sélection Mutual Infos
    X_train_sel, selected_features = apply_mutual_info(X_train)
    X_test_sel, _ = apply_mutual_info(X_test)

    # Pipeline final
    preprocessor = ColumnTransformer([
        ("num", StandardScaler(), selected_features)
    ])

    model = Pipeline([
        ("prep", preprocessor),
        ("lasso", Lasso(alpha=0.8601819985213441, max_iter=5000))
    ])

    model.fit(X_train_sel, y_train)

    joblib.dump(model, save_path)
    print(f"Modèle sauvegardé dans {save_path}")

