"""
Classifica um único par de tweets.
"""

from app.predict import conflict_predict


texto1 = input("Tweet 1: ")
texto2 = input("Tweet 2: ")

resultado = conflict_predict(texto1, texto2)

print()

print("===== RiftSense =====")

print()

print(f"P(NoConflict): {resultado['prob_nao_conflito']:.4f}")
print(f"P(Conflict): {resultado['prob_conflito']:.4f}")

print()

print(
    "Classificação:",
    "CONFLITO"
    if resultado["classificacao"]
    else "NÃO CONFLITO"
)