import os
import csv
import sys
import re
import numpy as np
import pandas as pd
from surprise import Dataset
from surprise import Reader
from common.flatten import flatten
from collections import defaultdict


class Carreras:
    carreras_path = 'common/CarrerasFull.csv'
    carrera_id_to_name = {}
    carrera_name_to_carrera_id = {}
    habDict = {} 

    def loadCarreras(self):
        self.carrera_id_to_name = {}
        self.carrera_name_to_carrera_id = {}

        with open(self.carreras_path, newline='', encoding='utf8') as csvfile:
                carrerasReader = csv.reader(csvfile)
                next(carrerasReader)  #Skip header line
                for row in carrerasReader:
                    carreraID = int(row[0])
                    carreraName = row[1]
                    self.carrera_id_to_name[carreraID] = carreraName
                    self.carrera_name_to_carrera_id[carreraName] = carreraID

    def getDataset(self):
        df = pd.read_csv(self.carreras_path)
        habilidades = flatten(df['habilidades'].to_numpy())
        del df['habilidades']
        df  = pd.concat([df, habilidades], axis=1, join='inner')
        #df.to_html("out.html")
        return df
           
    def getHabilidades(self):
        habilidades = defaultdict(list)
        habilidadesIDs = {}
        maxHabilidadesID = 0
        with open(self.carreras_path, newline='', encoding='utf8') as csvfile:
            carrerasReader = csv.reader(csvfile)
            next(carrerasReader)  #Skip header line
            for row in carrerasReader:
                carreraID = int(row[0])
                habilidadesList = row[2].split(' - ')
                habilidadesIDList = []
                for habilidad in habilidadesList:
                    if habilidad in habilidadesIDs:
                        habilidadID = habilidadesIDs[habilidad]
                    else:
                        habilidadID = maxHabilidadesID
                        self.habDict[habilidad] = habilidadID
                        habilidadesIDs[habilidad] = habilidadID
                        maxHabilidadesID += 1
                    habilidadesIDList.append(habilidadID)
                habilidades[carreraID] = habilidadesIDList
        # Convert integer-encoded genre lists to bitfields that we can treat as vectors
        #print("HOLA POR DIOS")
        #print(habilidades)
        for (carreraID, habilidadesIDList) in habilidades.items():
            bitfield = [0] * maxHabilidadesID
            for habilidadID in habilidadesIDList:
                bitfield[habilidadID] = 1
            habilidades[carreraID] = bitfield            
        
        return habilidades

    def getCarreraName(self, carreraID):
        if carreraID in self.carrera_id_to_name:
            return self.carrera_id_to_name[carreraID]
        else:
            return ""

    def getHabilidadID(self, habilidad):
        return self.habDict[habilidad]
      
    def getHabiliadesdDict(self):
        return self.habDict

    def getCarreraID(self, carreraName):
        if carreraName in self.carrera_name_to_carrera_id:
            return self.carrera_name_to_carrera_id[carreraName]
        else:
            return 0
