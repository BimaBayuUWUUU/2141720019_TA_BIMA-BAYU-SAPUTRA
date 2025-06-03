import os

# Base directory project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Folder model
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Folder data
DATA_DIR = os.path.join(BASE_DIR, "data")

# Folder scaler
SCALERS_DIR = os.path.join(BASE_DIR, "scalers")

# Folder logs (jika pakai logging)
LOGS_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

# app.py

MODEL_INFO = {
    "ann": {
        "name": "Artificial Neural Network",
        "description": "Model berbasis jaringan saraf tiruan.",
        "slides": [
            {"image": "/static/images/ann/7.png", "caption": "ANN - Sekilas Model"},
            {"image": "/static/images/ann/8.png", "caption": "ANN - Parameter Model"},
            {"image": "/static/images/ann/9.png", "caption": "ANN - Parameter Model"},
            {"image": "/static/images/ann/Performance_CV.png", "caption": "ANN - Hasil Evaluasi Cross Validation"},
            {"image": "/static/images/ann/LC_CV.png", "caption": "ANN - Learning Curve dengan Cross Validation"},
            {"image": "/static/images/ann/Performance_Final.png", "caption": "ANN - Hasil Evaluasi Data Testing"},
            {"image": "/static/images/ann/LC_Final.png", "caption": "ANN - Learning Curve Data Testing"},
            {"image": "/static/images/ann/Performance_Final.png", "caption": "ANN - Hasil Evaluasi Data Testing"}
        ]
    },
    "adaboost_dt": {
        "name": "AdaBoost Decision Tree",
        "description": "Model ensemble menggunakan pohon keputusan.",
        "slides": [
            {"image": "/static/images/adaboost_dt/5.png", "caption": "Adaboost DT - Sekilas Model"},
            {"image": "/static/images/adaboost_dt/6.png", "caption": "Adaboost DT  - Parameter Model"},
            {"image": "/static/images/adaboost_dt/Performance_CV.png", "caption": "Adaboost DT  - Hasil Evaluasi Cross Validation"},
            {"image": "/static/images/adaboost_dt/LC_CV.png", "caption": "Adaboost DT  - Learning Curve dengan Cross Validation"},
            {"image": "/static/images/adaboost_dt/Performance_Final.png", "caption": "Adaboost DT  - Hasil Evaluasi Data Testing"},
            {"image": "/static/images/adaboost_dt/LC_Final.png", "caption": "Adaboost DT  - Learning Curve Data Testing"},
            {"image": "/static/images/adaboost_dt/Performance_Final.png", "caption": "Adaboost DT  - Hasil Evaluasi Data Testing"}
        ]
    },
    "adaboost_svm": {
        "name": "AdaBoost SVM RBF",
        "description": "Model ensemble menggunakan kernel RBF.",
        "slides": [
            {"image": "/static/images/adaboost_svm/3.png", "caption": "Adaboost SVM - Sekilas Model"},
            {"image": "/static/images/adaboost_svm/4.png", "caption": "Adaboost SVM - Parameter Model"},
            {"image": "/static/images/adaboost_svm/Performance_CV.png", "caption": "Adaboost SVM - Hasil Evaluasi Cross Validation"},
            {"image": "/static/images/adaboost_svm/LC_CV.png", "caption": "Adaboost SVM - Learning Curve dengan Cross Validation"},
            {"image": "/static/images/adaboost_svm/Performance_Final.png", "caption": "Adaboost SVM - Hasil Evaluasi Data Testing"},
            {"image": "/static/images/adaboost_svm/LC_Final.png", "caption": "Adaboost SVM - Learning Curve Data Testing"},
            {"image": "/static/images/adaboost_svm/Performance_Final.png", "caption": "Adaboost SVM - Hasil Evaluasi Data Testing"}
        ]
    },
    "bagging_svm": {
        "name": "Bagging SVM RBF",
        "description": "Ensemble method menggunakan SVM sebagai base estimator.",
        "slides": [
            {"image": "/static/images/bagging_svm/1.png", "caption": "Adaboost DT - Sekilas Model"},
            {"image": "/static/images/bagging_svm/2.png", "caption": "Adaboost DT - Parameter Model"},
            {"image": "/static/images/bagging_svm/Performance_CV.png", "caption": "Adaboost DT - Hasil Evaluasi Cross Validation"},
            {"image": "/static/images/bagging_svm/LC_CV.png", "caption": "Adaboost DT - Learning Curve dengan Cross Validation"},
            {"image": "/static/images/bagging_svm/Performance_Final.png", "caption": "Adaboost DT - Hasil Evaluasi Data Testing"},
            {"image": "/static/images/bagging_svm/LC_Final.png", "caption": "Adaboost DT - Learning Curve Data Testing"},
            {"image": "/static/images/bagging_svm/Performance_Final.png", "caption": "Adaboost DT - Hasil Evaluasi Data Testing"}
        ]
    }
}

MODEL_LIST = {
    "ann": "Artificial Neural Network",
    "adaboost_dt": "AdaBoost Decision Tree",
    "adaboost_svm": "AdaBoost Support Vector Machine",
    "bagging_svm": "Bagging Support Vector Machine"
}

CLASS_LABELS = {
    '0': 'Tanpa Penyemprotan Silika Sekam Padi',
    '1': 'Dosis Satu Kali Penyemprotan Silika Sekam Padi',
    '2': 'Dosis Tiga Kali Penyemprotan Silika Sekam Padi',
    '3': 'Dosis Lima Kali Penyemprotan Silika Sekam Padi',
}

CLASS_RECOMMENDATIONS = {
    '0': 'Lakukan penyemprotan pupuk Silika Sekam Padi sebanyak Satu Kali untuk melihat hasil yang berbeda. Jika hasilnya tidak memuaskan, pertimbangkan untuk meningkatkan jumlah penyemprotan menjadi Tiga sampai Lima Kali Penyemprotan.',
    '1': 'Lakukan penyemprotan pupuk Silika Sekam Padi sebanyak Tiga Kali untuk melihat hasil yang berbeda. Jika hasilnya tidak memuaskan, pertimbangkan untuk meningkatkan jumlah penyemprotan menjadi Lima Kali Penyemprotan.',
    '2': 'Lakukan penyemprotan pupuk Silika Sekam Padi sebanyak Lima Kali untuk melihat hasil yang berbeda. Lima kali setiap pemeberian adalah jumlah penyemprotan yang sudah diuji, jika hasilnya tidak memuaskan, pertimbangkan untuk mencoba Tujuh atau Enam Penyemprotan terlebih dahulu.',
    '3': 'Anda sudah mencapai jumlah optimal penyemprotan pupuk Silika Sekam Padi yang pernah diuji. Jika anda ingin melakukan uji coba lebih lanjut, pertimbangkan untuk mencoba Enam atau Tujuh Penyemprotan terlebih dahulu.',
}

# Mapping model
MODEL_NAMES = {
    "ann": "ANN_Best.joblib",
    "adaboost_dt": "AdaBoost_DT_Best.joblib",
    "adaboost_svm": "AdaBoost_SVM_Best.joblib",
    "bagging_svm": "Bagging_SVM_Best.joblib",
}

# Mapping model -> 
SCALER_MAP = {
    "ann": "scaler_ANN_Best.joblib",
    "adaboost_svm": "scaler_AdaBoost_SVM_Best.joblib",
    "bagging_svm": "scaler_Bagging_SVM_Best.joblib",
    # adaboost_dt tidak memerlukan scaler
}