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

id_questions = {}
questions_count = 0
test = []
stop_words = []


def setup():
    global id_questions
    global questions_count
    global test
    global stop_words

    root = ET.parse(sys.argv[1]).getroot()

    for document in root.findall('documento'):
        for faq in document[1]:
            answer_id = faq[2].get('id')
            answer = faq[2].text
            questions = []

            for question in faq[1]:
                q = question.text.strip()
                if len(q) > 0:
                    questions_count += 1
                    questions.append(q)

            id_questions[answer_id] = questions

    with open(stop_words_file, 'r', encoding='utf-8') as swf:
        for line in swf:
            stop_words.append(line)

    if input_type == 1:
        with open(sys.argv[2], 'r', encoding='utf-8') as tests:
            for line in tests.readlines():
                test.append(line)


def preprocess():
    for answer_id, questions in id_questions.items():
        unprocessed = id_questions[answer_id]
        processed = []

        for question in unprocessed:
            processed.append(preprocess_sentence(question))

        id_questions[answer_id] = processed


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
    column_id = {}
    column = 0
    corpus = []

    for answer_id, questions in id_questions.items():
        for question in questions:
            corpus.append(question)
            column_id[column] = answer_id
            column += 1

    corpus.append(preprocess_sentence(input('Enter your input:\n')))

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    user_input = tfidf_matrix[-1, :].toarray()[0]
    best_similarity = -1
    best_id = 0

    for i in range(tfidf_matrix.shape[0] - 1):
        comparing = tfidf_matrix[i, :].toarray()[0]
        similarity = 0
        for j in range(len(user_input)):
            similarity += user_input[j] * comparing[j]
            if similarity > best_similarity:
                best_similarity = similarity
                best_id = column_id[i]

    print(f'Melhor id = {best_id}')
    print(f'Similaridade = {best_similarity}')


def main():
    setup()
    preprocess()
    evaluate()


if __name__ == '__main__':
    main()
