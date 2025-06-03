from flask import Flask, render_template, request, jsonify, send_from_directory
from utils.model_loader import load_all_models
from utils.preprocess import extract_features_for_model
from utils.scaler_loader import get_scaler_for_model
from config import LOGS_DIR, MODEL_INFO, CLASS_LABELS, MODEL_LIST, MODELS_DIR, DATA_DIR, CLASS_RECOMMENDATIONS
from models import db, InputData, ClassificationResult, ClassificationResultFile
from utils.exporter import export_classification_results
import logging
import os
import pandas as pd
from collections import defaultdict
from dotenv import load_dotenv
import joblib
import numpy as np

# Load environment variables
load_dotenv()

# Inisialisasi Flask App
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
if app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inisialisasi SQLAlchemy
db.init_app(app)

# Load semua model saat aplikasi mulai
models = load_all_models()

# Setup logging
logging.basicConfig(
    filename=os.path.join(LOGS_DIR, "app.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


@app.route("/")
def welcome():
    return render_template("welcome.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", models=MODEL_INFO)


@app.route("/get_model_info/<model_name>")
def get_model_info(model_name):
    info = MODEL_INFO.get(model_name, "Informasi model tidak ditemukan.")
    return jsonify({"info": info})


@app.route("/classification", methods=["GET", "POST"])
def classification():
    results = []
    summary = {}  # Untuk menyimpan ringkasan hasil prediksi per model
    download_link = None  # Untuk link download file excel hasil
    classification_results = {}  # Untuk input manual

    if request.method == "POST":
        selected_models = request.form.get("selected_model", "").split(",")
        r = request.form.get("r")
        g = request.form.get("g")
        b = request.form.get("b")
        uploaded_file = request.files.get("csv_file")

        # Load PCA untuk ANN
        pca = None
        if "ann" in selected_models:
            try:
                pca = joblib.load(f"{MODELS_DIR}/best_pca_ANN_cv.pkl")
            except Exception as e:
                logging.error(f"Gagal memuat PCA: {e}")
                results.append("Error: File PCA tidak ditemukan atau rusak.")

        # Jika upload file CSV/Excel
        if uploaded_file:
            filename = uploaded_file.filename
            file_path = os.path.join(DATA_DIR, filename)
            uploaded_file.save(file_path)

            # Baca file berdasarkan ekstensi
            if filename.endswith(".csv"):
                df = pd.read_csv(file_path)
            elif filename.endswith((".xls", ".xlsx")):
                df = pd.read_excel(file_path)
            else:
                results.append("Error: Hanya file CSV atau Excel yang didukung.")
                return render_template(
                    "classification.html",
                    classification_results=results,
                    models=MODEL_LIST.items(),
                    model_info=MODEL_INFO,
                    summary=summary
                )

            # Validasi kolom
            required_columns = ['R', 'G', 'B']
            if not all(col in df.columns for col in required_columns):
                results.append("Error: File harus mengandung kolom R, G, dan B.")
                return render_template(
                    "classification.html",
                    classification_results=results,
                    models=MODEL_LIST.items(),
                    model_info=MODEL_INFO,
                    summary=summary
                )
            df = df[required_columns]

            # Inisialisasi summary
            for model_name in selected_models:
                summary[model_name] = defaultdict(int)

            new_input = None
            classification_results_list = []

            for _, row in df.iterrows():
                r_val = row['R']
                g_val = row['G']
                b_val = row['B']

                # Simpan input data sekali saja
                if new_input is None:
                    new_input = InputData(r=r_val, g=g_val, b=b_val, file_path=filename)
                    db.session.add(new_input)
                    db.session.flush()

                result_row = {
                    'R': r_val,
                    'G': g_val,
                    'B': b_val
                }

                for model_name in selected_models:
                    try:
                        x = extract_features_for_model(model_name, float(r_val), float(g_val), float(b_val))
                        scaler = get_scaler_for_model(model_name)
                        if scaler:
                            x = scaler.transform([x])

                        if model_name == "ann":
                            if pca is None:
                                raise ValueError("PCA belum dimuat atau tidak tersedia.")
                            x = pca.transform(x)
                        if model_name == "adaboost_dt":
                            x = np.array(x).reshape(1, -1)

                        prediction = models[model_name].predict(x)
                        predicted_class = str(prediction[0])
                        class_label = CLASS_LABELS.get(predicted_class, f"Kelas {predicted_class}")

                        summary[model_name][predicted_class] += 1

                        result = ClassificationResult(
                            input_data_id=new_input.id,
                            model_name=model_name,
                            predicted_class=predicted_class
                        )
                        db.session.add(result)

                        result_row[f"{MODEL_LIST[model_name]}"] = class_label
                    except Exception as e:
                        logging.error(f"Error processing model {model_name}: {e}")
                        result_row[f"{MODEL_LIST[model_name]}"] = f"Error: {str(e)}"
                        results.append(f"{MODEL_LIST[model_name]}: Error - {str(e)}")

                classification_results_list.append(result_row)

            # Ekspor hasil ke file
            exported = export_classification_results(classification_results_list, filename, DATA_DIR, MODEL_LIST)
            download_link = f"/static/data/{exported['filename']}"

            # Simpan informasi file hasil ke database
            new_result_file = ClassificationResultFile(
                filename=exported['filename'],
                file_path=exported['file_path'],
                input_file_id=new_input.id
            )
            db.session.add(new_result_file)

            db.session.commit()

        # Jika input manual
        elif all([r, g, b]):
            # Simpan input manual ke database
            new_input = InputData(r=r, g=g, b=b, file_path="Manual Input")
            db.session.add(new_input)
            db.session.commit()

            # Prediksi untuk tiap model
            for model_name in selected_models:
                try:
                    x = extract_features_for_model(model_name, float(r), float(g), float(b))
                    scaler = get_scaler_for_model(model_name)
                    if scaler:
                        x = scaler.transform([x])
                    if model_name == "ann":
                        if pca is None:
                            raise ValueError("PCA belum dimuat atau tidak tersedia.")
                        x = pca.transform(x)
                    if model_name == "adaboost_dt":
                        x = np.array(x).reshape(1, -1)

                    prediction = models[model_name].predict(x)
                    class_label = CLASS_LABELS.get(str(prediction[0]), f"Kelas {prediction[0]}")
                    classification_results[model_name] = class_label

                    result = ClassificationResult(
                        input_data_id=new_input.id,
                        model_name=model_name,
                        predicted_class=str(prediction[0])
                    )
                    db.session.add(result)
                    db.session.commit()
                except Exception as e:
                    logging.error(f"Error processing model {model_name}: {e}")
                    classification_results[model_name] = f"Error: {str(e)}"

    return render_template(
        "classification.html",
        classification_results=classification_results,
        models=MODEL_LIST.items(),
        models_names=MODEL_LIST,
        class_labels=CLASS_LABELS,  # Sudah benar
        summary=summary,
        download_link=download_link
    )
    
@app.route("/classification_bagging", methods=["GET", "POST"])
def classification_bagging():
    classification_result = None
    summary = {}
    download_link = None

    if request.method == "POST":
        r = request.form.get("r")
        g = request.form.get("g")
        b = request.form.get("b")
        uploaded_file = request.files.get("csv_file")

        model_name = "bagging_svm"
        model = models.get(model_name)
        if not model:
            classification_result = "Error: Model Bagging SVM tidak ditemukan."
            return render_template(
                "classification_bagging.html",
                classification_result=classification_result
            )

        if uploaded_file:
            filename = uploaded_file.filename
            file_path = os.path.join(DATA_DIR, filename)
            uploaded_file.save(file_path)

            try:
                if filename.endswith(".csv"):
                    df = pd.read_csv(file_path)
                elif filename.endswith((".xls", ".xlsx")):
                    df = pd.read_excel(file_path)
                else:
                    classification_result = "Error: Format file tidak didukung."
                    return render_template(
                        "classification_bagging.html",
                        classification_result=classification_result
                    )

                required_columns = ['R', 'G', 'B']
                if not all(col in df.columns for col in required_columns):
                    classification_result = "Error: File harus memiliki kolom R, G, dan B."
                    return render_template(
                        "classification_bagging.html",
                        classification_result=classification_result
                    )

                classification_results_list = []
                summary[model_name] = defaultdict(int)
                new_input = None

                for _, row in df.iterrows():
                    r_val, g_val, b_val = row['R'], row['G'], row['B']

                    if new_input is None:
                        new_input = InputData(r=r_val, g=g_val, b=b_val, file_path=filename)
                        db.session.add(new_input)
                        db.session.flush()

                    x = extract_features_for_model(model_name, float(r_val), float(g_val), float(b_val))
                    scaler = get_scaler_for_model(model_name)
                    if scaler:
                        x = scaler.transform([x])

                    prediction = model.predict(x)
                    predicted_class = str(prediction[0])
                    class_label = CLASS_LABELS.get(predicted_class, f"Kelas {predicted_class}")
                    recommendation = CLASS_RECOMMENDATIONS.get(predicted_class, "Tidak ada rekomendasi tersedia.")
                    summary[model_name][predicted_class] += 1

                    result_row = {
                        'R': r_val,
                        'G': g_val,
                        'B': b_val,
                        "Bagging SVM": class_label,
                        "Rekomendasi": recommendation
                    }
                    classification_results_list.append(result_row)

                exported = export_classification_results(classification_results_list, filename, DATA_DIR, MODEL_LIST)
                download_link = f"/static/data/{exported['filename']}"

                new_result_file = ClassificationResultFile(
                    filename=exported['filename'],
                    file_path=exported['file_path'],
                    input_file_id=new_input.id
                )
                db.session.add(new_result_file)
                db.session.commit()

            except Exception as e:
                logging.error(f"Error processing CSV: {e}")
                classification_result = f"Error: {str(e)}"

        elif all([r, g, b]):
            new_input = InputData(r=r, g=g, b=b, file_path="Manual Input")
            db.session.add(new_input)
            db.session.commit()

            x = extract_features_for_model(model_name, float(r), float(g), float(b))
            scaler = get_scaler_for_model(model_name)
            if scaler:
                x = scaler.transform([x])

            prediction = model.predict(x)
            predicted_class = str(prediction[0])
            class_label = CLASS_LABELS.get(predicted_class, f"Kelas {predicted_class}")
            recommendation = CLASS_RECOMMENDATIONS.get(predicted_class, "Tidak ada rekomendasi tersedia.")

            classification_result = f"<strong>Hasil Deteksi: </strong><span style='font-size: 24px; font-weight: bold;'>{class_label}</span><br><br>{recommendation}"

            db.session.add(ClassificationResult(
                input_data_id=new_input.id,
                model_name=model_name,
                predicted_class=predicted_class
            ))
            db.session.commit()

    return render_template(
        "classification_bagging.html",
        classification_result=classification_result,
        summary=summary,
        download_link=download_link,
        models_names=MODEL_LIST,
        CLASS_LABELS=CLASS_LABELS
    )

@app.route("/history")
def history():
    input_page = request.args.get("input_page", 1, type=int)
    result_file_page = request.args.get("result_file_page", 1, type=int)
    per_page = 10

    # Query gabungan untuk InputData dan ClassificationResult
    input_results_query = (
        db.session.query(InputData, ClassificationResult)
        .join(ClassificationResult, ClassificationResult.input_data_id == InputData.id)
        .order_by(InputData.uploaded_at.desc())
    )
    inputs_pagination = input_results_query.paginate(page=input_page, per_page=per_page)

    # Query untuk ClassificationResultFile
    result_files_pagination = ClassificationResultFile.query.order_by(ClassificationResultFile.created_at.desc()).paginate(
        page=result_file_page, per_page=per_page
    )

    return render_template(
        "history.html",
        inputs=inputs_pagination.items,
        result_files=result_files_pagination.items,
        input_pagination=inputs_pagination,
        result_file_pagination=result_files_pagination,
        models_names=MODEL_LIST,  # Pastikan MODEL_LIST didefinisikan
    )
    
@app.route("/download_csv/<filename>")
@app.route("/static/data/<filename>")
def download_result(filename):
    return send_from_directory(directory=DATA_DIR, path=filename, as_attachment=True)


if __name__ == "__main__":
    print("Aplikasi akan berjalan di http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)