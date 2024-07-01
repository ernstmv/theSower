import matplotlib.pyplot as plt

# Lista de coordenadas (x, y) proporcionadas
coordenadas = [(1, 2), (2, 3), (3, 5), (4, 7), (5, 11), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2)]

# Extraer los valores únicos de x y y
x_vals = sorted(set(punto[0] for punto in coordenadas))
y_vals = sorted(set(punto[1] for punto in coordenadas))

# Determinar el rango de valores esperados
x_min, x_max = min(x_vals), max(x_vals)
y_min, y_max = min(y_vals), max(y_vals)

# Generar todas las combinaciones posibles de coordenadas dentro del rango
coordenadas_completas = [(x, y) for x in range(x_min, x_max + 1) for y in range(y_min, y_max + 1)]

# Encontrar las coordenadas faltantes
coordenadas_faltantes = [coord for coord in coordenadas_completas if coord not in coordenadas]

# Mostrar las coordenadas faltantes
print("Coordenadas faltantes:", coordenadas_faltantes)

# Graficar las coordenadas existentes y faltantes
x_existentes = [punto[0] for punto in coordenadas]
y_existentes = [punto[1] for punto in coordenadas]
x_faltantes = [punto[0] for punto in coordenadas_faltantes]
y_faltantes = [punto[1] for punto in coordenadas_faltantes]

plt.scatter(x_existentes, y_existentes, marker='o', color='blue', label='Existentes')
plt.scatter(x_faltantes, y_faltantes, marker='x', color='red', label='Faltantes')

# Añadir títulos y etiquetas
plt.title('Gráfico de coordenadas')
plt.xlabel('Eje X')
plt.ylabel('Eje Y')
plt.legend()

# Mostrar el gráfico
plt.show()

