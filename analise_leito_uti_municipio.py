import pandas as pd

# Carregar dados dos hospitais
df_uti = pd.read_csv("hospitais_com_uti.csv", dtype=str)

# Carregar dados dos municípios
df_municipios = pd.read_excel("dados_bahia_limpo.xlsx", dtype=str)

# -----------------------------
# 🔹 ETAPA 1 - LIMPEZA DF_UTI
# -----------------------------
# Preencher NaNs com 0 onde for valor numérico
colunas_numericas = [
    "LEITOS_EXISTENTES", "LEITOS_SUS", "UTI_TOTAL_EXIST", "UTI_TOTAL_SUS",
    "UTI_ADULTO_EXIST", "UTI_ADULTO_SUS", "UTI_PEDIATRICO_EXIST", "UTI_PEDIATRICO_SUS",
    "UTI_NEONATAL_EXIST", "UTI_NEONATAL_SUS", "UTI_QUEIMADO_EXIST", "UTI_QUEIMADO_SUS",
    "UTI_CORONARIANA_EXIST", "UTI_CORONARIANA_SUS"
]
for col in colunas_numericas:
    df_uti[col] = pd.to_numeric(df_uti[col], errors='coerce').fillna(0).astype(int)

# Padronizar nomes dos municípios (letras maiúsculas e sem acentos)
df_uti['MUNICIPIO'] = df_uti['MUNICIPIO'].str.upper().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

# -----------------------------
# 🔹 ETAPA 2 - LIMPEZA DF_MUNICIPIOS
# -----------------------------
# Renomear colunas para facilitar o join
df_municipios.rename(columns={
    "Município [-]": "MUNICIPIO",
    "Código [-]": "CODIGO_IBGE",
    "População estimada - pessoas [2024]": "POPULACAO_2024"
}, inplace=True)

# Padronizar os nomes dos municípios da mesma forma
df_municipios['MUNICIPIO'] = df_municipios['MUNICIPIO'].str.upper().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

# Converter população para número
df_municipios['POPULACAO_2024'] = pd.to_numeric(df_municipios['POPULACAO_2024'], errors='coerce')

# -----------------------------
# 🔹 ETAPA 3 - AGRUPAMENTO E JUNÇÃO
# -----------------------------
# Agrupar leitos de UTI por município
df_leitos_mun = df_uti.groupby('MUNICIPIO')[[
    "UTI_TOTAL_EXIST", "UTI_TOTAL_SUS"
]].sum().reset_index()

# Juntar com dados dos municípios
df_final = pd.merge(df_municipios, df_leitos_mun, on='MUNICIPIO', how='left')

# Preencher municípios sem hospitais com 0
df_final["UTI_TOTAL_EXIST"] = df_final["UTI_TOTAL_EXIST"].fillna(0).astype(int)
df_final["UTI_TOTAL_SUS"] = df_final["UTI_TOTAL_SUS"].fillna(0).astype(int)

# -----------------------------
# 🔹 ETAPA 4 - CALCULAR LEITOS POR 10000 HABITANTES
# -----------------------------
df_final['LEITOS_UTI_POR_10000_HAB'] = (df_final["UTI_TOTAL_EXIST"] / df_final["POPULACAO_2024"]) * 10000
df_final['LEITOS_UTI_POR_10000_HAB'] = df_final['LEITOS_UTI_POR_10000_HAB'].round(2)

# Exibir alguns resultados
print(df_final[["MUNICIPIO", "POPULACAO_2024", "UTI_TOTAL_EXIST", "LEITOS_UTI_POR_10000_HAB"]].sort_values(by="LEITOS_UTI_POR_10000_HAB", ascending=False))

# Salvar resultado
df_final.to_csv("analise_leitos_uti_por_municipio.csv", index=False)
print("✅ Arquivo salvo: [10mil]analise_leitos_uti_por_municipio.csv")
