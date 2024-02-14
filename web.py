
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
# E:\developr\phyton\bgsH\pemuli

dpemilu = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vTwaEzBdh--gpIVE4pBwsbY9JqCHcGPXlH8MTnpz0lwDUG_lZwVP5XhEtYIr3LbEtvZBOy244y826IL/pub?output=csv")
# dpemilu = pd.read_csv("./realC1.csv")

def getDesa(pemilu):
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


    return pd.Series(ddesa,index=nmDesax)

def prosesData(pemilu,ddesa):
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
    for i,v in enumerate(dhasil):
        for i1,v1 in enumerate(v):  # daftar Caleg
            totSuara = 0
            for i2,v2 in enumerate(ddesa):
                v1[ddesa.index[i2]]=[]
                totDesa = 0
                totalTps = 0 
                for v3 in v2:   
                    totTps = 0 if str(dpartai[int(v1['ind'])][int(v3['noCol'])]) =='nan' else int(dpartai[int(v1['ind'])][int(v3['noCol'])])
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
    return dhasil #pd.DataFrame(dhasil[0])[['no','nm','totSuara']]

ddesa=getDesa(dpemilu)
dt = prosesData(dpemilu, ddesa)

# print(dt[0][10])
# print(pd.DataFrame(dt[0])[['totSuara','TaliwangTot','KertasariTot','DasanTot' ]])

dpartai = []
dtop1=[]
dsuaraPartai=[]
for v in dt.index:
    ind = 0
    totPartai = 0
    totSuara = 0
    for i1,v1 in enumerate(dt[v]):
        if(v1['totSuara']>totSuara):
            totSuara = v1['totSuara']
            ind = i1
        totPartai+=v1['totSuara']
        if(str(v1['nm']).lower().replace(" ","")=="suarapartai"):
            dsuaraPartai.append({
                'Partai':v,
                'Total Suara':v1['totSuara']
            })

    dtop1.append({
        'Partai':v,
        'No Urut':dt[v][ind]['no'],
        'Nama Caleg':dt[v][ind]['nm'],
        'Total Suara':dt[v][ind]['totSuara']
    })
    dpartai.append({
        'partai':v,
        'total':totPartai
    })

import streamlit as st
st.set_page_config(page_title="Real Count", layout="wide")
with st.sidebar:    
    st.markdown("<h1 style='text-align: center; color: black;'>2G18 Hartiansyah</h1>", unsafe_allow_html=True)
    st.image("https://avatars.githubusercontent.com/u/53298436?s=400&u=91201d3b54610cdcd1840515f24c3827f4d9ba00&v=4")
    st.markdown("<h1 style='text-align: center; color: dark-blue;'>Perhitungan Suara<br> Caleg 2024</h1>", unsafe_allow_html=True)


if 'viewTabel' not in st.session_state:
    st.session_state['viewTabel'] = 0
if 'selPartai' not in st.session_state: 
    st.session_state['selPartai'] = 0
if 'selCaleg' not in st.session_state: 
    st.session_state['selCaleg'] = 0
if 'selDesa' not in st.session_state: 
    st.session_state['selDesa'] = ddesa.index[0]


def changePartai():
    st.session_state.viewTabel = 1
    st.session_state.selPartai = st.session_state['partai']

vcalegPartai = dt[st.session_state.selPartai]
vcaleg = pd.DataFrame(dt[st.session_state.selPartai])[['nm']]



def getDaftarTotalDesa():
    fresp = []
    fdt = dt[st.session_state.selPartai][st.session_state.selCaleg]
    for v1 in ddesa.index:
        fresp.append({
            'desa':v1,
            'total':fdt[str(v1)+'Tot']
        })
    return fresp

def getDaftarTpsTotalDesa():  
    return pd.DataFrame(dt[st.session_state.selPartai][st.session_state.selCaleg][st.session_state.selDesa])[['noTps','tot']]
     


vdesa = getDaftarTotalDesa()
vtps = getDaftarTpsTotalDesa()


if st.session_state.viewTabel ==1:
    vcalegPartai =  dt[st.session_state.selPartai]
    vcaleg =  pd.DataFrame(dt[st.session_state.selPartai])[['nm']]

def changeCaleg():
    for i,v in enumerate(dt[st.session_state.selPartai]):
        if(v['nm'] ==st.session_state['caleg']):
            st.session_state.selCaleg =i
            break


def changeDesa():
    st.session_state.selDesa = st.session_state.desa


# 1. manampilkan suara caleg tertinggi berdasarkan partainya
style ="""
    <style>
        .container1{
            border: 2px solid gray; 
        }
    </style>
"""
st.markdown(style, unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='container1'></div>", unsafe_allow_html=True)
    st.header(':sparkles:. Total Suara di Partai')  

    dgroup = pd.DataFrame(dpartai).groupby(by="partai").agg({
        'total':'sum'
    })['total'].sort_values(ascending=False)
    col11, col22 = st.columns(2)
    with col11:
        tvCalegPartai =st.table(dgroup) 
    with col22:
        st.bar_chart(dgroup)

with st.container():
    st.markdown("<div class='container1'></div>", unsafe_allow_html=True)
    st.header(':sparkles:. Suara Partai, (bukan caleg)')  
    st.table(dsuaraPartai) 


container1 = st.container()
container1.markdown("<div class='container1'>", unsafe_allow_html=True)
with container1:
    st.header(':sparkles:. Daftar Suara Tertinggi Perwakilan Partai ')
    st.dataframe(dtop1,use_container_width=True)
    container1.markdown("</div>", unsafe_allow_html=True)

# 2. menampilkan daftar suara setiap caleg berdasarkan partainya 

with st.container():
    st.markdown("<div class='container1'></div>", unsafe_allow_html=True)
    st.header(':sparkles:. Daftar Caleg Berdasarkan Partai')   
    sdesa = st.selectbox("Pilih Opsi ", options=dt.index, key="partai",on_change=changePartai)
    col11, col22 = st.columns(2)
    with col11:
        tvCalegPartai =st.table(pd.DataFrame(vcalegPartai)[['no','nm','totSuara']]) 
    with col22:
        st.bar_chart(pd.DataFrame(vcalegPartai)[['nm','totSuara']].groupby(by="nm").agg({
            'totSuara':'sum'
        }))
        # print("")
        

# 3. menampilkan detail suara untuk setiap desanya 
with st.container():
    st.markdown("<div class='container1'></div>", unsafe_allow_html=True)
    st.header(':sparkles:. Daftar Suara dari Desa / Kelurahan Berdasarkan Nama Caleg')   
    sdesa = st.selectbox("Pilih Opsi Caleg", options=vcaleg, key="caleg",on_change=changeCaleg)
    col11, col22 = st.columns(2)
    with col11:
        tvCalegPartai =st.table(pd.DataFrame(vdesa)) 
    with col22:
        st.bar_chart(pd.DataFrame(vdesa).groupby(by="desa").agg({
            'total':'sum'
        }))
        # print("")

# 4. menampilkan total setiap Tps dari setiap desa untuk tiap caleg
with st.container():
    st.markdown("<div class='container1'></div>", unsafe_allow_html=True)
    st.header(':sparkles:. total suara tiap TPS dari setiap Desa / Kelurahan Berdasarkan Nama Caleg')   
    sdesa = st.selectbox("Pilih Opsi Desa", options=pd.DataFrame(vdesa)['desa'], key="desa",on_change=changeDesa)
    
    list =st.columns(4)
    for v in range(int(len(vtps.values)/4)-1):
        list += st.columns(4)
    
    sisa =( len(vtps.values)%4)
    if(sisa>0):
        list += st.columns(sisa)

    for i,col in enumerate(list):
        col.metric("TPS "+str(vtps.values[i][0]),vtps.values[i][1])
