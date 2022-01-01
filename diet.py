#lista de ingredients na dieta dos caes
ings =['A', 'C', 'H', 'V', 'F']

perc = { 
    "C" : 0.25,
    "H" : 0.2,
    "V" : 0.3,
    "A" : 0.20,
    "F" : 0.05
}
nomes ={ 
    "C" : "Carne",
    "H" : "Hidratos de Carbono",
    "V" : "Vegetais",
    "A" : "Arroz",
    "F" : "Figado"
}


#pede ao utilizador o ingredient e a quantidade
ing = input("Qual é o ingrediente: ").upper()

while ing not in ings:
    print('Ingredient invalido')
    ing = input("Qual é o ingrediente: ").upper()

quat = input("Qual é a quantidade: ")

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

while not isfloat(quat):
    quat = input("Quantidade invalida\nQual é a quantidade: ")
quat = float(quat)
### os dados estão validos para computação ###    

#calcular o total da reifeição
total = quat / perc[ing]

#imprimir as quantidades necessariaas de cada ingredient
for j in ings:
    print(f"{nomes[j]}: {total * perc[j]}")
print(f'Total: {total}')




