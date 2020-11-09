'''
DESC: Retrieves track features and track analysis for each song in csv 'MoodyLyrics4Q.csv'

Last edited: 7/13/2020

'''
import os
import csv
import spotipy
import spotipy.util as util
import pandas as pd
from spotipy.oauth2 import SpotifyOAuth
import ast

os.environ["SPOTIPY_CLIENT_ID"] = '9013dc5d86b84ffca62df2f22e00968e'
os.environ["SPOTIPY_CLIENT_SECRET"] = 'b9484118ab374707925b1b15100cc58b'
os.environ["SPOTIPY_REDIRECT_URI"] = 'https://github.com/HalfMillennium'

scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

token = util.prompt_for_user_token("Garrett Chestnut",
                           scope,
                           client_id=os.environ["SPOTIPY_CLIENT_ID"],
                           client_secret=os.environ["SPOTIPY_CLIENT_SECRET"],
                           redirect_uri=os.environ["SPOTIPY_REDIRECT_URI"])

dataset = pd.read_csv('MoodyLyrics4Q.csv')

track_info = dataset.iloc[:,1:].values

#writer = csv.writer(open('output_observations.csv', 'w'))
writer = csv.writer(open('track_names_en_val.csv', 'w', encoding="utf-8"))

# Stores all review values
search_results = []
all_features = []
total_feat_set = 1

def retrieve(raw_search, left, total_feat_set, spot):
    #print(ids)
    global all_features
    if(left != 0):
        if(left < 100):
            res = spot.audio_features(get_ids(raw_search[(len(raw_search)-left-1):len(raw_search)]))
            all_features = all_features + res
            print(total_feat_set, '- Feature set appended.')
            left = 0
        else:
            res = spot.audio_features(get_ids(raw_search[(len(raw_search)-left-1):((len(raw_search)-left-1)+100)]))
            all_features = all_features + res
            left = left - 100
            print(total_feat_set, '- Feature set appended.')

        retrieve(raw_search, left, total_feat_set+1,spot)

def get_ids(raw_results):
    ids = []
    for entry in raw_results:
        if(len(entry['tracks']['items']) > 0):
            ids.append(entry['tracks']['items'][0]['id'])
            print(entry['tracks']['items'][0]['id'])
    return ids

if token:
    for obs in track_info:
        sp = spotipy.Spotify(auth=token)
        results = sp.search(q=obs[0]+' '+obs[1], limit=1)
        if(len(results) == 0):
            print(obs[1],'by',obs[0],'not found.')
        else:
            search_results.append(results)
            print(len(search_results),'- Search result appended.')
    #print(search_results)
    retrieve(search_results,len(search_results)-1,total_feat_set,sp)

    track_count = 0
    for track, search, obs_info in zip(all_features, search_results, track_info):
            #feat = sp.audio_features(track['id'])
            #print(search)
            if(len(search['tracks']['items']) > 0):
                track_obj = search['tracks']['items'][0]
                analysis = sp.audio_analysis(track_obj['id'])
                print(track)
                energy_valence_f = [track['energy'],track['valence'], track_obj['name'] + ' by ' + track_obj['artists'][0]['name']]
                #feat = [track[0]['energy'],track[0]['tempo'],track[0]['mode'],track[0]['key'],track[0]['valence']] + analysis['segments'][0]['pitches']
                #f = [track[0]['key'],track[0]['mode'],track[0]['danceability'],track[0]['energy'],track[0]['valence'],track[0]['tempo']]
                print(energy_valence_f)
                full = energy_valence_f + [obs_info[2]]
                writer.writerow(full)
                track_count = track_count + 1
else:
    print("Can't get token for", username)
