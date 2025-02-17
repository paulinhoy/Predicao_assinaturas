import pandas as pd
from functools import reduce
from datetime import datetime, timedelta

# DataFrame para acumular os resultados processados
df_acumulado = pd.DataFrame()


def listar_dias(data_inicial, data_final):
    # Converter as strings de data em objetos datetime
    data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d')
    data_final = datetime.strptime(data_final, '%Y-%m-%d')

    # Gerar uma lista de strings representando os dias entre as datas
    dias = []
    delta = timedelta(days=1)
    while data_inicial <= data_final:
        dias.append(data_inicial.strftime('%Y-%m-%d'))
        data_inicial += delta

    return dias


# Definir o intervalo de datas para análise
data_inicial = '2021-10-14'
data_final = '2022-01-15'
dias = listar_dias(data_inicial, data_final)

# Carregar o arquivo CSV contendo as informações das medalhas
df = pd.read_csv('tb_players_medalha.csv')
df['dtCreatedAt'] = pd.to_datetime(df['dtCreatedAt'])
df['dtExpiration'] = pd.to_datetime(df['dtExpiration'])
df['dtRemove'] = pd.to_datetime(df['dtRemove'])

# Filtrar registros onde a data de criação é anterior à data de expiração
df = df[df['dtCreatedAt'] < df['dtExpiration']]

for dia_ref in dias:
    # Recarregar o CSV para processar os dados de cada dia separadamente
    df = pd.read_csv('tb_players_medalha.csv')
    df['dtCreatedAt'] = pd.to_datetime(df['dtCreatedAt'])
    df['dtExpiration'] = pd.to_datetime(df['dtExpiration'])
    df['dtRemove'] = pd.to_datetime(df['dtRemove'])
    df = df[df['dtCreatedAt'] < df['dtExpiration']]

    # Filtrar registros com medalhas criadas antes da data de referência
    df = df[df['dtCreatedAt'] < dia_ref]
    df['Data_Ref'] = dia_ref

    # Definir o limite para análise (30 dias antes da data de referência)
    date_limit = pd.to_datetime(dia_ref) - pd.Timedelta(days=30)

    # Filtrar medalhas ainda válidas ou removidas dentro do período de 30 dias
    filtered_df = df[df.apply(
        lambda row: (row['dtRemove'] > date_limit) if pd.notnull(row['dtRemove']) else (row['dtExpiration'] > date_limit),
        axis=1
    )]

    # Contar quantas medalhas diferentes cada jogador possui
    df_Medals = filtered_df.groupby(['idPlayer', 'Data_Ref'])['idMedal'].nunique().reset_index(name='qtMedalhaDist')

    # Contar o número de medalhas adquiridas no período de 30 dias
    filtered_df_condition = filtered_df[filtered_df['dtCreatedAt'] > date_limit]
    trans_medals = filtered_df_condition.groupby(['idPlayer', 'Data_Ref'])['id'].count().reset_index(name='qtMedalhaAdquiridas')
    df_final = pd.merge(df_Medals, trans_medals, on=['idPlayer', 'Data_Ref'], how='outer')

    # Substituir valores ausentes por 0
    df_final = df_final.fillna(0)

    # Identificar o tipo de assinatura com base no ID da medalha
    filtered_df['Tipo_Assinatura'] = filtered_df['idMedal'].replace({
        1: 'Membro Premium',
        3: 'Membro Plus'
    }, regex=True)
    filtered_df['Tipo_Assinatura'] = filtered_df['Tipo_Assinatura'].replace(
        {r'^(?!Membro Premium|Membro Plus)$': 'Outra_Medalha'}, regex=True
    )

    # Contar jogadores com assinaturas específicas
    qtPremium = filtered_df.groupby(['idPlayer', 'Data_Ref'])['Tipo_Assinatura'].apply(
        lambda x: (x == 'Membro Premium').sum()
    ).reset_index(name='qtPremium')

    qtPlus = filtered_df.groupby(['idPlayer', 'Data_Ref'])['Tipo_Assinatura'].apply(
        lambda x: (x == 'Membro Plus').sum()
    ).reset_index(name='qtPlus')

    qtOther = filtered_df.groupby(['idPlayer', 'Data_Ref'])['Tipo_Assinatura'].apply(
        lambda x: (x == 'Outra_Medalha').sum()
    ).reset_index(name='qtOtherMedal')

    # Unir os DataFrames gerados anteriormente
    dataframes = [df_final, qtPremium, qtPlus, qtOther]
    df_final = reduce(lambda left, right: pd.merge(left, right, on=['idPlayer', 'Data_Ref'], how='left'), dataframes)

    # Verificar se a assinatura está ativa na data de referência
    Assin_Ativa = filtered_df[filtered_df.apply(
        lambda row: (row['dtRemove'] > pd.to_datetime(dia_ref)) if pd.notnull(row['dtRemove']) else (row['dtExpiration'] > pd.to_datetime(dia_ref)),
        axis=1
    )]
    Assin_Ativa['AssinaturaAtiva'] = 1
    Assin_Ativa = Assin_Ativa[['idPlayer', 'Data_Ref', 'AssinaturaAtiva']].sort_values(by='idPlayer')
    df_final = pd.merge(df_final, Assin_Ativa, on=['idPlayer', 'Data_Ref'], how='outer')

    # Substituir valores ausentes por 0 para o campo AssinaturaAtiva
    df_final['AssinaturaAtiva'] = df_final['AssinaturaAtiva'].fillna(0)

    # Concatenar os resultados no DataFrame acumulado
    df_acumulado = pd.concat([df_acumulado, df_final], ignore_index=True)

# Exportar o DataFrame acumulado para um arquivo CSV
df_acumulado.to_csv('New_csv/df_info_medalhas')