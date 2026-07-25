"""
Configurações globais do projeto.
"""

import os

# Modelo treinado publicado no Hugging Face - 
#"MODEL_PATH" é a  variavel. Caso eu treine outro modelo, basta setar ela
# no docker com a rota do novo modelo
# do contrario, seleciona o modelo caiocardosost/RiftSense-BERTimbau-Base 
MODEL_PATH = os.getenv(
    "MODEL_PATH",
    "caiocardosost/RiftSense-BERTimbau-Base"
)

# Threshold de classificação
THRESHOLD = 0.40

# Tokenização
MAX_LENGTH = 128