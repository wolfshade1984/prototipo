
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import numpy as np
import random

# Datos iniciales
data = {
    'alcohol': [5.0, 6.0, 4.5, 7.0, 5.2, 6.5, 5.8],
    'amargor': [20, 40, 15, 60, 25, 50, 30],
    'color': [10, 20, 10, 30, 15, 25, 20],
    'tipo': ['albina', 'clara', 'rubia', 'castaña', 'morena', 'negra', 'dark vader']
}
df = pd.DataFrame(data)
X = df[['alcohol', 'amargor', 'color']]
y = df['tipo']
# Dividir los datos en conjunto de entrenamiento y de prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
# Crear y entrenar el modelo Random Forest
clf_rf = RandomForestClassifier(n_estimators=100, random_state=42)
clf_rf.fit(X_train, y_train)
# Crear y entrenar el modelo de Árbol de Decisiones
clf_dt = DecisionTreeClassifier(random_state=42)
clf_dt.fit(X_train, y_train)
# Inicializar lista para guardar precisiones y contador de entradas
precisiones_rf = []
precisiones_dt = []
contador_datos = 0
def mostrar_cervezas():
    print("\nValores de las cervezas disponibles:")
    print(df)
# Función para generar datos aleatorios
def generar_datos_aleatorios(n):
    global df
    tipos = ['albina', 'clara', 'rubia', 'castaña', 'morena', 'negra', 'dark vader']
    for _ in range(n):
        alcohol = round(random.uniform(4.0, 8.0), 2)
        amargor = random.randint(10, 70)
        color = random.randint(5, 35)
        tipo = random.choice(tipos)
        df.loc[len(df)] = [alcohol, amargor, color, tipo]
# Bucle para ingresar datos manualmente o automáticamente
while True:
    mostrar_cervezas()  # Mostrar cervezas antes de ingresar datos
    modo = input("¿Desea ingresar datos manualmente (m) o generar datos aleatorios (a)? (m/a): ")
    if modo.lower() == 'm':
        # Solicitar datos al usuario
        while True:
            try:
                alcohol = float(input("Ingrese el porcentaje de alcohol (ej. 5.5, debe ser un número positivo): "))
                if alcohol < 0:
                    raise ValueError
                break
            except ValueError:
                print("Valor inválido. Por favor, ingrese un número positivo para el porcentaje de alcohol.")
        while True:
            try:
                amargor = int(input("Ingrese el amargor (IBU, ej. 30, debe ser un número positivo): "))
                if amargor < 0:
                    raise ValueError
                break
            except ValueError:
                print("Valor inválido. Por favor, ingrese un número positivo para el amargor (IBU).")

        while True:
            try:
                color = int(input("Ingrese el color (EBC, ej. 15, debe ser un número positivo): "))
                if color < 0:
                    raise ValueError
                break
            except ValueError:
                print("Valor inválido. Por favor, ingrese un número positivo para el color (EBC).")

        # Agregar los nuevos datos al DataFrame
        df.loc[len(df)] = [alcohol, amargor, color, 'Nuevo']  # Etiqueta temporal
    elif modo.lower() == 'a':
        n = int(input("¿Cuántos datos aleatorios desea generar? "))
        generar_datos_aleatorios(n)
    # Predecir el tipo de cerveza usando Random Forest
    prediction_rf = clf_rf.predict(df[['alcohol', 'amargor', 'color']].tail(1))  # Predecir la última entrada
    print(f"Tipo de cerveza predicho por Random Forest: {prediction_rf[0]}")
    # Predecir el tipo de cerveza usando Árbol de Decisiones
    prediction_dt = clf_dt.predict(df[['alcohol', 'amargor', 'color']].tail(1))  # Predecir la última entrada
    print(f"Tipo de cerveza predicho por Árbol de Decisiones: {prediction_dt[0]}")
    # Contador de entradas
    contador_datos += 1
    # Entrenar los modelos con los datos actualizados
    X = df[['alcohol', 'amargor', 'color']]
    y = df['tipo']
    clf_rf.fit(X, y)  # Reentrenar el modelo de Random Forest
    clf_dt.fit(X, y)  # Reentrenar el modelo de Árbol de Decisiones
    # Evaluar precisión del modelo con el conjunto de prueba
    y_pred_rf = clf_rf.predict(X_test)
    accuracy_rf = accuracy_score(y_test, y_pred_rf)
    precisiones_rf.append(accuracy_rf * 100)  # Guardar la precisión
    y_pred_dt = clf_dt.predict(X_test)
    accuracy_dt = accuracy_score(y_test, y_pred_dt)
    precisiones_dt.append(accuracy_dt * 100)  # Guardar la precisión
    print(f"Precisión del modelo Random Forest después de la entrada: {accuracy_rf * 100:.2f}%")
    print(f"Precisión del modelo Árbol de Decisiones después de la entrada: {accuracy_dt * 100:.2f}%")
    # Mostrar estadísticas cada 10 entradas
    if contador_datos % 10 == 0:
        print(f"\nEstadísticas después de {contador_datos} entradas:")
        print(f"Precisión promedio del modelo Random Forest: {np.mean(precisiones_rf[-10:]):.2f}%")
        print(f"Precisión promedio del modelo Árbol de Decisiones: {np.mean(precisiones_dt[-10:]):.2f}%")
        plt.figure(figsize=(12, 6))
        plt.plot(precisiones_rf, label='Precisión Random Forest')
        plt.plot(precisiones_dt, label='Precisión Árbol de Decisiones')
        plt.title('Precisión de los Modelos a lo Largo del Tiempo')
        plt.xlabel('Iteración')
        plt.ylabel('Precisión (%)')
        plt.axhline(y=np.mean(precisiones_rf[-10:]), color='r', linestyle='--', label='Promedio RF')
        plt.axhline(y=np.mean(precisiones_dt[-10:]), color='g', linestyle='--', label='Promedio DT')
        plt.legend()
        plt.show()
        # Visualización del Árbol de Decisiones
        plt.figure(figsize=(12, 6))
        plot_tree(clf_dt, filled=True, feature_names=['alcohol', 'amargor', 'color'], class_names=clf_dt.classes_)
        plt.title('Árbol de Decisiones')
        plt.show()
    # Preguntar si desea continuar
    continuar = input("¿Desea ingresar otra cerveza? (s/n): ")
    if continuar.lower() != 's':
        break