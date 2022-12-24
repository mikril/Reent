import requests
import json
import  csv
import datetime
from time import sleep
import pandas as pd
import numpy as np
sum=0
df={"name":[],"salary_from":[],"salary_to":[],"currency":[],"area_name":[],"published_at":[]}
for hour in range(0,24):
    print(hour)
    for page in range(0,21):
        hour=("0"+str(hour))[-2:]
        x=requests.get("https://api.hh.ru/vacancies/", params={"specialization":1, "per_page":100,"page":page,'date_from':f"2022-12-15T{hour}:00:00+0000", 'date_to':f"2022-12-15T{hour}:59:59+0000"})
        vacancyes=json.loads(x.text)
        if "items" in vacancyes:
            for i in vacancyes["items"]:
                for  j in df:
                    if j== "salary_from":
                        try:
                            df[j].append(i["salary"]["from"])
                        except:
                            df[j].append("")
                    elif j== "salary_to":
                        try:
                            df[j].append(i["salary"]["to"])
                        except:
                            df[j].append("")
                    elif j== "currency":    
                        try:
                            df[j].append(i["salary"]["currency"])
                        except:
                            df[j].append("")
                    elif j=="area_name":
                        try:
                            df[j].append(i["address"]["city"])
                        except:
                            df[j].append("")
                    else:
                        try:
                            df[j].append(i[j])
                        except:
                            df[j].append("")
        else:
            break
df = pd.DataFrame(data=df)
df.index = np.arange(1, len(df) + 1)
print(df)
df.to_csv('vacancies_mine.csv', index=False)   