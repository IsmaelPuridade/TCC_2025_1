import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
from yellowbrick.cluster import KElbowVisualizer, SilhouetteVisualizer

# --- Configuração ---
# Nome do arquivo CSV de entrada gerado pelo script de processamento de dados
# Use o nome exato do seu arquivo CSV processado
INPUT_CSV_FILE = "[10mil]dados_uti_bahia_processado.csv" 

# Colunas (features) a serem usadas para a clusterização, conforme a metodologia do TCC.
# ATENÇÃO: Verifique se os nomes das colunas aqui correspondem EXATAMENTE aos nomes no seu CSV.
FEATURES = [
    "População estimada - pessoas [2024]",
    "Densidade demográfica - hab/km² [2022]",
    "IDHM Índice de desenvolvimento humano municipal [2010]",
    "PIB per capita - R$ [2021]",
    "leitos_por_1000_hab",  # Nome da coluna no CSV, corresponde a 'Taxa de leitos de UTI por 10 mil habitantes'
    "deficit_leitos"       # Nome da coluna no CSV, corresponde a 'Déficit de leitos de UTI'
]

N_CLUSTERS_FINAL = 2 # Conforme a análise do TCC e o Coeficiente de Silhueta, k=2 é o ideal

# --- 1. Carregar os dados ---
try:
    df = pd.read_csv(INPUT_CSV_FILE)
    print(f"✅ Arquivo '{INPUT_CSV_FILE}' carregado com sucesso.")
except FileNotFoundError:
    print(f"❌ Erro: O arquivo '{INPUT_CSV_FILE}' não foi encontrado. Certifique-se de que ele está no mesmo diretório do script.")
    exit()

# --- 2. Preparar os dados para clusterização ---
# Selecionar apenas as features que serão usadas para clusterização
df_cluster = df[FEATURES].copy()

# Preencher quaisquer valores NaN nas features com 0 ou a média, se apropriado.
# Para clusterização, NaNs devem ser tratados antes da normalização.
# Aqui, preenchemos com 0. Se seus dados têm muitos NaNs, considere imputar com a média ou mediana.
for col in FEATURES:
    if df_cluster[col].isnull().any():
        print(f"⚠️ Atenção: Coluna '{col}' contém valores NaN. Preenchendo com 0 para a clusterização.")
        df_cluster[col] = df_cluster[col].fillna(0)

# Normalizar os dados usando StandardScaler
# Isso garante que todas as features contribuam igualmente para a distância na clusterização
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_cluster)
df_scaled = pd.DataFrame(X_scaled, columns=FEATURES, index=df_cluster.index)
print("✅ Dados normalizados com StandardScaler.")

# --- 3. Determinar o número ideal de clusters (k) ---
print("\n--- Analisando o número ideal de clusters (k) ---")

# Método do Cotovelo (Elbow Method)
model_elbow = KMeans(random_state=42, n_init=10)
visualizer_elbow = KElbowVisualizer(model_elbow, k=(1,11), timings=False)
visualizer_elbow.fit(X_scaled)
visualizer_elbow.show(outpath="elbow_method.png") # Salva o gráfico
plt.title("Método do Cotovelo para K-Means")
plt.xlabel("Número de Clusters (k)")
plt.ylabel("Inércia")
plt.tight_layout()
plt.show()
print("✅ Gráfico 'elbow_method.png' gerado para o Método do Cotovelo.")


# Coeficiente de Silhueta (Silhouette Score) - Trecho corrigido
print("\n--- Calculando e plotando o Coeficiente de Silhueta ---")

silhouette_scores = []
k_values = range(2, 11) # Testar de K=2 a K=10 (o mínimo para silhouette é 2 clusters)

for i in k_values:
    model_silhouette = KMeans(n_clusters=i, random_state=42, n_init=10)
    
    # Criar uma figura e um eixo para cada visualizador de silhueta
    # Desta forma, 'ax' será sempre um Axes object, não um array.
    fig, ax = plt.subplots(1, 1, figsize=(8, 6)) 
    visualizer_silhouette = SilhouetteVisualizer(model_silhouette, colors='yellowbrick', ax=ax)
    
    visualizer_silhouette.fit(X_scaled)
    score = visualizer_silhouette.silhouette_score_
    silhouette_scores.append(score)
    
    # Se 'i' for o número de clusters final do seu TCC (K=2), salve o gráfico principal
    if i == N_CLUSTERS_FINAL:
        visualizer_silhouette.show(outpath=f"silhouette_score_k_{i}.png")
        plt.title(f"Coeficiente de Silhueta para K={i} (Score: {score:.4f})")
        plt.tight_layout()
        plt.show()
    else: # Fechar a figura para não exibir os plots intermediários no output se não for o k final
        plt.close(fig) 

# Opcional: Plotar todos os scores de silhueta em um gráfico separado (similar ao elbow)
plt.figure(figsize=(10, 6))
plt.plot(k_values, silhouette_scores, marker='o')
plt.title('Visão Geral do Coeficiente de Silhueta para Diferentes Números de Clusters')
plt.xlabel('Número de Clusters (k)')
plt.ylabel('Coeficiente de Silhueta')
plt.grid(True)
plt.tight_layout()
plt.savefig("silhouette_scores_overview.png")
plt.show()
print(f"✅ Gráfico 'silhouette_score_k_{N_CLUSTERS_FINAL}.png' gerado para o Coeficiente de Silhueta para K={N_CLUSTERS_FINAL}.")
print(f"✅ Gráfico 'silhouette_scores_overview.png' gerado com a visão geral dos scores de silhueta.")
print(f"   - Conforme o TCC, K={N_CLUSTERS_FINAL} é o valor ideal.")


# --- 4. Aplicar o KMeans com o número de clusters final (k=2) ---
kmeans_final = KMeans(n_clusters=N_CLUSTERS_FINAL, random_state=42, n_init=10)
df['cluster'] = kmeans_final.fit_predict(X_scaled)
print(f"\n✅ Clusterização KMeans com K={N_CLUSTERS_FINAL} aplicada e clusters atribuídos ao DataFrame.")

# --- 5. Visualização dos Clusters com PCA ---
print("\n--- Visualizando Clusters com PCA ---")
pca = PCA(n_components=2) # Reduzir para 2 dimensões para visualização
X_pca = pca.fit_transform(X_scaled)

plt.figure(figsize=(10, 7))
# Usar df['cluster'] para colorir os pontos, pois o 'cluster' já foi adicionado ao DataFrame original
sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=df['cluster'], palette='viridis', legend='full', s=100, alpha=0.8)
plt.title('Visualização dos Clusters (PCA)')
plt.xlabel(f'Componente Principal 1 ({pca.explained_variance_ratio_[0]*100:.2f}%)')
plt.ylabel(f'Componente Principal 2 ({pca.explained_variance_ratio_[1]*100:.2f}%)')
plt.grid(True)
plt.tight_layout()
plt.savefig("pca_clusters.png") # Salva o gráfico
plt.show()
print("✅ Gráfico 'pca_clusters.png' gerado para a Visualização PCA dos Clusters.")

# --- 6. Caracterização dos Clusters (Tabela 2) ---
print("\n--- Caracterização dos Clusters (Média das Variáveis por Cluster) ---")
# Selecionar as colunas que você quer na Tabela 2 (as features e outras relevantes)
# Certifique-se de que esses nomes de coluna correspondem EXATAMENTE aos do seu DataFrame
COLUNAS_TABELA2 = [
    "UTI_TOTAL_EXIST", # Para 'Leitos UTI Existentes Totais' na Tabela 2
    "População estimada - pessoas [2024]",
    "Densidade demográfica - hab/km² [2022]",
    "IDHM Índice de desenvolvimento humano municipal [2010]",
    "PIB per capita - R$ [2021]",
    "leitos_por_1000_hab", # Para 'Taxa Leitos UTI/10 mil hab.'
    "deficit_leitos"       # Para 'Déficit Leitos UTI'
]

# Garantir que as colunas existem antes de tentar calcular as médias
valid_cols_tabela2 = [col for col in COLUNAS_TABELA2 if col in df.columns]
if len(valid_cols_tabela2) != len(COLUNAS_TABELA2):
    missing_cols = set(COLUNAS_TABELA2) - set(df.columns)
    print(f"⚠️ Aviso: As seguintes colunas da Tabela 2 não foram encontradas no DataFrame e serão ignoradas: {missing_cols}. Verifique os nomes das colunas no seu CSV.")

cluster_summary = df.groupby('cluster')[valid_cols_tabela2].mean().round(2)
print("\nEstatísticas Médias por Cluster (Tabela 2):")
print(cluster_summary)

# Opcional: Salvar o DataFrame com os clusters para uso posterior (ex: mapas)
output_clustered_csv = "analise_leitos_uti_por_municipio_com_clusters.csv"
df.to_csv(output_clustered_csv, index=False)
print(f"✅ DataFrame com clusters salvo em '{output_clustered_csv}'.")

# --- 7. Estatísticas Descritivas Gerais (Tabela 1) ---
print("\n--- Estatísticas Descritivas Gerais (Tabela 1) ---")
# Certifique-se de que as colunas aqui correspondem às da sua Tabela 1 no TCC
# e que os nomes das colunas são os que realmente existem no DataFrame
COLUNAS_TABELA1_DESC = [
    "UTI_TOTAL_EXIST", # 'Leitos UTI Existentes Totais'
    "População estimada - pessoas [2024]",
    "Densidade demográfica - hab/km² [2022]",
    "IDHM Índice de desenvolvimento humano municipal [2010]",
    "PIB per capita - R$ [2021]",
    "leitos_por_1000_hab", # 'Taxa Leitos UTI/10 mil hab.'
    "deficit_leitos" # 'Déficit Leitos UTI'
]

valid_cols_tabela1 = [col for col in COLUNAS_TABELA1_DESC if col in df.columns]
if len(valid_cols_tabela1) != len(COLUNAS_TABELA1_DESC):
    missing_cols = set(COLUNAS_TABELA1_DESC) - set(df.columns)
    print(f"⚠️ Aviso: As seguintes colunas da Tabela 1 não foram encontradas no DataFrame e serão ignoradas: {missing_cols}. Verifique os nomes das colunas no seu CSV.")

general_stats = df[valid_cols_tabela1].agg(['mean', 'std', 'min', 'max']).round(2)
# Renomear os índices para corresponder à sua Tabela 1: Média, Desvio Padrão, Mínimo, Máximo
general_stats = general_stats.rename(index={'mean': 'Média', 'std': 'Desvio Padrão', 'min': 'Mínimo', 'max': 'Máximo'})
print("\nEstatísticas Descritivas Gerais (Tabela 1):")
print(general_stats)

print("\n--- Geração de gráficos e tabelas de clusterização concluída. ---")
print("Por favor, inspecione os arquivos PNG gerados ('elbow_method.png', 'silhouette_score_k_2.png', 'silhouette_scores_overview.png', 'pca_clusters.png').")
print("As tabelas (Estatísticas Descritivas e Caracterização dos Clusters) foram impressas acima.")
print("Lembre-se de executar também seus scripts de mapas (mapa.py e mapa_clusters.py) para gerar os arquivos HTML.")