import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import numpy as np

# 1. Carregar dados agregados por município
df = pd.read_csv("dados_hospitais_unicos.csv")  # <-- use o nome correto do arquivo que contém 1 linha por município

# 2. Selecionar variáveis explicativas e alvo
features = [
    "População estimada - pessoas [2024]",
    "PIB per capita - R$ [2021]",
    "IDHM Índice de desenvolvimento humano municipal [2010]",
    "Mortalidade infantil - óbitos por mil nascidos vivos [2022]",
    "Densidade demográfica - hab/km² [2022]",
    "leitos_existentes",
    "leitos_por_1000_hab",
]

# Remover registros com valores faltando nas colunas selecionadas
df = df.dropna(subset=features + ["classificacao"])

X = df[features]
y = df["classificacao"]

# 3. Codificar os rótulos (classificacao)
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# 4. Dividir em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# 5. Treinar o modelo
clf = RandomForestClassifier(random_state=42)
clf.fit(X_train, y_train)

# 6. Avaliar o modelo
y_pred = clf.predict(X_test)
print("📊 Relatório de Classificação:")
print(classification_report(
    y_test,
    y_pred,
    labels=np.unique(y_encoded),
    target_names=le.inverse_transform(np.unique(y_encoded))
))


print("\n📉 Matriz de Confusão:")
print(confusion_matrix(y_test, y_pred))

# 7. Importância das variáveis
importances = pd.Series(clf.feature_importances_, index=X.columns).sort_values(ascending=False)
print("\n🔍 Importância das Variáveis:")
print(importances)
