"""
Predição para datasets.
"""

import pandas as pd

from app.predict import conflict_predict


def classificar_linha(row):

    resultado = conflict_predict(
        row["tweet_1"],
        row["tweet_2"]
    )

    row["P(NoConflict)"] = resultado["prob_nao_conflito"]
    row["P(Conflict)"] = resultado["prob_conflito"]
    row["Conflict"] = resultado["classificacao"]

    return row


def conflict_predict_dataset(df: pd.DataFrame):

    return df.apply(classificar_linha, axis=1)


def predict_csv(input_file: str, output_file: str):

    df = pd.read_csv(input_file)

    df = conflict_predict_dataset(df)

    df.to_csv(output_file, index=False)

    return df