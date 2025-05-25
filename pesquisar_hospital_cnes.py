import pandas as pd
import requests
import time

def buscar_coordenadas(cnes):
    url = f"https://apidadosabertos.saude.gov.br/cnes/estabelecimentos/{str(cnes).zfill(7)}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            lat = data.get("latitude_estabelecimento_decimo_grau")
            lon = data.get("longitude_estabelecimento_decimo_grau")
            if lat is not None and lon is not None:
                return float(lat), float(lon)
        else:
            print(f"Status {response.status_code} para CNES {cnes}")
    except Exception as e:
        print(f"Erro na consulta CNES {cnes}: {e}")
    return None, None

# Carregar CSV com os dados
df = pd.read_csv("hospitais_com_uti.csv")

# Criar colunas para latitude e longitude
df['latitude'] = None
df['longitude'] = None

# Iterar por cada CNES e buscar as coordenadas
for i, cnes in enumerate(df['CNES']):
    lat, lon = buscar_coordenadas(cnes)
    df.at[i, 'latitude'] = lat
    df.at[i, 'longitude'] = lon
    print(f"{i+1}/{len(df)} - CNES {cnes}: lat={lat}, lon={lon}")
    time.sleep(0.2)  # delay para não sobrecarregar a API

# Salvar arquivo atualizado
df.to_csv("estabelecimentos_com_coordenadas.csv", index=False)
