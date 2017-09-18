# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 16:28:32 2016

@author: Кирилл
"""

import requests
import csv

#на входе список брендов
#из списка по бренду запросом http://apigeo.morion.ua/m/1/page/by-text/ + БРЕНД получаем список страниц
#из ответа вида [{"id":"148087","name":"ПАРАЦЕТАМОЛ","path":"/paracetamol"}] получаем урл и id=148087 для получения drug_id
#по имеющейся "id":"148087" получаем список drug_id
#по url из превед. шага строим url с городами
#по списку drug_id строим страницы вида /drug/1-1- + drug_id1 + drug_id2 и т.д.
#по списку drug_id строим страницы вида /drug/ + drug_id1 /drug/ + drug_id2 и т.д.
#сохраняем все в файл одна строка - один url

#Объявляем значения/переменные/методы
Page_list_quest = 'http://apigeo.morion.ua/m/1/page/by-text/'
Drug_id_list_quest = 'http://apigeo.morion.ua/m/1/item/by-page/'
List_result = []
Income_list=['ЮНИДОКС', 'ВИБРАМИЦИН', 'ДОКСИ', 'ДОКСИБЕНЕ', 'ДОКСИЦИКЛИН', 'ТЕТРАЦИКЛИН', 'ТИГАЦИЛ', 'ЛЕВОМИЦЕТИН', 'ФЛУИМУЦИЛ', 'АМПИЦИЛЛИН', 'АМОКСИЛ', 'ОСПАМОКС', 'ФЛЕМОКСИН', 'ХИКОНЦИЛ', 'ФЛЕМОКСИН', 'БЕНЗИЛПЕНИЦИЛЛИН', 'ПЕНИЦИЛЛИН', 'РЕТАРПЕН']
City_list = ['/odessa', '/kremenchug', '/zaporozhe', '/cherkassy', '/izyum', '/krivoy-rog', '/ternopol', '/sumy', '/chernigov', '/kiev', '/poltava', '/dnepropetrovsk', '/dneprodzerzhinsk', '/vinnica', '/lvov', '/chernovcy', '/nikolaev', '/pavlograd', '/zhitomir', '/ivano-frankovsk', '/nikopol', '/belaya-cerkov', '/kirovograd', '/hmelnickiy', '/rovno', '/kamenec-podolskiy','/merefa']


#читаем бренды из файла с брендами
exampleFile = open('C:/Python/Service/Olesya_drug_lists/Olesya_16.csv')
exampleReader = csv.reader(exampleFile)
Brend_list = list(exampleReader)

#Brend_list=Income_list

    
for Brend in Brend_list:
    url=Page_list_quest+Brend[0]
    req = requests.get(url)
    parsed_json=req.json()
#    print(Brend, parsed_json)
    for Page in parsed_json:
        drug_url=Drug_id_list_quest+Page['id']
        req_drug=requests.get(drug_url)
        drug_parsed_json=req_drug.json()
#        print(Page['name'],'\n', drug_parsed_json)
        List_drug_id=[]
        for Drug in drug_parsed_json:
            List_drug_id.append(Drug['id'])
        print(List_drug_id)
        List_result.append(Page['name'])
       
        if len(Page['path'].split('/'))==2:
            List_result.append(Page['path']) 
            print(len(Page['path'].split('/')))
            for City in City_list:
                List_result.append(Page['path']+City)
        elif len(Page['path'].split('/'))>2:
            List_result.append(Page['path'])
            Query_row='/drug/1-1'
            for Drugs in List_drug_id:
                 List_result.append('/drug/'+str(Drugs))
                 Query_row += str('-'+ str(Drugs))
            List_result.append(Query_row)
                 
with open('C:/Python/Service/Olesya_drug_lists/Drug_list_to_Olesya_16.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    for Item in List_result:
        csv_writer.writerow([Item])
csv_file.close()