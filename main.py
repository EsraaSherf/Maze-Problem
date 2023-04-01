from tkinter import *
import nltk
import numpy as np
import pandas as pd
nltk.data.path.append('.')
with open ("file.txt")as f:
    data =f.read()
def Data_Cleaning(data):
    data = data.split("\n")
    data = [s.strip() for s in data]
    data = [s for s in data if len(s) > 0]
    return data
def tokenize_sentences(data):
    tokenize_sentences=[]
    for sentence in data:
        sentence = sentence.lower()
        tokenized = nltk.word_tokenize(sentence)
        tokenize_sentences .append(tokenized)
    return tokenize_sentences
def Bi_grams(tokenized_sentences,n, start_token='<s>', end_token='<e>'):
        n_grams = {}
        for sentence in range(len(tokenized_sentences)):
            sentences = [start_token]*n + list(tokenized_sentences[sentence]) + [end_token]
            sentences = tuple(sentences)
            for i in range(0, len(sentences) - n + 1):
                n_gram = sentences[i:i + n]
                if n_gram in n_grams.keys():
                    n_grams[n_gram] += 1
                else:
                    n_grams[n_gram] = 1
        return n_grams
def prob_matrix(prev_word, BIGRAM):
    vocabulary = []
    unigrams = []
    for BI_tuple in BIGRAM.keys():
        unigram = BI_tuple[0:-1]
        vocab = BI_tuple[-1]
        unigrams.append(unigram)
        vocabulary.append(vocab)
    vocabulary = list(set(vocabulary))
    unigrams = list(set(unigrams))
    row_index = {n_gram: i for i, n_gram in enumerate(unigrams)}
    col_index = {word: j for j, word in enumerate(vocabulary)}
    nrow = len(unigrams)
    ncol = len(vocabulary)
    count_matrix = np.zeros((nrow, ncol))
    for n_plus1_gram, count in BIGRAM.items():
        unigram = n_plus1_gram[0:-1]
        word = n_plus1_gram[-1]
        i = row_index[unigram]
        j = col_index[word]
        count_matrix[i, j] = count
    count_matrix = pd.DataFrame(count_matrix,columns=vocabulary)
    row_sums = count_matrix.sum(axis="columns")
    prob_matrix = count_matrix.div(row_sums, axis="rows")
    prob_matrix["word"] = [tup[0] for tup in unigrams]
    next = prob_matrix.loc[prob_matrix['word'] == prev_word]
    ind=next.index
    ind=ind[-1]
    v=prob_matrix.iloc[ind]
    probdict=dict(v)
    words={}
    keys=[]
    for key,vaue in probdict.items():
        if probdict[key]!=0.0:
            keys.append(prev_word+" "+key)
            words[prev_word]=keys
    return words
s=Data_Cleaning(data)
t=tokenize_sentences(s[0:4000])
#print("tekonised sequence:",t)
bi_gram=Bi_grams(t,2)
#print("Uni_grams:",bi_gram)
#print("segessions",prob_matrix("feel",bi_gram))
#seg=prob_matrix("feel",bi_gram)
#print("seggestions",seg)
window = Tk()
window.title("Welcome to NLP")
window.geometry('500x300')
def update(data):
    mylist.delete(0, END)
    for item in data:
        mylist.insert(END, item)
def fillout(e):
    myentry.delete(0, END)
    myentry.insert(0, mylist.get(ANCHOR))
def check(e):
    typed = myentry.get()
    if typed == '':
        item = toppings
    else:
        typed = myentry.get()
        x=prob_matrix(typed,bi_gram)
        xlist=x.values()
        data = []
        for item in xlist:
                data.append(item)
    update(item)
label =Label(window, text='Google', font=('calibre',20) ,fg="blue",width=50,bg="black")
label.pack()
myentry=Entry(window, font=('calibre',15,'normal'),fg="blue")
myentry.pack()
mylist=Listbox(window,width=70,fg="blue",bg="black")
mylist.pack()
toppings=[]
update(toppings)
mylist.bind("<<ListboxSelect>>", fillout)
myentry.bind("<Return>", check)
window.configure(bg='black')
window.mainloop()



