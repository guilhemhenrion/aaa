import numpy as np
import pandas as pd
import csv as csv
import plotly.express as px
from collections import Counter
import math
import graphe
import TrouveMax as Tm
from scipy import stats
from utilitaires import *

pente = 60
C = 4
o1 = 5
o2 = 10
o3 = 20

c1 = 0.001
c2 = 0.002
c3 = 0.004
c4 = 0.007

critSaut = 8

concLog = [math.log(c1, 10), math.log(c2, 10), math.log(c3, 10), math.log(c4, 10)]


class resultat:
    def __init__(self, pente, offset, r, pot, derive4):
        self.pente = pente
        self.offset = offset
        self.r = r
        self.pot = pot
        self.derive4 = derive4


class calibration:
    def __init__(self, resultat, date, puce):
        self.resultat = resultat
        self.puce = puce
        self.date = date

    def toString(self):
        return str(self.puce) + 'a ete teste le ' + str(self.date) + '; pente=' + str(
            self.resultat.pente) + ';offset=' + str(self.resultat.offset) + '; r=' + str(
            self.resultat.r) + 'les potentiels retenus sont p1[' + str(self.resultat.pot[0]) + '];p2[' + str(
            self.resultat.pot[1]) + '];p4[' + str(self.resultat.pot[2]) + '];p7[' + str(self.resultat.pot[3]) + ']'


class maxListAll:
    def __init__(self, maxList1, maxList2, maxList3):
        self.maxList1 = maxList1
        self.maxList2 = maxList2
        self.maxList3 = maxList3

    def toString(self):
        return 'p1:' + str(self.maxList1[0]) + 'p2:' + str(self.maxList1[1]) + 'p3:' + str(
            self.maxList1[2]) + 'p4:' + str(self.maxList1[3]) + '////////' + 'p1:' + str(
            self.maxList2[0]) + 'p2:' + str(self.maxList2[1]) + 'p4:' + str(self.maxList2[2]) + 'p7:' + str(
            self.maxList2[3]) + '////////' + 'p1:' + str(self.maxList3[0]) + 'p2:' + str(
            self.maxList3[1]) + 'p4:' + str(self.maxList3[2]) + 'p7:' + str(self.maxList3[3]) + '$$$$$$$$$$$$$$$'


def detPuce(datanumpy):
    # get infos stick
    i = 0
    puce = []
    while i < 5:
        puce.append(datanumpy[1 + i][3])
        i = i + 1
    return puce


def detDate(datanumpy):
    return datanumpy[25][0]


def detOperateur(datanumpy):
    return datanumpy[6][1]


def detSolution(datanumpy):
    return datanumpy[8][1]


def detWafer(datanumpy):
    return datanumpy[7][1]


def clean(datanumpy):
    datanumpy = np.delete(datanumpy, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 0)
    datanumpy = np.delete(datanumpy, [0, 1, 3, 4, 8, 12, 16, 20], 1)
    return datanumpy


def moyenPot3(data, date):
    result = (data[date - 1] + data[date] + data[date + 1]) / 3
    return result


def split5(datanumpy):
    data = []
    data.append(np.delete(datanumpy, [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], 1))
    data.append(np.delete(datanumpy, [1, 2, 3, 7, 8, 9, 10, 11, 12, 13, 14, 15], 1))
    data.append(np.delete(datanumpy, [1, 2, 3, 4, 5, 6, 10, 11, 12, 13, 14, 15], 1))
    data.append(np.delete(datanumpy, [1, 2, 3, 4, 5, 6, 7, 8, 9, 13, 14, 15], 1))
    data.append(np.delete(datanumpy, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 1))
    return data


def detMax(data, time):
    maxList1 = Tm.Raffine2(data[:, 1], critSaut, time)
    #graphe.enregistreCalWSautSimple(data[:,1],maxList1)
    maxList2 = Tm.Raffine2(data[:, 2], critSaut, time)
    maxList3 = Tm.Raffine2(data[:, 3], critSaut, time)
    mxlst = maxListAll(maxList1, maxList2, maxList3)
    return mxlst


def detDerive4(data, time):
    max = Tm.Raffine2(data, critSaut, time)
    derive4 = 60 * (moyenPot3(data, int(max[2] - 25 / time)) - moyenPot3(data, int(max[1] + 25 / time))) / (
                (max[2] - max[1] - 50 / time) * time)
    return tronk(derive4)


def detPotDC(data, time):
    pot = detMax(data, time)
    res1 = [0]
    res2 = [0]
    res3 = [0]
    for j in range(3):
        if len(pot.maxList1) == 4:
            res1.append(tronk(res1[j] + moyenPot3(data[:, 1], int(pot.maxList1[j] + 25 / time)) - moyenPot3(data[:, 1], int(
                pot.maxList1[j] - 25 / time))))
        if len(pot.maxList2) == 4:
            res2.append(tronk(res2[j] + moyenPot3(data[:, 2], int(pot.maxList2[j] + 25 / time)) - moyenPot3(data[:, 2], int(
                pot.maxList2[j] - 25 / time))))
        if len(pot.maxList3) == 4:
            res3.append(tronk(res3[j] + moyenPot3(data[:, 3], int(pot.maxList3[j] + 25 / time)) - moyenPot3(data[:, 3], int(
                pot.maxList3[j] - 25 / time))))
    res = maxListAll(res1, res2, res3)
    return res


def detPot(data, time):
    pot = detMax(data, time)
    for j in range(4):
        if len(pot.maxList1) == 4:
            pot.maxList1[j] = tronk(data[:, 1][int(pot.maxList1[j] - 60 / time)])
        if len(pot.maxList2) == 4:
            pot.maxList2[j] = tronk(data[:, 2][int(pot.maxList2[j] - 60 / time)])
        if len(pot.maxList3) == 4:
            pot.maxList3[j] = tronk(data[:, 3][int(pot.maxList3[j] - 60 / time)])
    return pot


def detCal(data, time, date, puce,path1,path2,path3):
    cali = []
    if len(detPot(data, time).maxList1) == 4:
        slope, intercept, r_value, p_value, std_err = stats.linregress(concLog, detPot(data, time).maxList1)
        cali.append(
            calibration(resultat(tronk(slope), tronk(intercept), tronk(r_value), detPot(data, time).maxList1, detDerive4(data[:, 1], time)),
                        date, puce))
        graphe.enregistreCalWSautSimpleNoDC(data[:, 1], detMax(data, time).maxList1, path1)
    else:
        cali.append(calibration(resultat('NA', 'NA', 'NA', ['NA', 'NA', 'NA', 'NA'], 'NA'), date, puce))
        graphe.enregistreCalWSautSimpleNoDC(data[:, 1], detMax(data, time).maxList1, path1)
    if len(detPot(data, time).maxList2) == 4:
        slope, intercept, r_value, p_value, std_err = stats.linregress(concLog, detPot(data, time).maxList2)
        cali.append(
            calibration(resultat(tronk(slope), tronk(intercept), tronk(r_value), detPot(data, time).maxList2, detDerive4(data[:, 2], time)),
                        date, puce))
        graphe.enregistreCalWSautSimpleNoDC(data[:, 2], detMax(data, time).maxList2, path2)
    else:
        cali.append(calibration(resultat('NA', 'NA', 'NA', ['NA', 'NA', 'NA', 'NA'], 'NA'), date, puce))
        graphe.enregistreCalWSautSimpleNoDC(data[:, 2], detMax(data, time).maxList2, path2)
    if len(detPot(data, time).maxList3) == 4:
        slope, intercept, r_value, p_value, std_err = stats.linregress(concLog, detPot(data, time).maxList3)
        cali.append(
            calibration(resultat(tronk(slope), tronk(intercept), tronk(r_value), detPot(data, time).maxList3, detDerive4(data[:, 3], time)),
                        date, puce))
        graphe.enregistreCalWSautSimpleNoDC(data[:, 3], detMax(data, time).maxList3, path3)
    else:
        cali.append(calibration(resultat('NA', 'NA', 'NA', ['NA', 'NA', 'NA', 'NA'], 'NA'), date, puce))
        graphe.enregistreCalWSautSimpleNoDC(data[:, 3], detMax(data, time).maxList3, path3)
    return cali


def detCalDC(data, time, date, puce,path1,path2,path3):
    cali = []
    if len(detPotDC(data, time).maxList1) == 4:
        slope, intercept, r_value, p_value, std_err = stats.linregress(concLog, detPotDC(data, time).maxList1)
        cali.append(calibration(
            resultat(tronk(slope), tronk(intercept), tronk(r_value), detPotDC(data, time).maxList1, detDerive4(data[:, 1], time)), date,
            puce))
        graphe.enregistreCalWSautSimpleDC(data[:,1],detMax(data,time).maxList1,path1)
    else:
        cali.append(calibration(resultat('NA', 'NA', 'NA', ['NA', 'NA', 'NA', 'NA'], 'NA'), date, puce))
        graphe.enregistreCalWSautSimpleDC(data[:, 1], detMax(data, time).maxList1,path1)
    if len(detPotDC(data, time).maxList2) == 4:
        slope, intercept, r_value, p_value, std_err = stats.linregress(concLog, detPotDC(data, time).maxList2)
        cali.append(calibration(
            resultat(tronk(slope), tronk(intercept), tronk(r_value), detPotDC(data, time).maxList2, detDerive4(data[:, 2], time)), date,
            puce))
        graphe.enregistreCalWSautSimpleDC(data[:, 2], detMax(data, time).maxList2,path2)
    else:
        cali.append(calibration(resultat('NA', 'NA', 'NA', ['NA', 'NA', 'NA', 'NA'], 'NA'), date, puce))
        graphe.enregistreCalWSautSimpleDC(data[:, 2], detMax(data, time).maxList2,path2)
    if len(detPotDC(data, time).maxList3) == 4:
        slope, intercept, r_value, p_value, std_err = stats.linregress(concLog, detPotDC(data, time).maxList3)
        cali.append(calibration(
            resultat(tronk(slope), tronk(intercept), tronk(r_value), detPotDC(data, time).maxList3, detDerive4(data[:, 3], time)), date,
            puce))
        graphe.enregistreCalWSautSimpleDC(data[:, 3], detMax(data, time).maxList3,path3)
    else:
        cali.append(calibration(resultat('NA', 'NA', 'NA', ['NA', 'NA', 'NA', 'NA'], 'NA'), date, puce))
        graphe.enregistreCalWSautSimpleDC(data[:, 3], detMax(data, time).maxList3,path3)
    return cali
