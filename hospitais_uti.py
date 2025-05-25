import pandas as pd

# 1. Especificar o caminho do arquivo CSV
caminho_arquivo_csv = "leitos_bahia.csv"  # Substitua pelo caminho correto

# 2. Tentar ler o arquivo CSV com diferentes codificações
try:
    df = pd.read_csv(caminho_arquivo_csv, encoding='utf-8')  # Tentar utf-8 primeiro
except UnicodeDecodeError:
    try:
        df = pd.read_csv(caminho_arquivo_csv, encoding='latin-1')
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(caminho_arquivo_csv, encoding='windows-1252')
        except UnicodeDecodeError:
            print(f"Erro: Não foi possível decodificar o arquivo usando utf-8, latin-1 ou windows-1252.")
            exit()

# 3. Filtrar os hospitais que possuem UTI (UTI_TOTAL_EXIST > 0)
hospitais_com_uti_df = df[df['UTI_TOTAL_EXIST'] > 0]

# 4. Salvar o DataFrame filtrado em um novo arquivo CSV (opcional)
hospitais_com_uti_df.to_csv("hospitais_com_uti.csv", index=False)

# 5. Exibir os resultados (opcional)
print("Hospitais com UTI:\n")
print(hospitais_com_uti_df[["NOME_ESTABELECIMENTO", "UTI_TOTAL_EXIST"]])

print("\nArquivo 'hospitais_com_uti.csv' criado com sucesso!")