import pandas as pd
import json
import urllib3
import requests 
import numpy as np

# header = {
#     "accept": "*/*",
#     "accept-language": "en-US,en;q=0.9",
#     "content-type": "application/json",
#     "if-none-match": "W/\"36ec-bgt7Mf4A+Wodquvw8MDDs4d9JLI\"",
#     "sec-ch-ua": "\"Not A(Brand\";v=\"99\", \"Microsoft Edge\";v=\"121\", \"Chromium\";v=\"121\"",
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": "\"Windows\"",
#     "sec-fetch-dest": "empty",
#     "sec-fetch-mode": "cors",
#     "sec-fetch-site": "same-origin",
#     "referrer": "https://goodkind.id/pemilu/Kabupaten/Sumbawa-Barat-1?city=kabupaten-sumbawa-barat&page=1",
#     "referrerPolicy": "strict-origin-when-cross-origin",
    
#     "mode": "cors",
#     "credentials": "include"
# }
# dt= requests.get(
#     "https://goodkind.id/api/search/calegs?dapilIDs=ba3162cf-b0fb-40a9-90f1-be59c2866ae4&titles=Kabupaten&page=1&size=123&sortDirection=DESC", 
#     headers=header,
#     data="",
#     verify=False
# ).json()
# with open('dataD1.json', 'w') as f:
#     json.dump(dt, f)

f = open('dataD1.json')

dt = json.load(f)

# {'HANURA', 'PERINDO', 'PKB', 'PBB', 'PAN', 'UMMAT', 'GOLKAR', 'GELORA', 
# 'DEMOKRAT', 'NASDEM', 'PDIP', 'GERINDRA', 'PKS', 'PPP'}
# partai = set()
partai = {
    "nama":[],
    "no":[]
}
for v in dt['data']:
    if(v['party']['code']=="UMMAT"):
        partai['nama'].append(v['name'])
        partai['no'].append(int(v['noKpu'][3:]))
# print(partai[0])
no = pd.Series(partai['no'],index=partai['nama'])
print(no.sort_values(ascending=True))

# dt['data'][0]['party']['code'] 