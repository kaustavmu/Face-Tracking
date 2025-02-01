# Face Tracker

This library contains a script that can track a face in a video based on a reference image. It is written in python and made to run on a CPU. 

## Installation
The script is run on Python version 3.10.11. To install the script, you can run the following commands:

    git clone https://github.com/kaustavmu/Face-Tracking/
    cd Face-Tracking
    python3 -m venv venv

If on Linux or Mac, run:

    source ./venv/bin/activate
If on Windows:

    ./venv/Scripts/activate

Finally:

    python3 -m pip install -r requirements.txt

## Usage

The script takes the following inputs:

 1. **Reference Image**: A path to a .jpeg or .png image of any size or shape, containing mainly the target face to be tracked.
 2. **Video**: A path to a .mp4 video of any length.
 3. **Output Folder**: Output folder path.
 4. **Processes**: Number of subprocesses to be run concurrently. This is used to speed up the processing of the frames.

The script has the following outputs:

1. **Clips**: Cropped clips of the image containing the target face.
2. **Metadata**: Metadata for each clip, consisting of start times, end times, and the bounding box in [x, y, width, height] format for the face in each frame of each clip.

To run the script, use the following command:

    python3 process.py -r {reference image path} -v {video path} -o {output folder path} -p {number of processes}

For example,

    python3 process.py -r 'reference.png' -v 'video.mp4' -p 4 -o 'output'

## Assumptions and Limitations

This script makes the following assumptions about the content and format of the video:

 - Only one person with the reference face is in every frame. If not, it will only detect one.
 - The face is of sufficient resolution to be detected by RetinaFace and DeepFace.
 - An assumption is made that a scene change occurs when the face changes from being visible to not visible. In the case that a scene change occurs but the face is visible in both of them, they will be in a single clip.
   
## Samples
[Here](https://drive.google.com/drive/folders/1iW7iCTOLdKXwhZdyIHd6v5dwv11xWOSK?usp=drive_link) is a link to a google drive folder with sample videos, reference images, and outputs.
