import pandas as pd

# Usar 'latin1' para evitar erro de decodificação
df = pd.read_csv("Leitos_2025.csv", sep=",", encoding="latin1")

# Filtrar registros da Bahia
df_bahia = df[df["UF"] == "BA"]

# Salvar o novo CSV com os dados da Bahia
df_bahia.to_csv("leitos_bahia.csv", index=False, encoding="utf-8")

print("Arquivo 'leitos_bahia.csv' criado com sucesso.")
