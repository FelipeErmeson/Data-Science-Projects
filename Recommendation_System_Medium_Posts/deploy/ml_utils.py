import pandas as pd
import re
import joblib as jb
from scipy.sparse import hstack, csr_matrix
import numpy as np
import json
import string
#NLTK
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import  WordPunctTokenizer
nltk.download('stopwords')
#WORDCLOUD
from wordcloud import WordCloud, STOPWORDS

#Loading Models
scaler = jb.load("scaler_20200803.pkl.z")
title_vec = jb.load("title_vectorizer_20200803.pkl.z")
mdl_lg = jb.load("logistic_reg_20200803.pkl.z")
mdl_lgbm = jb.load("lgbm_20200803.pkl.z")
mdl_rf = jb.load("random_forest_20200803.pkl.z")

#Build set of stopwords
STOPWORDS.remove('r')
STOPWORDS.add('’')
STOPWORDS.add('“')
STOPWORDS.add('”')
STOPWORDS.add('—')
stopwords_ = STOPWORDS.union(set(string.punctuation)).union(set(stopwords.words('english')))

tokenizer = WordPunctTokenizer()

def remove_stopwords(title):
    new_title = list()
    title = title.lower()
    #title = unidecode.unidecode(title)
    words_title = tokenizer.tokenize(title)
    for w_title in words_title:
        if w_title not in stopwords_:
            new_title.append(w_title)
    return ' '.join(re.sub('[{}—]'.format(string.punctuation), ' ', ' '.join(new_title)).split())

'''Remove todos os caracteres, deixando apenas os pontos finais e os dígitos'''
def parse_to_numeric(x):
    return re.sub('[^.0-9]', '', x)

'''Ajusta as strings para uma representação numérica adequada... Ex: 21K para 21000'''
def adjust_numbers(x):
    if re.sub('[.0-9]', '', x) == 'K':
        aux = float(re.sub('[^.0-9]', '', x))
        return aux * 1000
    else:
        return float(re.sub('[^.0-9]', '', x))

def clean_data(data):
    comments = int(parse_to_numeric(data['comments']))
    reading_time = int(parse_to_numeric(data['reading_time']))
    palms = adjust_numbers(data['palms'])
    title = remove_stopwords(data['title'])
    
    return {"comments": comments, "palms": palms, "reading_time": reading_time, "title": title}

def compute_features(data):
    features_json = clean_data(data)
    title = features_json['title']

    X_scaled = scaler.transform([[features_json['comments'], features_json['palms'], features_json['reading_time']]])
    vectorized_title = title_vec.transform([title])
    feature_array = hstack([X_scaled, vectorized_title])
    
    return feature_array

def compute_prediction(data):
    feature_array = compute_features(data)

    prf = mdl_rf.predict_proba(feature_array)[0][1]
    plr = mdl_lg.predict_proba(feature_array)[0][1]
    plgbm = mdl_lgbm.predict_proba(feature_array)[0][1]
    p = (plr + prf + plgbm)/3
    
    return p
