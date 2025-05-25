import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Carregar o arquivo
df = pd.read_csv("dados_uti_bahia_processado.csv")

# Filtrar municípios com população acima de 30 mil
df_prioridade = df[df["População estimada - pessoas [2024]"] > 30000].copy()

# Colunas utilizadas
colunas = [
    "leitos_por_1000_hab",
    "Mortalidade infantil - óbitos por mil nascidos vivos [2022]",
    "PIB per capita - R$ [2021]",
    "deficit_leitos"
]

# Preencher nulos
df_prioridade[colunas] = df_prioridade[colunas].fillna(0)

# Normalizar com MinMax
scaler = MinMaxScaler()
df_prioridade[["norm_leitos", "norm_mortalidade", "norm_pib", "norm_deficit"]] = scaler.fit_transform(df_prioridade[colunas])

# Calcular score de prioridade
df_prioridade["score_prioridade"] = (
    (1 - df_prioridade["norm_leitos"]) * 0.35 +
    df_prioridade["norm_mortalidade"] * 0.25 +
    (1 - df_prioridade["norm_pib"]) * 0.2 +
    df_prioridade["norm_deficit"] * 0.2
)

# Ordenar e exibir top 20
df_top = df_prioridade.sort_values(by="score_prioridade", ascending=False).head(20)
print(df_top[["Município [-]", "score_prioridade"]])
