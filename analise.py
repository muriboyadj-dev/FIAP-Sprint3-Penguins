"""
Challenge Sprint 3
Base de dados: Palmer Penguins (CC0)
Fonte: Gorman KB, Williams TD, Fraser WR (2014). PLoS ONE 9(3): e90081.
        Disponibilizado por Allison Horst - https://github.com/allisonhorst/palmerpenguins

Este script reproduz as três análises feitas no notebook:
1. Probabilidade acima da mediana
2. Probabilidade no intervalo (media +/- 2 desvios-padrao)
3. Regressao linear simples

Todas as analises usam apenas a especie Adelie, pois misturar as tres
especies quebra a suposicao de distribuicao Normal (cada especie tem
uma media de massa corporal bem diferente).
"""

import seaborn as sns
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt


def classificar(p):
    """Classifica uma probabilidade como raro, pouco provavel, provavel ou quase certo."""
    if p < 0.10:
        return "raro"
    elif p < 0.50:
        return "pouco provável"
    elif p < 0.90:
        return "provável"
    else:
        return "quase certo"


def carregar_dados():
    """Carrega a base Palmer Penguins e filtra apenas a especie Adelie."""
    df = sns.load_dataset("penguins")
    df.to_csv("penguins.csv", index=False)
    adelie = df[df["species"] == "Adelie"].copy()
    return df, adelie


def analise_1_probabilidade_mediana(adelie):
    """Questao 1: P(X > mediana) assumindo Normal."""
    adelie = adelie.dropna(subset=["body_mass_g"])
    var = adelie["body_mass_g"]

    mediana = var.median()
    media = var.mean()
    desvio = var.std()

    prob_acima_mediana = 1 - stats.norm.cdf(mediana, loc=media, scale=desvio)

    print("=== ANÁLISE 1: Probabilidade acima da mediana ===")
    print(f"Variável: body_mass_g (massa corporal, espécie Adélie)")
    print(f"Quantidade de dados: {len(var)}")
    print(f"Mediana: {mediana:.2f} g")
    print(f"Média: {media:.2f} g")
    print(f"Desvio-padrão: {desvio:.2f} g")
    print(f"P(X > mediana) = {prob_acima_mediana*100:.2f}%")
    print(f"Classificação: {classificar(prob_acima_mediana)}")
    print()

    return {
        "mediana": mediana, "media": media, "desvio": desvio,
        "probabilidade": prob_acima_mediana, "n": len(var)
    }


def analise_2_intervalo_2s(adelie):
    """Questao 2: P(media - 2s <= X <= media + 2s) assumindo Normal."""
    adelie = adelie.dropna(subset=["body_mass_g"])
    var = adelie["body_mass_g"]

    media = var.mean()
    desvio = var.std()
    limite_inferior = media - 2 * desvio
    limite_superior = media + 2 * desvio

    prob_intervalo = (
        stats.norm.cdf(limite_superior, loc=media, scale=desvio)
        - stats.norm.cdf(limite_inferior, loc=media, scale=desvio)
    )

    dentro_intervalo = var[(var >= limite_inferior) & (var <= limite_superior)]
    proporcao_real = len(dentro_intervalo) / len(var)

    print("=== ANÁLISE 2: Probabilidade no intervalo média ± 2 desvios ===")
    print(f"Média: {media:.2f} g")
    print(f"Desvio-padrão: {desvio:.2f} g")
    print(f"Limite inferior: {limite_inferior:.2f} g")
    print(f"Limite superior: {limite_superior:.2f} g")
    print(f"P(intervalo) = {prob_intervalo*100:.2f}%")
    print(f"Classificação: {classificar(prob_intervalo)}")
    print(f"Proporção real de dados no intervalo: {proporcao_real*100:.2f}%")
    print()

    return {
        "media": media, "desvio": desvio,
        "limite_inferior": limite_inferior, "limite_superior": limite_superior,
        "probabilidade": prob_intervalo, "proporcao_real": proporcao_real
    }


def analise_3_regressao(adelie):
    """Questao 3: Regressao linear simples entre nadadeira (X) e massa (Y)."""
    dados_reg = adelie.dropna(subset=["flipper_length_mm", "body_mass_g"])

    X = dados_reg[["flipper_length_mm"]]
    y = dados_reg["body_mass_g"]

    modelo = LinearRegression()
    modelo.fit(X, y)

    intercepto = modelo.intercept_
    coef_angular = modelo.coef_[0]
    y_pred = modelo.predict(X)
    r2 = r2_score(y, y_pred)

    print("=== ANÁLISE 3: Regressão Linear ===")
    print(f"X = flipper_length_mm, Y = body_mass_g (espécie Adélie)")
    print(f"n = {len(dados_reg)}")
    print(f"Intercepto (b0): {intercepto:.2f}")
    print(f"Coeficiente angular (b1): {coef_angular:.2f}")
    print(f"Equação: body_mass_g = {intercepto:.2f} + {coef_angular:.2f} * flipper_length_mm")
    print(f"R²: {r2:.4f}")
    print()

    plt.figure(figsize=(8, 6))
    plt.scatter(X, y, alpha=0.6, label="Dados observados (Adélie)")
    plt.plot(X, y_pred, color="red", linewidth=2, label="Reta de regressão")
    plt.title("Regressão Linear: Massa Corporal vs. Comprimento da Nadadeira (Adélie)")
    plt.xlabel("Comprimento da nadadeira (mm)")
    plt.ylabel("Massa corporal (g)")
    plt.legend()
    plt.savefig("regressao_linear.png", dpi=150, bbox_inches="tight")
    plt.show()

    return {
        "intercepto": intercepto, "coef_angular": coef_angular,
        "r2": r2, "n": len(dados_reg)
    }


if __name__ == "__main__":
    df, adelie = carregar_dados()
    resultado_1 = analise_1_probabilidade_mediana(adelie)
    resultado_2 = analise_2_intervalo_2s(adelie)
    resultado_3 = analise_3_regressao(adelie)
