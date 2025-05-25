import pandas as pd
import folium

# 1. Carregar o CSV
df = pd.read_csv("estabelecimentos_com_coordenadas.csv")
print(df.columns.tolist())


# 2. Filtrar hospitais com leitos de UTI
df_uti = df[df["UTI_TOTAL_EXIST"] > 0].copy()

# 3. Remover registros sem coordenadas
df_uti = df_uti.dropna(subset=["latitude", "longitude"])

# 4. Criar o mapa centralizado na Bahia
mapa = folium.Map(location=[-12.8, -38.5], zoom_start=6)

# 5. Adicionar marcadores
for _, row in df_uti.iterrows():
    nome = row["NOME_ESTABELECIMENTO"]
    municipio = row["MUNICIPIO"]
    leitos_uti = row["UTI_TOTAL_EXIST"]
    leitos_sus = row["UTI_TOTAL_SUS"]
    latitude = float(row["latitude"])
    longitude = float(row["longitude"])

    popup = folium.Popup(f"""
        <b>{nome}</b><br>
        Município: {municipio}<br>
        UTI Total: {leitos_uti}<br>
        UTI SUS: {leitos_sus}
    """, max_width=300)

    folium.Marker(
        location=[latitude, longitude],
        popup=popup,
        icon=folium.Icon(color="red", icon="plus-sign")
    ).add_to(mapa)

# 6. Salvar o mapa
mapa.save("mapa_hospitais_uti_bahia.html")
print("✅ Mapa gerado com sucesso!")
