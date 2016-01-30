# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 00:01:50 2015

@author: Phani
"""

from pandas import read_csv

DATA_FILES_SOURCE_DIRECTORY = "C:\\Users\\dell\\Desktop\\Wallmart\\Predict how sales of weather-sensitive products are affected by snow and rain\\DATA"

STORE_AND_STATION_MAP_FILE = "key.csv"
WEATHER_DATA_FILE = "weather.csv"
SALES_DATA_FILE = "train.csv"

STORE_STATION_MAP_DICT = {} # Storeno : Station No
WEATHER_DICTIONARY = {} # "Stationno_date" : [rest of the data in a list]
STORE_SALES_DICTIONARY= {} # "Storeno_date_item_no" : units_sold}
ITEM_ID = []

UNDERSCORE = "_"
COMMA = ","

file_handle = open(STORE_AND_STATION_MAP_FILE,'r')
header_found = False
for line in file_handle.readlines():
    if header_found == False:
        header_found = True
        continue
    line = line.strip()
    data = line.split(',')
    store_no = data[0]
    station_no = data[1]
    STORE_STATION_MAP_DICT[store_no] = station_no
file_handle.close()
#print(STORE_STATION_MAP_DICT)
#print(len(STORE_STATION_MAP_DICT))

file_handle = open(WEATHER_DATA_FILE,'r')
header_found = False
for line in file_handle.readlines():
    rest_of_data = []
    if header_found == False:
        header_found = True
        continue
    line = line.strip()
    data = line.split(',')
    
    for char in '"':
        for i in range(len(data)):
            data[i] = data[i].replace(char,"")
    
    station_no = str(data[0].strip())
    date_list = str(data[1].strip()).split("-")
    #DD-MM-YYYY
    date = str(date_list[0].strip() + "-" + date_list[1].strip() + "-" +date_list[2].strip())
    rest_of_data = data[2:]
    
    key = station_no + UNDERSCORE + date
    #print(key)
    WEATHER_DICTIONARY[key] = rest_of_data
file_handle.close()
#print(WEATHER_DICTIONARY)
#print(len(WEATHER_DICTIONARY))

file_handle = open(SALES_DATA_FILE,'r')
header_found = False
item_sale_dict = {}

for line in file_handle.readlines():
    if header_found == False:
        header_found = True
        continue
    
    line = line.strip()
    data = line.split(',')
    for char in '"':
        for i in range(len(data)):
            data[i] = data[i].replace(char,"")

    date_list = str(data[0].strip()).split("-")
    #YYYY-MM-DD
    date = str(date_list[2].strip() + "-" + date_list[1].strip() + "-" + date_list[0].strip())
    store_no = str(data[1].strip())
    item_id = str(data[2].strip())
    unit_sold = str(data[3].strip())
    
    if item_id not in ITEM_ID:
        ITEM_ID.append(item_id)
        
    key = store_no + UNDERSCORE + date + UNDERSCORE + item_id
    #print(key)
    STORE_SALES_DICTIONARY[key] = unit_sold

#print(STORE_SALES_DICTIONARY)
#print(len(STORE_SALES_DICTIONARY))
file_handle.close()

#print(ITEM_ID)
#print(len(ITEM_ID))

#print(WEATHER_DICTIONARY["14_01-01-2012"])
#print(STORE_STATION_MAP_DICT["2"])
#print(STORE_SALES_DICTIONARY["2_01-01-2012_63"])

output_file_handler = open("new_train.csv","w")
output_file_handler.write("date" + COMMA + "store_no" + COMMA + "item_id" + COMMA + "unit_sale" + COMMA + "station_no" + COMMA + "weather" +  "\n")
for store_date_itemid_key in STORE_SALES_DICTIONARY.keys():
    data = store_date_itemid_key.split(UNDERSCORE)
    store_no = data[0].strip()    
    date = data[1].strip()
    item_id = data[2].strip()
    unit_sale = STORE_SALES_DICTIONARY[store_date_itemid_key]
    
    station_no = STORE_STATION_MAP_DICT[store_no]
    station_no_date_key = station_no + UNDERSCORE + date
    
    all_info_about_weather = list(WEATHER_DICTIONARY[station_no_date_key])
    weather = all_info_about_weather[10].strip()
    if weather.strip() == "":
        weather = "MODERATE"
    
    STRING_TO_WRITE = str(date + COMMA + store_no + COMMA + item_id + COMMA + unit_sale + COMMA + station_no + COMMA + weather)
    #print(STRING_TO_WRITE)
    output_file_handler.write(STRING_TO_WRITE + "\n")
    
output_file_handler.close()
    
