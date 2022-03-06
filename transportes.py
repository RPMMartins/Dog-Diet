import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os

nome= input('Qual é o nome do ficheiro: ')
if not os.path.exists(f'./transportes/{nome}'):
    os.mkdir(f'./transportes/{nome}')

print("Escolha o tipo de separador:")
print("1) ';' ")
print("2) ',' ")
stilo = input('Qual Separador: ')

if stilo == "1":
    df = pd.read_csv( r''+f'transportes/{nome}.csv' ,
                 sep = ',', 
                 error_bad_lines=False,
                 decimal=',')
else:
    df = pd.read_csv( r''+f'transportes/{nome}.csv' ,
                 sep = ';', 
                 error_bad_lines=False,
                 decimal=',',
                 encoding = 'ISO-8859-1')



df.drop(df[(df['DIA SEMANA'] == 'domingo') | (df['DIA SEMANA'] == 'sábado')].index, inplace=True)


#função q cria plots de barra sobre o numero de envios e Incidencias
def plotbar(labels,envios,incidencias,companhia,freq):

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, envios, width, label='Incidencias')
    rects2 = ax.bar(x + width/2, incidencias, width, label='Envios')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Envios/Incidencias')
    ax.set_title(f'Numero de Envios e Incidencias {companhia}')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


    autolabel(rects1)
    autolabel(rects2)
    plt.margins(y=0.1)
    plt.xticks(rotation=45)
    fig.tight_layout()

    plt.savefig(f"./transportes/{nome}/{companhia}_{freq}.png")
    plt.close()


def plotbarpercent(labels,percentagens,companhia,freq):

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects = ax.bar(x - width/2, percentagens, width, label='percentagens')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Percentagem')
    ax.set_title(f'Percentagem de Incidencias {companhia}')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


    autolabel(rects)
    plt.margins(y=0.1)
    plt.xticks(rotation=45)
    fig.tight_layout()

    plt.savefig(f"./transportes/{nome}/{companhia}_{freq}_percentagem.png")
    plt.close()

#Para cada companhia calcular o total mensal e semanal de incidencias
# e as percentagens, e criar graficos de barras que vão fizar guardados
#na pasta de transportes

df['INC Todas']=df['INC DHL']+df['INC MRW']+df['INC CTT']
df['ENVIOS Todas']=df['ENVIOS DHL']+df['ENVIOS MRW']+df['ENVIOS CTT']

for companhia in ['DHL', 'MRW', 'CTT','Todas']:

    #calcular o valores mensais das vendas e das incidencias
    tmp=df[['MÊS','DIA SEMANA',f'ENVIOS {companhia}',f'INC {companhia}']]
    tmp.dropna(inplace=True)
    tmp_mes=tmp.groupby('MÊS')[[f'ENVIOS {companhia}',f'INC {companhia}']].sum()
    tmp_mes['Percentagem']=round(tmp_mes[f'INC {companhia}']/tmp_mes[f'ENVIOS {companhia}'] *100,2)
    
    meses = ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']
    index_mes=[]
    for mes in meses:
        if mes in tmp_mes.index.tolist():
            index_mes.append(mes)
    
    tmp_mes=tmp_mes.loc[index_mes]
    print(tmp_mes)
    
    #criar o grafico de barras
    plotbar(tmp_mes.index.tolist(),tmp_mes[f'INC {companhia}'],
                                    tmp_mes[f'ENVIOS {companhia}'],
                                    companhia,
                                    'mensal')

    plotbarpercent(tmp_mes.index.tolist(),tmp_mes['Percentagem'],
                                                        companhia,
                                                        'mensal')

    tmp_mes.to_csv(f"./transportes/{nome}/{companhia}_mensal.csv",encoding = 'ISO-8859-1')

   
    #calcular o valores mensais das vendas e das incidencias
    tmp_semana=tmp.groupby('DIA SEMANA')[[f'ENVIOS {companhia}',f'INC {companhia}']].sum()
    tmp_semana['Percentagem']=round(tmp_semana[f'INC {companhia}']/tmp_semana[f'ENVIOS {companhia}'] *100,2)
    tmp_semana=tmp_semana.loc[['segunda','terça','quarta','quinta','sexta']]


    #criar o graficos de barras do numero de envios, incidencias e as percentagens
    plotbar(tmp_semana.index.tolist(),tmp_semana[f'INC {companhia}'],
                                    tmp_semana[f'ENVIOS {companhia}'],
                                    companhia,
                                    'semanal')

    plotbarpercent(tmp_semana.index.tolist(),tmp_semana['Percentagem'],
                                                        companhia,
                                                        'semanal')

    tmp_semana.to_csv(f"./transportes/{nome}/{companhia}_semanal.csv",encoding = 'ISO-8859-1')
    print(tmp_semana)


print("Processo Completo")

#TRANSPORTES_2021