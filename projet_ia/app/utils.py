import pandas as pd
import numpy as np
from app.preprocessing import preprocess

def preprocess_single(features: dict):
    df = pd.DataFrame([features])
    df = preprocess(df)
    return df.values
