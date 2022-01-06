import streamlit as st
import pandas as pd
import requests
import time
import numpy as np


anime = pd.read_csv('anime_data.csv')
    
def get_img(anime_ids):
    response = requests.get('https://api.jikan.moe/v4/anime/{}/pictures'.format(anime_ids))
    data = response.json()
    # res = data['data'][0]['jpg']["image_url"]
    if 'data' in data:
        return data['data'][0]['jpg']["image_url"]
    else:
        return "./movie_placeholder.png"

def recommend(anime_name):
    name_index = anime[anime['name'] == anime_name].index[0]
    dist = similarity[name_index]
    anime_list = sorted(list(enumerate(dist)),reverse = True, key = lambda x:x[1])[0:10]
    # for i in anime_list:
    #     print(anime.iloc[i[0]]['name'])
    rec_anime = []
    for i in anime_list:
        rec_anime.append(anime.iloc[i[0]]['anime_id'])
    return rec_anime
        
similarity = np.load('simi.npz')['arr_0']

ls = list(anime['name'])

st.title("Anime Recommended System")
opt = st.selectbox('What anime do you like?',ls)

if st.button('recommend'):
    rec = recommend(opt)

    i, j = 0, 0
    while j<5 and i<len(rec):
        if j==5: j=0
        col = st.columns(2)
        for k in range(2):
            if i >= len(rec): break
            with col[k]:
                st.image(get_img(rec[i]))
                st.write(anime[anime['anime_id'] == rec[i]]['name'].iloc[0])
                time.sleep(0.4)
            i+=1
        j+=1