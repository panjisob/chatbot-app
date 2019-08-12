# things we need for NLP
import nltk
from nltk.stem.lancaster import LancasterStemmer
from nltk.chunk import conlltags2tree, tree2conlltags
from nltk import word_tokenize,ne_chunk, pos_tag
stemmer = LancasterStemmer()
import requests

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
# from flask_restplus import Api, Resource, fields

# things we need for Tensorflow
import numpy as np
import tflearn
import tensorflow as tf
import random

import re
import nltk
from nltk.corpus import stopwords
stop = stopwords.words('indonesia')

import json
with open('intents.json') as json_data:
    intents = json.load(json_data)

words = []
classes = []
documents = []
ignore_words = ['?']
# loop through each sentence in our intents patterns
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # tokenize each word in the sentence
        w = nltk.word_tokenize(pattern)
        # add to our words list
        words.extend(w)
        # add to documents in our corpus
        documents.append((w, intent['tag']))
        # add to our classes list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# stem and lower each word and remove duplicates
words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))

# remove duplicates
classes = sorted(list(set(classes)))

# print (len(documents), "documents")
# print (len(classes), "classes", classes)
# print (len(words), "unique stemmed words", words)

# create our training data
training = []
output = []
# create an empty array for our output
output_empty = [0] * len(classes)

# training set, bag of words for each sentence
for doc in documents:
    # initialize our bag of words
    bag = []
    # list of tokenized words for the pattern
    pattern_words = doc[0]
    # stem each word
    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
    # create our bag of words array
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    # output is a '0' for each tag and '1' for current tag
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])

# shuffle our features and turn into np.array
random.shuffle(training)
training = np.array(training)

# create train and test lists
train_x = list(training[:,0])
train_y = list(training[:,1])

#reset underlying graph data
# tf.reset_default_graph()
# Build neural network
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)

# Define model and setup tensorboard
model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
# Start training (apply gradient descent algorithm)
model.fit(train_x, train_y, n_epoch=1000, batch_size=8)
model.save('model.tflearn')

# save all of our data structures
import pickle
pickle.dump( {'words':words, 'classes':classes, 'train_x':train_x, 'train_y':train_y}, open( "training_data", "wb" ) )

# restore all of our data structures
import pickle
data = pickle.load( open( "training_data", "rb" ) )
words = data['words']
classes = data['classes']
train_x = data['train_x']
train_y = data['train_y']

# import our chat-bot intents file
import json
with open('intents.json') as json_data:
    intents = json.load(json_data)

# load our saved model
model.load('./model.tflearn')

def clean_up_sentence(sentence):
    # tokenize the pattern
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=False):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)

    return(np.array(bag))

# create a data structure to hold user context
context = {}

def extract_phone_numbers(string):
    r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    phone_numbers = r.findall(string)
    return [re.sub(r'\D', '', number) for number in phone_numbers]

def extract_email_addresses(string):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(string)

def ie_preprocess(document):
    document = ' '.join([i for i in document.split() if i not in stop])
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    print(sentences)
    return sentences

def extract_names(document):
    names = []
    sentences = ie_preprocess(document)
    # sentences = document
    for tagged_sentence in sentences:
        for chunk in nltk.ne_chunk(tagged_sentence):
            if type(chunk) == nltk.tree.Tree:
                if chunk.label() == 'PERSON':
                    names.append(' '.join([c[0] for c in chunk]))
    return names

ERROR_THRESHOLD = 0.25
def classify(sentence):
    # generate probabilities from the model
    results = model.predict([bow(sentence, words)])[0]
    # filter out predictions below a threshold
    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    # return tuple of intent and probability
    print(return_list)
    return return_list

def check_tgl(sentence):
    ne_tree = ne_chunk(pos_tag(word_tokenize(sentence)))       
    iob_tagged = tree2conlltags(ne_tree)
    print (iob_tagged)
    for x in iob_tagged:
            if x[1] == "CD":
                    return x[0]


def response(sentence, userID='123', show_details=False):
    results = classify(sentence)
    # if we have a classification then find the matching intent tag
    if results:
        # loop as long as there are matches to process
        while results:
            for i in intents['intents']:
                # find a tag matching the first result
                if i['tag'] == results[0][0]:
                    if 'request' in i:
                        if 'get_tgl' in i['request']['action']:
                            print("get")
                            tgl = check_tgl(sentence)
                            t = tgl.replace("/","-")
                            req = i['request']['link']+t
                            print(req)
                            text = requests.get(req).json()
                            try:
                                print(text["data"][0])
                                return {"text":i['responses'][0]}
                            except:
                                print('penuh ')
                                return {"text":i['responses'][1]}
                        
                        if 'get_name' in i['request']['action']:
                            # print("get")
                            name = extract_names(sentence)
                            # t = tgl.replace("/","-")
                            req = i['request']['link']+t
                            print(req)
                            text = requests.get(req).json()
                        if 'get_email' in i['request']['action']:
                            # print("get")
                            name = extract_email_addresses(sentence)
                            # t = tgl.replace("/","-")
                            req = i['request']['link']+t
                            print(req)
                            text = requests.get(req).json()
                        if 'get_nohp' in i['request']['action']:
                            # print("get")
                            name = extract_phone_numbers(sentence)
                            # t = tgl.replace("/","-")
                            req = i['request']['link']+t
                            print(req)
                            text = requests.get(req).json()
                        else:
                            print (i['request']['link'])
                            text = requests.get(i['request']['link']).json()
                            y = ""
                            z = 0
                            while z < len(text["data"]):
                                y = y + "\n" + text["data"][z]["nama_produk"]
                                z += 1
                            resp = random.choice(i['responses'])+y
                            return {"text":resp}
                    # set context for this intent if necessary
                    if 'context_set' in i:
                        if show_details: print ('context:', i['context_set'])
                        context[userID] = i['context_set']

                    # check if this intent is contextual and applies to this user's conversation
                    if not 'context_filter' in i or \
                        (userID in context and 'context_filter' in i and i['context_filter'] == context[userID]):
                        if show_details: print ('tag:', i['tag'])
                        # a random response from the intent
                        return {"text":random.choice(i['responses'])}

            results.pop(0)
            if i['tag'] == results[0][0]:
                # set context for this intent if necessary
                if 'context_set' in i:
                    if show_details: print ('context:', i['context_set'])
                    context[userID] = i['context_set']

                # check if this intent is contextual and applies to this user's conversation
                if not 'context_filter' in i or \
                    (userID in context and 'context_filter' in i and i['context_filter'] == context[userID]):
                    if show_details: print ('tag:', i['tag'])
                    # a random response from the intent
                    return {"text":random.choice(i['responses'])}

# while True:
#     request = input('> ')
#     r = response(request)
#     print(r)

app = Flask(__name__)
api = Api(app)
app.config.from_object(__name__)
CORS(app)
# api = Api(app, version='1.0', title='Bot Api', description='An Api for Chat bot')

@app.route('/chat', methods=['POST'])
# class Book(Resource):
def post():
    # print (request.get_json())
    # return jsonify({'tasks': 'gagal'})
    if not request.json or not 'me' in request.json:
        print (request.json)
        return jsonify({'tasks': 'gagal'})
    else:
        r = response(request.json['me'])
        return jsonify(r)

if __name__ == '__main__':
    app.run(debug=True, port=9001)