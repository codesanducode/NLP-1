#!/usr/bin/env python
# coding: utf-8

# In[1]:


import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet
wordnet.synsets('school')


# In[2]:


def f1(word):
    for syn in wordnet.synsets(word):
        print(syn.definition())
f1('cat')


# In[3]:


def f2(word1, word2):
    syn1 = [i.hypernyms() for i in wordnet.synsets(word1)]
    syn2 = [i.hypernyms() for i in wordnet.synsets(word2)]

    syn3=[]
    [syn3.append(i) for i in syn1 if i in syn2 if i not in syn3]
    if syn3!= []:
        for i in syn3:
            print(i[0].definition())
f2('school','university')


# In[4]:


def f3(syn):
    holo1 = syn.part_holonyms()
    holo2 = syn.substance_holonyms()
    holo3 = syn.member_holonyms()
    holo =holo1+holo2+holo3
    
    mero1 = syn.part_meronyms()
    mero2 = syn.substance_meronyms()
    mero3 = syn.member_meronyms()
    mero = mero1+mero2+mero3
    
    return (holo,mero)

syn1 = wordnet.synset('animal.n.01')
print(syn1.part_holonyms())
print(syn1.substance_holonyms())
print(syn1.member_holonyms())
print(syn1.part_meronyms())
print(syn1.substance_meronyms())
print(syn1.member_meronyms())
print()
print(f3(syn1))


# In[5]:


def f4(syn):
    def print_path(path):
        for i in path:
            print(i,end='->')
        print('[]')
    def rec(syn):
        paths.append(syn)
        if len(syn.hypernyms())==0:
            print_path(paths)
        for hyp in syn.hypernyms():   
            rec(hyp)
        paths.remove(syn)
        
    paths = []
    rec(syn)
    
syn2 = wordnet.synset('cell.n.01')
f4(syn2)


# In[6]:


def f5(syn1,syn2):
    #get all possible hypernym paths to root for synset
    def f4mod(syn):
        path_list = []
        
        def rec(syn):
            paths.append(syn)
            if len(syn.hypernyms())==0:
                path_list.append(paths.copy())
            for hyp in syn.hypernyms():   
                rec(hyp)
            paths.remove(syn)
        paths = []
        rec(syn)
        return path_list

    def distance(hyp,path1,path2):
        return path1.index(hyp)+path2.index(hyp)
    

    pl1 = f4mod(syn1)
    pl2 = f4mod(syn2)
        
#     print(pl1)
#     print()
#     print(pl2)
#     print()

    # get common hypernyms of both synsets
    common_hyp=[]
    for path1 in pl1:
        for path2 in pl2:
            for i in path1:
                if i in path2:
                    common_hyp.append(i)
                    
    common_hyp=list(dict.fromkeys(common_hyp))
    
    # get the distance d1(k)+d2(k) for each hypernym in its respective path
    distances =[]
    for hyp in common_hyp:
        for path1 in pl1:
            for path2 in pl2:
                if hyp in path1:
                    if hyp in path2:
                        distances.append((hyp,distance(hyp,path1,path2)))

    # take the smallest distace
    distances.sort(key=lambda x:x[1])
    minimum = distances[0][1]
    
    # save all hypernyms that minimize the distance between the two synsets
    hyp_list = []
    for i in distances:
        if i[1]==minimum:
            hyp_list.append(i[0])
    
    return hyp_list
    
syn3 = wordnet.synset('cat.n.01')
syn4 = wordnet.synset('dog.n.01')
f5(syn3,syn4)


# In[88]:


def f6(syn,synlist):
    # one idea for this is to use the same metric we used previously,
    # namely to check the closest hypernym that pertains to both synsets
    #get all possible hypernym paths to root for synset
    def f5mod(syn1,syn2):
        def f4mod(syn):
            path_list = []

            def rec(syn):
                paths.append(syn)
                if len(syn.hypernyms())==0:
                    path_list.append(paths.copy())
                for hyp in syn.hypernyms():   
                    rec(hyp)
                paths.remove(syn)
            paths = []
            rec(syn)
            return path_list

        def distance(hyp,path1,path2):
            return path1.index(hyp)+path2.index(hyp)


        pl1 = f4mod(syn1)
        pl2 = f4mod(syn2)

        # get common hypernyms of both synsets
        common_hyp=[]
        for path1 in pl1:
            for path2 in pl2:
                for i in path1:
                    if i in path2:
                        common_hyp.append(i)

        common_hyp=list(dict.fromkeys(common_hyp))

        # get the distance d1(k)+d2(k) for each hypernym in its respective path
        distances =[]
        for hyp in common_hyp:
            for path1 in pl1:
                for path2 in pl2:
                    if hyp in path1:
                        if hyp in path2:
                            distances.append((hyp,distance(hyp,path1,path2)))

        # take the smallest distace
        distances.sort(key=lambda x:x[1])
        minimum = distances[0][1]

        # save all hypernyms that minimize the distance between the two synsets
        hyp_list = []
        for i in distances:
            if i[1]==minimum:
                hyp_list.append(i)
                
        return hyp_list[0][1]
    
    words = []
    for i in synlist:
        words.append((i, f5mod(syn,wordnet.synsets(i)[0])))
        
    words.sort(key=lambda x:x[1])
    word_list = []
    for i in words:
        word_list.append(i[0])
    
    print(word_list)

def f6v2(syn,synlist):
    # now we use wup similarity from wordnet
    
    words = []
    for i in synlist:
        words.append((i,syn.wup_similarity(wordnet.synsets(i)[0])))
        
    words.sort(key=lambda x:x[1],reverse=True)
    word_list = []
    for i in words:
        word_list.append(i[0])
    
    print(word_list)    
    
def f6v3(syn,synlist):
    # now we use path similarity from wordnet
    # by the results, it looks like this is what I implemented on f5
    words = []
    for i in synlist:
        words.append((i,syn.path_similarity(wordnet.synsets(i)[0])))
        
    words.sort(key=lambda x:x[1],reverse=True)
    word_list = []
    for i in words:
        word_list.append(i[0])
    
    print(word_list)    
    
syn5 = wordnet.synset('cat.n.01')
f6(syn5,['animal','tree','house','object','public_school','mouse','dog','feline','alien','pet'])
f6v2(syn5,['animal','tree','house','object','public_school','mouse','dog','feline','alien','pet'])
f6v3(syn5,['animal','tree','house','object','public_school','mouse','dog','feline','alien','pet'])


# In[78]:


def f7(syn1, syn2): # syn1 and syn2 are part meronyms of synk iif synk is a common part holonym
    def myholonyms(syn):
        holo,_ = f3(syn)
        return holo
    
    def allholonyms(synlist):
        newlist = []
        for i in synlist:
            newlist =newlist + myholonyms(i) 
        return  list(dict.fromkeys(synlist+newlist))
    
    def rec(syn):
        newsyn = allholonyms(syn)
        if newsyn!=syn:
            return rec(newsyn)
        else:
            return newsyn
    
    # holonym list
#     print(rec([syn1]))
#     print(rec([syn2]))
    
    if [syn for syn in rec([syn1]) if syn in rec([syn2])] !=[]:
        return True
    return False

syn6 = wordnet.synset('water.n.01')
syn7 = wordnet.synset('ground.n.01')
f7(syn6,syn7)


# In[127]:


def f8(adj):
    synonyms = []
    antonyms = []
    counter = 0
    for syn in wordnet.synsets(adj):
        counter +=1
        for l in syn.lemmas():
            synonyms.append(l.name())
            if l.antonyms():
                for i in l.antonyms():
                    antonyms.append(i.name())
    print( [list(set(synonyms)),list(set(antonyms))])
    if counter >1:
        for syn in wordnet.synsets(adj):
            print(syn.definition())
            

f8('good')

