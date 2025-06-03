# utils/scaler_loader.py

import joblib
import os
from config import SCALERS_DIR, SCALER_MAP

def get_scaler_for_model(model_name):
    if model_name not in SCALER_MAP:
        print(f"[INFO] Model '{model_name}' tidak memerlukan scaler.")
        return None

    scaler_filename = SCALER_MAP[model_name]
    scaler_path = os.path.join(SCALERS_DIR, scaler_filename)

    if not os.path.exists(scaler_path):
        print(f"[ERROR] File scaler '{scaler_filename}' tidak ditemukan di: {scaler_path}")
        return None

    try:
        scaler = joblib.load(scaler_path)
        print(f"[INFO] Scaler '{scaler_filename}' untuk model '{model_name}' berhasil dimuat.")
        return scaler
    except Exception as e:
        print(f"[ERROR] Gagal memuat scaler '{scaler_filename}' untuk model '{model_name}': {e}")
        return None