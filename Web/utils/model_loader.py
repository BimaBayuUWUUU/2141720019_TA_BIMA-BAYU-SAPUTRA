import joblib
import os
from utils.config import MODELS_DIR, MODEL_NAMES

def load_all_models():
    return {
        key: joblib.load(os.path.join(MODELS_DIR, filename))
        for key, filename in MODEL_NAMES.items()
    }