import re
import nltk

frase = 'darlhe'
dar = 'dar'
lhe = 'lhe'
stemmer = nltk.stem.RSLPStemmer()



print(stemmer.stem(dar))
print(stemmer.stem(lhe))
print(stemmer.stem(frase))