import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import csv as csv
import plotly.express as px

# $$ IMPORT DATA $$
data = pd.read_csv("testcal.csv")

def affiche(data):
	print(data)
	plt.plot(data)
	plt.show()
	plt.savefig('image.png')
	plt.close()

affiche(data)

def calcul(data):
	datanumpy = data.to_numpy()
	data0 = datanumpy[:,0]
	data1 = datanumpy[:,1]
	data2 = datanumpy[:,2]
	data3 = datanumpy[:,3]
	derivees1 = [((data1[i+1] - data1[i])/(data0[i+1]-data0[i])) for i in range(len(data1)-1)]
	derivees2 = [(data2[i+1] - data2[i]) for i in range(len(data2)-1)]
	derivees3 = [(data3[i+1] - data3[i]) for i in range(len(data3)-1)]
	derivees1 = np.absolute(derivees1)
	return derivees1

affiche(calcul(data))

#plt.plot(derivees1)
#plt.show()
#plt.savefig('image2.png'); plt.close()
#fig.show()

