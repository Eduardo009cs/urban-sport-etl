import dataBase as db

def obtenerDiccionarioFechas(fechas):
    bodyquery = ""
    for fecha in fechas:
        bodyquery = bodyquery + f" OR fecha = '{fecha}'"
    bodyquery = bodyquery[4:]
    query = f"SELECT id_fecha, fecha FROM dimension_tiempo WHERE {bodyquery}"
    #print(query)
    idFechas = db.selectQuery(query)
    #AGREGAMOS LOS ID AL DICCIONARIO DE FECHAS
    diccionarioFechas = {}
    
    if not idFechas:
        print("No hay fechas")
    else:
        for fecha in idFechas:
            aux = str(fecha[1])
            diccionarioFechas[aux] = fecha[0]
    
    #VERIFICAMOS SI TODAS LAS FECHAS YA ESTAN EN LA BASE
    fechaFaltante = False
    fechaNoEncontrada = []
    for fecha in fechas:
        if fecha not in diccionarioFechas.keys():
            fechaFaltante = True
            fechaNoEncontrada.append(fecha)
    
    #INGRESAMOS LAS FECHAS QUE NO SE ENCONTRARON
    if fechaFaltante:
        bodyquery = ""
        for fecha in fechaNoEncontrada:
            año = fecha.split("-")[0]
            mes = fecha.split("-")[1]
            dia = fecha.split("-")[2]
            bodyquery = bodyquery + f", ('{fecha}','00:00:00',{año},{mes},{dia})"
        bodyquery = bodyquery[2:]
        query = f"INSERT INTO dimension_tiempo VALUES {bodyquery};"
        #print(query)
        db.updateQuery(query)
        #BUSCAMOS LOS ID DE LAS FECHAS NO ENCONTRADAS
        bodyquery = ""
        for fecha in fechaNoEncontrada:
            bodyquery = bodyquery + f" OR fecha = '{fecha}'"
        bodyquery = bodyquery[4:]
        query = f"SELECT id_fecha, fecha FROM dimension_tiempo WHERE {bodyquery}"
        #print(query)
        idFechas = db.selectQuery(query)
        #AGREGAMOS LAS FECHAS FALTANTES AL DICCIONARIO
        for fecha in idFechas:
            aux = str(fecha[1])
            diccionarioFechas[aux] = fecha[0]
    return diccionarioFechas

def obtenerDiccionarioTipoJugadas(tipoJugadas):
    bodyquery = ""
    for tipoJugada in tipoJugadas:
        if type(tipoJugada) == type(" "):
            bodyquery = bodyquery + f" OR nombre_tipo_jugada = '{tipoJugada}'"
    bodyquery = bodyquery[4:]
    query = f"SELECT id_tipo_jugada, nombre_tipo_jugada FROM dimension_tipo_jugada WHERE {bodyquery}"
    #print(query)
    idTipoJugadas = db.selectQuery(query)
    #AGREGAMOS LOS ID AL DICCIONARIO DE FECHAS
    diccionarioTipoJugadas = {}
    for tipoJugada in idTipoJugadas:
        aux = str(tipoJugada[1])
        diccionarioTipoJugadas[aux] = tipoJugada[0]
    
    #VERIFICAMOS SI TODAS LAS FECHAS YA ESTAN EN LA BASE
    tipoJugadaFaltante = False
    tipoJugadaNoEncontrada = []
    for tipoJugada in tipoJugadas:
        if tipoJugada not in diccionarioTipoJugadas.keys() and type(tipoJugada) == type(" "):
            
            tipoJugadaFaltante = True
            tipoJugadaNoEncontrada.append(tipoJugada)
    
    #INGRESAMOS LAS FECHAS QUE NO SE ENCONTRARON
    if tipoJugadaFaltante:
        bodyquery = ""
        for tipoJugada in tipoJugadaNoEncontrada:
            bodyquery = bodyquery + f", ('{tipoJugada}')"
        bodyquery = bodyquery[2:]
        query = f"INSERT INTO dimension_tipo_jugada VALUES {bodyquery};"
        #print(query)
        db.updateQuery(query)
        #BUSCAMOS LOS ID DE LAS FECHAS NO ENCONTRADAS
        bodyquery = ""
        for tipoJugada in tipoJugadaNoEncontrada:
            bodyquery = bodyquery + f" OR nombre_tipo_jugada = '{tipoJugada}'"
        bodyquery = bodyquery[4:]
        query = f"SELECT id_tipo_jugada, nombre_tipo_jugada FROM dimension_tipo_jugada WHERE {bodyquery};"
        #print(query)
        idTipoJugadas = db.selectQuery(query)
        #print(idTipoJugadas)
        #AGREGAMOS LAS FECHAS FALTANTES AL DICCIONARIO
        for tipoJugada in idTipoJugadas:
            aux = str(tipoJugada[1])
            diccionarioTipoJugadas[aux] = tipoJugada[0]
    return diccionarioTipoJugadas

def obtenerDiccionarioEquipos(equipos):
    bodyquery = ""
    for equipo in equipos:
        bodyquery = bodyquery + f" OR nombre = '{equipo}'"
    bodyquery = bodyquery[4:]
    query = f"SELECT id_equipo, nombre FROM dimension_equipo WHERE {bodyquery}"
    #print(query)
    idEquipos = db.selectQuery(query)
    #AGREGAMOS LOS ID AL DICCIONARIO DE FECHAS
    diccionarioEquipos = {}
    for equipo in idEquipos:
        aux = str(equipo[1])
        diccionarioEquipos[aux] = equipo[0]
    
    
    return diccionarioEquipos

def obtenerDiccionarioJugadores(jugadores):
    bodyquery = ""
    for jugador in jugadores:
        bodyquery = bodyquery + f" OR nombre = '{jugador}'"
    bodyquery = bodyquery[4:]
    query = f"SELECT id_jugador, nombre FROM dimension_jugador WHERE {bodyquery}"
    #print(query)
    idJugadores = db.selectQuery(query)
    #AGREGAMOS LOS ID AL DICCIONARIO DE JUGADORES
    diccionarioJugadores = {}
    for jugador in idJugadores:
        aux = str(jugador[1]).upper()
        diccionarioJugadores[aux] = jugador[0]
    
    
    return diccionarioJugadores


def obtenerDiccionarioPosiciones(posiciones):
    bodyquery = ""
    for posicion in posiciones:
        bodyquery = bodyquery + f" OR descripcion = '{posicion}'"
    bodyquery = bodyquery[4:]
    query = f"SELECT id_posicion, descripcion FROM dimension_posicion WHERE {bodyquery}"
    #print(query)
    idPosiciones = db.selectQuery(query)
    #AGREGAMOS LOS ID AL DICCIONARIO DE JUGADORES
    diccionarioPosiciones = {}
    if not idPosiciones:
        print("No hay Posiciones")
    else:
        for posicion in idPosiciones:
            aux = str(posicion[1])
            diccionarioPosiciones[aux] = posicion[0]
    
    return diccionarioPosiciones


def obtenerDiccionarioPartidos(datosPartidos):
    bodyquery = ""
    for datos in datosPartidos:
        
        bodyquery = bodyquery + f" OR id_fecha = {datos[6]}"
    bodyquery = bodyquery[4:]
    query = f"SELECT id_partido, id_fecha FROM tab_hechos_partido WHERE {bodyquery}"
    #print(query)
    idPartidos = db.selectQuery(query)
    #AGREGAMOS LOS ID AL DICCIONARIO DE PARTIDOS
    diccionarioPartidos = {}
    for partidos in idPartidos:
        aux = str(partidos[1])
        diccionarioPartidos[aux] = partidos[0]

    #VERIFICAMOS SI TODAS LOS PARTIDOS ESTAN EN LA BASE

    i = 0
    partidosFaltantes = False
    partidosNoEncontrados = []
    for datos in datosPartidos:
        if str(datos[6]) not in diccionarioPartidos.keys():
            partidosFaltantes = True
            partidosNoEncontrados.append(datos)
        i = i + 1 
    #"TIPO_PARTIDO","FAVOR","CONTRA","LOCAL","VISITA","TEMPORADA","FECHA"
    #INGRESAMOS LOS PARTIDOS QUE NO SE ENCONTRARON
    if partidosFaltantes:
        bodyquery = ""
        for datos in partidosNoEncontrados:
            bodyquery = bodyquery + f", ({datos[0]},{datos[1]},{datos[2]},{datos[3]},{datos[4]},2,{datos[5]},{datos[6]})"
        bodyquery = bodyquery[2:]
        query = f"INSERT INTO tab_hechos_partido VALUES {bodyquery};"
        #print(query)
        db.updateQuery(query)

        #BUSCAMOS LOS ID FALTANTES

        bodyquery = ""
        for datos in partidosNoEncontrados:
            bodyquery = bodyquery + f" OR id_fecha = {datos[6]}"
        
        bodyquery = bodyquery[4:]

        query = f"SELECT id_partido, id_fecha FROM tab_hechos_partido WHERE {bodyquery}"
        #print(query)
        idPartidos = db.selectQuery(query)

        #AGREGAMOS LOS PARTIDOS FALTANTES AL DICCIONARIO
        for partidos in idPartidos:
            aux = str(partidos[1])
            diccionarioPartidos[aux] = partidos[0]
    return diccionarioPartidos


def obtenerDiccionarioTipoMedicion(tipoMedicion):
    bodyquery = ""
    for medicion in tipoMedicion:
        bodyquery = bodyquery + f" OR descripcion = '{medicion}'"
    bodyquery = bodyquery[4:]
    query = f"SELECT id_medicion, descripcion FROM dimension_tipo_medicion WHERE {bodyquery}"
    #print(query)
    idTipoMedicion = db.selectQuery(query)
    #
    diccionarioTipoMedicion = {}
    for medicion in idTipoMedicion:
        aux = str(medicion[1])
        diccionarioTipoMedicion[aux] = medicion[0]
    
    #VERIFICAMOS SI TODAS LAS FECHAS YA ESTAN EN LA BASE
    tipoMedicionFaltante = False
    tipoMedicionNoEncontrada = []
    for medicion in tipoMedicion:
        if medicion not in diccionarioTipoMedicion.keys() and type(medicion) == type(" "):
            
            tipoMedicionFaltante = True
            tipoMedicionNoEncontrada.append(medicion)
    
    #INGRESAMOS LAS FECHAS QUE NO SE ENCONTRARON
    if tipoMedicionFaltante:
        bodyquery = ""
        for medicion in tipoMedicionNoEncontrada:
            bodyquery = bodyquery + f", ('{medicion}','')"
        bodyquery = bodyquery[2:]
        query = f"INSERT INTO dimension_tipo_medicion VALUES {bodyquery};"
        #print(query)
        db.updateQuery(query)
        #BUSCAMOS LOS ID DE LAS FECHAS NO ENCONTRADAS
        bodyquery = ""
        for medicion in tipoMedicionNoEncontrada:
            bodyquery = bodyquery + f" OR descripcion = '{medicion}'"
        bodyquery = bodyquery[4:]
        query = f"SELECT id_medicion, descripcion FROM dimension_tipo_medicion WHERE {bodyquery};"
        #print(query)
        idTipoMedicion = db.selectQuery(query)
        #print(idtipoMedicion)
        #AGREGAMOS LAS FECHAS FALTANTES AL DICCIONARIO
        for medicion in idTipoMedicion:
            aux = str(medicion[1])
            diccionarioTipoMedicion[aux] = medicion[0]
    
    
    return diccionarioTipoMedicion

def obtenerDiccionarioTipoMedicionBiometrica(tipoMedicionBiometrica):
    bodyquery = ""
    for medicion in tipoMedicionBiometrica:
        bodyquery = bodyquery + f" OR descripcion = '{medicion}'"
    bodyquery = bodyquery[4:]
    query = f"SELECT id_medicion_biometrica, descripcion FROM dimension_tipo_medicion_biometrica WHERE {bodyquery}"
    #print(query)
    idTipoMedicionBiomtrica = db.selectQuery(query)
    #
    diccionarioTipoMedicionBiometrica = {}
    for medicion in idTipoMedicionBiomtrica:
        aux = str(medicion[1])
        diccionarioTipoMedicionBiometrica[aux] = medicion[0]
    
    
    return diccionarioTipoMedicionBiometrica

def obtenerDiccionarioPartidosPorFecha(fechas):
    bodyquery = ""
    for fecha in fechas:
        
        bodyquery = bodyquery + f" OR id_fecha = {fecha}"
    bodyquery = bodyquery[4:]
    query = f"SELECT id_partido, id_fecha FROM tab_hechos_partido WHERE {bodyquery}"
    #print(query)
    idPartidos = db.selectQuery(query)
    
    #AGREGAMOS LOS ID AL DICCIONARIO DE PARTIDOS
    diccionarioPartidos = {}
    for partidos in idPartidos:
        aux = str(partidos[1])
        diccionarioPartidos[aux] = partidos[0]
    return diccionarioPartidos

def obtenerDiccionarioTipoEtapa(tipoEtapa):
    bodyquery = ""
    for etapa in tipoEtapa:
        
        bodyquery = bodyquery + f" OR nombre_etapa = '{etapa}'"
    bodyquery = bodyquery[4:]
    query = f"SELECT id_etapa, nombre_etapa FROM dimension_tipo_etapa WHERE {bodyquery}"
    #print(query)
    idTipoEtapa = db.selectQuery(query)
    #print(idTipoEtapa)
    #AGREGAMOS LOS ID AL DICCIONARIO DE PARTIDOS
    diccionarioTipoEtapa = {}
    for etapa in idTipoEtapa:
        aux = str(etapa[1])
        diccionarioTipoEtapa[aux] = etapa[0]
    return diccionarioTipoEtapa