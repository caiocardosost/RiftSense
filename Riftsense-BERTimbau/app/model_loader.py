"""
Carregamento do modelo treinado.
"""

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)

from app.config import MODEL_PATH

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

model.eval()