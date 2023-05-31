#!/usr/bin/env python
# coding: utf-8

from collections import Counter
from textblob import TextBlob
from textblob import Word
import requests
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud 

def frekvensGenerator(text, stoppord=False, wordcloud=False, vanligaste=False, lemmatisera=False):
    """Tar ut frekvenser. Stoppord en eller sv, vanligaste tar fram de vanligaste orden"""
    if lemmatisera=="sv":
        ordlista=tokeniserareSvenska(text, lemma=True).split()
    else:
        ordlista=tokeniserareSvenska(text).split()
    if stoppord=="sv":
    	with open("stoppord.txt") as s:
    		stoppord=s.read().split()
    	ordlista=[word.lower() for word in ordlista if word.lower() not in stoppord]     
    if stoppord=="en":
    	with open("stopwords.txt") as s:
    		stoppord=s.read().split()
    	ordlista=[word.lower() for word in ordlista if word.lower() not in stoppord]
    if lemmatisera=="en":
    	ordlista=[Word(word).lemmatize() for word in ordlista if word.lower() not in stoppord]
    frekvens=Counter(ordlista)
    if vanligaste!=False:
        vanligast=frekvens.most_common(vanligaste)
        print("De hundra vanligaste orden är:",vanligast)
    if wordcloud==True:
        wcText=""
        for item in frekvens.most_common(100):
            wcText=wcText+(item[0]+" ")*item[1] 
        wordCloud(wcText)
    return frekvens
    
def stoppBort (ordlista,lang):
	 if lang=="sv":
	 	with open("stoppord.txt") as s:
	 		stoppord=s.read().split()
	 	ordlista=[word.lower() for word in ordlista if word.lower() not in stoppord]
	 if lang=="en":
	 	with open("stopwords.txt") as s:
	 		stoppord=s.read().split()
	 	ordlista=[word.lower() for word in ordlista if word.lower() not in stoppord]
	 return(ordlista)
    
def lemmatiserareSparv (text):
    url = 'https://ws.spraakbanken.gu.se/ws/sparv/v2/?settings={"positional_attributes":{"lexical_attributes":["lemma"]}}'
    myobj = text
    x=requests.post(url, data={"text":myobj})
    lemmatiserat=x.text
    meningdelat=lemmatiserat.split("</sentence>")
    textlemma=""
    for lemma in meningdelat:
        a=re.findall(">.+</w", lemma)
        b=re.findall('lemma=.+\|',lemma)
        ind=0
        for word in b:
            if len(word.split("|"))==4 and ":" not in word.split("|")[2]:
                textlemma=textlemma+ " " + word.split("|")[2]
                ind=ind+1
            elif len(word.split("|"))==3:
                textlemma=textlemma+ " " + word.split("|")[1]
                ind=ind+1
            elif len(word.split("|"))==2:
                textlemma=textlemma+" "+ a[ind][1:-3]
                ind=ind+1           
            else:
                ind=ind+1
    return textlemma


def tokeniserareSvenska (text, lemma=False, stoppord=None):
    if lemma==True:
        text=lemmatiserare(text)
    text=re.sub(r'[0-9]+','',text)
    blob=TextBlob(text)
    words=blob.words.lower()
    if stoppord=="en":
    	words=stoppBort(words, "en")
    if stoppord=="sv":
    	words=stoppBort(words, "sv")
    tokeniserad=" ".join([word for word in words if len(word)>1])
    return tokeniserad

def sentenceExtract(text,wordlist=None, unika=False):
    """Funktionen tar ut meningar ur texter. 
    Det går att specificera meningar som innehåller vissa ord, och också bestämma om man
    vill ha med dubletter eller ej"""
    blob=TextBlob(text)
    meningslista=[]
    if wordlist!=None:
        for item in wordlist:
            meningar=[str(mening.lower()) for mening in blob.sentences if item.lower() in mening.lower() and mening.lower() not in meningslista]
            meningslista.extend(meningar)
    else:
        meningslista=[str(mening.lower()) for mening in blob.sentences]
    print("Det totala antalet meningar är {}".format(len(meningslista)))
    print("Antalet unika meningar är {}".format(len(set(meningslista))))
    if unika!=True:
        return(meningslista)
    else:
        return(set(meningslista))

def wordCloud(text):
    wordcloud = WordCloud(regexp=r"\w[\w´-]+",max_font_size=100, max_words=100, background_color="black", collocations=False, stoppwords=None).generate(text)
    plt.figure(figsize=(20, 25))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

def wordCloudGenerator(text,nowords):
	"""Skapar worldcloud lämplig för publicering"""
	import random
	import matplotlib.pyplot as plt
	from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator 
    #def grey_color(word, font_size, position, orientation, random_state=None, **kwargs):
        #return 'hsl(0, 0%%, %d%%)' % random.randint(50, 100)
	wordcloud = WordCloud(regexp=r"\w[\w´-]+",max_font_size=50, max_words=nowords, colormap=None,
                          background_color="white", collocations=False, color_func=lambda *args,**kwargs: "black",
                         prefer_horizontal=1, height=200, width=400).generate(text)
    #plt.figure(figsize=(10, 15))
	plt.imshow(wordcloud, interpolation='bilinear')#wordcloud.recolor(color_func=grey_color, random_state=3)
	plt.axis("off")
	plt.savefig("WC.png", dpi=600)
	plt.show()
	return
