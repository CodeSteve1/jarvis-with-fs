import os

import cv2
import face_recognition
import pickle

 #importing images
folder="images"
PathList = os.listdir(folder)
imglst=[]
id=[]
#na,e inside folder
for path in PathList:
    imglst.append(cv2.imread(os.path.join(folder,path)))
    id.append(os.path.splitext(path)[0])
    print(os.path.splitext(path)[0])
print(id)

def findEncodings(imglst):
    print(imglst)
    encode_list=[]
    for img in imglst:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encode_list.append(encode)
    return encode_list
print("Encoding Started")
encodeListKnown=findEncodings(imglst)
encodeListknownwithids=[encodeListKnown,id]
print(encodeListKnown)
print("Encoding complete")

file=open("encodefile.p",'wb')
pickle.dump(encodeListknownwithids,file)
file.close()
print("file saved")



