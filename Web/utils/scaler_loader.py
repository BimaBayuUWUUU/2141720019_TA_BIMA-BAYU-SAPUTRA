import joblib
import os
from utils.config import SCALERS_DIR, SCALER_MAP

def get_scaler_for_model(model_name):
    scaler_filename = SCALER_MAP.get(model_name)
    if scaler_filename:
        return joblib.load(os.path.join(SCALERS_DIR, scaler_filename))
    return None  # Jika model tidak butuh scaler