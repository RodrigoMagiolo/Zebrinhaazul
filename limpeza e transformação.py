# Importar biblioteca pandas #

import pandas as pd

# Extrair base de dados e mostra-los #

dataframe = pd.read_csv("Dados_clima_transito.csv")
dataframe.head()

#informações da tabela#

dataframe.info()

#checando valores nulos#

ValoresNulos = dataframe.isna().sum()
print (ValoresNulos)

# Remover duplicatas e registros inválidos (Ex: coluna umidade) #

dataframe = dataframe.drop_duplicates().dropna(subset=['umidade'])

# Preencher valores nulos com a média da coluna (Ex: coluna temperatura)

dataframe['temperatura'] = dataframe['temperatura'].fillna(dataframe['temperatura'].mean())

# Converter os valores da coluna data para o tipo datetime e alterar o formato #

dataframe["Data"] = pd.to_datetime(dataframe["Data"], format="%d-%m-%Y")

# Checar os anos, meses e dias da tabela Data, passando os nomes para português#

dataframe["Ano"] = dataframe["Data"].dt.year
dataframe["Mês"] = dataframe["Data"].dt.month
dataframe["Dia da Semana"] = dataframe["Data"].dt.day_name()

Meses = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril", 5: "Maio", 6: "Junho",
    7: "Julho", 8: "Agosto", 9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}

Dias_Semana = {
    'Monday': 'Segunda-feira', 'Tuesday': 'Terça-feira', 'Wednesday': 'Quarta-feira',
    'Thursday': 'Quinta-feira', 'Friday': 'Sexta-feira', 'Saturday': 'Sábado', 'Sunday': 'Domingo'
}

dataframe["Mês"] = dataframe["Mês"].map(Meses)
dataframe["Dia da Semana"] = dataframe["Dia da Semana"].map(Dias_Semana)

DiaDaSemana = dataframe["Data"].dt.day_name().unique()

print(f"Os dados se relacionam aos anos de : {dataframe['Ano'].unique()}")
print(f"Os dados se relacionam aos meses de : {dataframe['Mês'].unique()}")
print(f"Os dados se relacionam aos dias: {dataframe['Dia da Semana'].unique()}")