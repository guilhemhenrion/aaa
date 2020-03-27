import numpy as np
import pandas as pd
import csv as csv
import plotly.express as px
from collections import Counter
import math
import graphe
import number


class K:
    def __init__(self, K1, K2, K3):
        self.K1 = K1
        self.K2 = K2
        self.K3 = K3

class resultatK:
    def __init__(self,date,puce,pota,dateSaut):
        self.date=date
        self.puce=puce
        self.pota=pota
        self.dateSaut=dateSaut

class pente:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3


def moyenPot1(data, date):
    return data[date]


def moyenPot3(data, date):
    result = (data[date - 1] + data[date] + data[date + 1]) / 3
    return result


def moyenPot5(data, date):
    result = (data[date - 2] + data[date - 1] + data[date] +
              data[date + 1] + data[date + 2]) / 5
    return result


def convertComa(datanumpy):
    for i in range(len(datanumpy)):
        for j in range(len(datanumpy[i])):
            datanumpy[i][j] = number.parseNumber(datanumpy[i][j])
    datanumpy = datanumpy.astype(np.float)
    return datanumpy


def convertPoint(datanumpy):
    datanumpy = datanumpy.astype(np.float)
    return datanumpy


def findLastAbove(data, threshold):
    res = 0
    for i in range(len(data)):
        if data[i] > threshold + 200 or data[i] < threshold - 200:
            res = i
    return res

def detPlasmaUsed(datanumpy):
    return datanumpy[1][5]

def detPotassiumGoldStandard(plasmaUsed, plasmaList):
    plasmaUsed = plasmaUsed.replace('-','')
    potassiumGoldStandard = None
    for i in range(len(plasmaList)):
        if plasmaList[i][0]==plasmaUsed:
            potassiumGoldStandard=plasmaList[i][1]
    return potassiumGoldStandard


def cleanK1(datanumpy):
    datanumpy = np.delete(datanumpy, [0, 1, 2, 3, 4, 5], 0)
    datanumpy = np.delete(datanumpy, [0, 1, 3, 4], 1)
    return datanumpy

def cleanK2(datanumpy):
    index = findLastAbove(datanumpy[:, 1], 200)
    for i in range(index + 10):
        datanumpy = np.delete(datanumpy, [0], 0)
    return datanumpy

def dateSaut(data):
    derivees = [(data[i + 1] - data[i]) for i in range(len(data) - 1)]
    return np.argmax(np.absolute(derivees))

def mesureKNoDC(data,C,p):
    pota = C * 10 ** ((moyenPot3(data, int(dateSaut(data) - 5)) - moyenPot3(data, int(dateSaut(data) + 40))) / p)
    return pota

def detDriftEtalo(data):
    return (moyenPot3(data,int(dateSaut(data)+45))-moyenPot3(data,int(dateSaut(data)+35)))*6

def detDriftPlasma(data):
    return (moyenPot3(data,int(dateSaut(data)-5))-moyenPot3(data,int(dateSaut(data)-15)))*6

def mesureKDC(data,C,p):
    return C * 10 ** (((moyenPot3(data, int(dateSaut(data) - 5))) - (moyenPot3(data, int(dateSaut(data) + 40))-detDriftEtalo(data)*40/60)) / p)

def mesureKDCcorrected(data,C,p):
    return C * 10 ** ((((moyenPot3(data, int(dateSaut(data) - 5))) - (moyenPot3(data, int(dateSaut(data) + 40))-detDriftEtalo(data)*40/60))+4.7+1.3*detInversionDerive(data)) / p)

def detInversionDerive(data):
    return detDriftPlasma(data)-detDriftEtalo(data)

def mesure(datanumpy, path,C,p):
    # $$ SPLIT DATA 3 VOIES $$
    # $$ Le t=0 sec doit etre la premiere ligne du data input, et le delataT entre chaque points doit etre de 1 sec, je prends l'index automatique du dataFrame comme axe des temps
    data1 = datanumpy[:, 1]
    data2 = datanumpy[:, 2]
    data3 = datanumpy[:, 3]
    graphe.enregistreWSautCombine(data1, data2, data3,path,dateSaut(data1))
    driftEtalo=K(detDriftEtalo(data1),detDriftEtalo(data2),detDriftEtalo(data3))
    driftPlasma = K(detDriftPlasma(data1),detDriftPlasma(data2),detDriftPlasma(data3))
    potaNoDC = K(mesureKNoDC(data1,C, p ), mesureKNoDC(data2, C, p), mesureKNoDC(data3, C, p))
    potaDC = K(mesureKDC(data1,C,p),mesureKDC(data2,C,p),mesureKDC(data3,C,p))
    potaDCcor = K(mesureKDCcorrected(data1,C,p),mesureKDCcorrected(data2,C,p),mesureKDCcorrected(data3,C,p))
    date_saut = K(dateSaut(data1), dateSaut(data2), dateSaut(data3))
    return (potaNoDC, potaDC,potaDCcor,driftEtalo,driftPlasma,date_saut)
