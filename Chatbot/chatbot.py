import sys
import re
import numpy
import xml.etree.ElementTree as ET

# 0 for user input, 1 for file input
input_type = 0
stop_words_file = 'stop_words.txt'

unprocessed_questions = {}
processed_questions = {}
questions_count = 0
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
                questions_count += 1
                questions.append(question.text)

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
    pass


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
            aux1 += biggest_vector ** 2

    denominator += numpy.sqrt(aux1) * numpy.sqrt(aux2)

    return numerator / denominator


def main():
    setup()
    preprocess()
    evaluate()


if __name__ == '__main__':
    main()
