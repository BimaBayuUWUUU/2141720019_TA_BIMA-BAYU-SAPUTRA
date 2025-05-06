from flask import Flask, render_template, request, jsonify
from utils.model_loader import load_all_models
from utils.preprocess import extract_features_for_model
from utils.scaler_loader import get_scaler_for_model
from utils.config import LOGS_DIR
import logging
import os

app = Flask(__name__)

# Load semua model saat aplikasi mulai
models = load_all_models()

# Data deskripsi model
MODEL_INFO = {
    "ann": "Artificial Neural Network: Model berbasis jaringan saraf tiruan.",
    "adaboost_dt": "AdaBoost Decision Tree: Model ensemble menggunakan pohon keputusan.",
    "adaboost_svm_rbf": "AdaBoost SVM RBF: Model ensemble menggunakan kernel RBF.",
    "bagging_svm": "Bagging SVM: Ensemble method menggunakan SVM sebagai base estimator."
}

# Setup logging
logging.basicConfig(
    filename=os.path.join(LOGS_DIR, "app.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Route untuk halaman utama (Welcome Page)
@app.route("/")
def welcome():
    return render_template("welcome.html")

# Route untuk halaman Dashboard Model
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", models=MODEL_INFO.items())

# Route untuk mendapatkan informasi model (API JSON)
@app.route("/get_model_info/<model_name>")
def get_model_info(model_name):
    info = MODEL_INFO.get(model_name, "Informasi model tidak ditemukan.")
    return jsonify({"info": info})

# Route untuk halaman Klasifikasi
@app.route("/classification", methods=["GET", "POST"])
def classification():
    results = []
    if request.method == "POST":
        selected_models = request.form.getlist("selected_model")
        r = request.form.get("r")
        g = request.form.get("g")
        b = request.form.get("b")

        # Logging data yang diterima
        logging.info(f"Form submitted with R={r}, G={g}, B={b}, Models={selected_models}")

        # Validasi input
        if not all([r, g, b]):
            results.append("Error: Semua nilai R, G, dan B harus diisi.")
        elif not (0 <= int(r) <= 255 and 0 <= int(g) <= 255 and 0 <= int(b) <= 255):
            results.append("Error: Nilai R, G, dan B harus berada dalam rentang 0–255.")
        elif not selected_models:
            results.append("Error: Tidak ada model yang dipilih.")
        else:
            # Proses prediksi dengan model yang dipilih
            for model_name in selected_models:
                try:
                    # Ekstraksi fitur
                    x = extract_features_for_model(model_name, int(r), int(g), int(b))

                    # Scaler untuk model
                    scaler = get_scaler_for_model(model_name)
                    if scaler is not None:
                        x = scaler.transform([x])

                    # Prediksi
                    prediction = models[model_name].predict(x)
                    results.append(f"{MODEL_INFO[model_name]}: Kelas {prediction[0]}")
                except Exception as e:
                    logging.error(f"Error processing model {model_name}: {e}")
                    results.append(f"{MODEL_INFO[model_name]}: Error - {str(e)}")

    return render_template("classification.html", classification_results=results, models=MODEL_INFO.items())

if __name__ == "__main__":
    app.run(debug=True)