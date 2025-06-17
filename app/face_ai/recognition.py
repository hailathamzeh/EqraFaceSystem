import os, sys
#sys.path.insert(0, "/home/fobeid/.local/lib/python3.8/site-packages/")
import face_recognition
#from deepface import DeepFace
import numpy as np
from PIL import Image, ImageDraw
from IPython.display import display
import argparse
import json, io

def generate_id(image_path, id, used_cpu, id_folder):
    try:
        image = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(image)[0]
        # print(type(face_encoding))
        np.savetxt(id_folder+'/'+str(id)+'.txt', face_encoding, fmt='%f')
        if used_cpu == 'yes' or used_cpu >= 1:
            print('{"ok": "face and ID save"}')
        else:
            print('{"warning": "the defualt number of CPU will use", "ok": "face and ID save"}')
        return True    
    except:
        print('{"err": "no features detected"}')
        return False

def detect_id(image_path, tol, used_cpu, id_folder):
    known_face_encodings = []
    known_face_names = []
    acc_result = []
    id_result = []
    age_list, race_list, emotion_list, gender_list = [], [], [], []
    id_list = os.listdir(id_folder+'/')
    if len(id_list) == 1 or len(id_list) == 0:
        print('{"err": "there is no data stored"}')
        #return json.dumps({"err": "there is no data stored"})
        return json.dumps({"data": [{"id": "Unknown"}]})
        # return False
        #sys.exit('{"err": "there is no data stored"}')
    for i in id_list:
        if i.endswith('.txt'):
            encode = np.loadtxt(id_folder+'/'+i, dtype=float)
            known_face_encodings.append(encode)
            i = i.replace('.txt','')
            known_face_names.append(i)
    
    unknown_image = face_recognition.load_image_file(image_path)

    # Find all the faces and face encodings in the unknown image
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

    
    pil_image = Image.fromarray(unknown_image)
    # Create a Pillow ImageDraw Draw instance to draw with
    draw = ImageDraw.Draw(pil_image)

    # Loop through each face found in the unknown image
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=float(tol))

        name = "Unknown"

        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        accuracy = np.max(face_distances)
        # print(accuracy)
        acc_result.append(round(accuracy*100,3))
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        # print(name)
        id_result.append(name)
    if len(id_result) != 0:
        #obj = DeepFace.analyze(img_path = image_path, actions = ['age', 'gender', 'race', 'emotion'], prog_bar=False)
        #age, gender, race, emotion = obj['age'], obj['gender'], obj['dominant_race'], obj['dominant_emotion']
        #info = 'info: [{"age": '+str(age)+', '+'"gender": "'+gender+'", '+'"race": "'+race+'", '+'"emotion": "'+emotion+'"''}]'
        data = [{"id": _id, "accuracy": _acc, "tolerance": float(tol)} for _id, _acc in zip(id_result, acc_result)]
        #, 'age': int(_age), 'gender': _gender, 'race': _race, 'emotion': _emotion       , _age, _gender, _race, _emotion      , age_list, gender_list, race_list, emotion_list
        
        if used_cpu == 'yes' or used_cpu >= 1:
            print('{"data": '+str(data)+'}')
            return json.dumps({"data": data})
            #return True
        else:
            print('{"warning": "the defualt number of CPU will use", "data": '+str(data)+'}')
            return json.dumps({"warning": "the defualt number of CPU will use", "data": data})
            #return True
    else:
        if used_cpu == 'yes' or used_cpu >= 1:
            print('{"data": [{"id": "Unknown"}]}')
            return json.dumps({"data": [{"id": "Unknown"}]})
            #return True
        else:
            print('{"warning": "the defualt number of CPU will use", "data": [{"id": "Unknown"}]}')
            return json.dumps({"warning": "the defualt number of CPU will use", "data": [{"id": "Unknown"}]})
            #return False

def del_id(id, id_folder):
    try:
        os.remove(id_folder+'/'+str(id)+'.txt')
        print('{"ok": "id '+str(id)+' removed"}')
        return True
    except:
        print('{"err": "id '+str(id)+' already not in our database"}')
        return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='face recognition params')
    parser.add_argument('--mode', help='img mode')
    parser.add_argument('--image_path', help='path to image')
    parser.add_argument('--id', help='id for the person')
    parser.add_argument('--tol', help='tolerance value')
    parser.add_argument('--cpu', help='number of cpu')
    parser.add_argument('--id_folder', help='id_folder dir')
    

    args = parser.parse_args()
    used_cpu = 'yes'
    id_folder = 'id_folder'
    if args.id_folder != None:
        id_folder = args.id_folder
    if args.mode == None:
        sys.exit('{"err": "please provide the mode"}')
    if args.cpu == None:
        used_cpu = 'no'
        # print('{"warning": "the defualt number of CPU will use"}')
    
    if args.mode == 'new':
        if args.id == None:
          sys.exit('{"err": "please provide the id"}')
        if args.image_path == None:
          sys.exit('{"err": "please provide the image path"}')
        try:
          test = Image.open(args.image_path)
        except:
          sys.exit('{"err": "please provide correct image path"}')
        generate_id(args.image_path, args.id, used_cpu, id_folder)
    
    elif args.mode == 'detect':
        if args.tol == None:
          sys.exit('{"err": "please add tol argument"}')
        if args.image_path == None:
          sys.exit('{"err": "please provide the image path"}')
        try:
          test = Image.open(args.image_path)
        except:
          sys.exit('{"err": "please provide correct image path"}')
        detect_id(args.image_path, args.tol, used_cpu, id_folder)

    elif args.mode == 'del':
        if args.id == None:
            sys.exit('{"err": "please provide the id"}')
        else:
            del_id(args.id, id_folder)
