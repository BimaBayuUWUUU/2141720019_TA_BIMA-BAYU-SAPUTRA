# utils/exporter.py
import pandas as pd
from datetime import datetime
import os

def export_classification_results(results_list, filename, data_dir, model_list):
    df = pd.DataFrame(results_list)

    # Buat nama file output
    base_name = os.path.splitext(filename)[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"hasil_klasifikasi_{base_name}_{timestamp}.xlsx"
    output_path = os.path.join(data_dir, output_filename)

    # Simpan ke Excel
    df.to_excel(output_path, index=False)

    return {
        "filename": output_filename,
        "file_path": output_path
    }