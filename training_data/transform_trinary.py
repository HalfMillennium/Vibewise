import os
import csv
import pandas as pd
import numpy as np

#dataset = pd.read_csv('musix_tone_data.csv')
current_info = pd.read_csv('1500_all_features.csv')
current_info = current_info.iloc[:,:].values

writer = csv.writer(open('1500_trinary_class.csv', 'w', encoding='utf-8'))

#writer.writerow(["Song","T-Anger","T-Fear","T-Joy","T-Sadness","T-Analytical","T-Confident","T-Tentative","Mood"])
for song in current_info:
    val = ''
    if(song[-1] == 'happy' or song[-1] == 'relaxed'):
        val = 'chill'
    else:
        val = song[-1]
    temp = np.array(song[:-1]).tolist()
    temp.append(val)
    writer.writerow(temp)
