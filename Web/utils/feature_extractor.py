import numpy as np
import pandas as pd
import cv2


def normalize_rgb(df):
    df_norm = df.copy()
    df_norm['r'] = df_norm['R'] / 255
    df_norm['g'] = df_norm['G'] / 255
    df_norm['b'] = df_norm['B'] / 255
    return df_norm


def calculate_ratios(df):
    df_rasio = df.copy()
    df_rasio['R_G_ratio'] = df_rasio['R'] / df_rasio['G']
    df_rasio['G_B_ratio'] = df_rasio['G'] / df_rasio['B']
    return df_rasio


def rgb_to_hsv(df):
    df_hsv = df.copy()
    r, g, b = df_hsv['r'], df_hsv['g'], df_hsv['b']

    cmax = np.maximum.reduce([r, g, b])
    cmin = np.minimum.reduce([r, g, b])
    delta = cmax - cmin

    def calculate_hue():
        hue = np.zeros_like(delta)
        mask_r_max = (cmax == r) & (delta != 0)
        mask_g_max = (cmax == g) & (delta != 0)
        mask_b_max = (cmax == b) & (delta != 0)

        hue[mask_r_max] = (60 * ((g[mask_r_max] - b[mask_r_max]) / delta[mask_r_max]) + 360) % 360
        hue[mask_g_max] = (60 * ((b[mask_g_max] - r[mask_g_max]) / delta[mask_g_max]) + 120) % 360
        hue[mask_b_max] = (60 * ((r[mask_b_max] - g[mask_b_max]) / delta[mask_b_max]) + 240) % 360
        return hue

    h = calculate_hue()
    s = np.where(cmax != 0, delta / cmax, 0)
    v = cmax

    df_hsv['H'] = h
    df_hsv['S'] = s
    df_hsv['V'] = v
    return df_hsv


def rgb_to_lab(df):
    df_lab = df.copy()
    r = df_lab['r']
    g = df_lab['g']
    b = df_lab['b']

    def gamma_correction(c):
        return np.where(c > 0.04045, ((c + 0.055) / 1.055) ** 2.4, c / 12.92)

    r_linear = gamma_correction(r)
    g_linear = gamma_correction(g)
    b_linear = gamma_correction(b)

    X = 0.4124564 * r_linear + 0.3575761 * g_linear + 0.1804375 * b_linear
    Y = 0.2126729 * r_linear + 0.7151522 * g_linear + 0.0721750 * b_linear
    Z = 0.0193339 * r_linear + 0.1191920 * g_linear + 0.9503041 * b_linear

    Xn, Yn, Zn = 0.95047, 1.0, 1.08883

    def f(t):
        return np.where(t > 0.008856, t ** (1 / 3), 7.787 * t + 16 / 116)

    L = 116 * f(Y / Yn) - 16
    a = 500 * (f(X / Xn) - f(Y / Yn))
    b_val = 200 * (f(Y / Yn) - f(Z / Zn))

    df_lab['cL'] = L
    df_lab['ca'] = a
    df_lab['cb'] = b_val
    return df_lab


# Fungsi untuk membuat DataFrame dari input RGB tunggal
def create_single_df(r, g, b):
    return pd.DataFrame({"R": [r], "G": [g], "B": [b]})