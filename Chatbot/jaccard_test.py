import sys
import re
import numpy
import xml.etree.ElementTree as ET
import os
import nltk


#Test
import csv
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize



# 0 for user input, 1 for file input
input_type = 0
stop_words_file = 'stop_words.txt'

#unprocessed_questions = {}
#processed_questions = {}
#isto é para saber das respostas repetidas
processed_answers = {}
same_question_id={}

test_for_same_answers={}

questions_count = 0
answers = {}
test = []
stop_words = []

id_questions = {}
test_cases = {}

stopWords = []


def setup():
    global id_questions
    global questions_count
    global answers
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

            if len(questions) > 0:
                id_questions[answer_id] = questions
                answers[answer_id] = answer

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
           processed_answers[answer_id] = preprocess_sentence(answers[answer_id])

           for question in unprocessed:
               processed.append(preprocess_sentence(question))

           id_questions[answer_id] = processed

    

def preprocess_sentence(sentence):
    stemmer = nltk.stem.RSLPStemmer()
    sentence = re.sub(u'[ãâáàÃÂÁÀ]', 'a', sentence)
    sentence = re.sub(u'[êéèÊÉÈ]', 'e', sentence)
    sentence = re.sub(u'[îíìÎÍÌ]', 'i', sentence)
    sentence = re.sub(u'[õôóòÕÔÓÒ]', 'o', sentence)
    sentence = re.sub(u'[ûúùÛÚÙ]', 'u', sentence)
    sentence = re.sub(u'[çÇ]', 'c', sentence)

    sentence = sentence.lower()
    #sentence = re.sub(u'[\?\.!:,;\(\)-_\\\'\"ºª/]', '', sentence)
    #stemmer não ajuda!
    #stemmer = nltk.stem.RSLPStemmer()
    #stemmer = SnowballStemmer("portuguese")
    #Podem usar o portter e o pt e ver qual é melhor
    #sentence = stemmer.stem(sentence)
    #sentence = SnowballStemmer("porter").stem(sentence)
#    
#    sentence = sentence.split()
#    frase = []
#    
#    with open('stop_words.txt', "r") as f:
#        stopWords = f.read().split()
#    
#    for word in sentence:
#        if word.lower() not in stopWords:
#            frase.append(word)
#        fraseAux = ' '.join(frase)
#    

    return sentence


def get_jaccard_sim(str1, str2):
    a = set(str1.split())
    b = set(str2.split())
    c = a.intersection(b)
    
    return float(len(c)) / (len(a) + len(b) - len(c))
  
  
def get_dice_sim(str1, str2):
    a = set(str1.split())
    b = set(str2.split())
    c = a.intersection(b)
    
    return float(2 * len(c)) / (len(a) + len(b))
    
def get_cos_dist(X,Y):

    X_list = word_tokenize(X)
    Y_list = word_tokenize(Y)
    l1 =[];l2 =[]
    X_set = {w for w in X_list}
    Y_set = {w for w in Y_list}
    # form a set containing keywords of both strings
    rvector = X_set.union(Y_set)
    for w in rvector:
        if w in X_set: l1.append(1) # create a vector
        else: l1.append(0)
        if w in Y_set: l2.append(1)
        else: l2.append(0)
    c = 0
      
    # cosine formula
    for i in range(len(rvector)):
            c+= l1[i]*l2[i]
    cosine = c / float((sum(l1))**0.5*(sum(l2))**0.5)
    #print("similarity: ", cosine)
    return cosine



    
def save_dict_to_file(dic,name):
    f = open(name,'w')
    f.write(str(dic))
    f.close()

def load_dict_from_file(name):
    f = open(name,'r')
    data=f.read()
    f.close()
    return eval(data)

    

def compare_same_questions(processed_questions, processed_answers):
    if(os.path.isfile('./compare_same_questions.txt') ):
        same_question_id = load_dict_from_file('compare_same_questions.txt')
        test_for_same_answers = load_dict_from_file('test_for_same_answers.txt')
    else:
        samex=[]
        samei = []
        same_question_id = {}
        test_for_same_answers ={}
        for x in processed_questions:
            for y in processed_questions[x]:
                for i in processed_questions:
                    for j in processed_questions[i]:
                        if(x != i):
                            try:
                                jac= get_jaccard_sim(y,j)
                                if( jac> 0.9 and i not in samex and i not in samei ):
                                    test_for_same_answers[i] = x
                                    jac_answer = get_jaccard_sim(processed_answers[str(i)],processed_answers[str(x)])
                                    if (jac_answer<0.8):
                                        #print(str(x)+' : '+str(i)+'  jac: '+str(jac)+' jac answer: '+ str(jac_answer))
                                        try:
                                            if (same_question_id[str(x)] < 1):
                                                same_question_id[str(x)] = 0
                                        except:
                                            same_question_id[str(x)] = 0
                                        try:
                                            if (same_question_id[str(i)] < 1):
                                                same_question_id[str(i)] = 0
                                        except:
                                            same_question_id[str(i)] = 0
                                    if (jac_answer >= 0.8):
                                        try:
                                            same_question_id[str(x)] +=1
                                        except:
                                            same_question_id[str(x)] =1
                                        try:
                                            same_question_id[str(i)] +=1
                                        except:
                                            same_question_id[str(i)] =1
                                        #print(str(x)+' : '+str(i)+'  jac: '+str(jac)+' jac answer: '+ str(jac_answer))
                                    samex.append(x)
                                    samei.append(i)
                                    #print(str(jac)+'\n'+j+'\n\n'+y+'\n\n\n')
                            except:
                                pass
                                
        save_dict_to_file(same_question_id,'compare_same_questions.txt')
        save_dict_to_file(test_for_same_answers,'test_for_same_answers.txt')
   
    #print(test_for_same_answer)
    
    #samex = set(samex)
    #print(samex)
    #samei = set(samei)
    #print(samei)



def weighted_score(id_questions,processed_answers, user_input):
    
    min_score = 0.44
   
    max_question = 0
    max_answer = 0
    max_score = 0
    id_max_score = 0
    score_answer ={}
    score_question = {}
    score={}
    
    for id in id_questions:
        processed = id_questions[id]
        
        max_question = 0
        for question in processed:
            
            jac_question = get_jaccard_sim(user_input,question)#+ textdistance.ratcliff_obershelp(user_input, question) #use for 2% more add this to report
            if (max_question < jac_question):
                    max_question = jac_question
            score_question[id] = max_question
    
    for ida in id_questions:
        score[ida] =  score_question[ida]
        if(max_score < score[ida]):
            max_score = score[ida]
            id_max_score = ida
    #print(str(max_score)+' for question id: '+str(id_max_score)+"\n")
        if(max_score< min_score):
            id_max_score = str(0)
    return (max_score,id_max_score)
    



def Read_Two_Column_File(file_name):
        with open(file_name, 'r') as f_input:
            csv_input = csv.reader(f_input, delimiter=',', skipinitialspace=True)
            x = []
            y = []
            for cols in csv_input:
                x.append(cols[0])
                y.append(cols[1])

        return x, y

def setup_test():
    global test_cases
    global id_questions

    for answer_id, questions in id_questions.items():
        test_cases[answer_id] = questions[-1]
        if len(questions) > 1:
            del questions[-1]
 
 
def Test_accuracy():

    right = 0
    total = 0
    accuracy = 0
    
    #print(test_cases)
    
    for answer_id, question in test_cases.items():
        Max_score = weighted_score(id_questions,processed_answers,question)
        same_thing = 0
        same_thing0 = 0
        total+=1
             
        try:
            test_for_same_answers = load_dict_from_file('test_for_same_answers.txt')
            same_thing = test_for_same_answers[str(answer_id)]
        except:
            pass
        try:
            test_for_same_answers = load_dict_from_file('test_for_same_answers.txt')
            #print(test_for_same_answers[str(Max_score[1])])
            same_thing0 = test_for_same_answers[str(Max_score[1])]
            
        except:
            pass
       
        #print('Result: '+str(Max_score[1]) +' Theoric: ' +str(answer_id)+ ' , '+ str(same_thing)+ ' , '+ str(same_thing0))
        if( Max_score[1] == answer_id or Max_score[1] == same_thing or answer_id == same_thing0):
            right +=1
        #else:
            #print('failed')
        
        #print(question+'\n')
#        try:
#            #print(id_questions[Max_score[1]][0])
#        except:
#            pass
        print(str(Max_score)+'\n\n')
            
    accuracy=right/total
                    
    print('Accuracy: '+ str(accuracy))
            
    

def Test_accuracy_txt():
    x, y = Read_Two_Column_File('test.txt')
    test_for_same_answers = load_dict_from_file('test_for_same_answers.txt')
    right = 0
    for i in range(len(y)):
        processed = preprocess_sentence(y[i])
        Max_score = weighted_score(id_questions,processed_answers,processed)
        
        same_thing = 0
        same_thing0 = 0
        
        
        print(y[i]+'\n')
        print(processed+'\n')
        try:
            print(id_questions[Max_score[1]][0])
        except:
            pass
        print(str(Max_score)+'\n\n')
        
        try:
            test_for_same_answers = load_dict_from_file('test_for_same_answers.txt')
            same_thing = test_for_same_answers[str(x[i])]
        except:
            pass
        try:
            test_for_same_answers = load_dict_from_file('test_for_same_answers.txt')
            print(test_for_same_answers[str(Max_score[1])])
            same_thing0 = test_for_same_answers[str(Max_score[1])]
            
        except:
            pass
       
        print('Result: '+str(Max_score[1]) +' Theoric: ' +str(x[i])+ ' , '+ str(same_thing)+ ' , '+ str(same_thing0))
        if( Max_score[1] == x[i] or Max_score[1] == same_thing or x[i] == same_thing0 ):
            right +=1
        else:
            print('failed')
            
    print('Accuracy: '+ str(right/len(y)))
    
    
def Test_txt():
    x, y = Read_Two_Column_File('test_mail.txt')
    test_for_same_answers = load_dict_from_file('test_for_same_answers.txt')
    right = 0
    for i in range(len(y)):
        processed = preprocess_sentence(y[i])
        Max_score = weighted_score(id_questions,processed_answers,processed)
        
        print(y[i]+'\n')
        print(processed+'\n')
        try:
            print(id_questions[Max_score[1]][0])
            #print(answers[Max_score[1]])
        except:
            pass
        print(str(Max_score)+'\n\n')
        





def main():
    import time
    start_time = time.time()
    
    setup()
    preprocess()
    setup_test() # retirar se não for para testar
    
    
    compare_same_questions(id_questions,processed_answers) # change to processed_questions if not in test
    
    
    Test_accuracy()
    #Test_txt()
    
    
    ##test if user string is null or ''
    ## process user input
    
    
    elapsed_time = time.time() - start_time
    print('Seconds to process:'+str(elapsed_time))

if __name__ == '__main__':
    main()
