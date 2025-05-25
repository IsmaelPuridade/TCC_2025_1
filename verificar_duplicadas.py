import pandas as pd

# Carrega o CSV
df = pd.read_csv("dados_hospitais_unicos.csv")

# 1. Verificar duplicatas completas (todas as colunas)
duplicatas_completas = df[df.duplicated(keep=False)]

print("🔁 Duplicatas completas (todas as colunas):")
print(duplicatas_completas)

# 2. Verificar duplicatas por colunas-chave (ex: CNES + nome do hospital + município)
colunas_chave = ['cnes', 'nome_do_estabelecimento', 'municipio']
duplicatas_chave = df[df.duplicated(subset=colunas_chave, keep=False)]

print("\n🔁 Duplicatas por CNES, nome do estabelecimento e município:")
print(duplicatas_chave)

# 3. Mostrar apenas os CNES duplicados (resumo)
cnes_duplicados = df[df.duplicated(subset='cnes', keep=False)]
print("\n🔁 Estabelecimentos com mesmo CNES:")
print(cnes_duplicados[['cnes', 'nome_do_estabelecimento', 'municipio']].drop_duplicates())


