import pandas as pd
from utils.feature_extractor import create_single_df, normalize_rgb, calculate_ratios, rgb_to_hsv, rgb_to_lab

def extract_features_for_model(model_name, r, g, b):
    # Buat DataFrame dari input tunggal
    df = create_single_df(r, g, b)

    # Sesuaikan ekstraksi berdasarkan model
    if model_name == "ann":
        df = normalize_rgb(df)
        df = rgb_to_hsv(df)
        features = df[['r', 'g', 'b', 'H', 'S', 'V']].values

    elif model_name in ["adaboost_svm_rbf", "bagging_svm"]:
        df = normalize_rgb(df)
        df = calculate_ratios(df)
        df = rgb_to_lab(df)
        features = df[['r', 'g', 'b', 'R_G_ratio', 'G_B_ratio', 'cL', 'ca', 'cb']].values

    elif model_name == "adaboost_dt":
        # Hanya gunakan R, G, B mentah
        features = df[['R', 'G', 'B']].values

    else:
        raise ValueError(f"Model {model_name} tidak dikenali.")

    return features[0]  # Kembalikan sebagai array 1D