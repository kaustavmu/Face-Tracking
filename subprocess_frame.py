import cv2
from deepface import DeepFace
from retinaface import RetinaFace
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-p', "--processes", type=int)
parser.add_argument('-i', "--process", type=int)
parser.add_argument('-v', "--video_path", type=str)
parser.add_argument('-r', "--reference_path", type=str)
parser.add_argument('-o', "--output_folder", type=str)

args = parser.parse_args()
procs = args.processes
proc = args.process
video_path = args.video_path
reference_path = args.reference_path
output_folder = args.output_folder

def process(video_path, reference_path, procs, proc, output_folder):

    ref = cv2.imread(reference_path)
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video file.")
        exit()

    i = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        if i%procs != proc:
            i += 1
            continue

        print("Frame " + str(i))

        resp = RetinaFace.detect_faces(frame)

        faces = RetinaFace.extract_faces(frame, align = False)

        f = 0

        for face in faces:
           
            f += 1

            new_ref = cv2.resize(ref, face.shape[:2])

            try:
                obj = DeepFace.verify(new_ref, face)
                if obj["verified"]:
                    cv2.imwrite(output_folder + "frame_" + str(i) + ".jpg", frame)
                    data = [int(i) for i in resp['face_' + str(f)]['facial_area']]
                    print(data)
                    with open(output_folder + 'data_' + str(i) + '.json', 'w') as jsonfile:
                        json.dump(data, jsonfile)
            except Exception as e:
                print(e)
                continue

        i += 1

process(video_path, reference_path, procs, proc, output_folder)