import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import csv as csv
import plotly.express as px
from collections import Counter
import math
import graphe


def Split(data,time):
	return np.array_split(data,int(len(data)*time/90))

def TrouveMaxSplit(data,time):
	data = np.array_split(data,int(len(data)*time/90))
	maxList =[]
	for i in range(len(data)):
		a=0
		for j in range(i):
			a = a + len(data[j])
		maxList.append(np.argmax(data[i])+a)
	return maxList	

def Raffine(maxList,data,critSaut,time):
#rafine en enlevant la premiere et derniere valeurs
	print(maxList)
	del maxList[len(maxList)-1]
	del maxList[0]
	print(maxList)
#rafine maxList en eliminant les valeurs doubles
	maxList = [maxList[x] for x in range(len(maxList)-1) if maxList[x]!=maxList[x+1]]
#rafine si c'est des sauts ou pas
	maxList = [maxList[x] for x in range(len(maxList)) if abs(data[maxList[x]-5]-data[maxList[x]+5])>critSaut]
#attention a tester ici si il a 4 elements ds maxList
	print(maxList)
	if len(maxList) == 4:
		return maxList

def Raffine2(data,critSaut,time):
	maxList =[]
	i=1
	while i<(len(data)-7):
		if abs(data[i+1]-data[i+3])>critSaut and abs(data[i-1]-data[i+5])>critSaut:
			maxList.append(i+2)
			i=i+6
		else:
			i=i+1
	return maxList
