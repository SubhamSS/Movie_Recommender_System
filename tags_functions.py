import ast
import numpy
import openpyxl
import pandas as pd
from nltk.stem.porter import PorterStemmer

def convert(text):
    L = []
    for i in ast.literal_eval(text):
        L.append(i['name'])
    return L

def convertfromdict(text):
    #resultList = list(text.items())
    #resultList = [(key, value) for key, value in inputDictionary.items()]
    if pd.isnull(text):
        return ""
    L = []
    j = ast.literal_eval(text)
    L.append(j['name'])

    # for i in ast.literal_eval(text):
    #     resultList = list(i.items())
    #     L.append(resultList['name'])
    return L

def fetch_director(text):
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            L.append(i['name'])
    return L

def fetch_music_composer(text):
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Original Music Composer':
            L.append(i['name'])
    return L

def producer(text):
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Producer':
            L.append(i['name'])
    return L

def screenplay(text):
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Screenplay':
            L.append(i['name'])
    return L

def writer(text):
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Writer':
            L.append(i['name'])
    return L

def remove_space(L):
    cc = []
    for i in L:
        cc.append(i.replace(" ",""))
    return cc

ps = PorterStemmer()
def stem(word):
    root = []
    for i in word.split():
        root.append(ps.stem(i))
    return " ".join(root)