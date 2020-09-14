from flask import Flask
from flask import request, jsonify
import json,os,string
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity



#Import the file with my swahii keyword
with open('intents.JSON' ,'r') as file1:
    key_data = json.load(file1)
    keys_data = list(key_data.keys())

#Import the file with swahili stopword
with open('stopword.JSON','r') as file2:
    stopword_data = json.load(file2)

#A function to remove stopwords
def remove_mystopwords(sentence):
    tokens = sentence.split(" ")
    tokens_filtered= [word for word in tokens if not word in stopword_data]
    return (" ").join(tokens_filtered)

#Instatiate an app for my chatbot

app = Flask(__name__)

@app.route("/", methods = ["POST","GET"])
def ask():
  
    question  = request.get_json()["question"].lower()                                               #Get user's input
    filtered_text = remove_mystopwords(question)                                                     #Remove stopwords from the user's input
    after_puctuation = filtered_text.translate(str.maketrans('', '', string.punctuation)).strip()    #Remove puctuation marks
    final_ans = bot_responses(after_puctuation)                                                      # call a fxn to find similarity of the user input 
    if final_ans== "Sijakuelewa":                                                                    #Returned if word doesnt match any
        return "Samahani, sijakuelewa. Naomba uliza tena"
    else:                                                                                            #if match found, return its value
        test_ = key_data[final_ans]
        return test_

#########################################################

#Function to sort the index from similarity scores list
def index_sort(list_var):
    length = len(list_var)
    list_index = list(range(0,length))
    
    x = list_var
    for i in range (length):
        for j in range(length):
            if x[list_index[i]] > x[list_index[j]]:
                #swap
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp
                
    return list_index
#A fuction to vectorize user input and find the best match answer  from key_data database
def bot_responses(val):
    user_input = val
    sentence_list = keys_data
    sentence_list.append(user_input)
    
    bot_response = '' 
    cm  = CountVectorizer().fit_transform(sentence_list)
    # get the similarity score
    similarity_scores = cosine_similarity(cm[-1], cm)
    similarity_scores_list = similarity_scores.flatten()

    #get index of highest score
    index = index_sort(similarity_scores_list)
    index = index[1:]
    response_flag = 0
 
    #for counting the number of scores that are above 0
    j = 0

    for i in range(len(index)):
        if similarity_scores_list[index[i]] > 0.0:
            bot_response = sentence_list[index[i]]
            response_flag = 1   #I found a response
            
            j = j+1             #How many scores above 0
            
        if j > 2:
            break
    if response_flag == 0:      #did not find similar sentence
        bot_response = "Sijakuelewa"

    sentence_list.remove(user_input)

    return bot_response


    

    
