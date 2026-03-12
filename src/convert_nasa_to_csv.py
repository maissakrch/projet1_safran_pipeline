import pandas as pd
from logger import log


def load_nasa_file(path):
    # Colonnes NASA (21 capteurs + settings)
    col_names = [
        "unit", "time", "op_setting_1", "op_setting_2", "op_setting_3"
    ] + [f"sensor_{i}" for i in range(1, 22)]

    df = pd.read_csv(path, sep=" ", header=None)
    df = df.dropna(axis=1, how="all")  # supprime colonnes vides
    df.columns = col_names
    return df

if __name__ == "__main__":
    df = load_nasa_file("data/raw/train_FD001.txt")
    df.to_csv("data/raw/train_FD001.csv", index=False)
    print("✔️ Conversion terminée : train_FD001.csv créé")
