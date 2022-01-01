import pandas as pd


#leitura do ficheiro csv (ficheiro é separado com ponto e virgula)
df = pd.read_csv('vendas_2021.csv' ,
                 encoding = 'unicode_escape',
                 sep = ';',
                 skiprows=12, 
                 error_bad_lines=False,
                 decimal=',')

df['Data']=pd.to_datetime(df['Data'])

#Eliminar linhas que não têm valores (provavelmente feriados e fins-de-semana)
df.dropna(axis=0, how='all', inplace=True)




#selecionar colunas com data, artigos e qtd vendidas
df= df[['Data','Artigos', 'Qtd.']]
df=df.dropna()

#agrupar os artigos e vendas por semana
df['Data'] = pd.to_datetime(df['Data']) - pd.to_timedelta(7, unit='d')
df = df.groupby(['Artigos', pd.Grouper(key='Data', freq='W-MON')])['Qtd.'].sum().reset_index().sort_values('Data')

#numero de semanas 
ns= len(df['Data'].unique())

#calcular a media semanal de vendas de cada artigo
df = df.groupby('Artigos')['Qtd.'].sum() /ns



df.to_csv('media_vendas_semanal_2021.csv', sep = ';', encoding="utf-8-sig", decimal=',')