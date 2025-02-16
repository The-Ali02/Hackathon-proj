import sys
import cv2
import matplotlib.pyplot as plt
import torch
import argparse
import pprint
import distutils
import os
import os.path
import os
from moviepy.editor import VideoFileClip
from glob import glob
from json.tool import main
from statistics import mode
from scipy.special import expit
from cv2 import VIDEOWRITER_PROP_FRAMEBYTES
from utils import utils, ensemble
from architectures.fornet import FeatureExtractor
from architectures import fornet
from blazeface import FaceExtractor, BlazeFace, VideoReader
from pathlib import Path
from distutils import util

sys.path.append('..')

def testVideo(Annotation):

    media_type = 'video'
    data_dir = r"../input/"
    dataset = 'dfdc'
    model = ['TimmV2', 'TimmV2ST']
    model_dir = '..\models/'
    blazeface_dir = 'blazeface/'
    face_policy = 'scale'
    face_size = 224
    fpv = 32
    device = torch.device('cuda:{:d}'.format(args.device)) if torch.cuda.is_available() else torch.device('cpu')
    num_videos = 1
    annotate = Annotation
    output_dir = 'buffer/'
    video_idxs = [0]

    file_names, video_glob = utils.get_video_paths(data_dir, num_videos)

    model_choices = {'v2': 'TimmV2', 'v2st': 'TimmV2ST','vit': 'ViT', 'vitst': 'ViTST'}

    model_paths = utils.get_model_paths(model, model_dir, dataset, choices=model_choices)

    models_loaded = utils.load_weights(model_paths, model_choices, device) 

    ensemble_models = ensemble.ensemble(models_loaded, device)

    transformer = utils.get_transformer(face_policy, face_size, models_loaded[0].get_normalizer(), train=False)

    if(media_type == 'video'):
        if(annotate):
            predictions = utils.extract_predict_annotate(
                output_dir, ensemble_models, video_glob, video_idxs, transformer, blazeface_dir, device, models_loaded)

        else:
            face_extractor = utils.load_face_extractor(
                blazeface_dir, device, fpv)
            print('Face extractor Loaded!')

            faces, faces_frames = utils.extract_faces(
                data_dir, file_names, video_idxs, transformer, face_extractor, num_videos, fpv)
            print("Faces extracted and transformed!")

            predictions, predictions_frames = utils.predict(
                ensemble_models, data_dir, file_names, video_idxs, num_videos, faces, faces_frames, model, save_csv=True, true_class=False)


def convert_avi_to_mp4(input_path, output_path):
 
    os.makedirs(output_path, exist_ok=True)
    files = os.listdir(input_path)

    for file in files:
        if file.endswith(".avi"):
            input_file_path = os.path.join(input_path, file)
            output_file_path = os.path.join(output_path, file.replace(".avi", ".mp4"))

            clip = VideoFileClip(input_file_path)
            clip.write_videofile(output_file_path, codec="libx264")
            clip.close()

def displayOutput(Annotation):

    testVideo(Annotation)
    convert_avi_to_mp4(r"C:/Users/abdul/Documents/HackRrev/DeepFake-Spot/src/buffer", r"C:/Users/abdul/Documents/HackRrev/DeepFake-Spot/output/")

def delete_files_in_directory(directory_path):
    try:
        files = os.listdir(directory_path)

        for file in files:
            file_path = os.path.join(directory_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")

        print("All files deleted successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

def clearDirectories(*directories):
    for directory in directories:
        delete_files_in_directory(directory)


if __name__ == "__main__" :
    
        # convert_avi_to_mp4(r"C:/Users/abdul/Documents/HackRrev/DeepFake-Spot/src/buffer", r"C:/Users/abdul/Documents/HackRrev/DeepFake-Spot/output/")


    # clearDirectories(r"C:/Users/abdul/Documents/HackRrev/DeepFake-Spot/input", r"C:/Users/abdul/Documents/HackRrev/DeepFake-Spot/src/buffer" , r"C:/Users/abdul/Documents/HackRrev/DeepFake-Spot/output" )

    displayOutput(True)