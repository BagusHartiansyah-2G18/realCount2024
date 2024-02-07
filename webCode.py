import pandas as pd
import numpy as np
# https://suarabersama-kthfdus3appndhfq4nodeff.streamlit.app/

# pemilu = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vTwaEzBdh--gpIVE4pBwsbY9JqCHcGPXlH8MTnpz0lwDUG_lZwVP5XhEtYIr3LbEtvZBOy244y826IL/pub?output=csv")
dpemilu = pd.read_csv("./realC1.csv")
def prosesData(pemilu):
    ddesa = []
    ind = 0
    nmDesa = ""
    nmDesax =[]
    for v in pemilu.columns[4:]:
        cekColl = str(v).split(":")
        if(len(cekColl)>1): 
            noCol =int(cekColl[1])
            if(len(ddesa[ind]) == 0):
                ddesa[ind].append({
                    'noCol':noCol-1,
                    'noTps':int(pemilu.values[0][noCol-1])
                }) 
            ddesa[ind].append({
                'noCol':noCol,
                'noTps':int(pemilu.values[0][noCol])
            })
        else:
            ddesa.append([])
            if(len(ddesa) == 0):
                ind =  0
            else:
                ind =  len(ddesa)-1
            nmDesa = str(v)
            nmDesax.append(str(v))


    ddesa = pd.Series(ddesa,index=nmDesax)

    partai = []
    dpartai = pemilu.values[1:]
    nmPartai=[]
    ind = 0
    for i,v in enumerate(dpartai):
        if str(v[0]) != 'nan':
            nmPartai.append(v[1])
            partai.append([])
            if(len(partai[ind])!=0):
                ind+=1
        partai[ind].append({
            'no':v[2],
            'nm':str(v[3]).replace("  ",""),
            'ind':i
        })    


    dhasil = pd.Series(partai,index=nmPartai)
    # print(ddesa)

    for i,v in enumerate(dhasil):
        for v1 in v:
            totSuara = 0
            for i2,v2 in enumerate(ddesa):
                v1[ddesa.index[i2]]=[]
                totDesa = 0
                totalTps = 0
                for v3 in v2:   
                    totTps = 0 if str(dpartai[i][int(v3['noCol'])]) =='nan' else int(dpartai[i][int(v3['noCol'])])
                    if(totTps>0):
                        totalTps+=1

                    totDesa+=totTps
                    v1[ddesa.index[i2]].append({
                        'noTps':v3['noTps'],
                        'tot': totTps
                    })
                totSuara+=totDesa
                v1[ddesa.index[i2]+'Tot'] =totDesa
                v1[ddesa.index[i2]+'TotTps'] =totalTps
            v1['totSuara'] = totSuara
    return dhasil

dt = prosesData(dpemilu)

def gnmPartai():
    return dt.index

def gdtop1():
    dtop1=[]
    for v in dt.index:
        ind = 0
        totSuara = 0
        for i1,v1 in enumerate(dt[v]):
            if(v1['totSuara']>totSuara):
                totSuara = v1['totSuara']
                ind = i1
        dtop1.append({
            'Partai':v,
            'No Urut':dt[v][ind]['no'],
            'Nama Caleg':dt[v][ind]['nm'],
            'Total Suara':dt[v][ind]['totSuara']
        })
    return dtop1

def gcalegPartai(find):
    vcalegPartai = []
    for fv in dt[find]: 
        vcalegPartai.append({
            'No Urut':fv['no'],
            'Nama Caleg':fv['nm'],
            'Total Suara':fv['totSuara']
        })
    return vcalegPartai


# print(dt['Partai Nasdem'])
# print(gcalegPartai(0))
# print( pd.DataFrame(dt[0]).apply(lambda i,x: x[i]['nm']))