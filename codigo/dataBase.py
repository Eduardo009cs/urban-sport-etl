import pyodbc

def conexionBase():
    try:
        
        #print("INFO - Intentando conexion con la base de datos") 
        conexion = pyodbc.connect(
            'Driver={ODBC Driver 17 for SQL Server};'
            'Server=SQL5110.site4now.net;'
            'Database=db_aa1ec5_proteus;'
            'uid=db_aa1ec5_proteus_admin;'
            'pwd=Qg2c}7Zk@a%5zVD&;'
        )
        
        print("INFO - Conexión exitosa con la base de datos")
        return conexion
    except Exception as e:
        print("ERROR - Fallo la conexión con la base de datos", e)

def selectQuery(query):

    #Parametros:
    #query -> Consulta que se hará

    #Funcion: Ingresar parametros dentro de la base de datos 

    
    try :
        conexion = conexionBase()
        cursor = conexion.cursor()
        #print("INFO - Ejecutando query")
        cursor.execute(query)
        resultados = cursor.fetchall()
        return resultados
    except Exception as ex:
        print("ERROR - Error al ejecutar la query", ex)
    finally:
        conexion.close()

def updateQuery(query):
    try :
        conexion = conexionBase()
        cursor = conexion.cursor()
        print("INFO - Ejecutando query")
        cursor.execute(query)
        cursor.commit()
        
    except Exception as ex:
        print("ERROR - Error al ejecutar la query", ex)
    finally:
        conexion.close()