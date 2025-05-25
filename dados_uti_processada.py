import pandas as pd

# === 1. Carregar os dados ===
df_uti = pd.read_csv("hospitais_com_uti.csv", dtype=str)
df_municipios = pd.read_excel("dados_bahia_limpo.xlsx")

# === 2. Corrigir tipos de dados numéricos nas colunas de leitos ===
colunas_leitos = [
    "LEITOS_EXISTENTES", "LEITOS_SUS", "UTI_TOTAL_EXIST", "UTI_TOTAL_SUS",
    "UTI_ADULTO_EXIST", "UTI_ADULTO_SUS", "UTI_PEDIATRICO_EXIST", "UTI_PEDIATRICO_SUS",
    "UTI_NEONATAL_EXIST", "UTI_NEONATAL_SUS", "UTI_QUEIMADO_EXIST", "UTI_QUEIMADO_SUS",
    "UTI_CORONARIANA_EXIST", "UTI_CORONARIANA_SUS"
]

for col in colunas_leitos:
    df_uti[col] = pd.to_numeric(df_uti[col], errors="coerce").fillna(0)

# === 3. Agrupar por município e somar os leitos ===
df_agrupado = df_uti.groupby("MUNICIPIO")[colunas_leitos].sum().reset_index()

# === 4. Padronizar nomes para junção ===
df_agrupado["MUNICIPIO"] = df_agrupado["MUNICIPIO"].str.upper().str.normalize("NFKD").str.encode("ascii", errors="ignore").str.decode("utf-8").str.strip()
df_municipios["Município [-]"] = df_municipios["Município [-]"].str.upper().str.normalize("NFKD").str.encode("ascii", errors="ignore").str.decode("utf-8").str.strip()

# === 5. Juntar os dados ===
df_final = pd.merge(df_municipios, df_agrupado, left_on="Município [-]", right_on="MUNICIPIO", how="left")

# === 6. Calcular taxa de leitos de UTI por 1000 habitantes ===
df_final["População estimada - pessoas [2024]"] = pd.to_numeric(df_final["População estimada - pessoas [2024]"], errors="coerce")
df_final["leitos_por_1000_hab"] = (df_final["UTI_TOTAL_EXIST"] / df_final["População estimada - pessoas [2024]"]) * 1000

# === 7. Definir meta de cobertura e classificar ===
meta_ideal = 2.5  # leitos por 1000 habitantes
df_final["leitos_ideais"] = (df_final["População estimada - pessoas [2024]"] * meta_ideal) / 1000
df_final["deficit_leitos"] = df_final["leitos_ideais"] - df_final["UTI_TOTAL_EXIST"]
df_final["classificacao"] = df_final["leitos_por_1000_hab"].apply(
    lambda x: "Acima da média" if x >= meta_ideal else "Abaixo da média"
)

# === 8. Exportar resultado para CSV ===
df_final.to_csv("dados_uti_bahia_processado.csv", index=False)
print("✅ Dados processados e exportados com sucesso.")
