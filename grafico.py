import pandas as pd
import matplotlib.pyplot as plt

# Carregar dados
df = pd.read_csv("dados_uti_bahia_processado.csv")

# Filtrar municípios com maior déficit
top_deficit_uti = df.sort_values("deficit_leitos", ascending=False).head(10)

# Criar gráfico de barras
plt.figure(figsize=(12, 6))
plt.barh(top_deficit_uti["MUNICIPIO"], top_deficit_uti["deficit_leitos"], color="red")
plt.xlabel("Déficit de Leitos de UTI")
plt.ylabel("Município")
plt.title("Municípios com Maior Déficit de UTI na Bahia")
plt.gca().invert_yaxis()
plt.grid(axis="x", linestyle="--", alpha=0.7)

# Salvar e exibir gráfico
plt.savefig("grafico_deficit_uti.png")
plt.show()
print("Gráfico salvo: grafico_deficit_uti.png")



import folium

# Criar mapa centrado na Bahia
mapa = folium.Map(location=[-12.5, -41.5], zoom_start=6)

# Adicionar marcadores para municípios críticos
for _, row in top_deficit_uti.iterrows():
    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        popup=f"{row['MUNICIPIO']} - Déficit: {row['deficit_leitos']}",
        icon=folium.Icon(color="red")
    ).add_to(mapa)

# Salvar mapa
mapa.save("mapa_deficit_uti.html")
print("Mapa salvo: mapa_deficit_uti.html")



from folium.plugins import HeatMap

# Criar mapa
mapa_calor = folium.Map(location=[-12.5, -41.5], zoom_start=6)

# Preparar dados
heat_data = df[["latitude", "longitude", "deficit_leitos"]].dropna().values.tolist()

# Adicionar mapa de calor
HeatMap(heat_data, min_opacity=0.2, radius=15).add_to(mapa_calor)

# Salvar mapa
mapa_calor.save("mapa_calor_deficit_uti.html")
print("Mapa de calor salvo: mapa_calor_deficit_uti.html")
