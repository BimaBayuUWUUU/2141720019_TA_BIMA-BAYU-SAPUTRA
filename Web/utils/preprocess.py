from utils.feature_extractor import create_single_df, normalize_rgb, calculate_ratios, rgb_to_hsv, rgb_to_lab

def extract_features_for_model(model_name, r, g, b):
    # Buat DataFrame dari input tunggal
    df = create_single_df(r, g, b)

    if model_name == "ann":
        # Gunakan semua 14 fitur untuk ANN_Best
        df = normalize_rgb(df)
        df = calculate_ratios(df)
        df = rgb_to_hsv(df)
        df = rgb_to_lab(df)
        features = df[['R', 'G', 'B', 'r', 'g', 'b', 'R_G_ratio', 'G_B_ratio', 'H', 'S', 'V', 'cL', 'ca', 'cb']].values

        return features[0]

    elif model_name == "adaboost_dt":
        # Gunakan semua 13 fitur
        df = normalize_rgb(df)
        df = calculate_ratios(df)
        df = rgb_to_hsv(df)
        df = rgb_to_lab(df)
        features = df[['R', 'G', 'B', 'r', 'g', 'b', 'R_G_ratio', 'G_B_ratio', 'H', 'S', 'cL', 'ca', 'cb']].values
        return features[0]

    elif model_name in ["adaboost_svm", "bagging_svm"]:
        # Hanya gunakan fitur r, g, b
        df = normalize_rgb(df)
        features = df[['r', 'g', 'b']].values
        return features[0]

    else:
        raise ValueError(f"Model {model_name} tidak dikenali.")
