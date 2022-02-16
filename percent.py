
#pergunta ao utilizador se introduz comida ou razão

tipo=input('''
Comida: c  
Ração: r
Comida ou Ração: ''')



#pergunta ao utilizador a quantidade de ração
quat = input("Qual é a quantidade: ")

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

while not isfloat(quat):
    quat = input("Quantidade invalida\nQual é a quantidade de ração: ")


quat = float(quat)



if tipo == 'r':
    PR = quat / 350
    PC = 1 - PR
    print()
    print(f"Percentagem de comida: {round(100* PC,2)}%")
    print(f"Quantidade de comida: {round(750 * PC)}")
else:
    PR = quat / 750
    PC = 1 - PR
    print()
    print(f"Percentagem de comida : {round(100* PR,2)}%")
    print(f"Quantidade de ração: {round(350 * PC)}")
