import re
import nltk
import numpy
from sklearn.feature_extraction.text import TfidfVectorizer
import string

test = 'abc \?\.!:,;\(\)-_\\\'\"ºª/ def'
print(test)
print(test.translate(str.maketrans('', '', string.punctuation)))

# corpus = ['This is the first document.', 'This document is the second document.', 'And this is the third one.', 'Is this the first document?']
#corpus = ['This is the first document.', 'This document is the second document.']
# vectorizer = TfidfVectorizer()
# corpus.append(input('Enter your input:\n'))
# x = vectorizer.fit_transform(corpus)

# last = x[-1,:].toarray()[0]
# print(last)
# print(x.shape)
# best = -1
# best_id = 0
# for i in range(x.shape[0] - 1):
#     print(i)
#     compare = x[i,:].toarray()[0]
#     similarity = 0
#     for j in range(len(last)):
#         similarity += last[j] * compare[j]
#         if similarity > best:
#             best = similarity
#             best_id = i
# print(f'Melhor id = {best_id}')
# print(f'Similaridade = {best}')
# print(vectorizer.get_feature_names())
# for i in range(X.shape[0]):
#     for j in range(X.shape[1]):
#         print(f'({i}, {j}): {X[(i, j)]}')

# a1 = [1, 3, 1]
# a2 = [2, 2]

# d = {'asd': 44, '333': -1}

# f = 'a bb ccc dddd'

# print(f.split())