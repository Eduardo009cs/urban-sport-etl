import pandas as pd
import numpy as np
import dataBase as db
import os
import diccionarios as d


PATH = "../Evaluaciones"
JUGADASPATH = "../Evaluaciones/jugadas.csv"
PRODUCTIVIDADPATH = "../Evaluaciones/productividad.csv"
listFileNames = os.listdir(PATH)
def cargaJugadas():
    df = pd.read_csv(JUGADASPATH)

    fecha = df["FECHA"].values
    fechas = list(set(fecha))
    diccionarioFechas = d.obtenerDiccionarioFechas(fechas)

    equiposLocal = df["LOCAL"].values
    equiposVisita = df["VISITA"].values
    equipos = list(set(equiposLocal)) + list(set(equiposVisita))
    diccionarioEquipos = d.obtenerDiccionarioEquipos(equipos)

    jugador = df["NOMBRE"].values
    jugadores = list(set(jugador))
    diccionarioJugadores = d.obtenerDiccionarioJugadores(jugadores)
    
    jugada = df["TIPO_JUGADA"].values
    jugadas = list(set(jugada))
    diccionarioTipoJugadas = d.obtenerDiccionarioTipoJugadas(jugadas)
    
    posicion = df["POSICION"].values
    posiciones = list(set(posicion))
    diccionarioPosiciones = d.obtenerDiccionarioPosiciones(posiciones)

    partidos = df[["TIPO_PARTIDO","FAVOR","CONTRA","LOCAL","VISITA","TEMPORADA","FECHA"]].values
    datosPartido = set(map(tuple,partidos))
    datosPartido = list(map(list,datosPartido))
    for datos in datosPartido:
        datos[3] = diccionarioEquipos[datos[3]]
        datos[4] = diccionarioEquipos[datos[4]]
        datos[6] = diccionarioFechas[datos[6]]
    diccionarioPartidos = d.obtenerDiccionarioPartidos(datosPartido)
    
    print("-----DICCIONARIOS CREADOS CORRECTAMENTE-----")
    print(diccionarioFechas)
    print(diccionarioEquipos)
    print(diccionarioJugadores)
    print(diccionarioTipoJugadas)
    print(diccionarioPosiciones)
    print(diccionarioPartidos)
    print("-----CREANDO QUERY PARA INSERTAR DATOS-----")
    tipoEtapa = df["TIPO_ETAPA"].values
    numJugada = df["NUM_JUGADA"].values
    presnap = df["PRESNAP"].values
    desarrollo = df["DESARROLLO"].values
    finish = df["FINISH"].values
    pride = df["PRIDE"].values
    bodyquery = ""
    aux = 0
    for i in range(len(fecha)):
        if aux == 999:
            aux = 0
            bodyquery = bodyquery[2:]
            query = f"INSERT INTO dimension_jugada VALUES {bodyquery}"
            print(query)
            db.updateQuery(query)
            bodyquery = ""
        idFecha = str(diccionarioFechas[fecha[i]])
        tipoJugada = jugada[i]
        if type(tipoJugada) != type(" "):
            tipoJugada = "193"
        else:
            tipoJugada = diccionarioTipoJugadas[jugada[i]]
        bodyquery = bodyquery + f", ({tipoEtapa[i]},{diccionarioPartidos[idFecha]},{numJugada[i]},{presnap[i]},{desarrollo[i]},{finish[i]},{pride[i]},{diccionarioJugadores[jugador[i]]},{tipoJugada},{diccionarioPosiciones[posicion[i]]})"
        aux = aux + 1
    bodyquery = bodyquery[2:]
    query = f"INSERT INTO dimension_jugada VALUES {bodyquery}"
    print(query)
    db.updateQuery(query)

    


def cargaProductividad():
    df = pd.read_csv(PRODUCTIVIDADPATH)

    fecha = df["FECHA"].values
    fechas = list(set(fecha))
    diccionarioFechas = d.obtenerDiccionarioFechas(fechas)

    equiposLocal = df["LOCAL"].values
    equiposVisita = df["VISITA"].values
    equipos = list(set(equiposLocal)) + list(set(equiposVisita))
    diccionarioEquipos = d.obtenerDiccionarioEquipos(equipos)

    jugador = df["NOMBRE"].values
    jugadores = list(set(jugador))
    diccionarioJugadores = d.obtenerDiccionarioJugadores(jugadores)
    
    
    
    posicion = df["POSICION"].values
    posiciones = list(set(posicion))
    diccionarioPosiciones = d.obtenerDiccionarioPosiciones(posiciones)
    
    medicion = df["TIPO_EVALUACION"].values
    mediciones = list(set(medicion))
    diccionarioMediciones = d.obtenerDiccionarioTipoMedicion(mediciones)

    partidos = df[["TIPO_PARTIDO","FAVOR","CONTRA","LOCAL","VISITA","TEMPORADA","FECHA"]].values
    datosPartido = set(map(tuple,partidos))
    datosPartido = list(map(list,datosPartido))
    for datos in datosPartido:
        datos[3] = diccionarioEquipos[datos[3]]
        datos[4] = diccionarioEquipos[datos[4]]
        datos[6] = diccionarioFechas[datos[6]]
    diccionarioPartidos = d.obtenerDiccionarioPartidos(datosPartido)
    
    print("-----DICCIONARIOS CREADOS CORRECTAMENTE-----")
    print(diccionarioFechas)
    print(diccionarioEquipos)
    print(diccionarioJugadores)
    print(diccionarioMediciones)
    print(diccionarioPosiciones)
    print(diccionarioPartidos)
    print("-----CREANDO QUERY PARA INSERTAR DATOS-----")
    valor = df["EVALUACION"].values
    bodyquery = ""
    aux = 0
    for i in range(len(fecha)):
        if aux == 999:
            aux = 0
            bodyquery = bodyquery[2:]
            query = f"INSERT INTO tab_hechos_estadisticas_productividad VALUES {bodyquery}"
            print(query)
            db.updateQuery(query)
            bodyquery = ""
        idFecha = str(diccionarioFechas[fecha[i]])

        bodyquery = bodyquery + f", ({diccionarioJugadores[jugador[i]]},{diccionarioMediciones[medicion[i]]},{valor[i]},{diccionarioPartidos[idFecha]},{diccionarioPosiciones[posicion[i]]})"
        aux = aux + 1
    bodyquery = bodyquery[2:]
    query = f"INSERT INTO tab_hechos_estadisticas_productividad VALUES {bodyquery}"
    print(query)
    db.updateQuery(query)

def mainCarga():
    print("Carga")
    for fileName in listFileNames:
        print(fileName)
        if  fileName == "jugadas.csv":
            cargaJugadas()
            print("")
        else :
            cargaProductividad()
        
            

