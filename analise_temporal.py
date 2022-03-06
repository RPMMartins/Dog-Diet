from numpy.core.numeric import full
import pandas as pd


def unico(ano):
    df = pd.read_csv( r''+f'vendas/vendas_{ano}.csv' ,
                 encoding = 'ISO-8859-1',
                 sep = ';',
                 skiprows=12, 
                 error_bad_lines=False,
                 decimal=',')
    return df

#função faz dowload das vendas do artigo nos anos seleciona 
def serie(lista, referencia):
    
    full_df = None
    for ano in lista:
        
        df=unico(ano)
        df=df[df['Cód. Artigo']==referencia]
        if full_df is None:
            full_df = df
        else:
            full_df = full_df.append(df, ignore_index=True)
    full_df['Data']=pd.to_datetime(full_df['Data'])
    full_df.index = pd.to_datetime(full_df['Data'],format='%m/%d/%y %I:%M%p')
    full_df=full_df['Qtd.']
    full_df=full_df.groupby(pd.Grouper(freq='M')).sum()
    print(full_df)
    return full_df

from statsmodels.tsa.holtwinters import ExponentialSmoothing
import matplotlib.pyplot as plt


#lista =[input("Escolha o primeiro ano: ")]
referencia =input("Escolha a referencia: ")

anos=[2019,2020,2021]

serie(anos,referencia).plot()

plt.show()
plt.close()