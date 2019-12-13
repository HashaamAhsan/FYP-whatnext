from flask import Flask, request, jsonify, render_template
import os
import dialogflow
import requests
import json
import pusher
import random 
from queue import Queue 
app = Flask(__name__)

check = "0"
surveystart = 0

class Score:     
    def __init__(self):
        self.Openness = 0.0
        self.Conscientiousness = 0.0
        self.Extraversion = 0.0
        self.Agreeableness = 0.0
        self.Neuroticism = 0.0
        self.Subjects=[]

    def ADD(self,marks,personality):
        if (personality == "O"):
            self.Openness = self.Openness + marks 
        elif (personality == "C"):
            self.Conscientiousness = self.Conscientiousness + marks 
        elif (personality == "E"):
            self.Extraversion = self.Extraversion + marks 
        elif (personality == "A"):
            self.Agreeableness = self.Agreeableness + marks 
        elif (personality == "N"):
            self.Neuroticism = self.Neuroticism + marks

    def ADDsubjects(self,s):
        self.Subjects.append(s)
        print(self.Subjects)
    def getjobs(self):
        s="\n"
        if (self.Openness>5):
            if ("math" in self.Subjects or "Math" in self.Subjects):
                s+="Architect,\nAstronomer,\n"
            if ("english" in self.Subjects or "urdu" in self.Subjects or "English" in self.Subjects or "Urdu" in self.Subjects):
                s+="Travel agent,\n"
            if ("chemistry" in self.Subjects or "Chemistry" in self.Subjects):
                s+="Chef,\nPainter,\n"
            if ("physics" in self.Subjects or "Physics" in self.Subjects):
                s+="Designer,\n"    
        if (self.Conscientiousness>5):
            if ("math" in self.Subjects or "Math" in self.Subjects):
                s+="Accountant,\nPilot,\n"
            if ("english" in self.Subjects or "urdu" in self.Subjects or "English" in self.Subjects or "Urdu" in self.Subjects):
                s+="Judge,\nPoliceman/Policewoman,\nSoldier\nFireman,\n"
            if ("chemistry" in self.Subjects or "Chemistry" in self.Subjects):
                s+="Farmer,\n" 
            if ("physics" in self.Subjects or "Physics" in self.Subjects):
                 s+="Engineer,\nOptician,\n"
            if ("biology" in self.Subjects or "Biology" in self.Subjects):
                s+="Dentist,\nDoctor,\nPharmacist,\n"
        if (self.Extraversion>5):
            if ("english" in self.Subjects or "urdu" in self.Subjects or "English" in self.Subjects or "Urdu" in self.Subjects):
                s+="Actor/Actress,\nJournalist,\nModel,\nNewsreader,\nPolitician,\nReceptionist,\nShop assistant,\nTranslator,\n"
            if ("biology" in self.Subjects or "Biology" in self.Subjects):
                s+="Lifeguard,\n"
        if (self.Agreeableness>5):
            if ("english" in self.Subjects or "urdu" in self.Subjects or "English" in self.Subjects or "Urdu" in self.Subjects):
                s+="Real estate agent,\nSecretary,\n"
            if ("biology" in self.Subjects or "Biology" in self.Subjects):
                s+="Nurse,\n"
            s+="Lecturer,\nTeacher,\n"
        s=s[:-2]
        return s
    def Display(self):
        print("O: "+str(self.Openness)+" C: "+str(self.Conscientiousness)+" E: "+str(self.Extraversion)+" A: "+str(self.Agreeableness)+" N: "+str(self.Neuroticism)+"\n") 

class Questions:  
    def __init__(self):
        self.threshO=0
        self.threshC=0
        self.threshE=0
        self.threshA=0
        self.threshN=0
        self.eval=Score()
        self.prev="None"
        self.prevq = [""]
        self.subject=-1
        self.falseintent=False

    def getO(self):
        while True:
            x = random.randrange(1, 31, 1)
            s="Qno1."+ str(x)
            if s in self.prevq:
                print(s+" already exist")
            else:
                self.prevq.append(s)
                return s
                break
        
    def getC(self):
        while True:
            x = random.randrange(1, 30, 1)
            s="Qno2."+ str(x)
            if s in self.prevq:
                print(s+" already exist")
            else:
                self.prevq.append(s)
                return s
                break
    def getE(self):
        while True:
            x = random.randrange(1, 27, 1)
            s="Qno3."+ str(x)
            if s in self.prevq:
                print(s+" already exist")
            else:
                self.prevq.append(s)
                return s
                break
    def getA(self):
        while True:
            x = random.randrange(1,29 , 1)
            s="Qno4."+ str(x)
            if s in self.prevq:
                print(s+" already exist")
            else:
                self.prevq.append(s)
                return s
                break
    def getN(self):
        while True:
            x = random.randrange(1, 29, 1)
            s="Qno5."+ str(x)
            if s in self.prevq:
                print(s+" already exist")
            else:
                self.prevq.append(s)
                return s
                break
    def getquestion(self):
        while True:
            x = random.randrange(1, 6, 1)
            if (x==1 and self.threshO<2):
                self.threshO+=1
                return self.getO()
            elif (x==2 and self.threshC<2):
                self.threshC+=1
                return self.getC()
            elif (x==3 and self.threshE<2):
                self.threshE+=1
                return self.getE()
            elif (x==4 and self.threshA<2):
                self.threshA+=1
                return self.getA()
            elif (x==5 and self.threshN<2):
                self.threshN+=1
                return self.getN()
            elif (self.threshO>=2 and self.threshC>=2 and self.threshE>=2 and self.threshA>=2 and self.threshN>=2):
                return "Done"
    def setanswer(self,sc,quest):
        if (quest[0:4]== "Qno1"):
            self.eval.ADD(sc,"O")
        if (quest[0:4]== "Qno2"):
            self.eval.ADD(sc,"C")
        if (quest[0:4]== "Qno3"):
            self.eval.ADD(sc,"E") 
        if (quest[0:4]== "Qno4"):
            self.eval.ADD(sc,"A") 
        if (quest[0:4]== "Qno5"):                               
            self.eval.ADD(sc,"N")  
    def Add_Subjects(self,sub):
        self.eval.ADDsubjects(sub)
    def Displaythresh(self):
        print ("O: "+str(self.threshO)+" C: "+str(self.threshC)+" E: "+str(self.threshE)+" A: "+str(self.threshA)+" N: "+str(self.threshN)+"\n")
    def Displayscore(self):
        self.eval.Display()
    def getprofession(self):
        return self.eval.getjobs()
        

s = Score()   
q = Questions()


@app.route('/')
def index():
    while True:
        if (check == "0"):
            return render_template('Chatbot.html',check = "0")
        if (q.subject == 0):
            return render_template('Chatbot.html',check = "1")

def detect_intent_texts(project_id, session_id, text, language_code):
    global surveystart
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        if q.falseintent == True:
            q.falseintent=False
        #print (str(surveystart) + "User side")
        if (q.subject >=0 and q.subject <3):
            print (text+ ": subject")
            q.Add_Subjects(text)
            q.subject+=1
        if surveystart == 1 and q.prev!="None":
            print (text)
            mark=0.0
            if text == "yes" or text == "yeah":
                mark=5
                q.setanswer(float(mark),q.prev)
                q.Displaythresh()
                q.Displayscore()
            elif text == "no" or text == "nah":
                mark=1
                q.setanswer(float(mark),q.prev)
                q.Displaythresh()
                q.Displayscore()
            elif text=="maybe" or text=="somewhat" or text=="sometimes":
                mark=3
                q.setanswer(float(mark),q.prev)
                q.Displaythresh()
                q.Displayscore()
            else:
                q.falseintent=True
        if (surveystart == 1 and q.falseintent==False):
            print ("start survey")
            text = q.getquestion()
            q.prev=text
            if (text == "Done"):
                text = "Qno6"
            #print (text)
        text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        print (query_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)
        print ("+++++"+response.query_result.fulfillment_text+"+++++")
        if (text=="Qno6"):
            return response.query_result.fulfillment_text+"<br>\n"+q.getprofession()
        elif (surveystart == 1 and q.falseintent==False):
            return response.query_result.fulfillment_text+"<br>\n(Answer in yes,no or maybe)\n"
        else:
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
        #q.check = "1"
        q.subject=0
    #print (str(surveystart) + "botside")
    if (fulfillment_text == "ahmmmm .... okay so now i am gonna ask you some questions relax, you are not getting marked for it! So are you ready?"):
        print ("Startinggggg sruvey")
        surveystart = 1
    response_text = { "message":  fulfillment_text }
    return jsonify(response_text)
    
# run Flask app
if __name__ == "__main__":
    app.run()










#x = random.randrange(1, 32, 1)
        #if s in self.prevq:
        #    print(s+" before")
        #self.prevq.append(s)
        #print(self.prevq.index(s))