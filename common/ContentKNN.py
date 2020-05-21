from surprise import AlgoBase
from surprise import PredictionImpossible
from sklearn.linear_model import LogisticRegression
from Carreras import Carreras
import pandas as pd
import json
import math
import numpy as np
import heapq

class ContentKNN(AlgoBase):
    def __init__(self, k=5, sim_options={}):
        AlgoBase.__init__(self)
        self.k = k
    
    def fit(self, trainset):
        AlgoBase.fit(self,trainset)

        #Modelo de regresion Logit
        datax = Carreras()
        datax.loadCarreras()
        habilidades = datax.getHabilidades()

        train_df = pd.DataFrame(columns=datax.getHabilidadesList())
        train_labels = []

        for data in trainset:
            train_df = train_df.append(data[0], ignore_index=True)
            train_labels.append(datax.getCarreraID(data[1]))

        #train_df.to_html('prueba.html')
        train_df = train_df.dropna(axis=1)

        print(train_df.shape)

        self.model = LogisticRegression(multi_class='multinomial',solver='newton-cg')
        self.model.fit(train_df,train_labels)
        

    def computeHabilidadesSimilarity(self, carrera1, carrera2, habilidades):
        habilidades1 = habilidades[carrera1]
        habilidades2 = habilidades[carrera2]
        sumxx, sumxy, sumyy = 0, 0, 0
        for i in range(len(habilidades1)):
            x = habilidades1[i]
            y = habilidades2[i]
            sumxx += x * x
            sumyy += y * y
            sumxy += x * y
        
        return sumxy/math.sqrt(sumxx*sumyy)

    def calculateSimHabilidades(self, carrera1, u, habilidades,habilidadesDict):
        habilidades1 = habilidades[carrera1]
        habilidades2 = u
        sumxx, sumxy, sumyy = 0, 0, 0
        for habilidad in habilidades2:
            index = habilidadesDict[habilidad]
            x = habilidades1[index]
            y = 1 if habilidades2[habilidad] else 0

            sumxx += x * x
            sumyy += y * y
            sumxy += x * y
        
        if sumxx*sumyy == 0:
            return 0
        else:
            return sumxy/math.sqrt(sumxx*sumyy)

    def predict(self, array_usuarios, limit=3):
        neighbors = []
        data = Carreras()
        data.loadCarreras()
        habilidades = data.getHabilidades()
        habilidades_dict = data.getHabiliadesdDict()
        valuesToPredict = []
        print(array_usuarios)
        for habilidad in habilidades_dict:
            if (habilidad in array_usuarios) and array_usuarios[habilidad]:
                valuesToPredict.append(1)
            else:
                valuesToPredict.append(0)
        # valuesToPredict = valuesToPredict[:len(valuesToPredict)-14]
        # valuesToPredict = np.array(valuesToPredict).reshape(1,22)
        valuesToPredict = np.array(valuesToPredict).reshape(1,len(list(habilidades_dict.keys())))
        print(valuesToPredict.shape)

        #print(self.model.predict_proba(valuesToPredict))
        #print("Carrera recomendada por LOGIT model: " + data.getCarreraName(self.model.predict(valuesToPredict)[0]))

        for carrera in range(1, len(habilidades) + 1):
            user_x_carrera_similarity = self.calculateSimHabilidades(carrera,
                                                                    array_usuarios,
                                                                    habilidades,
                                                                    habilidades_dict)
            neighbors.append((user_x_carrera_similarity, carrera))

        neighbors.sort(reverse=True)
        k_neighbors = neighbors
        k_neighbors = k_neighbors[:int(limit)]

        predictedByLogit = self.model.predict(valuesToPredict)[0]
        probabilities = self.model.predict_proba(valuesToPredict)
        probabilities = probabilities.tolist()
        probabilities.sort(reverse=True)

        #print(predictedByLogit)
        #print(probabilities[0][0])
        copia_k_neighbors = []

        # for i in range(len(k_neighbors)):
        #     if k_neighbors[i][1] == predictedByLogit:
        #         copia_k_neighbors[i][0] = k_neighbors[i][0] + (k_neighbors[i][0] + probabilities[0][0])/3


        return [{'name': data.getCarreraName(item[1]), 'percentage': item[0]} for item in k_neighbors]