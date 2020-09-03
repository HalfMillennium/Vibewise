import os
import csv
import pandas as pd
import ast
import socket
from musixmatch import Musixmatch
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

dataset = pd.read_csv('MoodyLyrics4Q.csv')
current_info = pd.read_csv('musix_tone_data.csv')
current_info = current_info.iloc[:,:].values
track_info = dataset.iloc[500:1500,1:].values

writer = csv.writer(open('musix_tone_data.csv', 'w', encoding='utf-8'))
song_names = []
all_features = []
all_harmonies = []

labels = []
all_lyric_object = []
all_lyric_tones = []

# MusixMatch API
musixmatch = Musixmatch('')

# Tone Analyzer API
authenticator = IAMAuthenticator('')
tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    authenticator=authenticator
)

tone_analyzer.set_service_url('https://api.us-south.tone-analyzer.watson.cloud.ibm.com/instances/b8f00a45-63d1-4bb9-b1a0-1c2e6bc3e4ca')

writer.writerow(["Song","T-Anger","T-Fear","T-Joy","T-Sadness","T-Analytical","T-Confident","T-Tentative","Mood"])

for obs in track_info:
    try:
        lyrics = musixmatch.matcher_lyrics_get(obs[1], obs[0])

        lyric_body = ''
        #print(obs[1] + ' by ' + obs[0] + ' (' + obs[2] + '):\n\n', lyrics['message']['body']['lyrics']['lyrics_body'][:-70])
        if(lyrics['message']['header']['status_code'] != 404):
            lyric_body = lyrics['message']['body']['lyrics']['lyrics_body'][:-70]
        else:
            print('404 for ' + obs[1] + ' by ' + obs[0])

        if(lyric_body == ''):
            print('No lyrics available for ' + obs[1] + ' by ' + obs[0] + '\n')
        else:
            #song_names.append(obs[1] + ' by ' + obs[0])
            #labels.append(obs[2])
            tone_analysis = tone_analyzer.tone(
                {'text': lyric_body},
                content_type='application/json'
            ).get_result()

            lyric_moods = { "anger": 0, "fear": 0, "joy": 0, "sadness": 0, "analytical": 0, "confident": 0, "tentative": 0 }

            print(obs[1] + ' by ' + obs[0] + ' (' + obs[2] + '):\n')
            for tone in tone_analysis['document_tone']['tones']:
                lyric_moods[tone['tone_id']] = tone['score']
                print(tone['tone_id'],':',lyric_moods[tone['tone_id']],'\n')

            #all_lyric_tones.append([lyric_moods['anger'],lyric_moods['fear'],lyric_moods['joy'],lyric_moods['sadness'],lyric_moods['analytical'],lyric_moods['confident'],lyric_moods['tentative']])
            writer.writerow([obs[1] + ' by ' + obs[0]]+[lyric_moods['anger'],lyric_moods['fear'],lyric_moods['joy'],lyric_moods['sadness'],lyric_moods['analytical'],lyric_moods['confident'],lyric_moods['tentative']]+[obs[2]])

    except socket.timeout:
        print("Socket read timeout.")


for entry in current_info:
    writer.writerow(entry)

'''for song,tone,label in zip(song_names, all_lyric_tones, labels):
    tones = [tone[0],tone[1],tone[2],tone[3],tone[4],tone[5],tone[6]]
    writer.writerow([song]+tones+[label])'''
