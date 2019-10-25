import sys
import re
import time
import nltk
import xml.etree.ElementTree as ET
from nltk.metrics.scores import accuracy
from sklearn.feature_extraction.text import TfidfVectorizer

input_type = 0

id_questions = {}
id_column = {}
corpus = []
test_cases = {}
stop_words = []
file_test = []


def setup():
    global id_questions
    global stop_words
    global file_test

    root = ET.parse(sys.argv[1]).getroot()
    column = 0

    for document in root.findall('documento'):
        for faq in document[1]:
            answer_id = faq[2].get('id')
            questions = []

            for question in faq[1]:
                raw = question.text.strip()
                if len(raw) > 0:
                    processed = preprocess(raw)
                    if len(processed) > 0:
                        questions.append(processed)

            if len(questions) > 0 and questions not in id_questions.values():
                test_cases[answer_id] = questions[-1]

                if len(questions) > 1:
                    del questions[-1]

                id_questions[answer_id] = questions

                for question in questions:
                    corpus.append(question)
                    id_column[column] = answer_id
                    column += 1

    with open('stop_words.txt', 'r', encoding='utf-8') as sw:
        for line in sw:
            stop_words.append(line)

    if input_type == 1:
        with open(sys.argv[2], 'r', encoding='utf-8') as tests:
            for test in tests.readlines():
                file_test.append(line)


def preprocess(sentence):
    stemmer = nltk.stem.RSLPStemmer()

    sentence = sentence.lower()
    #sentence = re.sub(u'[\?\.!:,;\(\)_\\\'\"ºª/]', '', sentence)
    #sentence = re.sub(u'[-]', ' ', sentence)
    sentence = ' '.join([word for word in sentence.split() if word not in stop_words])

    sentence = re.sub(u'[ãâáàÃÂÁÀ]', 'a', sentence)
    sentence = re.sub(u'[êéèÊÉÈ]', 'e', sentence)
    sentence = re.sub(u'[îíìÎÍÌ]', 'i', sentence)
    sentence = re.sub(u'[õôóòÕÔÓÒ]', 'o', sentence)
    sentence = re.sub(u'[ûúùÛÚÙ]', 'u', sentence)
    sentence = re.sub(u'[çÇ]', 'c', sentence)

    return sentence


def run_test():
    real = []
    result = []
    vectorizer = TfidfVectorizer()

    start = time.time()
    for answer_id, question in test_cases.items():
    # for t in range(1, 31):
    #     print(f'Running test {t}')
    #     answer_id = str(t)
    #     question = test_cases[answer_id]
        print(f'Running test on id {answer_id}')
        corpus.append(question)
        real.append(answer_id)
        tfidf = vectorizer.fit_transform(corpus)
        question_array = tfidf[-1, :].toarray()[0]
        best_similarity = -1
        best_id = 0

        for i in range(tfidf.shape[0] - 1):
            comparing = tfidf[i, :].toarray()[0]
            similarity = 0
            for j in range(len(question_array)):
                similarity += question_array[j] * comparing[j]
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_id = id_column[i]

        result.append(best_id)
        del corpus[-1]

    print("Accuracy:", accuracy(real, result))
    print(f'Duration: {time.time() - start}')


def main():
    setup()
    run_test()


if __name__ == '__main__':
    main()
