import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://Hashaam:112211@cluster0-qxzg2.mongodb.net/test?retryWrites=true&w=majority")
db = cluster["WhatNext"]
#collection1 = db["Rawalpindi"]
collection2 = db["Courses"]
#s = "[["
print("hello")
post = {"_id": 20,"Name":"check1","Credit Hours":"120","Desc":"hey 1122","Image_uri":"hu.jpg","Name1":"hey1","Name2":"hey2","Name3":"hey3","OneLiner":"heyllllllls"}
collection2.insert_one(post)
print ("Uploaded")
#collection2.insert_many([post2,post3,post4,post5,post6,post7,post8,post9,post10,post11,post13])
#courses = collection1.find({"_id":2})
#universities = collection2.find({})

#for x in courses:
#    print(x)
# for x in courses:
#     s+='('
#     print(x["_id"])
#     s+="'"+str(x["_id"])+"'"+','
#     print(x["Name"])
#     s+="'"+x["Name"]+"'"+','
#     print(x["Credit Hours"])
#     s+="'"+x["Credit Hours"]+"'"+','
#     print(x["Desc"])
#     s+="'"+x["Desc"]+"'"+ ','
#     print(x["Image_uri"])
#     s+="'"+x["Image_uri"]+"'"+ ')'
#     s+=','
# s = s[:-1]
# s+="]]"
# print (s)
#for y in universities:
#    print(y)
