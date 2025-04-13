from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Data dummy untuk deskripsi model
MODEL_INFO = {
    "ann": "Artificial Neural Network: Model berbasis jaringan saraf tiruan.",
    "adaboost_dt": "AdaBoost Decision Tree: Model ensemble menggunakan pohon keputusan.",
    "adaboost_svm_rbf": "AdaBoost SVM RBF: Model ensemble menggunakan kernel RBF."
}

# Route untuk halaman utama (Welcome Page)
@app.route("/")
def welcome():
    return render_template("welcome.html")

# Route untuk halaman Dashboard Model
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", models=list(MODEL_INFO.keys()))

# Route untuk mendapatkan informasi model (API JSON)
@app.route("/get_model_info/<model_name>")
def get_model_info(model_name):
    info = MODEL_INFO.get(model_name, "Informasi model tidak ditemukan.")
    return jsonify({"info": info})

# Route untuk halaman Klasifikasi
@app.route("/classification", methods=["GET", "POST"])
def classification():
    classification_results = []
    if request.method == "POST":
        # Ambil data dari form
        selected_models = request.form.getlist("selected_model")  # Mendukung multi-select
        r = request.form.get("r")
        g = request.form.get("g")
        b = request.form.get("b")

        # Simulasi hasil klasifikasi untuk setiap model
        for model in selected_models:
            result = f"Model: {model}, RGB: ({r}, {g}, {b})"
            classification_results.append(result)

    return render_template("classification.html", classification_results=classification_results)

if __name__ == "__main__":
    app.run(debug=True)