import csv
import pandas as pd

writer = csv.writer(open('full_output_musix.csv', 'w'))
data_1 = pd.read_csv('song_features_musix.csv', encoding='utf-8')
data_2 = pd.read_csv('song_features_musix_temp_utf.csv', encoding='utf-8')

first = data_1.iloc[:,:].values
second = data_2.iloc[:,:].values

for f in first:
    writer.writerow(f)
for s in second:
    writer.writerow(s)
