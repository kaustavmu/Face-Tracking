import cv2
import argparse
import subprocess
import os
import json

parser = argparse.ArgumentParser()
parser.add_argument('-p', "--processes", type=int)
parser.add_argument('-v', "--video_path", type=str)
parser.add_argument('-r', "--reference_path", type=str)
parser.add_argument('-o', "--output_folder", type=str)

args = parser.parse_args()
procs = args.processes
video_path = args.video_path
reference_path = args.reference_path
output_folder = args.output_folder

if output_folder[-1] != "/":
    output_folder += "/"

if not os.path.isdir(output_folder):
    os.mkdir(output_folder)

cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)

if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

def run_subprocess(i):
    return subprocess.Popen(['python3', 'subprocess_frame.py', '--processes', str(procs), '--process', str(i), '--video_path', video_path, '--reference_path', reference_path, '--output_folder', output_folder])

processes = [run_subprocess(i) for i in range(procs)]

for p in processes:
    p.wait()

images = [img for img in os.listdir(output_folder) if img[-3:] == "jpg"]
images.sort(key = lambda x: int(x[6:-4]))

prev = -2
v_num = 0
start_f_num = 0
video_writer = None

metadata = {}
frames = {}

images.append('end')

for image in images:
    if image != 'end':
        f_num = int(image[6:-4])

    if image == 'end' or f_num != prev + 1:

        if video_writer:
            video_writer.release()
            v_num += 1

            end_f_num = prev
            start_time = str(int(start_f_num//(fps*60))) + ":" + str(int(start_f_num//fps%60))
            end_time = str(int(end_f_num//(fps*60))) + ":" + str(int(end_f_num//fps%60))

            package = {'start_time': start_time, 'end_time': end_time, 'boxes': frames}

            metadata['clip_' + str(v_num)] = package

            frames = {}

        if image == 'end':
            break

        first_image = cv2.imread(output_folder + image)
        h, w, layers = first_image.shape

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(output_folder + 'clip_' + str(v_num) + ".mp4", fourcc, fps, (w, h))

        start_f_num = f_num

    video_writer.write(cv2.imread(output_folder + image))

    json_file_path = output_folder + 'data_' + str(f_num) + '.json'
    with open(json_file_path, 'r') as jsonfile:
        json_data = jsonfile.read()
        xyxy = eval(json_data)
        xywh = [xyxy[0], xyxy[1], xyxy[2] - xyxy[0], xyxy[3] - xyxy[1]]
        frames['frame_' + str(f_num - start_f_num)] = xywh

    os.remove(json_file_path)
    os.remove(output_folder + image)

    prev = f_num

with open(output_folder + 'metadata.json', 'w') as jf:
    json.dump(metadata, jf)
    