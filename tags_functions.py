import ast
import numpy
import openpyxl
import pandas as pd
from nltk.stem.porter import PorterStemmer

def convert(text): #get data from list
    L = []
    for i in ast.literal_eval(text):
        L.append(i['name'])
    return L

def convertfromdict(text): #get data from dictionary
    if pd.isnull(text):
        return ""
    L = []
    j = ast.literal_eval(text)
    L.append(j['name'])

    return L

def fetch_director(text): #get director
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            L.append(i['name'])
    return L

def fetch_music_composer(text): #get music composer
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Original Music Composer':
            L.append(i['name'])
    return L

def producer(text): #get producer
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Producer':
            L.append(i['name'])
    return L

def screenplay(text): #get screenplay
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Screenplay':
            L.append(i['name'])
    return L

def writer(text): #get writer
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Writer':
            L.append(i['name'])
    return L

def remove_space(L): #remove space
    cc = []
    for i in L:
        cc.append(i.replace(" ",""))
    return cc

ps = PorterStemmer()
def stem(word): #get root word
    root = []
    for i in word.split():
        root.append(ps.stem(i))
    return " ".join(root)