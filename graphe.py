import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import math
import csv as csv
import plotly.express as px
from scipy import stats
from utilitaires import *


def affiche(data1,data2):
	plt.plot(data1,data2)
	plt.show()
	plt.close()

def displayErr(data,path):
	datanumpy = np.array(data)
	x_min=np.min(datanumpy)
	x_max=np.max(datanumpy)
	std = int(1000*datanumpy.std())/1000
	mean=int(1000*datanumpy.mean())/1000
	plt.hist(data,bins=20)
	s1='std. dev. = ' + str(std)
	s2='mean = '+str(mean)
	x = np.linspace(x_min, x_max, 100)
	y = stats.norm.pdf(x, mean, std)
	#plt.plot(x, y, color='coral')
	plt.text((x_min+x_max)/2,0.2,s1)
	plt.text((x_min+x_max)/2,0.8,s2)
	plt.savefig(path)
	plt.close()


def displayCorr(data,path):
	data1=[]
	data2=[]
	for i in range(len(data)):
		data1.append(data[i][0])
		data2.append(data[i][1])
	slope, intercept, r_value, p_value, std_err = stats.linregress(data1,data2)
	x = np.linspace(2, 8, 500)
	y1 = slope * x + intercept
	y2=x
	plt.plot(x, y1, '-r')
	plt.plot(x,y2,'--')
	plt.scatter(data1,data2)
	s1='R² = ' + str(round(r_value*r_value,4))
	s2='y = '+str(round(slope,3))+'*x + '+str(round(intercept,3))
	plt.text(3,7,s1)
	plt.text(3,6.5,s2)
	plt.xlim(2,8)
	plt.ylim(2,8)
	plt.xlabel('Mesure iStat')
	plt.ylabel('mesure CR')
	plt.savefig(path)
	plt.close()


def afficheSimple(data1,x1,x2,x3,x4):
	plt.plot(data1)
	plt.axvline(x=x1)
	plt.axvline(x=x2)
	plt.axvline(x=x3)
	plt.axvline(x=x4)
	plt.axvline(x=x1+5, color = 'red')
	plt.axvline(x=x1-5, color='green')
	plt.show()
	plt.close()

def enregistre(data,path):
	plt.plot(data)
	plt.savefig(path)
	plt.close()

def enregistreWSaut(data,path,saut):
	plt.plot(data)
	plt.axvline(x=saut,linestyle='--',color='r')
	plt.axvline(x=saut+40, linestyle='--',color='g')
	plt.axvline(x=saut-5,linestyle='--',color='b')
	plt.savefig(path)
	plt.close()

def enregistreWSautCombine(data1,data2,data3,path,saut):
	plt.plot(data1)
	plt.plot(data2)
	plt.plot(data3)
	plt.axvline(x=saut,linestyle='--',color='r')
	plt.axvline(x=saut+40, linestyle='--',color='g')
	plt.axvline(x=saut-5,linestyle='--',color='b')
	plt.savefig(path)
	plt.close()

def enregistreCalWSautSimpleDC(data,s,path):
	plt.plot(data)
	for i in range(len(s)):
		plt.axvline(x=s[i],linestyle='--',color='r')
		plt.axvline(x=s[i] + 5, linestyle='--', color='g')
		plt.axvline(x=s[i] - 5, linestyle='--', color='b')
	plt.savefig(path)
	plt.close()

def enregistreCalWSautSimpleNoDC(data,s,path):
	plt.plot(data)
	for i in range(len(s)):
		plt.axvline(x=s[i],linestyle='--',color='r')
		plt.axvline(x=s[i] - 12, linestyle='--', color='b')
	plt.savefig(path)
	plt.close()