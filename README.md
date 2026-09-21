# Challenge Sprint 3

## Integrantes
- Gustavo Guedes Pereira - RM 569779
- Lucas Angelo - RM 569530
- Gustavo de Souza - RM 570746
- Arthur Tae - RM 570647
- Gabriel Rodrigues - RM 569322
- Murillo Boyadjian - RM 570774

## Objetivo
Selecionar variáveis numéricas de uma base de dados real e aplicar conceitos
de probabilidade (assumindo Distribuição Normal) e de Regressão Linear,
utilizando Python.

## Base de dados utilizada
**Palmer Penguins** - medidas morfológicas de pinguins adultos (Adélie,
Chinstrap e Gentoo) coletadas no Arquipélago de Palmer, Antártida.

- Fonte: Gorman KB, Williams TD, Fraser WR (2014). *Ecological Sexual
  Dimorphism and Environmental Variability within a Community of Antarctic
  Penguins (Genus Pygoscelis)*. PLoS ONE 9(3): e90081.
- Disponibilizada por Allison Horst: https://github.com/allisonhorst/palmerpenguins
- Licença: CC0 (uso livre)
- 344 linhas, 7 colunas (species, island, bill_length_mm, bill_depth_mm,
  flipper_length_mm, body_mass_g, sex)

O arquivo `dados/penguins.csv` contém a base já exportada.

## Por que restringir a análise à espécie Adélie?
As três espécies de pinguim têm médias de massa corporal bem diferentes
entre si (Adélie ≈ 3700 g, Chinstrap ≈ 3733 g, Gentoo ≈ 5076 g). Se todas
as espécies fossem analisadas juntas, a distribuição da massa corporal não
teria formato de sino (teria vários "picos"), o que quebraria a suposição
de Distribuição Normal exigida pelo trabalho. Por isso, todas as análises
foram feitas apenas com a espécie **Adélie** (151 registros válidos), que
apresenta distribuição aproximadamente simétrica.

## Variáveis escolhidas
- **Questões 1 e 2 (probabilidade):** `body_mass_g` (massa corporal, g)
- **Questão 3 (regressão linear):**
  - X (independente): `flipper_length_mm` (comprimento da nadadeira, mm)
  - Y (dependente): `body_mass_g` (massa corporal, g)

A relação entre nadadeira e massa corporal tem justificativa biológica:
pinguins estruturalmente maiores tendem a pesar mais.

## Metodologia
1. Carregamento da base via biblioteca `seaborn` (`sns.load_dataset("penguins")`).
2. Filtro da espécie Adélie e remoção de valores ausentes nas colunas usadas.
3. Cálculo de mediana, média e desvio-padrão da massa corporal.
4. Cálculo de P(X > mediana) e de P(média − 2s ≤ X ≤ média + 2s), assumindo
   Distribuição Normal, usando `scipy.stats.norm`.
5. Classificação de cada evento como raro, pouco provável, provável ou
   quase certo, segundo a tabela abaixo.
6. Regressão linear simples com `scikit-learn` (`LinearRegression`),
   cálculo de intercepto, coeficiente angular e R².
7. Geração de gráfico de dispersão com reta ajustada.

### Tabela de classificação utilizada
| Classificação    | Probabilidade      |
|-------------------|--------------------|
| Raro               | menor que 10%      |
| Pouco provável      | de 10% a 50%      |
| Provável            | de 50% a 90%      |
| Quase certo         | 90% ou mais       |

## Resultados principais

**Análise 1 - Probabilidade acima da mediana**
- Mediana: 3700.00 g | Média: 3700.66 g | Desvio-padrão: 458.57 g
- P(X > mediana) = 50.06% -> **provável**

**Análise 2 - Probabilidade no intervalo média +/- 2 desvios**
- Limites: [2783.53 g ; 4617.79 g]
- P(intervalo) = 95.45% -> **quase certo**
- Proporção real observada na base: 96.69%

**Análise 3 - Regressão Linear**
- Equação: `body_mass_g = -2535.84 + 32.83 * flipper_length_mm`
- R² = 0.2192

Os resultados completos e as interpretações estão em `resultados/resultados.txt`.

## Conclusão
As análises de probabilidade confirmaram que a massa corporal dos pinguins
Adélie se comporta de forma próxima a uma Distribuição Normal, com os
resultados de P(X > mediana) e P(média +/- 2s) coerentes com a teoria (perto
de 50% e perto de 95%, respectivamente). Já a regressão linear mostrou que
existe uma relação positiva, porém estatisticamente fraca (R² = 0.22),
entre o comprimento da nadadeira e a massa corporal - ou seja, o tamanho da
nadadeira ajuda a explicar o peso do pinguim, mas está longe de ser o único
fator relevante. O trabalho ilustra como conceitos de estatística descritiva
e probabilidade servem de base para a construção e a avaliação de modelos
simples de aprendizado de máquina.

## Estrutura do repositório
```
Sprint3/
├── README.md
├── dados/
│   └── penguins.csv
├── notebooks/
│   └── sprint3.ipynb
├── src/
│   └── analise.py
├── graficos/
│   └── regressao_linear.png
└── resultados/
    └── resultados.txt
```

## Como executar
1. Abrir `notebooks/sprint3.ipynb` no Google Colab.
2. Executar as células em ordem (todas as bibliotecas usadas - pandas,
   numpy, scipy, matplotlib e scikit-learn.
