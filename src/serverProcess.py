from flask import Flask, render_template, request
import boto3
import os
from datetime import date
import inflect
import requestTranscribeJob as rt
import re
import nltk

app = Flask(__name__)
score1 = 0
score2 = 0
score4 = 0
score5 = 0
score6 = 0
score7 = 0
score8 = 0

"""
The methods described below use the Flask app to create different routes in the web server. 
They also compute a score for each question of the MMSE based on the user input .wav file.
"""
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/question1', methods=['POST'])
def question1():
    return render_template("question1.html")

"""App route for question one and its score. The datetime module is used to get the current
date, which will be compared against the user's repsonse. A final score for this function is
returned to the webpage for the user to see.
"""

@app.route('/question1Score', methods=['POST'])
def question1Score():
    global score1
    s3 = boto3.resource('s3')
    s3.Bucket('cs-proj-bucket').put_object(Key='question1/question1Speech.wav', Body=request.files['myFile'])
    
    location = boto3.client('s3').get_bucket_location(Bucket='cs-proj-bucket')['LocationConstraint']
    
    if location == None: 
        location = 'us-east-1'
    url = ""
    url = "https://s3-%s.amazonaws.com/%s/%s" % (location, "cs-proj-bucket", "question1/question1Speech.wav")
    
    speechString1 = rt.getResult('question1Test', url)
    
    correctMonth = False
    correctDay = False
    correctYear = False
    correctSeason = False

    today = date.today()
    d2 = today.strftime("%B %d, %Y")
    dateComponents = d2.split()

    dayString = dateComponents[1]
    dayString = dayString[:-1]
    p = inflect.engine()
    newDayString = p.number_to_words(p.ordinal(int(dayString)))
    dateComponents[1] = newDayString

    dayString2 = dateComponents[2]
    newDayString2 = p.number_to_words(int(dayString2), group=2)
    dateComponents[2] = newDayString2
    
    if(dateComponents[0] == "December" or dateComponents[0] == "January" or dateComponents[0] == "Feburary"):
        dateComponents.append("winter")

    elif(dateComponents[0] == "March" or dateComponents[0] == "April" or dateComponents[0] == "May"):
        dateComponents.append("spring")

    elif(dateComponents[0] == "June" or dateComponents[0] == "July" or dateComponents[0] == "August"):
        dateComponents.append("summer")

    elif(dateComponents[0] == "September" or dateComponents[0] == "October" or dateComponents[0] == "November"):
        dateComponents.append("fall")


    dateComponents[2] = dateComponents[2].replace(",","")

    score1 = 0
    if(dateComponents[0] in speechString1 and not correctMonth):
        correctMonth = True
        score1 +=1
    if(dateComponents[1] in speechString1 and not correctDay):
        correctDay = True
        score1+=1
    if(dateComponents[2] in speechString1 and not correctYear):
        correctYear = True
        score1+=1
    if(dateComponents[3] in speechString1 and not correctSeason):
        correctSeason = True
        score1+=1

    return render_template('question1Score.html', variable = score1)

"""App route for question two and its score. Code for this method is still under construction. 
Standard Flask app uses the IP address to obtain geolocation. However, because this site is run 
on a remote aws server, this location will not be the same as the user's location. Furthermore, 
goelocation obtained from IP addresses are not as accurate as location obtained through GPS. 
Hence, I am still in the process of finding solutions to this problem."""

@app.route('/question2', methods=['POST'])
def question2():
    return render_template("question2.html")
    
@app.route('/question2Score', methods=['POST'])
def question2Score():
    return render_template('question2Score.html')

"""App route for question three. The user is asked to memorize the names of certain objects
listen on screen. There is no file uploader for this question."""

@app.route('/question3', methods=['POST'])
def question3():
    return render_template("question3.html")
    
"""App route for question four and its score. The user is asked to count backwards from 100 
to 72 by increments of seven. Their response is compared to the correst response, and each
correct value is given one point."""

@app.route('/question4', methods=['POST'])
def question4():
    return render_template("question4.html")
@app.route('/question4Score', methods=['POST'])
def question4Score():
    global score4
    s3 = boto3.resource('s3')
    s3.Bucket('cs-proj-bucket').put_object(Key='question4/question4Speech.wav', Body=request.files['myFile'])
    
    location = boto3.client('s3').get_bucket_location(Bucket='cs-proj-bucket')['LocationConstraint']
    
    if location == None: 
        location = 'us-east-1'
    url = ""
    url = "https://s3-%s.amazonaws.com/%s/%s" % (location, "cs-proj-bucket", "question4/question4Speech.wav")
    
    speechString4 = rt.getResult('question4Test', url)
    numeric_string4 = re.sub("[^0-9]", "", speechString4)
    
    score4 = 0
    if("100" in numeric_string4):
        score4+=1
    if("93" in numeric_string4):
        score4+=1
    if("86" in numeric_string4):
        score4+=1
    if("79" in numeric_string4):
        score4+=1
    if("72" in numeric_string4):
        score4+=1
    return render_template('question4Score.html', variable = score4)

"""App route for question five and its score. The user is asked to remember the names of the 
objects asked in question three. Each correct response corrosponds to one point being awarded."""

@app.route('/question5', methods=['POST'])
def question5():
    return render_template("question5.html")
@app.route('/question5Score', methods=['POST'])
def question5Score():
    global score5
    object1 = "scissors"
    object2 = "legos"
    object3 = "rocks"
    s3 = boto3.resource('s3')
    s3.Bucket('cs-proj-bucket').put_object(Key='question5/question5Speech.wav', Body=request.files['myFile'])
    
    location = boto3.client('s3').get_bucket_location(Bucket='cs-proj-bucket')['LocationConstraint']
    if location == None: 
        location = 'us-east-1'
    url = ""
    url = "https://s3-%s.amazonaws.com/%s/%s" % (location, "cs-proj-bucket", "question5/question5Speech.wav")
    
    speechString5 = rt.getResult('question5Test', url)
    score5 = 0
    if(object1 in speechString5):
        score5+=1
    if(object2 in speechString5):
        score5+=1
    if(object3 in speechString5):
        score5+=1
        
    return render_template('question5Score.html', variable = score5)

"""App route for question six and its score. The user is asked to name two common house hold
items they see on screen, and each correct response is given one point."""

@app.route('/question6', methods=['POST'])
def question6():
    return render_template('question6.html')
    
@app.route('/question6Score', methods=['POST'])
def question6Score():
    global score6
    s3 = boto3.resource('s3')
    s3.Bucket('cs-proj-bucket').put_object(Key='question6/question6Speech.wav', Body=request.files['myFile'])
    
    location = boto3.client('s3').get_bucket_location(Bucket='cs-proj-bucket')['LocationConstraint']
    if location == None: 
        location = 'us-east-1'
    url = ""
    url = "https://s3-%s.amazonaws.com/%s/%s" % (location, "cs-proj-bucket", "question6/question6Speech.wav")
    
    speechString6 = rt.getResult('question6Test', url)
    
    score6 = 0
    if("watch" or "Watch" in speechString6):
        score6+=1
    if("pencil" or "Pencil" in speechString6):
        score6+=1
    
    return render_template('question6Score.html', variable = score6)

"""App route for question seven and its score. The user is asked to repeate a phrase. The sentence must
be fully accurate for them to recieve a point."""

@app.route('/question7', methods=['POST'])
def question7():
    return render_template("question7.html")
    
@app.route('/question7Score', methods=['POST'])
def question7Score():
    global score7
    s3 = boto3.resource('s3')
    s3.Bucket('cs-proj-bucket').put_object(Key='question7/question7Speech.wav', Body=request.files['myFile'])
    location = boto3.client('s3').get_bucket_location(Bucket='cs-proj-bucket')['LocationConstraint']
    if location == None: 
        location = 'us-east-1'
    url = ""
    url = "https://s3-%s.amazonaws.com/%s/%s" % (location, "cs-proj-bucket", "question7/question7Speech.wav")
    
    speechString7 = rt.getResult('question7Test', url)
    score7 =0
    correctPhrase = "No ifs ands or buts" 
    if(correctPhrase in speechString7):
        score7+=1    
    return render_template('question7Score.html', variable = score7)
    
"""App route for question eight and its score. The user is come up with a sentence. This sentence
must contain a noun and a verb for it to our. First occurance of each part of speech is award one point.
The NLTK module is used to tag the words in the sentence with its part of speech."""

@app.route('/question8', methods=['POST'])
def question8():
    return render_template("question8.html")
@app.route('/question8Score', methods=['POST'])
def question8Score():
    global score8
    s3 = boto3.resource('s3')
    s3.Bucket('cs-proj-bucket').put_object(Key='question8/question8Speech.wav', Body=request.files['myFile'])
    location = boto3.client('s3').get_bucket_location(Bucket='cs-proj-bucket')['LocationConstraint']
    if location == None: 
        location = 'us-east-1'
    url = ""
    url = "https://s3-%s.amazonaws.com/%s/%s" % (location, "cs-proj-bucket", "question8/question8Speech.wav")
    
    score8 = 0
    speechString8 = rt.getResult('question8Test', url)

    foundNoun = False
    foundVerb = False
    
    tokens8 = nltk.word_tokenize(speechString8)
    tokensWithPartOfSpeech = nltk.pos_tag(tokens8)

    for word, POS in tokensWithPartOfSpeech:
        if(POS == "VBD" or POS == "VBN" or POS == "VBP" == "VBZ"):
            if(not foundVerb):
                foundVerb = True
                score8+=1
        if(POS == "NN" or POS == "NNS" or POS == "NNP" or POS == "NNPS"):
            if(not foundNoun):
                foundNoun = True
                score8+=1

    return render_template('question7Score.html', variable = score8)


if __name__ == '__main__':
    app.run(host="172.31.24.193", port="8080", debug=True)