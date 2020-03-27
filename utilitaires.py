import math

def cvt(f):
    return str(f).replace('.',',')

def tronk(f):
    if math.isnan(f):
        return f
    else:
        return int(1000*f)/1000


def convertErreur(data):
    for i in range(len(data)):
        data[i][1]=data[i][1]-data[i][0]
    return data

def cleanSeuil(data,seuilDriftP):
    res=[]
    dataR=[]
    for i in range(len(data)):
        if abs(data[i][2])<seuilDriftP:
            res.append(data[i][1]-data[i][0])
            dataR.append([data[i][0],data[i][1]])
    return (res,dataR)