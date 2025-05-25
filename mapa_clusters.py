import pandas as pd
from sklearn.cluster import KMeans
import folium

# 1. Carrega os dados
df = pd.read_csv("analise_leitos_uti_por_municipio.csv")
coordenadas = pd.read_csv("estabelecimentos_com_coordenadas.csv")

print(coordenadas.columns)


# 2. Usa as colunas corretas
colunas = ["POPULACAO_2024", "LEITOS_UTI_POR_1000_HAB"]
df_cluster = df[colunas].dropna()

# 3. Aplica KMeans
kmeans = KMeans(n_clusters=4, random_state=42)
df["cluster"] = kmeans.fit_predict(df_cluster)




# 4. Gera coordenadas médias por município
coordenadas_mean = coordenadas.groupby("MUNICIPIO")[
    ["latitude", "longitude"]
].mean().reset_index()

# 5. Junta os dados
df_merge = pd.merge(df, coordenadas_mean, left_on="MUNICIPIO", right_on="MUNICIPIO", how="left")
df_merge = df_merge.dropna(subset=["latitude", "longitude"])

# 6. Cria o mapa
m = folium.Map(location=[-12.9, -38.5], zoom_start=6)

cores = ['blue', 'green', 'orange', 'red']  # cor por cluster

# 7. Adiciona marcadores por cluster
for _, row in df_merge.iterrows():
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=5,
        color=cores[row["cluster"]],
        fill=True,
        fill_opacity=0.7,
        popup=folium.Popup(f"{row['MUNICIPIO']}\nPop: {int(row['POPULACAO_2024'])}\nLeitos/1000 hab: {row['LEITOS_UTI_POR_1000_HAB']:.2f}", max_width=200)
    ).add_to(m)

# 8. Identifica cidades prioritárias para novas unidades
# Critério: população > 30 mil e LEITOS_UTI_POR_1000_HAB < 0.5
prioritarios = df_merge[
    (df_merge["POPULACAO_2024"] > 30000) &
    (df_merge["LEITOS_UTI_POR_1000_HAB"] < 0.5)
]

# 9. Adiciona marcadores em vermelho escuro
for _, row in prioritarios.iterrows():
    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        icon=folium.Icon(color="darkred", icon="plus", prefix="fa"),
        popup=f"⚠️ PRIORITÁRIO: {row['MUNICIPIO']}"
    ).add_to(m)

# 10. Salva o mapa
m.save("mapa_clusters.html")
print("✅ Mapa salvo como mapa_clusters.html")
