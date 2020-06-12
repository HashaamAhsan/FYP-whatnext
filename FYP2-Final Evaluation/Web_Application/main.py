from flask import *
import sqlite3, hashlib, os
from werkzeug.utils import secure_filename
import pymongo
from pymongo import MongoClient
import dialogflow
import requests
import json
import pusher
import random 
from queue import Queue 

app = Flask(__name__)
app.secret_key = 'random string'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
cluster = MongoClient("mongodb+srv://Hashaam:112211@cluster0-qxzg2.mongodb.net/test?retryWrites=true&w=majority")
db = cluster["WhatNext"]

check = "0"
surveystart = 0

unione=""
unitwo=""

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

def getLoginDetails():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        if 'email' not in session:
            loggedIn = False
            firstName = ''
            noOfItems = 0
        else:
            loggedIn = True
            cur.execute("SELECT userId, firstName FROM users WHERE email = ?", (session['email'], ))
            userId, firstName = cur.fetchone()
            cur.execute("SELECT count(productId) FROM kart WHERE userId = ?", (userId, ))
            noOfItems = cur.fetchone()[0]
    conn.close()
    return (loggedIn, firstName, noOfItems)

@app.route("/")
def root():    
    #, itemData=itemData, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems, categoryData=categoryData  
    return render_template('index.html')

@app.route("/chatbot")
def chatbot():     
    return render_template('Chatbot.html')

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


@app.route("/add")
def admin():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT categoryId, name FROM categories")
        categories = cur.fetchall()
    conn.close()
    return render_template('add.html', categories=categories)

@app.route("/addItem", methods=["GET", "POST"])
def addItem():
    if request.method == "POST":
        name = request.form['name']
        price = float(request.form['price'])
        description = request.form['description']
        stock = int(request.form['stock'])
        categoryId = int(request.form['category'])

        #Uploading image procedure
        image = request.files['image']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        imagename = filename
        with sqlite3.connect('database.db') as conn:
            try:
                cur = conn.cursor()
                cur.execute('''INSERT INTO products (name, price, description, image, stock, categoryId) VALUES (?, ?, ?, ?, ?, ?)''', (name, price, description, imagename, stock, categoryId))
                conn.commit()
                msg="added successfully"
            except:
                msg="error occured"
                conn.rollback()
        conn.close()
        #print(msg)
        return redirect(url_for('root'))

@app.route("/remove")
def remove():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT productId, name, price, description, image, stock FROM products')
        data = cur.fetchall()
    conn.close()
    return render_template('remove.html', data=data)

@app.route("/removeItem")
def removeItem():
    productId = request.args.get('productId')
    with sqlite3.connect('database.db') as conn:
        try:
            cur = conn.cursor()
            cur.execute('DELETE FROM products WHERE productID = ?', (productId, ))
            conn.commit()
            msg = "Deleted successsfully"
        except:
            conn.rollback()
            msg = "Error occured"
    conn.close()
    #print(msg)
    return redirect(url_for('root'))

@app.route("/displayCategory")
def displayCategory():
        loggedIn, firstName, noOfItems = getLoginDetails()
        categoryId = request.args.get("categoryId")
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT products.productId, products.name, products.price, products.image, categories.name FROM products, categories WHERE products.categoryId = categories.categoryId AND categories.categoryId = ?", (categoryId, ))
            data = cur.fetchall()
        conn.close()
        categoryName = data[0][4]
        data = parse(data)
        return render_template('displayCategory.html', data=data, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems, categoryName=categoryName)

@app.route("/account/profile")
def profileHome():
    if 'email' not in session:
        return redirect(url_for('root'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    return render_template("profileHome.html", loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)

@app.route("/account/profile/edit")
def editProfile():
    if 'email' not in session:
        return redirect(url_for('root'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId, email, firstName, lastName, address1, address2, zipcode, city, state, country, phone FROM users WHERE email = ?", (session['email'], ))
        profileData = cur.fetchone()
    conn.close()
    return render_template("editProfile.html", profileData=profileData, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)

@app.route("/account/profile/changePassword", methods=["GET", "POST"])
def changePassword():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    if request.method == "POST":
        oldPassword = request.form['oldpassword']
        oldPassword = hashlib.md5(oldPassword.encode()).hexdigest()
        newPassword = request.form['newpassword']
        newPassword = hashlib.md5(newPassword.encode()).hexdigest()
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT userId, password FROM users WHERE email = ?", (session['email'], ))
            userId, password = cur.fetchone()
            if (password == oldPassword):
                try:
                    cur.execute("UPDATE users SET password = ? WHERE userId = ?", (newPassword, userId))
                    conn.commit()
                    msg="Changed successfully"
                except:
                    conn.rollback()
                    msg = "Failed"
                return render_template("changePassword.html", msg=msg)
            else:
                msg = "Wrong password"
        conn.close()
        return render_template("changePassword.html", msg=msg)
    else:
        return render_template("changePassword.html")

@app.route("/updateProfile", methods=["GET", "POST"])
def updateProfile():
    if request.method == 'POST':
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        address1 = request.form['address1']
        address2 = request.form['address2']
        zipcode = request.form['zipcode']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        phone = request.form['phone']
        with sqlite3.connect('database.db') as con:
                try:
                    cur = con.cursor()
                    cur.execute('UPDATE users SET firstName = ?, lastName = ?, address1 = ?, address2 = ?, zipcode = ?, city = ?, state = ?, country = ?, phone = ? WHERE email = ?', (firstName, lastName, address1, address2, zipcode, city, state, country, phone, email))

                    con.commit()
                    msg = "Saved Successfully"
                except:
                    con.rollback()
                    msg = "Error occured"
        con.close()
        return redirect(url_for('editProfile'))

@app.route("/loginForm")
def loginForm():
    if 'email' in session:
        return redirect(url_for('root'))
    else:
        return render_template('login.html', error='')

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if is_valid(email, password):
            session['email'] = email
            return redirect(url_for('root'))
        else:
            error = 'Invalid UserId / Password'
            return render_template('login.html', error=error)

@app.route("/findCourse")
def findCourse():
    collection1 = db["Courses"]
    courses = collection1.find({})

    l=[]
    for x in courses:
        #print (x)
        l.append((x["_id"],x["Name"],x["Credit Hours"],x["Desc"],x["Image_uri"],x["Name1"],x["Name2"],x["Name3"],x["OneLiner"]))

    itemData = parse(l)
    return render_template("courses.html",itemData=itemData)

@app.route("/findUni")
def findUni():
    collection1 = db["Universities"]
    uni = collection1.find({})
    l=[]
    for x in uni:
        l.append((x["_id"],x["Name"],x["Desc"],x["Campus_Size"],x["Hostel"],x["Sport_Complex"],x["City"],x["HEC_Ranking"],x["User_Ranking"],x["Application"],x["Fee_Structure"],x["Img_uri"],x["Name1"],x["Name2"],x["Name3"],x["OneLiner"]))

    itemData = parse(l)
    #print (itemData)
    return render_template("universities.html",itemData=itemData)

@app.route("/findUniRawalpindi")
def findUniRawalpindi():
    collection1 = db["Rawalpindi"]
    uni = collection1.find({})
    l=[]
    for x in uni:
        l.append((x["_id"],x["Name"],x["Desc"],x["Campus_Size"],x["Hostel"],x["Sport_Complex"],x["City"],x["HEC_Ranking"],x["User_Ranking"],x["Application"],x["Fee_Structure"],x["Img_uri"],x["Name1"],x["Name2"],x["Name3"],x["OneLiner"]))

    itemData = parse(l)
    #print (itemData)
    return render_template("Rawalpindi.html",itemData=itemData)

@app.route("/findUniIslamabad")
def findUniIslamabad():
    collection1 = db["Islamabad"]
    uni = collection1.find({})
    l=[]
    for x in uni:
        l.append((x["_id"],x["Name"],x["Desc"],x["Campus_Size"],x["Hostel"],x["Sport_Complex"],x["City"],x["HEC_Ranking"],x["User_Ranking"],x["Application"],x["Fee_Structure"],x["Img_uri"],x["Name1"],x["Name2"],x["Name3"],x["OneLiner"]))

    itemData = parse(l)
    #print (itemData)
    return render_template("Islamabad.html",itemData=itemData)

@app.route("/findBusiness")
def findBusiness():
    collection1 = db["Business"]
    courses = collection1.find({})

    l=[]
    for x in courses:
        l.append((x["_id"],x["Name"],x["Credit Hours"],x["Desc"],x["Image_uri"],x["Name1"],x["Name2"],x["Name3"],x["OneLiner"]))

    itemData = parse(l)
    return render_template("Business.html",itemData=itemData)

@app.route("/findComputerScience")
def findComputerScience():
    collection1 = db["Computer Science"]
    courses = collection1.find({})

    l=[]
    for x in courses:
        l.append((x["_id"],x["Name"],x["Credit Hours"],x["Desc"],x["Image_uri"],x["Name1"],x["Name2"],x["Name3"],x["OneLiner"]))

    itemData = parse(l)
    return render_template("ComputerScience.html",itemData=itemData)

@app.route("/findHumanities")
def findHumanities():
    collection1 = db["Humanities"]
    courses = collection1.find({})

    l=[]
    for x in courses:
        l.append((x["_id"],x["Name"],x["Credit Hours"],x["Desc"],x["Image_uri"],x["Name1"],x["Name2"],x["Name3"],x["OneLiner"]))

    itemData = parse(l)
    return render_template("Humanities.html",itemData=itemData)

@app.route("/findEngineering")
def findEngineering():
    collection1 = db["Engineering"]
    courses = collection1.find({})

    l=[]
    for x in courses:
        l.append((x["_id"],x["Name"],x["Credit Hours"],x["Desc"],x["Image_uri"],x["Name1"],x["Name2"],x["Name3"],x["OneLiner"]))

    itemData = parse(l)
    return render_template("Engineering.html",itemData=itemData)

@app.route("/courseDisplay")
def courseDisplay():
    db = cluster["WhatNext"]
    collection1 = db["Courses"]
    productId = request.args.get('productId')
    courses = collection1.find({"_id":int(productId)})
    productData=[]
    for x in courses:
        #print(x)
        productData.append(x["_id"])
        productData.append(x["Name"])
        productData.append(x["Credit Hours"])
        productData.append(x["Desc"])
        productData.append(x["Image_uri"])
    productData=tuple(productData)
    #print(productData)
    return render_template("course.html", data=productData)

@app.route("/UniDisplay")
def UniDisplay():
    db = cluster["WhatNext"]
    collection1 = db["Universities"]
    productId = request.args.get('productId')
    courses = collection1.find({"_id":int(productId)})
    productData=[]
    for x in courses:
        #print(x)
        productData.append(x["_id"])
        productData.append(x["Name"])
        productData.append(x["Desc"])
        productData.append(x["Campus_Size"])
        productData.append(x["Hostel"])
        productData.append(x["Sport_Complex"])
        productData.append(x["City"])
        productData.append(x["HEC_Ranking"])
        productData.append(x["User_Ranking"])
        productData.append(x["Application"])
        productData.append(x["Fee_Structure"])
        productData.append(x["Img_uri"])
    productData=tuple(productData)
    #print(productData)
    return render_template("university.html", data=productData)


@app.route("/compareunidisplay")
def compareunidisplay():
    db = cluster["WhatNext"]
    collection1 = db["Universities"]
    productId = 1
    courses = collection1.find({"_id":int(productId)})
    productData=[]
    for x in courses:
        #print(x)
        productData.append(x["_id"])
        productData.append(x["Name"])
        productData.append(x["Desc"])
        productData.append(x["Campus_Size"])
        productData.append(x["Hostel"])
        productData.append(x["Sport_Complex"])
        productData.append(x["City"])
        productData.append(x["HEC_Ranking"])
        productData.append(x["User_Ranking"])
        productData.append(x["Application"])
        productData.append(x["Fee_Structure"])
        productData.append(x["Img_uri"])
    productData=tuple(productData)
    #print(productData)

    productId2 = request.args.get('productIdtwo')
    courses2 = collection1.find({"_id":int(productId2)})
    productData2=[]
    for x in courses2:
        #print(x)
        productData2.append(x["_id"])
        productData2.append(x["Name"])
        productData2.append(x["Desc"])
        productData2.append(x["Campus_Size"])
        productData2.append(x["Hostel"])
        productData2.append(x["Sport_Complex"])
        productData2.append(x["City"])
        productData2.append(x["HEC_Ranking"])
        productData2.append(x["User_Ranking"])
        productData2.append(x["Application"])
        productData2.append(x["Fee_Structure"])
        productData2.append(x["Img_uri"])
    productData2=tuple(productData2)
    return render_template("compareunidisplay.html", data=productData,datatwo=productData2)

@app.route("/courseSearch")
def courseSearch():
    text = request.args.get('mysearch')
    collection1 = db["Courses"]
    x=None

    courses = collection1.find({"Name":text})
    l=[]
    for x in courses:
        l.append((x["_id"],x["Name"],x["Credit Hours"],x["Desc"],x["Image_uri"],x["Name1"],x["Name2"],x["Name3"],x["OneLiner"]))
    itemData = parse(l)

    if x is None:
        courses = collection1.find({"Name1":text})
        l=[]
        for x in courses:
            l.append((x["_id"],x["Name"],x["Credit Hours"],x["Desc"],x["Image_uri"],x["Name1"],x["Name2"],x["Name3"],x["OneLiner"]))
        itemData = parse(l)
        if x is None:
            courses = collection1.find({"Name2":text})
            l=[]
            for x in courses:
                l.append((x["_id"],x["Name"],x["Credit Hours"],x["Desc"],x["Image_uri"],x["Name1"],x["Name2"],x["Name3"],x["OneLiner"]))
            itemData = parse(l)
            if x is None:
                courses = collection1.find({"Name3":text})
                l=[]
                for x in courses:
                    l.append((x["_id"],x["Name"],x["Credit Hours"],x["Desc"],x["Image_uri"],x["Name1"],x["Name2"],x["Name3"],x["OneLiner"]))
                itemData = parse(l)

    return render_template("courses.html",itemData=itemData)

@app.route("/uniSearch")
def uniSearch():
    text = request.args.get('message')
    collection1 = db["Universities"]
    x=None

    courses = collection1.find({"Name":text})
    l=[]
    for x in courses:
        l.append((x["_id"],x["Name"],x["Desc"],x["Campus_Size"],x["Hostel"],x["Sport_Complex"],x["City"],x["HEC_Ranking"],x["User_Ranking"],x["Application"],x["Fee_Structure"],x["Img_uri"],x["Name1"],x["Name2"],x["Name3"],x["OneLiner"]))
    itemData = parse(l)


    if x is None:
        courses = collection1.find({"Name1":text})
        l=[]
        for x in courses:
            l.append((x["_id"],x["Name"],x["Desc"],x["Campus_Size"],x["Hostel"],x["Sport_Complex"],x["City"],x["HEC_Ranking"],x["User_Ranking"],x["Application"],x["Fee_Structure"],x["Img_uri"],x["Name1"],x["Name2"],x["Name3"],x["OneLiner"]))
        itemData = parse(l)
        if x is None:
            courses = collection1.find({"Name2":text})
            l=[]
            for x in courses:
                l.append((x["_id"],x["Name"],x["Desc"],x["Campus_Size"],x["Hostel"],x["Sport_Complex"],x["City"],x["HEC_Ranking"],x["User_Ranking"],x["Application"],x["Fee_Structure"],x["Img_uri"],x["Name1"],x["Name2"],x["Name3"],x["OneLiner"]))
            itemData = parse(l)
            if x is None:
                courses = collection1.find({"Name3":text})
                l=[]
                for x in courses:
                    l.append((x["_id"],x["Name"],x["Desc"],x["Campus_Size"],x["Hostel"],x["Sport_Complex"],x["City"],x["HEC_Ranking"],x["User_Ranking"],x["Application"],x["Fee_Structure"],x["Img_uri"],x["Name1"],x["Name2"],x["Name3"],x["OneLiner"]))
                itemData = parse(l)
   
    return render_template("universities.html",itemData=itemData)

@app.route("/compareUnis")
def compareUnis():
    collection1 = db["Universities"]
    uni = collection1.find({})
    l=[]
    for x in uni:
        l.append((x["_id"],x["Name"],x["Desc"],x["Campus_Size"],x["Hostel"],x["Sport_Complex"],x["City"],x["HEC_Ranking"],x["User_Ranking"],x["Application"],x["Fee_Structure"],x["Img_uri"],x["Name1"],x["Name2"],x["Name3"],x["OneLiner"]))

    itemData = parse(l)
    random.shuffle(l)
    itemData2 = parse(l)
    #print (itemData)
    return render_template("compareUnis.html",itemData1=itemData,itemData2=itemData2)

@app.route("/uniSearchcompareone")
def uniSearchcompareone():
    text = request.args.get('messageone')
    global unione
    unione = text
    collection1 = db["Universities"]
    x=None

    courses = collection1.find({"Name":text})
    l=[]
    for x in courses:
        l.append((x["_id"],x["Name"],x["Desc"],x["Campus_Size"],x["Hostel"],x["Sport_Complex"],x["City"],x["HEC_Ranking"],x["User_Ranking"],x["Application"],x["Fee_Structure"],x["Img_uri"],x["Name1"],x["Name2"],x["Name3"],x["OneLiner"]))
    itemData = parse(l)


    if x is None:
        courses = collection1.find({"Name1":text})
        l=[]
        for x in courses:
            l.append((x["_id"],x["Name"],x["Desc"],x["Campus_Size"],x["Hostel"],x["Sport_Complex"],x["City"],x["HEC_Ranking"],x["User_Ranking"],x["Application"],x["Fee_Structure"],x["Img_uri"],x["Name1"],x["Name2"],x["Name3"],x["OneLiner"]))
        itemData = parse(l)
        if x is None:
            courses = collection1.find({"Name2":text})
            l=[]
            for x in courses:
                l.append((x["_id"],x["Name"],x["Desc"],x["Campus_Size"],x["Hostel"],x["Sport_Complex"],x["City"],x["HEC_Ranking"],x["User_Ranking"],x["Application"],x["Fee_Structure"],x["Img_uri"],x["Name1"],x["Name2"],x["Name3"],x["OneLiner"]))
            itemData = parse(l)
            if x is None:
                courses = collection1.find({"Name3":text})
                l=[]
                for x in courses:
                    l.append((x["_id"],x["Name"],x["Desc"],x["Campus_Size"],x["Hostel"],x["Sport_Complex"],x["City"],x["HEC_Ranking"],x["User_Ranking"],x["Application"],x["Fee_Structure"],x["Img_uri"],x["Name1"],x["Name2"],x["Name3"],x["OneLiner"]))
                itemData = parse(l)


    return render_template("compareUnis.html",itemData1=itemData)

@app.route("/uniSearchcomparetwo")
def uniSearchcomparetwo():
    global unione
    text = unione
    text2 = request.args.get('messagetwo')
    collection1 = db["Universities"]
    x=None

    courses = collection1.find({"Name":text})
    l=[]
    for x in courses:
        l.append((x["_id"],x["Name"],x["Desc"],x["Campus_Size"],x["Hostel"],x["Sport_Complex"],x["City"],x["HEC_Ranking"],x["User_Ranking"],x["Application"],x["Fee_Structure"],x["Img_uri"],x["Name1"],x["Name2"],x["Name3"],x["OneLiner"]))
    itemData = parse(l)


    if x is None:
        courses = collection1.find({"Name1":text})
        l=[]
        for x in courses:
            l.append((x["_id"],x["Name"],x["Desc"],x["Campus_Size"],x["Hostel"],x["Sport_Complex"],x["City"],x["HEC_Ranking"],x["User_Ranking"],x["Application"],x["Fee_Structure"],x["Img_uri"],x["Name1"],x["Name2"],x["Name3"],x["OneLiner"]))
        itemData = parse(l)
        if x is None:
            courses = collection1.find({"Name2":text})
            l=[]
            for x in courses:
                l.append((x["_id"],x["Name"],x["Desc"],x["Campus_Size"],x["Hostel"],x["Sport_Complex"],x["City"],x["HEC_Ranking"],x["User_Ranking"],x["Application"],x["Fee_Structure"],x["Img_uri"],x["Name1"],x["Name2"],x["Name3"],x["OneLiner"]))
            itemData = parse(l)
            if x is None:
                courses = collection1.find({"Name3":text})
                l=[]
                for x in courses:
                    l.append((x["_id"],x["Name"],x["Desc"],x["Campus_Size"],x["Hostel"],x["Sport_Complex"],x["City"],x["HEC_Ranking"],x["User_Ranking"],x["Application"],x["Fee_Structure"],x["Img_uri"],x["Name1"],x["Name2"],x["Name3"],x["OneLiner"]))
                itemData = parse(l)


    courses = collection1.find({"Name":text2})
    l=[]
    for x in courses:
        l.append((x["_id"],x["Name"],x["Desc"],x["Campus_Size"],x["Hostel"],x["Sport_Complex"],x["City"],x["HEC_Ranking"],x["User_Ranking"],x["Application"],x["Fee_Structure"],x["Img_uri"],x["Name1"],x["Name2"],x["Name3"],x["OneLiner"]))
    itemData2 = parse(l)


    if x is None:
        courses = collection1.find({"Name1":text2})
        l=[]
        for x in courses:
            l.append((x["_id"],x["Name"],x["Desc"],x["Campus_Size"],x["Hostel"],x["Sport_Complex"],x["City"],x["HEC_Ranking"],x["User_Ranking"],x["Application"],x["Fee_Structure"],x["Img_uri"],x["Name1"],x["Name2"],x["Name3"],x["OneLiner"]))
        itemData2 = parse(l)
        if x is None:
            courses = collection1.find({"Name2":text2})
            l=[]
            for x in courses:
                l.append((x["_id"],x["Name"],x["Desc"],x["Campus_Size"],x["Hostel"],x["Sport_Complex"],x["City"],x["HEC_Ranking"],x["User_Ranking"],x["Application"],x["Fee_Structure"],x["Img_uri"],x["Name1"],x["Name2"],x["Name3"],x["OneLiner"]))
            itemData2 = parse(l)
            if x is None:
                courses = collection1.find({"Name3":text2})
                l=[]
                for x in courses:
                    l.append((x["_id"],x["Name"],x["Desc"],x["Campus_Size"],x["Hostel"],x["Sport_Complex"],x["City"],x["HEC_Ranking"],x["User_Ranking"],x["Application"],x["Fee_Structure"],x["Img_uri"],x["Name1"],x["Name2"],x["Name3"],x["OneLiner"]))
                itemData2 = parse(l)

    return render_template("compareUnis.html",itemData1=itemData,itemData2=itemData2)

@app.route("/productDescription")
def productDescription():
    
    #print(courses)
    # with sqlite3.connect('database.db') as conn:
    #     cur = conn.cursor()
    #     cur.execute('SELECT productId, name, price, description, image, stock FROM products WHERE productId = ?', (productId, ))
    #     productData = cur.fetchone()
    # conn.close()
    # print(type(productData))
    # print(productData)
    productData=[]
    for x in courses:
        #print(x)
        productData.append(x["_id"])
        productData.append(x["Name"])
        productData.append(x["Credit Hours"])
        productData.append(x["Desc"])
        productData.append(x["Image_uri"])
    productData=tuple(productData)
    #print(productData)
    return render_template("course.html", data=productData, loggedIn = loggedIn, firstName = firstName, noOfItems = noOfItems)

@app.route("/addToCart")
def addToCart():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    else:
        productId = int(request.args.get('productId'))
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT userId FROM users WHERE email = ?", (session['email'], ))
            userId = cur.fetchone()[0]
            try:
                cur.execute("INSERT INTO kart (userId, productId) VALUES (?, ?)", (userId, productId))
                conn.commit()
                msg = "Added successfully"
            except:
                conn.rollback()
                msg = "Error occured"
        conn.close()
        return redirect(url_for('root'))

@app.route("/cart")
def cart():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    email = session['email']
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId FROM users WHERE email = ?", (email, ))
        userId = cur.fetchone()[0]
        cur.execute("SELECT products.productId, products.name, products.price, products.image FROM products, kart WHERE products.productId = kart.productId AND kart.userId = ?", (userId, ))
        products = cur.fetchall()
    totalPrice = 0
    for row in products:
        totalPrice += row[2]
    return render_template("cart.html", products = products, totalPrice=totalPrice, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)

@app.route("/removeFromCart")
def removeFromCart():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    email = session['email']
    productId = int(request.args.get('productId'))
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId FROM users WHERE email = ?", (email, ))
        userId = cur.fetchone()[0]
        try:
            cur.execute("DELETE FROM kart WHERE userId = ? AND productId = ?", (userId, productId))
            conn.commit()
            msg = "removed successfully"
        except:
            conn.rollback()
            msg = "error occured"
    conn.close()
    return redirect(url_for('root'))

@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('root'))

def is_valid(email, password):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT email, password FROM users')
    data = cur.fetchall()
    for row in data:
        if row[0] == email and row[1] == hashlib.md5(password.encode()).hexdigest():
            return True
    return False

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        #Parse form data    
        password = request.form['password']
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        address1 = request.form['address1']
        address2 = request.form['address2']
        zipcode = request.form['zipcode']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        phone = request.form['phone']

        with sqlite3.connect('database.db') as con:
            try:
                cur = con.cursor()
                cur.execute('INSERT INTO users (password, email, firstName, lastName, address1, address2, zipcode, city, state, country, phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (hashlib.md5(password.encode()).hexdigest(), email, firstName, lastName, address1, address2, zipcode, city, state, country, phone))

                con.commit()

                msg = "Registered Successfully"
            except:
                con.rollback()
                msg = "Error occured"
        con.close()
        return render_template("login.html", error=msg)

@app.route("/registerationForm")
def registrationForm():
    return render_template("register.html")

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def parse(data):
    ans = []
    i = 0
    while i < len(data):
        curr = []
        for j in range(7):
            if i >= len(data):
                break
            curr.append(data[i])
            i += 1
        ans.append(curr)
    return ans

if __name__ == '__main__':
    app.run(debug=True)
