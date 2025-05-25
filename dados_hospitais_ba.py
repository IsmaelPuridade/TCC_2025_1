import requests
import pandas as pd
from tqdm import tqdm

# 1. Configurações da API
base_url = "https://apidadosabertos.saude.gov.br/assistencia-a-saude/hospitais-e-leitos"
params = {
    "uf": "BA",
    "limit": 1000,
    "offset": 0
}

todos_registros = []
print("📥 Coletando dados da API...")

# 2. Paginação automática (limite de 100 por página)
while True:
    response = requests.get(base_url, params=params)
    data = response.json()
    
    registros = data.get("hospitais_leitos", [])
    if not registros:
        break
    
    todos_registros.extend(registros)
    
    # Avança para a próxima página
    params["offset"] += params["limit"]

print(f"✅ Total bruto de registros coletados: {len(todos_registros)}")

# 3. Converter para DataFrame
df = pd.json_normalize(todos_registros)

# 4. Filtrar apenas unidades com tipo contendo "HOSPITAL"
df['tipo_unidade'] = df['tipo_unidade'].fillna('').str.upper()
hospitais_df = df[df['tipo_unidade'].str.contains("HOSPITAL")].copy()

# 5. Converter colunas numéricas
colunas_numericas = ['leitos_existentes', 'leitos_sus']
for col in colunas_numericas:
    hospitais_df[col] = pd.to_numeric(hospitais_df[col], errors='coerce')

# 6. Salvar
hospitais_df.to_csv("dados_hospitais_filtrados.csv", index=False, encoding='utf-8-sig')
print(f"🏥 Total de hospitais filtrados: {len(hospitais_df)}")
print("💾 Arquivo salvo como 'dados_hospitais_filtrados.csv'")
