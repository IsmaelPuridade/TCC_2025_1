import pandas as pd

# Carrega o CSV
df = pd.read_csv("leitos_2025.csv", encoding="latin1")

# 1. Verificar duplicatas completas (todas as colunas)
duplicatas_completas = df[df.duplicated(keep=False)]

print(f"🔁 Total de duplicatas completas: {duplicatas_completas.shape[0]}")
print(duplicatas_completas)

# 2. Remover duplicatas completas
#df_sem_duplicatas = df.drop_duplicates()

#print(f"✅ Linhas após remoção de duplicatas completas: {df_sem_duplicatas.shape[0]}")

duplicados_cnes = df[df.duplicated(subset=["CNES"], keep=False)]
print("🏥 Estabelecimentos duplicados por CNES:")
print(duplicados_cnes.sort_values("CNES"))


# Converter COMP para string ou int, se necessário
df["COMP"] = pd.to_numeric(df["COMP"], errors="coerce")

# Ordenar do mais recente para o mais antigo
df_ordenado = df.sort_values(by="COMP", ascending=False)

# Manter apenas o registro mais recente de cada CNES
df_atualizado = df_ordenado.drop_duplicates(subset="CNES", keep="first")

print(f"✅ Registros após remover históricos: {df_atualizado.shape[0]}")

df_atualizado.to_csv("Leitos_2025_sem_Duplicadas.csv", index=False)



