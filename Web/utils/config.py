import os

# Base directory project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Folder model
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Folder scaler
SCALERS_DIR = os.path.join(BASE_DIR, "scalers")

# Folder logs (jika pakai logging)
LOGS_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)  # Buat otomatis jika belum ada

# Nama model
MODEL_NAMES = {
    "ann": "ANN.pkl",
    "adaboost_dt": "AdaBoost DT.pkl",
    "adaboost_svm_rbf": "AdaBoost SVM.pkl",
    "bagging_svm": "Bagging SVM.pkl",
}

# Mapping model -> scaler
SCALER_MAP = {
    "ann": "scaler_ann.pkl",
    "adaboost_svm_rbf": "scaler_svm.pkl",
    "bagging_svm": "scaler_svm.pkl",
    # adaboost_dt tidak perlu scaler
}