from numpy.core.numeric import full
import pandas as pd
import os
import csv
#programa que lé o ficheiro csv das vendas de um unico ano
def unico(ano):
    df = pd.read_csv( r''+f'vendas/vendas_{ano}.csv' ,
                 encoding = 'ISO-8859-1',
                 sep = ';',
                 skiprows=12, 
                 error_bad_lines=False,
                 decimal=',',low_memory=False)
    return df
#cria um dataframe completa de todas as vendas
def download():
    full_df = None
    for ano in [2019,2020,2021]:
        
        #faz dowload das vendas do artigo com o cod de artigo igual á referencia posta
        df=unico(ano)
        df=df[['Data','Cód. Artigo','Qtd.']]    
        if full_df is None:
            full_df = df
        else:
            full_df = full_df.append(df, ignore_index=True)
    return full_df

#função faz dowload das vendas do artigo usando a lista completa de vendas 
def serie(full_df, referencia):
    
    #dataframe fazia onde cada venda vai ser colocada
    
    full_df=full_df[full_df['Cód. Artigo']==referencia] 
    full_df['Data']=pd.to_datetime(full_df['Data'])
    full_df.index = pd.to_datetime(full_df['Data'],format='%m/%d/%y %I:%M%p')
    print(full_df)
    #selecionar apenas a qtd. das vendas
    full_df=full_df['Qtd.']
    #agrupar as vendas de forma mensal e fazer a soma mensal
    full_df=full_df.groupby(pd.Grouper(freq='M')).sum()
    return full_df




#### programa principal #####

#base de dados ondes as vendas todas vão estar colocadas
full_df=None

down =download()

modo= input("Lista ou Manual?: ")

if modo == 'm':
    referencia =input("Escolha a referencia: ")
    while referencia != '':
        vendas =serie(down,referencia).to_frame()
        if full_df is None:
            #datas de todos os meses
            Datas = vendas.index.tolist()
            full_df = pd.DataFrame(index=Datas)        
        vendas.columns = [referencia]
        full_df = full_df.join(vendas, how="outer")  #left join by default
        referencia =input("Escolha a referencia: ")

else:
    lista=input("Localização da Lista: ")
    with open(lista, newline='') as f:
        reader = csv.reader(f)
        lista = sum(list(reader), [])
    print(lista)

    for artigo in lista:
        vendas =serie(down,artigo).to_frame()
        if full_df is None:
            #datas de todos os meses
            Datas = vendas.index.tolist()
            full_df = pd.DataFrame(index=Datas)        
        vendas.columns = [artigo]
        full_df = full_df.join(vendas, how="outer")


#resultado final em tabela transposta
full_df=full_df.transpose()

if not os.path.exists('vendas-artigos'):
 os.mkdir('vendas-artigos')



#guardar tabela com nome pessoal
nome = input("Nome do ficheiro: ")



full_df['Cód. Artigo'] = full_df.index

for i in range(10):
    print('')



#dataframe com os codigos de artigo e o nomes
tmp = pd.read_csv( 'artigos.csv' ,
                 encoding = 'ISO-8859-1',
                 sep = ';',
                 skiprows=9, 
                 error_bad_lines=False,
                 decimal=',')

tmp=tmp[['Referência','Designação','Resumo']]
tmp=tmp.dropna()

full_df=tmp.merge(full_df,how='inner',right_on='Cód. Artigo', left_on='Referência')
print(full_df)

full_df.drop('Cód. Artigo', axis=1,inplace=True)

from datetime import datetime
full_df.columns = [i.strftime('%Y-%m-%d') if isinstance(i, datetime) else i for i in full_df.columns]

full_df.to_csv(f"vendas-artigos/{nome}.csv", sep = ';', encoding="utf-8-sig", decimal=',',index=False)

print('Processo Completo')