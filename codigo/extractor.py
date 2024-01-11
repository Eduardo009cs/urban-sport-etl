import pandas as pd
import numpy as np
import csv
import os
import diccionarios as d
import dataBase as db

PATH = "../Datos"
JUGADASPATH = "../Evaluaciones/jugadas.csv"
PRODUCTIVIDADPATH = "../Evaluaciones/productividad.csv"
listFileNames = os.listdir(PATH)

def extractorEvaluacionesPartido(pathFile,fileName):

    #Nombre de los archivos: 
    #Juego_Equipo-Local_Equipo-Visitante_Puntos-Local_Puntos-Visitante_Año-mes-dias.xlsx
    datosPartido = fileName.split(".")[0]
    datosPartido = datosPartido.split("_")
    
    equipoLocal = datosPartido[1]
    equipoVisita = datosPartido[2]
    puntosFavor = datosPartido[3]
    puntosContra = datosPartido[4]
    fecha = datosPartido[5]

    df = pd.read_excel(pathFile)
    nombreJugadores = df.columns[6:54]
    columnasEvaluacion = []
    arrayAuxiliar = []
    jugadores = []
    
    i = 1

    for jugador in nombreJugadores:
        arrayAuxiliar.append(jugador)
        if jugador.find("Unnamed") != 0: jugadores.append(jugador.strip())
        if i%4 ==0: 
            columnasEvaluacion.append(arrayAuxiliar)
            arrayAuxiliar = []
        i = i + 1
    #Obtenemos los headers para obtener la informacion
    df = pd.read_excel(pathFile, header=1)
    
    numeroClip = df.columns[1]
    nombreJugada = df.columns[5]
    

    numeroDeClip = np.isnan(df[numeroClip].values)
    numeroDeClip = len(numeroDeClip[~numeroDeClip])
    print(f"Se encontraron {numeroDeClip} jugadas") 
    jugadasTotales = numeroDeClip
    numeroDeClip = df[numeroClip].values[:numeroDeClip]
    
    nombreDeJugada = np.isnan(df[numeroClip].values)
    nombreDeJugada = len(nombreDeJugada[~nombreDeJugada]) 
    nombreDeJugada = df[nombreJugada].values[:nombreDeJugada]

    df = pd.read_excel(pathFile)
    
    for columnaJugador in columnasEvaluacion:
        index = 0
        numeroDeJugadas = pd.to_numeric(df[columnaJugador[0]].values[1:])
        numeroDeJugadas = np.isnan(numeroDeJugadas)
        numeroDeJugadas = len(numeroDeJugadas[~numeroDeJugadas])
        print(f"Se encotraron {numeroDeJugadas} jugadas de {columnaJugador[0]}")
        if numeroDeJugadas != 0:
            for evaluacion in df[columnaJugador].values[1:jugadasTotales+1]:
                if evaluacion[0] == 1 or evaluacion[0]==0:
                    if type(nombreDeJugada[index]) != type(" ") and type(nombreDeJugada[index]) != type(1):
                        nombreJugada = "Sin nombre"
                    else:
                        nombreJugada = nombreDeJugada[index]
                    row = [
                            fecha,
                            equipoLocal,
                            equipoVisita,
                            puntosFavor,
                            puntosContra,
                            columnaJugador[0],
                            evaluacion[0],
                            evaluacion[1],
                            evaluacion[2],
                            evaluacion[3],
                            int(numeroDeClip[index]),
                            nombreJugada,
                            "WR",
                            2, #Temporada
                            1, #TipoEtapa
                            1 #TipoPartido
                        ]
                    with open(JUGADASPATH,'a',newline='') as csvfile:
                        writerCSV = csv.writer(csvfile)
                        writerCSV.writerow(row)
                index = index + 1
        index = 0


def extractorEvaluacionesPracticas(pathFile,fileName):

    datosPartido = fileName.split(".")[0]
    datosPartido = datosPartido.split("_")
    
    equipoLocal = datosPartido[1]
    equipoVisita = datosPartido[2]
    puntosFavor = datosPartido[3]
    puntosContra = datosPartido[4]
    fecha = datosPartido[5]

    df = pd.read_excel(pathFile,header=3)
    
    numeroJugadores = df.columns[0]
    numeroJugadores = df[numeroJugadores].values[:12]

    numeroDeJugadores = 0

    for num in numeroJugadores:
        if type(num) == type(1):
            numeroDeJugadores = numeroDeJugadores + 1
    
    nombreJugadores = df.columns[1]

    print(f"Se encontraron {numeroDeJugadores} jugadores")


    #Columnas de productividad
    tipoProductividad = df.columns[11:]
    productividadJugador = []
    for productividad in tipoProductividad:
        if productividad.find("Unnamed")< 0:
            productividadJugador.append(productividad)
    

    #Columnas de evalucion tecnico-tactica

    tipoEvaluacion = df.columns[3:7]
    #Registro de las evaluaciones Tecnico - Tacticas
    for i in range(numeroDeJugadores):
        print(f"Se encontraron evaluaciones de {df[nombreJugadores].values[i].strip()}")
        [presnap,desarrollo,finish,pride] = df[tipoEvaluacion].values[i]
        if np.isnan(presnap):presnap = 0 
        if np.isnan(desarrollo):desarrollo = 0 
        if np.isnan(finish):finish = 0 
        if np.isnan(pride):pride = 0 
        
        row = [
                fecha,
                equipoLocal,
                equipoVisita,
                puntosFavor,
                puntosContra,
                df[nombreJugadores].values[i].strip(),
                int(presnap),
                int(desarrollo),
                int(finish),
                int(pride),
                0,
                "Sin nombre",
                "WR",
                2, #Temporada
                1, #TipoEtapa
                1 #TipoPartido
            ]
        with open(JUGADASPATH,'a',newline='') as csvfile:
            writerCSV = csv.writer(csvfile)
            writerCSV.writerow(row)

    #Registro de la productividad
#Fecha nombre evaluacion valor posicion
    count = 0
    for i in range(numeroDeJugadores):
        count = 0
        for productividad in productividadJugador:
            if np.isnan(df[productividad].values[i]):
                continue
            row = [
                fecha,
                equipoLocal,
                equipoVisita,
                puntosFavor,
                puntosContra,
                df[nombreJugadores].values[i].strip(),
                productividad.strip(),
                int(df[productividad].values[i]),
                0,
                "Sin nombre",
                "WR",
                2, #Temporada
                1, #TipoEtapa
                1 #TipoPartido
            ]
            count = count + 1
            with open(PRODUCTIVIDADPATH,'a',newline='') as csvfile:
                writerCSV = csv.writer(csvfile)
                writerCSV.writerow(row)
        

def extractorDimensionData(pathFile):
    excelFile = pd.ExcelFile(pathFile)

    hojas = excelFile.sheet_names

    for hoja in hojas:
        df = pd.read_excel(pathFile,sheet_name=hoja)
        bodyquery = ""
        if hoja == "tipo_medicion_biometrica":
            descripcion = df.columns[0]
            unidad = df.columns[1]
            
            for i in range(len(df[descripcion].values)):
                bodyquery = bodyquery + f", ('{df[descripcion].values[i]}','{df[unidad].values[i]}')"
            
        elif hoja == "tiempo":
            fecha = df.columns[0]
            hora = df.columns[1]
            año = df.columns[2]
            mes = df.columns[3]
            dia = df.columns[4]

            for i in range(len(df[fecha].values)):
                date = str(df[fecha].values[i])
                date = date.split("T")[0]
                bodyquery = bodyquery + f", ('{date}','{df[hora].values[i]}',{df[año].values[i]},{df[mes].values[i]},{df[dia].values[i]})"
        elif hoja == "temporada":
            descripcion = df.columns[0]
            
            fechaInico = df.columns[1]
            fechaInico = [str(fecha).split("T")[0] for fecha in df[fechaInico].values]
            
            fechaFinal = df.columns[2]
            fechaFinal = [str(fecha).split("T")[0] for fecha in df[fechaFinal].values]
            fechas = list(set(fechaInico)) + list(set(fechaFinal))
            
            diccionarioFechas = d.obtenerDiccionarioFechas(fechas)
            for i in range(len(df[descripcion].values)):
                bodyquery = bodyquery + f", ('{df[descripcion].values[i]}',{diccionarioFechas[fechaInico[i]]},{diccionarioFechas[fechaFinal[i]]})"
            
        elif hoja == "tipo_sensor":
            marca = df.columns[0]
            marca = df[marca].values
            nombre = df.columns[1]
            nombre = df[nombre].values
            modelo = df.columns[2]
            modelo = df[modelo].values
            for i in range(len(marca)):
                bodyquery = bodyquery + f", ('{marca[i]}','{nombre[i]}','{modelo[i]}')"
        elif hoja == "ubicacion":
            valor = df.columns[0]
            valor = df[valor].values
            latitud = df.columns[1]
            latitud = df[latitud].values
            longitud = df.columns[2]
            longitud = df[longitud].values
            for i in range(len(valor)):
                bodyquery = bodyquery + f", ('{valor[i]}',{latitud[i]},{longitud[i]})"
        elif hoja == "equipo":
            nombre = df.columns[0]
            nombre = df[nombre].values
            nombreExt = df.columns[1]
            nombreExt = df[nombreExt].values
            for i in range(len(nombre)):
                bodyquery = bodyquery + f", ('{nombre[i]}','{nombreExt[i]}')"
        elif hoja == "tipo_etapa":
            etapa = df.columns[0]
            etapa = df[etapa].values
            descripcion = df.columns[1]
            descripcion = df[descripcion].values
            for i in range(len(etapa)):
                bodyquery = bodyquery + f", ('{etapa[i]}','{descripcion[i]}')"
        elif hoja == "tipo_partido":
            descripcion = df.columns[0]
            descripcion = df[descripcion].values
            for i in range(len(descripcion)):
                bodyquery = bodyquery + f", ('{descripcion[i]}')"
        elif hoja == "posicion":
            ofensiva = df.columns[0]
            ofensiva = df[ofensiva].values
            descripcion = df.columns[1]
            descripcion = df[descripcion].values
            descripcionLarga = df.columns[2]
            descripcionLarga = df[descripcionLarga].values
            for i in range(len(ofensiva)):
                bodyquery = bodyquery + f", ({ofensiva[i]},'{descripcion[i]}','{descripcionLarga[i]}')"
        elif hoja == "jugador":
            nombre = df.columns[0]
            nombre = df[nombre].values
            numero = df.columns[1]
            numero = df[numero].values
            talla = df.columns[2]
            talla = df[talla].values
            peso = df.columns[3]
            peso = df[peso].values
            fecha = df.columns[4]
            fecha = [str(fecha).split("T")[0] for fecha in df[fecha].values]
            posicion = df.columns[5]
            posicion = df[posicion].values
            diccionarioPosiciones = d.obtenerDiccionarioPosiciones(posicion)
            for i in range(len(nombre)):
                bodyquery = bodyquery + f", ('{nombre[i]}',{numero[i]},{talla[i]},{peso[i]},'{fecha[i]}',{diccionarioPosiciones[posicion[i]]})"
        elif hoja == "tipo_medicion":
            
            descripcion = df.columns[0]
            descripcion = df[descripcion].values
            descripcionLarga = df.columns[1]
            descripcionLarga = df[descripcionLarga].values
            for i in range(len(descripcion)):
                bodyquery = bodyquery + f", ('{descripcion[i]}','{descripcionLarga[i]}')"
        elif hoja == "tipo_jugada":
            descripcion = df.columns[0]
            descripcion = df[descripcion].values
            for i in range(len(descripcion)):
                bodyquery = bodyquery + f", ('{descripcion[i]}')"
        bodyquery =  bodyquery[2:]
        query = f"INSERT INTO dimension_{hoja} VALUES {bodyquery};"
        db.updateQuery(query)
        print(query)

def extractorHechosData(pathFile):
    excelFile = pd.ExcelFile(pathFile)

    hojas = excelFile.sheet_names

    for hoja in hojas:
        df = pd.read_excel(pathFile,sheet_name=hoja)
        bodyquery = ""
        if hoja == "partido":
            tipoPartido = df.columns[0]
            tipoPartido = df[tipoPartido].values
            favor = df.columns[1]
            favor = df[favor].values
            contra = df.columns[2]
            contra = df[contra].values
            equiposLocal = df.columns[3]
            equiposLocal = df[equiposLocal].values
            equiposVisita = df.columns[4]
            equiposVisita = df[equiposVisita].values
            equipos = list(set(equiposLocal)) + list(set(equiposVisita))
            diccionarioEquipos = d.obtenerDiccionarioEquipos(equipos)
            ubicacion = df.columns[5]
            ubicacion = df[ubicacion].values
            temporada = df.columns[6]
            temporada = df[temporada].values
            fecha = df.columns[7]
            fecha = df[fecha].values
            # for i in range(len(tipoPartido)):
            #     bodyquery = bodyquery + f", ({tipoPartido[i]},{favor[i]},{contra[i]},{diccionarioEquipos[equiposLocal[i]]},{diccionarioEquipos[equiposVisita[i]]},{ubicacion[i]},{temporada[i]},{fecha[i]})"
            
            
        elif hoja == "estadisticas_productividad":
            jugador = df.columns[0]
            jugador = df[jugador].values
            jugadores = list(set(jugador)) 
            tipoMedicion = df.columns[1]
            tipoMedicion = df[tipoMedicion].values
            tiposMedicion = list(set(tipoMedicion)) 
            valor = df.columns[2]
            valor = df[valor].values
            partido = df.columns[3]
            partido = df[partido].values
            posicion = df.columns[4]
            posicion = df[posicion].values
            posiciones = list(set(posicion)) 

            diccionarioJugador = d.obtenerDiccionarioJugadores(jugadores)
            diccionarioTipoMedicion = d.obtenerDiccionarioTipoMedicion(tiposMedicion)
            diccionarioPosicion = d.obtenerDiccionarioPosiciones(posiciones)
            
            # for i in range(len(jugador)):
            #     valorMedicion = str(valor[i]).replace(',','.')
            #     bodyquery = bodyquery + f", ({diccionarioJugador[jugador[i]]},{diccionarioTipoMedicion[tipoMedicion[i]]},{valorMedicion},{partido[i]},{diccionarioPosicion[posicion[i]]})"
        elif hoja == "biometria":
            tipoMedicion = df.columns[0]
            tipoMedicion = df[tipoMedicion].values
            tiposMedicion = list(set(tipoMedicion)) 
            valor = df.columns[1]
            valor = df[valor].values
            sensor = df.columns[2]
            sensor = df[sensor].values
            jugador = df.columns[3]
            jugador = df[jugador].values
            jugadores = list(set(jugador)) 
            fecha = df.columns[4]
            fecha = [str(fecha).split("T")[0] for fecha in df[fecha].values]
            fechas = list(set(fecha)) 

            diccionarioJugador = d.obtenerDiccionarioJugadores(jugadores)
            diccionarioTipoMedicionBiometria = d.obtenerDiccionarioTipoMedicionBiometrica(tiposMedicion)
            diccionarioFechas = d.obtenerDiccionarioFechas(fechas)
            idFechas = []
            for i in range(len(fecha)):
                idFechas.append(diccionarioFechas[fecha[i]])
            idFecha = list(set(idFechas)) 
            diccionarioPartidos = d.obtenerDiccionarioPartidosPorFecha(idFecha)
            print(diccionarioPartidos)
            # for i in range(len(jugador)):
            #     valorMedicion = ""
            #     if tipoMedicion[i].find("Tiempo") >= 0:
            #         horas = str(valor[i]).split(":")[0]
            #         minutos = str(valor[i]).split(":")[1]
            #         segundos = str(valor[i]).split(":")[2]

            #         valorMedicion = float(horas) + float(minutos)/60 + float(segundos)/3600
            #         valorMedicion = str(valorMedicion)[:6]
            #     else:
            #         valorMedicion = str(valor[i]).replace(',','.')
            #     id = str(idFechas[i])
            #     bodyquery = bodyquery + f", ({diccionarioTipoMedicionBiometria[tipoMedicion[i]]},{valorMedicion},{diccionarioPartidos[id]},{sensor[i]},{diccionarioJugador[jugador[i]]})"

                


        elif hoja == "jugada":
            jugador = df.columns[0]
            jugador = df[jugador].values
            jugadores = list(set(jugador)) 
            tipoEtapa = df.columns[1]
            tipoEtapa = df[tipoEtapa].values
            tiposEtapa = list(set(tipoEtapa)) 
            idPartido = df.columns[2]
            idPartido = df[idPartido].values
            numJugada = df.columns[3]
            numJugada = df[numJugada].values
            presnap = df.columns[4]
            presnap = df[presnap].values
            desarrollo = df.columns[5]
            desarrollo = df[desarrollo].values
            finish = df.columns[6]
            finish = df[finish].values
            pride = df.columns[7]
            pride = df[pride].values
            tipoJugada = df.columns[8]
            tipoJugada = [str(tipo) for tipo in df[tipoJugada].values]
            tiposJugada = list(set(tipoJugada)) 
            posicion = df.columns[9]
            posicion = df[posicion].values
            posiciones = list(set(posicion)) 
            print(tiposJugada)
            diccionarioJugador = d.obtenerDiccionarioJugadores(jugadores)
            diccionarioPosicion = d.obtenerDiccionarioPosiciones(posiciones)
            diccionarioTipoEtapa = d.obtenerDiccionarioTipoEtapa(tiposEtapa)
            diccionarioTipoJugada = d.obtenerDiccionarioTipoJugadas(tiposJugada)
            print(diccionarioJugador)
            print(diccionarioPosicion)
            print(diccionarioTipoEtapa)
            print(diccionarioTipoJugada)
            aux = 0
            for i in range(len(jugador)):
                #print(bodyquery)
                if aux == 999:
                    bodyquery =  bodyquery[2:]
                    query = f"INSERT INTO dimension_{hoja} VALUES {bodyquery};"
                    bodyquery = ""
                    aux = 0
                    db.updateQuery(query)
                    print(query)
                bodyquery = bodyquery + f", ({diccionarioTipoEtapa[tipoEtapa[i]]},{idPartido[i]},{numJugada[i]},{presnap[i]},{desarrollo[i]},{finish[i]},{pride[i]},{diccionarioJugador[jugador[i]]},{diccionarioTipoJugada[tipoJugada[i]]},{diccionarioPosicion[posicion[i]]})"
                aux = aux + 1
        bodyquery =  bodyquery[2:]
        if hoja == "jugada":
            query = f"INSERT INTO dimension_{hoja} VALUES {bodyquery};"
        else:
            query = f"INSERT INTO tab_hechos_{hoja} VALUES {bodyquery};"
        print(query)
        db.updateQuery(query)
        
def mainExtraccion():
    for fileName in listFileNames:
        print(f"Leyendo archivo: {fileName}")
        if fileName.find("Dimension") >= 0:
            #extractorDimensionData(PATH + "/" + fileName)
            print("")
        elif fileName.find("Hechos") >= 0:
            #extractorHechosData(PATH + "/" + fileName)
            print("")
        elif fileName.find("Juego") >= 0:
            extractorEvaluacionesPartido(PATH + "/" + fileName,fileName)
        elif fileName.find("Practica") >= 0:
            extractorEvaluacionesPracticas(PATH + "/" + fileName,fileName)
        
            


#mainExtraccion()