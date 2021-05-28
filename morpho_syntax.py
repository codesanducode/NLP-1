# -*- coding: utf-8 -*-
"""morpho_syntax.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZkyN950OfD2pOihX5C0-ctTATsJMepd5
"""

!pip install wikipedia

import wikipedia
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')
from nltk.tag import pos_tag
from nltk.tokenize import sent_tokenize
nltk.download('averaged_perceptron_tagger')

nlp = wikipedia.WikipediaPage("Natural language processing")
print(nlp.title)
print(nlp.url)

tokens = word_tokenize(nlp.content)
print(tokens[:200])

sent_tokens = sent_tokenize(nlp.content)[:20]
postag=[]
for i in sent_tokens:
  postag.append(pos_tag(word_tokenize(i)))

for i in postag:
  print(i)

def example(pos_tag_var,text):
  word_list=[]
  sent_tokens = sent_tokenize(text)
  postag=[]
  for i in sent_tokens:
    postag.append(pos_tag(word_tokenize(i)))
  for i in postag:
    for j in i:
      if(j[1]==pos_tag_var):
        word_list.append(j[0])
  return word_list

print(example('NN',nlp.content))

def multiple_example(pos_tag_list,text):
  word_list=[]
  for tags in pos_tag_list:
    word_list.append(example(tags,text))
  return [item for items in word_list for item in items]

print(multiple_example(['NN','IN'],nlp.content))

nouns = multiple_example(['NN','NNS','NNP','NNPS'],nlp.content)
verbs = multiple_example(['VB','VBG','VBD','VBN','VBP','VBZ',],nlp.content)
print(nouns)
print(verbs)
print('verb+noun percentage',(len(nouns)+len(verbs))*100/len(tokens))

from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()

sent_tokens = sent_tokenize(nlp.content)
all_pos_tags=[]
for i in sent_tokens:
  all_pos_tags.append(pos_tag(word_tokenize(i)))
all_pos_tags = np.array([item for items in all_pos_tags for item in items])

lemmatizer.lemmatize('calm','N'.lower())

from nltk.corpus import wordnet
tag_dict = {"J": wordnet.ADJ,
            "N": wordnet.NOUN,
            "V": wordnet.VERB,
            "R": wordnet.ADV}

all_pos_tags = np.array([i for i in all_pos_tags if i[1][0] in ['J','N','V','R']])

import pandas as pd
data = {'Original word' : [word1 for word1 in all_pos_tags[:,0]],
        'POS':[tag1 for tag1 in all_pos_tags[:,1]],
        'Simple lemmatization':[lemmatizer.lemmatize(word) for word in all_pos_tags[:,0]],
        'Lemmatization with POS':[lemmatizer.lemmatize(word,tag_dict[tag[0]]) for word,tag in all_pos_tags[:]]}
df = pd.DataFrame(data)
df2 = pd.DataFrame(data)
df =df[df['Simple lemmatization']!=df['Lemmatization with POS']].drop_duplicates()
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    display(df)

print('Original word | POS | Simple lemmatization | Lemmatization with POS')
for _,row in df.iterrows():
  print(row['Original word'],'|',row['POS'],'|',row['Simple lemmatization'],'|',row['Lemmatization with POS'])

df2['POS'].value_counts().plot.bar()

