import json
import time

import requests as req
from flask import (
    Flask,
    render_template,
    request,
    send_from_directory
)

import graphe
from analyseCalv6 import *
from importParam import *
from mesureKv4 import *
from utilitaires import *

root = "C:/Users/guilhem%20henrion/Desktop/Geek/python/serveur_v0.9/"
p = 57
url = 'https://hooks.slack.com/services/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'
msgK={'text':'Plot K'}
msgCal={'text':'Det Cal'}
# Create the application instance
app = Flask(__name__, template_folder="templates")


# Create a URL route in our application for "/"


@app.route('/')
def home():
    """
    This function just responds to the browser ULR
    localhost:5000/

    :return:        the rendered template 'home.html'
    """

    return render_template('home.html')


@app.route('/uploadCal', methods=['POST'])
def Calibration():
    param = importParam()
    donnees= [["version","operateur","Solution","date","wafer", "puce", "p1", "p2", "p4", "p7", "derive4", "pente", "offset", "r","s1","s2","s4","s7","pente-DC","r-DC"]]
    resultat = []
    for file in request.files.getlist("fichier"):

        if request.form['LN'] == 'US':
            data = pd.read_csv(file, ',')
        else:
            data = pd.read_csv(file, ';')
        datanumpy = data.to_numpy()
        dateMesure = detDate(datanumpy)
        puce = detPuce(datanumpy)
        operateur = detOperateur(datanumpy)
        solution=detSolution(datanumpy)
        wafer=detWafer(datanumpy)
        datanumpy = clean(datanumpy)
        if request.form['LN'] == 'US':
            datanumpy = convertPoint(datanumpy)
        else:
            datanumpy = convertComa(datanumpy)
        data = split5(datanumpy)
        temps = int(data[0][:, 0][1] - (data[0][:, 0][0]))
        for i in range(5):
            date = int(time.time() * 1000000)
            NamePNG1 = str(dateMesure).replace('/', '').replace('-', '') + '-' + puce[i] + '-1-' + str(date)
            NamePNG2 = str(dateMesure).replace('/', '').replace('-', '') + '-' + puce[i] + '-2-' + str(date)
            NamePNG3 = str(dateMesure).replace('/', '').replace('-', '') + '-' + puce[i] + '-3-' + str(date)
            CalDC = detCalDC(data[i], temps, dateMesure, puce[i]+'-DC','plotCal/'+NamePNG1+'.png','plotCal/'+NamePNG2+'.png','plotCal/'+NamePNG3+'.png')
            Cal = detCal(data[i], temps, dateMesure, puce[i]+'-NoDC','plotCal/'+NamePNG1+'NoDC.png','plotCal/'+NamePNG2+'NoDC.png','plotCal/'+NamePNG3+'NoDC.png')
            resultat.append([CalDC,NamePNG1+'.png',NamePNG2+'.png',NamePNG3+'.png'])
            resultat.append([Cal,NamePNG1+'NoDC.png',NamePNG2+'NoDC.png',NamePNG3+'NoDC.png'])
            for j in range(3):
                donnees.append([param.get("version"),operateur,solution,dateMesure, wafer,puce[i]+"-"+str(j+1), cvt(Cal[j].resultat.pot[0]), cvt(Cal[j].resultat.pot[1]), cvt(Cal[j].resultat.pot[2]), cvt(Cal[j].resultat.pot[3]), cvt(CalDC[j].resultat.derive4), cvt(Cal[j].resultat.pente), cvt(Cal[j].resultat.offset), cvt(Cal[j].resultat.r),cvt(CalDC[j].resultat.pot[0]), cvt(CalDC[j].resultat.pot[1]), cvt(CalDC[j].resultat.pot[2]), cvt(CalDC[j].resultat.pot[3]), cvt(CalDC[j].resultat.pente), cvt(CalDC[j].resultat.r)])
    date = int(time.time() * 1000000)
    path = 'uploadCal/' + str(date)
    pathCSV = path + ".csv"
    NameCSV = str(date) + ".csv"
    req.post(url, data=json.dumps(msgCal))
    np.savetxt(pathCSV, donnees, delimiter=";", fmt='%s')
    return render_template('calibration.html', resultat=resultat,filename=NameCSV)

@app.route('/uploadCal/<filename>')
def downloadCal(filename):
    return send_from_directory('uploadCal', filename)

@app.route('/uploadK/<filename>')
def download(filename):
    return send_from_directory('uploadK', filename)

@app.route('/plot/<filename>')
def displayPNG(filename):
    return send_from_directory('plot',filename)

@app.route('/plotCal/<filename>')
def displayCal(filename):
    return send_from_directory('plotCal',filename)

@app.route('/uploadK', methods=['POST'])
def mesurePlasma():
    plasmaList = np.loadtxt('plasma.csv',dtype='str',delimiter= ';')
    param = importParam()
    seuil=float(param.get("SeuilDriftP"))
    result=[]
    pente=float(request.form['pente'])
    donnees = [["version","Operateur","date","test","wafer", "puce","pente","plasmaUsed","potassiumGoldStandard", "potassiumNoDC","potassiumDC","potassiumDC_superCorr", "drift_Etalo","driftPlasma","date Saut"]]
    dataR = []
    dataRSuper=[]
    for file in request.files.getlist("fichier"):
        date = int(time.time() * 1000000)
        path = 'plot/'
        if request.form['LN'] == 'US':
            data = pd.read_csv(file, ',')
        else:
            data = pd.read_csv(file, ';')
        datanumpy = data.to_numpy()
        dateMesure = detDate(datanumpy)
        puce = detPuce(datanumpy)
        NamePNG = str(dateMesure).replace('/','').replace('-','') +'-'+ puce[0] +'-'+ str(date) + '.png'
        plasmaUsed = detPlasmaUsed(datanumpy)
        #@TODO à passer en fonction plus tard
        wafer=datanumpy[3][1]
        operator=datanumpy[2][1]
        test=datanumpy[4][1]
        potassiumGoldStandard = detPotassiumGoldStandard(plasmaUsed,plasmaList)
        datanumpy = cleanK1(datanumpy)
        if request.form['LN'] == 'US':
            datanumpy = convertPoint(datanumpy)
        else:
            datanumpy = convertComa(datanumpy)
        datanumpy = cleanK2(datanumpy)
        mesPNoDC,mesPDC,mesPDCCorr,driftE,driftP,dateSaut = mesure(datanumpy, path+NamePNG, float(param.get("C")),pente)
        result.append([resultatK(dateMesure,puce[0],mesPNoDC,dateSaut),NamePNG])
        dataR.append([float(potassiumGoldStandard.replace(',','.')),mesPDC.K1,driftP.K1])
        dataR.append([float(potassiumGoldStandard.replace(',','.')),mesPDC.K2,driftP.K2])
        dataR.append([float(potassiumGoldStandard.replace(',','.')),mesPDC.K3,driftP.K3])
        dataRSuper.append([float(potassiumGoldStandard.replace(',','.')),mesPDCCorr.K1,driftP.K1])
        dataRSuper.append([float(potassiumGoldStandard.replace(',','.')),mesPDCCorr.K2,driftP.K2])
        dataRSuper.append([float(potassiumGoldStandard.replace(',','.')),mesPDCCorr.K3,driftP.K3])
        donnees.append([param.get("version"),operator,dateMesure,test,wafer, puce[0] + "-1",pente, plasmaUsed, potassiumGoldStandard, str(mesPNoDC.K1).replace('.',','), str(mesPDC.K1).replace('.',','),str(mesPDCCorr.K1).replace('.',','),str(driftE.K1).replace('.',','),str(driftP.K1).replace('.',','),dateSaut.K1])
        donnees.append([param.get("version"),operator,dateMesure,test,wafer, puce[0] + "-2",pente, plasmaUsed, potassiumGoldStandard, str(mesPNoDC.K2).replace('.',','), str(mesPDC.K2).replace('.',','),str(mesPDCCorr.K2).replace('.',','),str(driftE.K2).replace('.',','),str(driftP.K2).replace('.',','),dateSaut.K2])
        donnees.append([param.get("version"),operator,dateMesure,test,wafer, puce[0] + "-3",pente, plasmaUsed, potassiumGoldStandard, str(mesPNoDC.K3).replace('.',','), str(mesPDC.K3).replace('.',','),str(mesPDCCorr.K3).replace('.',','),str(driftE.K3).replace('.',','),str(driftP.K3).replace('.',','),dateSaut.K3])
        print(puce[0])
    date = int(time.time() * 1000000)
    pathCSV = 'uploadK/' + str(date)+'.csv'
    NameCSV=str(date)+".csv"
    dataError,dataR = cleanSeuil(dataR, seuil)
    dataErrorSuper,dataRSuper = cleanSeuil(dataRSuper,seuil)
    print('nb point pris en compte: '+str(len(dataError)))
    print('nb de points pris en compte: '+str(len(dataR)))
    graphe.displayCorr(dataR,'uploadK/'+str(date)+'.png')
    graphe.displayCorr(dataRSuper,'uploadK/'+str(date)+'-Super.png')
    NameGraphe=str(date)+'.png'
    graphe.displayErr(dataError,'uploadK/'+str(date)+'-Error.png')
    graphe.displayErr(dataErrorSuper, 'uploadK/' + str(date) + '-ErrorSuper.png')
    req.post(url,data=json.dumps(msgK))
    np.savetxt(pathCSV, donnees, delimiter=";", fmt='%s')
    return render_template('mesureK.html', result=result,filename=NameCSV,filenamePNG=NamePNG,filenameGraphe=str(date)+'.png',filenameError=str(date)+'-Error.png',filenameGrapheSuper=str(date)+'-Super.png', filenameErrorSuper=str(date)+'-ErrorSuper.png')
# If we're running in stand alone mode, run the application
# to RUN in prod please add host= '0.0.0.0', port=80
if __name__ == '__main__':
    app.run(debug=True)
