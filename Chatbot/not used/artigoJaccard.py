import sys
import re
import numpy
import xml.etree.ElementTree as ET
import os


# 0 for user input, 1 for file input
input_type = 0
stop_words_file = 'stop_words.txt'

unprocessed_questions = {}
processed_questions = {}
#isto é para saber das respostas repetidas
processed_answers = {}
same_question_id={}

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
        processed_answers[id] = preprocess_sentence(answers[id])
        

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


def get_jaccard_sim(str1, str2):
    a = set(str1.split())
    b = set(str2.split())
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))
    


    
def save_dict_to_file(dic):
    f = open('compare_same_questions.txt','w')
    f.write(str(dic))
    f.close()

def load_dict_from_file():
    f = open('compare_same_questions.txt','r')
    data=f.read()
    f.close()
    return eval(data)

    

def compare_same_questions(processed_questions, processed_answers):
    if(os.path.isfile('./compare_same_questions.txt') ):
        same_question_id = load_dict_from_file()
    else:
        samex=[]
        samei = []
        same_question_id = {}
        for x in processed_questions:
            for y in processed_questions[x]:
                for i in processed_questions:
                    for j in processed_questions[i]:
                        if(x != i):
                            try:
                                jac= get_jaccard_sim(y,j)
                                if( jac> 0.9 and i not in samex and i not in samei ):
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
                                
        save_dict_to_file(same_question_id)
                        
    #samex = set(samex)
    #print(samex)
    #samei = set(samei)
    #print(samei)

def weighted_score(processed_questions,processed_answers, user_input):
   
    max_question = 0
    max_answer = 0
    max_score = 0
    id_max_score = 0
    score_answer ={}
    score_question = {}
    score={}
    for id in processed_questions:
        processed = processed_questions[id]
        
        score_answer[id] = get_jaccard_sim(user_input,processed_answers[id])
        max_question = 0
        for question in processed:
            jac_question = get_jaccard_sim(user_input,question)
            if (max_question < jac_question):
                max_question = jac_question
        score_question[id] = max_question
        
    for i in processed_questions:
        try:
            same_question_id[i]+=1
            same_question_id[i]-=1
        except:
            same_question_id[i]=1
    
    #print(same_question_id)
    #print(score_answer)
    #print(score_question)
    for ida in processed_questions:
        score[ida] = score_answer[ida]*0.3 +  score_question[ida]*0.4 + same_question_id[ida]* 0.3
        #print( ida + '[ score_answer: '+ str(score_answer[ida]) +', score_question: '+ str(score_question[ida])+ ', same_question_id: '+ str(same_question_id[ida])+' ]')
        if(max_score < score[ida]):
            max_score = score[ida]
            id_max_score = ida
    #print(str(max_score)+' for question id: '+str(id_max_score)+"\n")
    return (max_score,id_max_score)
    
    


def main():
    import time
    start_time = time.time()

    setup()
    preprocess()
    
    compare_same_questions(processed_questions,processed_answers)
    ##test if user string is null or ''
    ## process user input
    
#    for id in processed_questions:
#        processed = processed_questions[id]
#        for question in processed:
#            if(int(id)<=50 and len(question)>=1 and not question.isspace() ):
#                print(id + ': ')
#                print('user input: '+ question)
#                weighted_score(processed_questions,processed_answers,question)
    processed = preprocess_sentence('Quando indicar representante efeitos tributários?')

    print(weighted_score(processed_questions,processed_answers,processed))

    #for i in range(50):
     #   i+=1
      #  weighted_score(processed_questions,processed_answers,processed_questions[i][1])
    
    #weighted_score(processed_questions,processed_answers, 'Pode ser emitido Cartão Eletrónico da Empresa ou de Pessoa Coletiva às entidades titulares de Cartão Definitivo de Identificação de Pessoa Coletiva ou entidade equiparada, emitido antes do dia 31/12/2008 ou inscritas anteriormente a essa data?')
   
    
    elapsed_time = time.time() - start_time
    print('Seconds to process:'+str(elapsed_time))

if __name__ == '__main__':
    main()
