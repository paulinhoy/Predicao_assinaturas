import matplotlib.pyplot as plt
import seaborn as sns
from functools import reduce
import pandas as pd
from datetime import datetime, timedelta

# Inicializa um DataFrame vazio para acumular os resultados processados
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

# Carrega o arquivo CSV com as informações de partidas e jogadores
df = pd.read_csv('tb_lobby_stats_player.csv')

# Converte a coluna de datas para o formato datetime
df['dtCreatedAt'] = pd.to_datetime(df['dtCreatedAt'])

# Define o intervalo de datas a ser analisado
data_inicial = '2021-10-14'
data_final = '2022-01-15'
dias = listar_dias(data_inicial, data_final)

# Itera sobre cada dia no intervalo definido
for dia_ref in dias:
    print(dia_ref)         # Printa na tela qual dia está gerando a estatística
    
    # Filtra os dados do último mês em relação ao dia de referência
    df_Past_month = df[(df['dtCreatedAt'] < dia_ref) & 
                       (df['dtCreatedAt'] >= pd.to_datetime(dia_ref) - pd.Timedelta(days=30))].sort_values(by='dtCreatedAt', ascending=True)
    
    # Adiciona uma coluna com a data de referência e converte a coluna de datas para datetime
    df_Past_month['Data_Ref'] = dia_ref
    df_Past_month['dtCreatedAt'] = pd.to_datetime(df['dtCreatedAt'])
    
    # Calcula o número de partidas, dias jogados e recência por jogador
    df_qtd_part = df_Past_month.groupby(['idPlayer', 'Data_Ref'])['idLobbyGame'].count().reset_index(name='qtPartidas')
    df_qtd_dias = df_Past_month.groupby(['idPlayer', 'Data_Ref'])['dtCreatedAt'].apply(
        lambda x: x.dt.date.nunique()).reset_index(name='qtDias')
    recencia = df_Past_month.groupby(['idPlayer', 'Data_Ref'])['dtCreatedAt'].apply(
        lambda x: pd.to_datetime(dia_ref) - pd.to_datetime(x.dt.date.max())).reset_index(name='qtRecencia')

    # Combina os DataFrames de métricas calculadas
    df_combined = pd.merge(df_qtd_part, df_qtd_dias, on=['idPlayer', 'Data_Ref'])
    df_combined = pd.merge(df_combined, recencia, on=['idPlayer', 'Data_Ref'])
    
    # Calcula a taxa de vitórias por jogador
    win_rate = df_Past_month.groupby(['idPlayer', 'Data_Ref'])['flWinner'].mean().reset_index(name='winRate')
    df_combined = pd.merge(df_combined, win_rate, on=['idPlayer', 'Data_Ref'])
    
    # Calcula a proporção de partidas jogadas em cada mapa
    maps = ['de_mirage', 'de_nuke', 'de_inferno', 'de_vertigo', 'de_ancient', 'de_dust2', 'de_train', 'de_overpass']
    for i, map_name in enumerate(maps):
        map_stats = df_Past_month.groupby(['idPlayer', 'Data_Ref'])['descMapName'].apply(
            lambda x: (x == map_name).mean()).reset_index(name=f'propd{map_name.capitalize()}')
        df_combined = pd.merge(df_combined, map_stats, on=['idPlayer', 'Data_Ref'], how='left')
    
    # Calcula estatísticas adicionais: K/D, KDA, HsRate
    Kill_tot = df_Past_month.groupby(['idPlayer', 'Data_Ref'])['qtKill'].sum()
    Hs_tot = df_Past_month.groupby(['idPlayer', 'Data_Ref'])['qtHs'].sum()
    Hs_Hate = (Hs_tot / Kill_tot).reset_index(name='HsHate')
    df_combined = pd.merge(df_combined, Hs_Hate, on=['idPlayer', 'Data_Ref'])
    
    Death_tot = df_Past_month.groupby(['idPlayer', 'Data_Ref'])['qtDeath'].sum()
    Assist_tot = df_Past_month.groupby(['idPlayer', 'Data_Ref'])['qtAssist'].sum()
    
    KDA_tot = ((Kill_tot + Assist_tot) / Death_tot).reset_index(name='KDA')
    KDR_tot = (Kill_tot / Death_tot).reset_index(name='KDR')
    df_combined = pd.merge(df_combined, KDA_tot, on=['idPlayer', 'Data_Ref'])
    df_combined = pd.merge(df_combined, KDR_tot, on=['idPlayer', 'Data_Ref'])
    
    # Inclui informações de partidas por dia da semana
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for day in weekdays:
        day_stat = df_Past_month.groupby(['idPlayer', 'Data_Ref'])['dtCreatedAt'].apply(
            lambda x: (x.dt.day_name() == day).mean()).reset_index(name=f'prop{day}')
        df_combined = pd.merge(df_combined, day_stat, on=['idPlayer', 'Data_Ref'], how='left')
    
    # Calcula as médias para variáveis de interesse
    var_qtd = df.columns[3:-1].tolist()
    var_qtd.remove('descMapName')
    for var in var_qtd:
        var_avg = df_Past_month.groupby(['idPlayer', 'Data_Ref'])[var].mean().reset_index(name=f'{var}AVG')
        df_combined = pd.merge(df_combined, var_avg, on=['idPlayer', 'Data_Ref'], how='left')
    df_combined = df_combined.drop(columns='flWinnerAVG')
    
    # Inclui outras estatísticas como partidas menores que 16 rounds
    qtPartidas_less16 = df_Past_month.groupby(['idPlayer', 'Data_Ref'])['qtRoundsPlayed'].apply(
        lambda x: (x < 16).sum()).reset_index(name='qtPartidasMenos16')
    df_combined = pd.merge(df_combined, qtPartidas_less16, on=['idPlayer', 'Data_Ref'])
    
    # Adiciona estatísticas sobre vitórias e níveis por mapa
    # Similar aos cálculos acima para mapas e vitórias
    
    df_acumulado = pd.concat([df_acumulado, df_combined], ignore_index=True)

# Salva o DataFrame acumulado como CSV
df_acumulado.to_csv('New_csv/df_info_statsplayers')
