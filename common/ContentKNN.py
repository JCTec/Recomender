import heapq
from surprise import AlgoBase
from surprise import PredictionImpossible
from common.Carreras import Carreras
import json
import math
import numpy as np


class ContentKNN(AlgoBase):
    def __init__(self, k=5, sim_options={}):
        AlgoBase.__init__(self)
        self.k = k
    
    def fit(self, trainset):
        AlgoBase.fit(self, trainset)

        data = Carreras()
        habilidades = data.getHabilidades()

        self.similarities = np.zeros((len(self.trainset.index), len(self.trainset.index)))

        for thisRating in range(1,len(self.trainset.index),1):
            if (thisRating % 100 == 0):
                print(thisRating, " of ", len(self.trainset.index))
            for otherRating in range(thisRating+1, len(self.trainset.index),1):
                thisMovieID = int(thisRating)
                otherMovieID = int(otherRating)
                habilidadesSimilarity = self.computeHabilidadesSimilarity(thisMovieID, otherMovieID, habilidades)
                self.similarities[thisRating, otherRating] = habilidadesSimilarity
                self.similarities[otherRating, thisRating] = self.similarities[thisRating, otherRating]
        
        return self.similarities

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

    def calculateSimHabilidades(self, carrera1, u, habilidades, habilidadesDict):
        habilidades1 = habilidades[carrera1]
        habilidades2 = u
        sumxx, sumxy, sumyy = 0, 0, 0
        for habilidad in habilidades2:
            index = habilidadesDict[habilidad]
            x = habilidades1[index]
            y = habilidades2[habilidad]
            if y == 'false':
                y = 0
            else:
                y=1
            sumxx += x * x
            sumyy += y * y
            sumxy += x * y
        
        if sumxx*sumyy == 0:
            return 0
        else:
            return sumxy/math.sqrt(sumxx*sumyy)

    def predict(self, u, limit=3):

        # if not (self.trainset.knows_user(u) and self.trainset.knows_item(i)):
        # raise PredictionImpossible('User and/or item is unkown.')

        # Build up similarity scores between this item and everything the user rated
        neighbors = []
        data = Carreras()
        data.loadCarreras()
        habilidades = data.getHabilidades()
        habilidadesDict = data.getHabiliadesdDict()

        arrayUsuarios = json.loads(u)

        for carrera in range(1, 31, 1):
            userXCarreraSimilarity = self.calculateSimHabilidades(carrera, arrayUsuarios, habilidades, habilidadesDict)
            neighbors.append((userXCarreraSimilarity, carrera))

        # Extract the top-K most-similar ratings
        neighbors.sort(reverse=True)
        k_neighbors = neighbors
        k_neighbors = k_neighbors[:3]
        respuestaJSON = [{'name': data.getCarreraName(item[1]), 'percentage': item[0]} for item in k_neighbors]

        # Compute average sim score of K neighbors weighted by user ratings
        # simTotal = weightedSum = 0
        # for simScore in k_neighbors:
        # if (simScore > 0):
        # simTotal += simScore

        # if (simTotal == 0):
        # raise PredictionImpossible('No neighbors')

        # predictedRating = weightedSum / simTotal

        return respuestaJSON

