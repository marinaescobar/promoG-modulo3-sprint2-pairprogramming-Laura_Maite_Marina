# %%
# Librerías necesarias
import pandas as pd
import numpy as np

# %%
def archivos():
    
    #Si al abrir el csv diera error porque no coinciden los números de columna:
    # error_bad_lines=False, warn_bad_lines=False
    # o tambien: on_bad_lines='warn'
    
    df1 = pd.read_csv('files/productos.csv')
    df2 = pd.read_csv('files/clientes.csv')
    df3 = pd.read_csv('files/ventas.csv')
    
    return df1 , df2 , df3

def exploracion (df1 , df2 , df3):
    
    for df, nombre in zip([df1, df2, df3] , ['productos', 'clientes', 'ventas']):
        print(f"INFORMACIÓN SOBRE {nombre.upper()}")
        print(f"La forma:")
        print(f"{df.shape}\n")
        print(f"Las columnas:")
        print(f"{df.columns}\n")
        print(f"Los tipos de datos:")
        print(f"{df.dtypes}\n")
        print(f"Los nulos:")
        print(f"{df.isnull().sum()}\n")
        print(f"Los duplicados:")
        print(f"{df.duplicated().sum()}\n")
        print(f"Los principales estadísticos:")
        print(f"{df.describe().T}\n")
        # Sacamos la moda de las columnas categóricas sólo del df2 (clientes) porque es el que tiene nulos
        if nombre == 'clientes':
            print(f"Las modas de las columnas categóricas:\n")
            columnas_cat = df.select_dtypes(include = 'object')
            for columna in columnas_cat:
                if df[columna].isnull().any():
                    print(f"Revisando {columna}")
                    print(df[columna].value_counts())  
                    print("") 
        print(f"\n-----------------------------\n")
    
    