from flask import Flask, render_template, request
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
import pickle
import numpy as np
import pandas as pd
import re
import nltk
nltk.download('punkt')
nltk.download('omw-1.4')
import nltk.data as nd
sent_tokenizer = nd.load('tokenizers/punkt/english.pickle')
import math
nltk.download('wordnet')
nltk.download('stopwords')
from nltk.corpus import stopwords
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.feature_extraction.text import CountVectorizer

model = pickle.load(open('model.pkl','rb'))
vectorizer = pickle.load(open('vectorizer.pkl','rb'))

app = Flask(__name__)


def utils_preprocess_text(text, flg_stemm=False, flg_lemm=True, lst_stopwords=None):
        text = re.sub(r'[^\w\s]','',str(text).lower().strip())
        lst_text = text.split()
        if lst_stopwords is not None:
            lst_text = [word for word in lst_text if word not in lst_stopwords]
        if flg_stemm==True:
            ps = nltk.stem.porter.PorterStemmer()
            lst_text = [ps.stem(word) for word in lst_text]
        if flg_lemm==True:
            lem = nltk.stem.wordnet.WordNetLemmatizer()
            lst_text = [lem.lemmatize(word) for word in lst_text]
        text = " ".join(lst_text)
        # print(text)
        return text

def transforming():
    fp = pd.read_csv("input.csv",header=None)
    fp = fp.dropna(axis = 0, how='any')
    lst_stopwords = nltk.corpus.stopwords.words("english")
    fp[len(fp.columns)] = ""
    fp.iloc[:,1] = fp.iloc[:, 0].apply(lambda x: utils_preprocess_text(x,flg_stemm=False,flg_lemm=True,lst_stopwords=lst_stopwords))
    fp.to_csv("input.csv",index=False)
    fp = pd.read_csv("input.csv")
    inps = fp.iloc[:, 1].values 
    prf = vectorizer.transform(inps)
    return prf

@app.route('/')
def base():
    return render_template('index.html')

@app.route('/home', methods=['POST'])
def home():
    data = request.form['message']
    # data2 = request.form['text1']
    # data3 = request.form['text2']
    # print(data)
    msg = sent_tokenizer.tokenize(data)
    # print(msg)
    file = open("input.csv","w")
    for each in msg:
        file.write(each+"\n")
    # file.write(data2+"\n")
    # file.write(data3+"\n")
    file.close()
    data1 = transforming()                         #data = request.form['data']
    # print(data1)
    pred = model.predict(data1)
    pred_avg = sum(pred)/len(pred)
    pred_avg = 1-pred_avg
    pred_avg *= 100
    pred_avg = math.trunc(pred_avg)
    print(pred)
    return render_template('result.html',pred = pred_avg)


if __name__ == "__main__":
    app.run(debug=True)


        # {%if pred == 1%}
        # {%else%}
        # {%endif%}

# I am currently happy with myself. I sometimes do feel sad.
