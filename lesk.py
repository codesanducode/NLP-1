#!/usr/bin/env python
# coding: utf-8

# In[144]:


import nltk
from nltk.wsd import lesk
import difflib
from nltk.corpus import wordnet
nltk.download('averaged_perceptron_tagger')
from nltk.stem.wordnet import WordNetLemmatizer


# In[145]:


lesk(nltk.word_tokenize('Students enjoy going to school, studying and reading books'),'school','n')


# In[146]:


wordnet.synset('school.n.01').examples()[0]


# In[147]:


def originalLesk(desc_list,word,pos):
    
    # based on the description and the word, tries to find most appropriate wordnet definition 
    # based on number of common words between the description and the definition
    
    def compare_glosses(list1,list2):
        return len([word for word in set(list1) if word in set(list2)])

    syn = wordnet.synsets(word)
    scores = []
    for i in syn:
        if i.pos() == pos:
            def_score = compare_glosses(nltk.word_tokenize(i.definition()),desc_list)
            scores.append(def_score)
            
    for i in syn:
        if i.pos() == pos:
            def_score = compare_glosses(nltk.word_tokenize(i.definition()),desc_list)
            if def_score == max(scores):
                print(i)
                print(i.definition())
            
        
originalLesk(nltk.word_tokenize('Students enjoy going to school, studying and reading books'),'school','n')


# In[245]:


def extendedLesk(desc_list,myword,pos):
    
    def compare_glosses(list1,list2):
        return len([word for word in set(list1) if word in set(list2)])
    
    def matches(list1c, list2c):
        list1=list1c.copy()
        list2=list2c.copy()
        while True:
            mbs = difflib.SequenceMatcher(None, list1, list2).get_matching_blocks()
            if len(mbs) == 1: break
            for i, j, n in mbs[::-1]:
                if n > 0: yield list1[i: i + n]
                del list1[i: i + n]
                del list2[j: j + n]
    # lemmatize, get pos in wordnet format and remove non information words(linkers)
    def process(tokenized_sent):
        
        # transform from treebank tagging to wordnet compatible
        def get_wordnet_pos(treebank_tag):
            if treebank_tag.startswith('J'):
                return wordnet.ADJ
            elif treebank_tag.startswith('V'):
                return wordnet.VERB
            elif treebank_tag.startswith('N'):
                return wordnet.NOUN
            elif treebank_tag.startswith('R'):
                return wordnet.ADV
            else:
                return ''
            
        lemmatizer = WordNetLemmatizer() 
        # tuple (lemmatized word, pos tag)
        return [(lemmatizer.lemmatize(pair[0].lower(), get_wordnet_pos(pair[1])),get_wordnet_pos(pair[1])) for pair in nltk.pos_tag(tokenized_sent) if get_wordnet_pos(pair[1])!='']
    
    
    def get_synsets(word):
        return wordnet.synsets(word[0],word[1])
    
    tagged_list = process(desc_list)
    synsets = {} 
    for word in tagged_list: 
        related = {} 
        for syn in get_synsets(word): # for all synsets of each word get all things
            related[syn] = {'hypernyms':syn.hypernyms(),
                            'hyponyms':syn.hyponyms(),
                            'part_meronyms':syn.part_meronyms(),
                            'substance_meronyms':syn.substance_meronyms(),
                            'member_meronyms':syn.member_meronyms(),
                            'part_holonyms':syn.part_holonyms(),
                            'substance_holonyms':syn.substance_holonyms(),
                            'member_holonyms':syn.member_holonyms(),
#                             'troponyms':syn.troponyms(),
                            'attributes':syn.attributes(),
                            'similar–to':syn.similar_tos(),
                            'also–see':syn.also_sees()
                           }
        synsets[word]=related
    
    extended_glosses = [] # get their definitions
    for word in tagged_list:
        x = synsets[word]
        for key,value in x.items():
            for k,v in value.items():
                for syn in v:
                    extended_glosses.append(nltk.word_tokenize(syn.definition()))
                    
    maximum = -1
    mysyn = None
    # get the scores based on the longest common phrase
    for syn in wordnet.synsets(myword):
        if syn.pos() == pos: 
            x = 0
            for defi in extended_glosses:
                tokenized = nltk.word_tokenize(syn.definition())

                match = list(matches(tokenized,defi))
                if match != []:
                    for i in match[0]:
                        x+=len(i)*len(i)
            if x >maximum:
                maximum = x
                mysyn=syn
            print(syn,x,syn.definition())
            
    print('final decision:')
    print(mysyn)
    print(mysyn.definition())
        
            
    
extendedLesk(nltk.word_tokenize('Students enjoy going to school, studying and reading books'),'school','n')    


# In[ ]:





# In[ ]:




