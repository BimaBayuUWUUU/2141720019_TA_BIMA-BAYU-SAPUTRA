# utils/model_loader.py

import joblib
import os
from config import MODELS_DIR, MODEL_NAMES

def load_all_models():
    models = {}
    for model_key, filename in MODEL_NAMES.items():
        model_path = os.path.join(MODELS_DIR, filename)
        if not os.path.exists(model_path):
            print(f"[ERROR] File model '{filename}' tidak ditemukan di: {model_path}")
            continue
        try:
            model = joblib.load(model_path)
            models[model_key] = model
            print(f"[INFO] Model '{model_key}' ({filename}) berhasil dimuat.")
        except Exception as e:
            print(f"[ERROR] Gagal memuat model '{model_key}': {e}")
    return models