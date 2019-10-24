import sys
import re
import numpy
import xml.etree.ElementTree as ET
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time

# 0 for user input, 1 for file input
input_type = 0
stop_words_file = 'stop_words.txt'

unprocessed_questions = {}
processed_questions = {}
questions_count = 0
tf_id_normalized = {}
tf_list = {}
idf_list = {}
answers = {}
test = []
stop_words = []


def setup():
    global unprocessed_questions
    global questions_count
    global answers
    global test
    global stop_words

    root = ET.parse(sys.argv[1]).getroot()

    for document in root.findall('documento'):
        for faq in document[1]:
            id = faq[2].get('id')
            answer = faq[2].text
            questions = []

            for question in faq[1]:
                q = question.text.strip()
                if len(q) > 0:
                    questions_count += 1
                    questions.append(q)

            unprocessed_questions[id] = questions
            answers[id] = answer

    with open(stop_words_file, 'r', encoding='utf-8') as swf:
        for line in swf:
            stop_words.append(line)

    if input_type == 1:
        with open(sys.argv[2], 'r', encoding='utf-8') as tests:
            for line in tests.readlines():
                test.append(line)


def preprocess():
    for id in unprocessed_questions:
        unprocessed = unprocessed_questions[id]
        processed = []

        for question in unprocessed:
            processed.append(preprocess_sentence(question))

        processed_questions[id] = processed


def preprocess_sentence(sentence):
    sentence = re.sub(u'[ãâáàÃÂÁÀ]', 'a', sentence)
    sentence = re.sub(u'[êéèÊÉÈ]', 'e', sentence)
    sentence = re.sub(u'[îíìÎÍÌ]', 'i', sentence)
    sentence = re.sub(u'[õôóòÕÔÓÒ]', 'o', sentence)
    sentence = re.sub(u'[ûúùÛÚÙ]', 'u', sentence)
    sentence = re.sub(u'[çÇ]', 'c', sentence)

    sentence = sentence.lower()
    sentence = re.sub(u'[\?\.!:,;\(\)-_\\\'\"ºª/]', '', sentence)

    return sentence


def evaluate():
    sentence = input('Enter your input:\n')
    sentence = preprocess_sentence(sentence)
    vector = tf_idf_vector(sentence)
    closest_id = 0
    best_similarity = 0

    for k, v in processed_questions.items():
        print(f'testing questions {k}')
        for s in v:
            vec = tf_idf_vector(s)
            similarity = cosine_similarity(vector, vec)
            if similarity > best_similarity:
                closest_id = k
                best_similarity = similarity

    print('Best id: ' + closest_id)


def testlib():
    corpus = []
    column_id = {}
    column = 0

    for id_answer, question_set in processed_questions.items():
        for question in question_set:
            corpus.append(question)
            column_id[column] = id_answer
            column += 1

    sentence = input('Enter your input:\n')
    sentence = preprocess_sentence(sentence)
    corpus.append(sentence)
    vectorizer = TfidfVectorizer()
    x = vectorizer.fit_transform(corpus)
    last = x[-1,:].toarray()[0]
    print(last)
    best = -1
    best_id = 0
    for i in range(x.shape[0] - 1):
        compare = x[i,:].toarray()[0]
        similarity = 0
        for j in range(len(last)):
            similarity += last[j] * compare[j]
            if similarity > best:
                best = similarity
                best_id = column_id[i]
    
    print(f'Melhor id = {best_id}')
    print(f'Similaridade = {best}')

    # k = 0
    # start = time.time()
    # with open('damn.txt', 'r', encoding='utf-8') as damn:
    #     for line in damn.readlines():
    #         corpus.append(line)
    #         x = vectorizer.fit_transform(corpus)
    #         print(str(k) + str(x.shape))
    #         k += 1
    #         del corpus[-1]

    # print(str(time.time() - start))


def tf(word, sentence):
    if sentence not in tf_list:
        vector = sentence.split()
        tf = {}

        for word in vector:
            tf[word] = vector.count(word) / len(vector)

        tf_list[sentence] = tf

    return tf_list[sentence]


def idf(word):
    if word not in idf_list:
        ocurrences = 1

        for question_set in processed_questions.values():
            for question in question_set:
                if word in question.split():
                    ocurrences += 1

        idf_list[word] = numpy.log10((questions_count + 1) / ocurrences)

    return idf_list[word]


def tf_idf_vector(sentence):
    vector = []
    sentence_vector = sentence.split()

    for word in sentence_vector:
        tf = sentence_vector.count(word) / len(sentence_vector)
        occurence = 1

        for questions_array in processed_questions.values():
            for question in questions_array:
                if word in question.split():
                    occurence += 1

        idf = numpy.log10(questions_count / occurence)
        vector.append(tf * idf)

    return vector


def cosine_similarity(vector1, vector2):
    biggest_vector = vector1 if len(vector1) >= len(vector2) else vector2
    smallest_vector = vector1 if len(vector1) < len(vector2) else vector2
    numerator = 0
    denominator = 0
    aux1 = 0
    aux2 = 0

    for i in range(len(biggest_vector)):
        if i < len(smallest_vector):
            numerator += biggest_vector[i] + smallest_vector[i]
            aux1 += biggest_vector[i] ** 2
            aux2 += smallest_vector[i] ** 2
        else:
            aux1 += biggest_vector[i] ** 2

    denominator += numpy.sqrt(aux1) * numpy.sqrt(aux2)

    return numerator / denominator


def main():
    setup()
    preprocess()
    # evaluate()
    testlib()


if __name__ == '__main__':
    main()
    # setup()
    # frase1 = 'no actual momento qual versao da cae em vigor'
    # frase2 = 'O que devo fazer para ser certificado? Que documentos me são exigidos?'
    # frase3 = 'Que passos devo seguir para ser certificado? Que documentação me é exigida?'
    # frase4 = 'Quais os documentos que preciso de apresentar e o que é que devo fazer para ser certificado?'
    # frase5 = 'Para ser certificado, o que é que eu devo fazer? São me exigidos que documentos?'

    # tf1 = tf_idf_vector(frase1)
    # tf2 = tf_idf_vector(frase2)
    # tf3 = tf_idf_vector(frase3)
    # tf4 = tf_idf_vector(frase4)
    # tf5 = tf_idf_vector(frase5)

    # print(cosine_similarity(tf1, tf2))
    # print(cosine_similarity(tf1, tf3))
    # print(cosine_similarity(tf1, tf4))
    # print(cosine_similarity(tf1, tf5))
