
#pergunta ao utilizador a quantidade de ração
quat = input("Qual é a quantidade de ração: ")

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

while not isfloat(quat):
    quat = input("Quantidade invalida\nQual é a quantidade de ração: ")
quat = float(quat)

PR = quat / 300
PC = 1 - PR
print(f"Percentagem de comida: {round(100* PC,2)}%")
print(f"Quantidade de comida: {round(750 * PC)}")