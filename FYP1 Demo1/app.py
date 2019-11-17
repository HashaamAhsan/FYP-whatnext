from flask import Flask, request, jsonify, render_template
import os
import dialogflow
import requests
import json
import pusher
import random 

app = Flask(__name__)

check = "0"
surveystart = 0

class Score:
    Openness = 0.0
    Conscientiousness = 0.0
    Extraversion = 0.0
    Agreeableness = 0.0
    Neuroticism = 0.0
     
    def __init__(self):
        Openness = 0.0
        Conscientiousness = 0.0
        Extraversion = 0.0
        Agreeableness = 0.0
        Neuroticism = 0.0

    def ADD(self,marks,personality):
        if (personality == "O"):
            Openness = Openness + marks 
        elif (personality == "C"):
            Conscientiousness = Conscientiousness + marks 
        elif (personality == "E"):
            Extraversion = Extraversion + marks 
        elif (personality == "A"):
            Agreeableness = Agreeableness + marks 
        elif (personality == "N"):
            Neuroticism = Neuroticism + marks 

class Questions:
    Openness = 0.0
    Conscientiousness = 0.0
    Extraversion = 0.0
    Agreeableness = 0.0
    Neuroticism = 0.0  
     
    def __init__(self):
        Openness = 0
        Conscientiousness = 0
        Extraversion = 0
        Agreeableness = 0
        Neuroticism = 0

    def getO(self):
        x = random.randrange(1, 10, 1)
        return ("Qno1."+ str(x))
    def getC(self):
        x = random.randrange(1, 10, 1)
        return ("Qno2."+ str(x))
    def getE(self):
        x = random.randrange(1, 10, 1)
        return ("Qno3."+ str(x))
    def getA(self):
        x = random.randrange(1, 10, 1)
        return ("Qno4."+ str(x))
    def getN(self):
        x = random.randrange(1, 10, 1)
        return ("Qno5."+ str(x))
        

s = Score()   
q = Questions()

@app.route('/')
def index():
    while True:
        if (check == "0"):
            return render_template('Chatbot.html',check = "0")
        if (check == "1"):
            return render_template('Chatbot.html',check = "1")

def detect_intent_texts(project_id, session_id, text, language_code):
    global surveystart
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        print (str(surveystart) + "User side")
        if (surveystart == 1):
            print ("start survey")
            text = q.getO()
            print (text)
        text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        print (query_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)
        print (response)
        return response.query_result.fulfillment_text

@app.route('/result',methods=['POST'])
def result():
    return render_template('Chatbot.html', check = "1")

@app.route('/send_message', methods=['POST'])
def send_message():
    global surveystart
    message = request.form['message']
    project_id = "testagent-ikborl"
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
    if fulfillment_text == "Name 3 subject in which you have scored highest?":
        print ("drop down show")
        check = "1"
    print (str(surveystart) + "botside")
    if (fulfillment_text == "ahmmmm .... okay so now i am gonna ask you some questions relax, you are not getting marked for it! So are you ready?"):
        print ("Startinggggg sruvey")
        surveystart = 1
    response_text = { "message":  fulfillment_text }
    return jsonify(response_text)
    
# run Flask app
if __name__ == "__main__":
    app.run()
