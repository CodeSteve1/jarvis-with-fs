import speech_recognition as sr #3.10.1
import pyttsx3 #2.90
import openai
import time
import pickle
import cv2
import os
import face_recognition

def __init__():
    global engine
    global voice_assistant_name
    global mess_his
    global encodeListKnown
    global id
    global cap
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    folder="images"
    PathList = os.listdir(folder)
    imglst=[]
    #na,e inside folder
    for path in PathList:
        imglst.append(cv2.imread(os.path.join(folder,path)))


#encode file opening
    file=open('encodefile.p','rb')
    encodeListknownwithids = pickle.load(file)
    encodeListKnown,id = encodeListknownwithids
    file.close()
    print("Encode file loaded...")




    mess_his = [{"role":"system","content":"you are a voice assistant named jarvis keep the number of lines of response less and appealing to listen to and refer to me as sir and if a request (such as return a something) is asked just the request "}]
    openai.api_key=''  #enter api key
    engine = pyttsx3.init(driverName='sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    #engine.runAndWait()
    voice_assistant_name="jarvis"
    print("initializing done")

def facial_scan():
    scanvar=[]
    print("start facial scan")
    for i in range(5):
        set = 0
        for i in range(1):
            success, img = cap.read()
            imgs = cv2.resize(img,(0,0),None,1,1)
            imgs = cv2.cvtColor(imgs,cv2.COLOR_BGR2RGB)

            facecurrFrame = face_recognition.face_locations(imgs)
            encodecurrframe = face_recognition.face_encodings(imgs,facecurrFrame)

        for encodeface,faceloc in zip(encodecurrframe,facecurrFrame):
            matches=face_recognition.compare_faces(encodeListKnown,encodeface)
            facedist = face_recognition.face_distance(encodeListKnown,encodeface)
            print(matches)
            print(facedist)
            for i in matches:
                scanvar.append(i)
        cv2.imshow('face', img)
        cv2.waitKey(10)

    print(scanvar)
    cv2.destroyAllWindows()
    if False in scanvar:
        return(False)
    elif True in scanvar:
        return(True)
    cv2.waitKey(1)
def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Listening...")
        audio=r.listen(source )

    try:
        statement = r.recognize_google(audio, language='en-in').lower()
        return statement
    #    engine.say(statement)
   #     engine.runAndWait()
   #     print(f"user said:{statement}\n")

    except Exception as e:
        return("none")
    return statement

def compute(statement):
    print(statement)
    if voice_assistant_name.lower() in statement and 'are you working' in statement:
        engine.say("Yes boss ... I am working")
        engine.runAndWait()
    elif voice_assistant_name.lower() in statement and 'time' in statement and 'now' in statement:
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)                 
        engine.say(current_time)
        engine.runAndWait()
    elif voice_assistant_name.lower() in statement:
        request = ask_openai(statement)
        if request[-1] == '?':
            print(request)
            engine.say(request)
            engine.runAndWait()
            r=sr.Recognizer()
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                audio=r.listen(source)
                statement = r.recognize_google(audio, language='en-in').lower()
            request = ask_openai(statement)
        else:
            pass
        engine.say(request)
        engine.runAndWait()
        print(request)


def ask_openai(question):
    global mess_his
    mess_his.append({"role": "user", "content": question})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=mess_his
    )
    gpt_response = completion.choices[0].message.content
    mess_his.append({"role": "assistant", "content": gpt_response})
    return gpt_response

abc=1
ct=0
def main():
    global ct
    __init__()
    engine.say("Starting facial scan for jarvis access!")
    engine.runAndWait()
    if facial_scan()==True:
        ct=0
        try:
            engine.say("Face Verified..Welcome Boss!")
            engine.runAndWait()
            while True:
                statement = takeCommand().lower()
                compute(statement)
        except:
            engine.say("error identified re-running program")
            engine.runAndWait()
            main()
    else:
        engine.say("scan failed !")
        engine.runAndWait()
        ct+=1
ct=0
while(ct<3):

    main()
    engine.say("retrying")
    engine.runAndWait()
engine.say("Facial scan failed.... jarvis locked ..please try again later!!!")
engine.runAndWait()



            

