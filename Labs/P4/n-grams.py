# -*- coding: utf-8 -*-
import os, re, codecs
from random import randrange

# Takes as input the name of a file in which each line has the form:
# NUM n-gram
def extrai(nameFile):
	file = open(nameFile, 'rU')
	freqs = [] # keep frequencies
	ngrams = [] # keep n-grams
	for line in file:
		field = re.search(r"(\d+)\s+(.+)", line)
		if field is None:
			print("Asneira com ", line)
		else:
			freq = field.group(1)
			ngram = field.group(2)
			freqs.append(freq)
			ngrams.append(ngram)
	file.close()
	return freqs, ngrams

# Faz o print de uma lista
def print_list(list):
	j = 0
	while j < len(list):
		print (list[j])
		j = j + 1

# search for the frequency of a n-gram
def searchFreq(ngrams, freqs, seq):
	if seq in ngrams:
		index = ngrams.index(seq) # 
		return freqs[index]
	else:
		return 0

# Find: prob(ab) = count(ab)/count(a)
def	prob(seq):
	freqFirstWord = searchFreq(unigrams, uniFreq, seq.split(' ')[0])
	freqSeq = searchFreq(bigrams, biFreq, seq)
	if int(freqFirstWord) == 0: # unknown word
		return 0
	else:
		return int(freqSeq)/int(freqFirstWord)


# Calculates n-grams
uniFreq, unigrams = extrai('contagensUnigramas.txt')
biFreq, bigrams = extrai('contagensBigramas.txt')
triFreq, trigrams = extrai('contagensTrigramas.txt')

# ------> Finds the probability of a sentence
sentence = "alice said the king"

words = sentence.split(' ')
index = 0
probability = 1
while (index + 1) < len(words):
	probability *= prob(words[index]+' '+words[index+1])
	index += 1

print("Probability of --", sentence, "-- is", probability)

# ------> Generates sentences of a pre defined size from a trigger word (see below)
# Check possible next words
def showsNext(word):
	result = [bigram for bigram in bigrams if bigram.startswith(word)]
	#print(result)
	return result

trigger = "alice"
size = 5

index = 0
fraseGerada = trigger
while (index < size):
	results = showsNext(trigger)
	random_index = randrange(len(results))
	triggerAux = results[random_index]
	fraseGerada = fraseGerada+' '+ triggerAux.split(' ')[1]
	trigger = triggerAux.split(' ')[1]
	print("Sentence being generated:", fraseGerada)
	index += 1
