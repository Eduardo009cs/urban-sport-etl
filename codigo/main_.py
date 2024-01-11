import extractor
import csv
import load
JUGADASPATH = "../Evaluaciones/jugadas.csv"
PRODUCTIVIDADPATH = "../Evaluaciones/productividad.csv"
row = [
        "FECHA",
        "LOCAL",
        "VISITA",
        "FAVOR",
        "CONTRA",
        "NOMBRE",
        "PRESNAP",
        "DESARROLLO",
        "FINISH",
        "PRIDE",
        "NUM_JUGADA",
        "TIPO_JUGADA",
        "POSICION",
        "TEMPORADA",
        "TIPO_ETAPA",
        "TIPO_PARTIDO"
        ]
with open(JUGADASPATH,'w',newline='') as csvfile:
    writerCSV = csv.writer(csvfile)
    writerCSV.writerow(row)
row = [
        "FECHA",
        "LOCAL",
        "VISITA",
        "FAVOR",
        "CONTRA",
        "NOMBRE",
        "TIPO_EVALUACION",
        "EVALUACION",
        "NUM_JUGADA",
        "TIPO_JUGADA",
        "POSICION",
        "TEMPORADA",
        "TIPO_ETAPA",
        "TIPO_PARTIDO"
        ]
with open(PRODUCTIVIDADPATH,'w',newline='') as csvfile:
    writerCSV = csv.writer(csvfile)
    writerCSV.writerow(row)
extractor.mainExtraccion()
load.mainCarga()
#Validar si se puede saber si hay repetidos por dos columnas para asi hacer los registro de los partidos 