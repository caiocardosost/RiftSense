"""
script abstrai as predições das instancias recebidas
"""

import torch

from app.config import THRESHOLD
from app.config import MAX_LENGTH
from app.model_loader import tokenizer
from app.model_loader import model


def conflict_predict(texto1: str, texto2: str):

    inputs = tokenizer(
        texto1,
        texto2,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=MAX_LENGTH
    )

    with torch.no_grad():

        outputs = model(**inputs)

        probs = torch.softmax(outputs.logits, dim=1)

    prob_nao_conflito = probs[0][0].item()
    prob_conflito = probs[0][1].item()

    classificacao = int(prob_conflito >= THRESHOLD)

    return {

        "classificacao": classificacao,

        "prob_conflito": prob_conflito,

        "prob_nao_conflito": prob_nao_conflito

    }