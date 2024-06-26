# %%
# Librerías necesarias
import pandas as pd
import numpy as np
import mysql.connector

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
    
    return

def limpieza (df2,df1,df3):
    print("LIMPIEZA DE CLIENTES:")
    df2[["email", "gender", "Address"]] = df2[["email", "gender", "Address"]].fillna("unknown")
    df2["City"] = df2["City"].fillna("Madrid")
    df2["Country"]= df2["Country"].fillna("Spain")
    df2['full_name'] = df2['first_name'] + ' ' + df2['last_name']
    df2["City"] = df2["City"].apply(lambda x : x.replace("," , "") if isinstance(x , str) else x)
    df2["Address"] = df2["Address"].apply(lambda x : x.replace("," , "") if isinstance(x , str) else x)
    df1['ID_Producto'] = df1['ID']
    df3['id'] = df3['ID_Cliente']
    
    return df1, df2, df3

def union(df1,df2,df3):



    df_ventas_productos = pd.merge(df3, df1, on='ID_Producto', how='left')
    tabla_unica = pd.merge(df_ventas_productos, df2, on='id', how='left')
    #return tabla_unica
    return tabla_unica


def transformacion(tabla_unica):

    tabla_unica = tabla_unica.drop(columns=['first_name', 'last_name', 'ID',"id"])

    columnas_ordenadas = ['ID_Cliente', 'full_name','email', 'gender', 'City', 
                          'Country', 'Address','ID_Producto', 'Nombre_Producto', 
                          'Categoría', 'Origen', 'Descripción','Fecha_Venta', 
                          'Cantidad','Precio', 'Total']
    tabla_final= tabla_unica[columnas_ordenadas]
    
    #Cambiar nombre de columnas a español
    mapeo_columnas = {
    'ID_Cliente': 'ID Cliente',
    'full_name': 'Nombre completo',
    'email': 'Correo electrónico',
    'gender': 'Género',
    'City': 'Ciudad',
    'Country': 'País',
    'Address': 'Dirección',
    'ID_Producto': 'ID Producto',
    'Nombre_Producto': 'Nombre del producto',
    'Categoría': 'Categoría',
    'Origen': 'Origen',
    'Descripción': 'Descripción',
    'Fecha_Venta': 'Fecha de venta',
    'Cantidad': 'Cantidad',
    'Precio': 'Precio',
    'Total': 'Total'
}
    tabla_final = tabla_final.rename(columns=mapeo_columnas)

    return tabla_final


def creacion_tablas_esquema(query, contraseña, nombre_bbdd=None):
    
    if nombre_bbdd is not None:
        cnx = mysql.connector.connect(
            user="root",
            password=contraseña,
            host="127.0.0.1")

        mycursor = cnx.cursor()

        try:
            mycursor.execute(query)
            print("Consulta ejecutada correctamente.")
            cnx.close()

        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            cnx.close()
    else:
        cnx = mysql.connector.connect(
            user="root",
            password=contraseña,
            host="127.0.0.1",
            database=nombre_bbdd)
        
        mycursor = cnx.cursor()

        try:
            mycursor.execute(query)
            print("Consulta ejecutada correctamente.")
            cnx.close()

        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            cnx.close()
            
def insertar_datos(query, contraseña, nombre_bdd, lista_tuplas):
    
    cnx = mysql.connector.connect(
        user="root", 
        password=contraseña, 
        host="127.0.0.1", database=nombre_bdd)
    
    mycursor = cnx.cursor()
    
    try:
        mycursor.executemany(query, lista_tuplas)
        cnx.commit()
        print(mycursor.rowcount, "registro/s insertado/s.")
        cnx.close()
        
    except mysql.connector.Error as err:
        print(err)
        print("Error Code:", err.errno)
        print("SQLSTATE", err.sqlstate)
        print("Message", err.msg)
        cnx.close()
        
def convertir_float(lista_tuplas):
    """
    Convierte los elementos de una lista de tuplas a float cuando sea posible.
    Args:
    - lista_tuplas (list): Una lista que contiene tuplas con elementos que pueden ser convertidos a float.
    Returns:
    - list: Una nueva lista con las mismas tuplas de entrada, pero con los elementos convertidos a float si es posible.
    """
    datos_tabla_caract_def = []
    
    for tupla in lista_tuplas:
        lista_intermedia = []
        for elemento in tupla:
            try:
                lista_intermedia.append(float(elemento))
            except:
                lista_intermedia.append(elemento)
            
        datos_tabla_caract_def.append(tuple(lista_intermedia))
    
    return datos_tabla_caract_def
