from Plot_AQI import avg_data_2018, avg_data_2019, avg_data_2020, avg_data_2021, avg_data_2022
import requests
import os
import sys
import pandas as pd
from bs4 import BeautifulSoup
import csv

def net_data(month, year):
    file_html = open('/DS Projects/Air_quality_index/Data/Html_Data/{}/{}.html'.format(year,month),'rb')
    plain_text = file_html.read()

    tempD = []
    finalD = []

    soup = BeautifulSoup(plain_text, "lxml")
    for table in soup.findAll('table', {'class': 'medias mensuales numspan'}):
        for tbody in table:
            for tr in tbody:
                a=tr.get_text()
                tempD.append(a)

    rows=len(tempD)/15

    for times in range(round(rows)):
        newtempD = []
        for i in range(15):
            newtempD.append(tempD[0])
            tempD.pop(0)
        finalD.append(newtempD)

    length = len(finalD)

    finalD.pop(length-1)
    finalD.pop(0)

    for a in range(len(finalD)):
        finalD[a].pop(6)
        finalD[a].pop(13)
        finalD[a].pop(12)
        finalD[a].pop(11)
        finalD[a].pop(10)
        finalD[a].pop(9)
        finalD[a].pop(0)

    return finalD

def combine(year, cs):
    for a in pd.read_csv('/DS Projects/Air_quality_index/Data/Real_data/real_'+str(year) + '.csv',chunksize=cs):
        df = pd.DataFrame(data=a)
        mylist = df.values.tolist()
    return mylist


if __name__ == "__main__":
    if not os.path.exists('/DS Projects/Air_quality_index/Data/Real_data'):
        os.makedirs('/DS Projects/Air_quality_index/Data/Real_data')

    for year in range(2018,2023):
        final_data = []
        with open('/DS Projects/Air_quality_index/Data/Real_data/real_' +str(year)+ '.csv','w') as csvfile:
            wr = csv.writer(csvfile,dialect='excel')
            wr.writerow(
                ['T','TM','Tm','SLP','H','VV','V','VM','PM 2.5']
            )

        for month in range(1,13):
            temp = net_data(month,year)
            final_data = final_data + temp

        pm = getattr(sys.modules[__name__], 'avg_data_{}'.format(year))()

        if len(pm) == 364:
            pm.insert(364, '-')

        for i in range(len(final_data)-1):
            final_data[i].insert(8,pm[i])

        with open('/DS Projects/Air_quality_index/Data/Real_data/real_' +str(year) + '.csv','a') as csvfile:
            wr = csv.writer(csvfile,dialect='excel')
            for row in final_data:
                flag=0
                for elem in row:
                    if elem == "" or elem == "-":
                        flag=1
                    if flag != 1:
                        wr.writerow(row)

    data_2018 = combine(2018,600)
    data_2019 = combine(2019,600)
    data_2020 = combine(2020,600)
    data_2021 = combine(2021,600)
    data_2022 = combine(2022,600)

    total = data_2018+data_2019+data_2020+data_2021+data_2022

    with open('/DS Projects/Air_quality_index/Data/Real_data/real_combine.csv','w') as csvfile:
            wr = csv.writer(csvfile,dialect='excel')
            wr.writerow(
                ['T','TM','Tm','SLP','H','VV','V','VM','PM 2.5']
            )
            wr.writerows(total)

