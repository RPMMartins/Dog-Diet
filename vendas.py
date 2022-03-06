from typing import TYPE_CHECKING
from numpy import square
from numpy.core.numeric import full
import pandas as pd
from glob import glob
import random

random.seed(10)

#leitura dos ficheiro csv (ficheiro é separado com ponto e virgula)
def todos():
    files = glob('vendas/*.csv')
    full_df = None
    for f in files:
        print(f)
        df = pd.read_csv( r''+f ,
                 encoding = 'ISO-8859-1',
                 sep = ';',
                 skiprows=12, 
                 error_bad_lines=False,
                 decimal=',')
        if full_df is None:
            full_df = df
        else:
            full_df = full_df.append(df, ignore_index=True)
    return full_df

def unico(ano):
    df = pd.read_csv( r''+f'vendas/vendas_{ano}.csv' ,
                 encoding = 'ISO-8859-1',
                 sep = ';',
                 skiprows=12, 
                 error_bad_lines=False,
                 decimal=',')
    return df



def compute(full_df,ano):

    #tornar a coluna das datas em classe de panda datetime
    full_df['Data']=pd.to_datetime(full_df['Data'])

    #Eliminar linhas que não têm valores (provavelmente feriados e fins-de-semana)
    full_df.dropna(axis=0, how='all', inplace=True)


    #selecionar colunas com data, codigo de artigos e qtd vendidas
    full_df= full_df[['Data','Cód. Artigo', 'Qtd.']]
    full_df=full_df.dropna()


    #agrupar os artigos e vendas por semana
    full_df['Data'] = pd.to_datetime(full_df['Data']) - pd.to_timedelta(7, unit='d')
    full_df = full_df.groupby(['Cód. Artigo', pd.Grouper(key='Data', freq='W-MON')])['Qtd.'].sum().reset_index().sort_values('Data')

    #numero de semanas 
    ns= len(full_df['Data'].unique())

    #calcular os quadrados das vendas semanais de cada artigo
    full_df['squa Qtd.']= full_df['Qtd.']**2


    #calcular a media semanal de vendas de cada artigo
    full_df = full_df.groupby('Cód. Artigo')[['Qtd.','squa Qtd.']]

    #calcular a media semanal de vendas  e os seus quadrados de cada artigo
    full_df = full_df.sum()/ns

    #calcular o desvio padrao semanal de cada artigo
    full_df['Sd']=(full_df['squa Qtd.']-full_df['Qtd.']**2)**(1/2)


    #ordenar os valores pela media de vendas
    full_df=full_df.reset_index()
    full_df=full_df[['Cód. Artigo','Qtd.','Sd']]
    full_df.sort_values('Cód. Artigo', inplace=True,ascending=False)


    #dataframe com os codigos de artigo e o nomes
    tmp = pd.read_csv( 'artigos.csv' ,
                 encoding = 'ISO-8859-1',
                 sep = ';',
                 skiprows=9, 
                 error_bad_lines=False,
                 decimal=',')
    print(tmp.head())
    tmp=tmp[['Referência','Designação','Resumo']]
    tmp=tmp.dropna()


    #criar versão final da tabela
    full_df=full_df.merge(tmp,how='inner',left_on='Cód. Artigo', right_on='Referência')
    full_df.sort_values('Qtd.', inplace=True,ascending=False)
    full_df=full_df[['Cód. Artigo','Qtd.','Sd','Designação','Resumo']]

    #converter tabela em ficheiro csv
    full_df.to_csv(f'media_vendas_semanal_{ano}.csv', sep = ';', encoding="utf-8-sig", decimal=',',index=False)








#pede ao utilizador o ano cujo
ano=input('Escolha o ano que queira analisar: ')

if ano== 'todos':
    full_df = todos()
else:
    full_df= unico(ano)
    

compute(full_df,ano)