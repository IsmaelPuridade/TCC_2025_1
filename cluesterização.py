import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Carrega os dados
df = pd.read_csv("analise_leitos_uti_por_municipio.csv")

# Define colunas usadas para clusterização (com nomes exatos)
colunas = ["POPULACAO_2024", "LEITOS_UTI_POR_1000_HAB"]
df_cluster = df[colunas].dropna()

# Aplica KMeans
kmeans = KMeans(n_clusters=4, random_state=42)
df["cluster"] = kmeans.fit_predict(df_cluster)

# Visualização simples
plt.scatter(df["POPULACAO_2024"], df["LEITOS_UTI_POR_1000_HAB"], c=df["cluster"], cmap="viridis")
plt.xlabel("População estimada 2024")
plt.ylabel("Leitos UTI por 1000 hab.")
plt.title("Clusterização de Municípios - Saúde")
plt.colorbar(label="Cluster")
plt.grid(True)
plt.show()
