import argparse
import glob
import os
import os.path as osp
import pandas as pd
import cv2
from pathlib import Path
from skmultilearn.model_selection import iterative_train_test_split

def get_frame_number(video):
    capture = cv2.VideoCapture(video)

    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    capture.release()
    return frame_count

def clean_df(df, dir, modality):
    modality_field = f"{modality}_name"
    index_to_removed = []

    for idx, row in df.iterrows():
        if not os.path.isfile(os.path.join(dir, row[modality_field])):
            index_to_removed.append(idx)

        if row[modality_field].startswith('_'):
            index_to_removed.append(idx)

    return df.drop(index_to_removed)

def convert_csv_to_ann(csv_path, modality):
    modality_field = f"{modality}_name"
    df = pd.read_csv(csv_path)
    csv_path = Path(csv_path)

    df = clean_df(df, csv_path.parent, modality)

    data_df = df[[modality_field]]
    label_df = df[["neutral", "happy", "sad", "contempt", "anger", "disgust", "surprised", "fear"]]

    data_train, label_train, data_test, label_test = iterative_train_test_split(
        data_df[[modality_field]].values,
        label_df[["neutral", "happy", "sad", "contempt", "anger", "disgust", "surprised", "fear"]].values,
        test_size = 0.2
    )

    emotions = ['neutral', 'happy', 'sad', 'contempt', 'anger', 'disgust', 'surprised', 'fear']
    class_emotions = []
    train_rows = []
    val_rows = []

    for index, video in enumerate(data_train):
        for idx, emotion in enumerate(emotions):
            if int(label_train[index][idx]) == 1:
                class_emotions.append(idx)
    
        items = " ".join(map(str, class_emotions))

        if modality == 'audio':
            audio_name = video[0].replace('wav', 'npy')
            vid_fname = os.path.join('data', 'response_video', video[0].replace('stimuli', 'response').replace("wav", "mp4"))
            # print(vid_fname)
            frame_number = get_frame_number(vid_fname) // 20

            if frame_number > 0:
                train_rows.append(f"{audio_name} {frame_number} {items}")
        else:
            train_rows.append(f"{audio_name} {items}")

        class_emotions = []

    for index, video in enumerate(data_test):
        for idx, emotion in enumerate(emotions):
            if int(label_test[index][idx]) == 1:
                class_emotions.append(idx)

        items = " ".join(map(str, class_emotions))

        if modality == 'audio':
            audio_name = video[0].replace('wav', 'npy')
            vid_fname = os.path.join('data', 'response_video', video[0].replace('stimuli', 'response').replace("wav", "mp4"))
            frame_number = get_frame_number(vid_fname) // 20

            if frame_number > 0:
                val_rows.append(f"{audio_name} {frame_number} {items}")
        else:
            val_rows.append(f"{audio_name} {items}")

        class_emotions = []

    with open(os.path.join(csv_path.parent, f"{csv_path.stem}_train.txt"), 'w') as f:
        for row in train_rows:
            f.write(f"{row}\n")
    
    with open(os.path.join(csv_path.parent, f"{csv_path.stem}_val.txt"), 'w') as f:
        for row in val_rows:
            f.write(f"{row}\n")

def convert_csv_to_ann2(csv_path, modality):
    modality_field = f"{modality}_name"
    df = pd.read_csv(csv_path)
    csv_path = Path(csv_path)

    df = clean_df(df, csv_path.parent, modality)

    data_df = df[[modality_field]]
    label_df = df[["neutral", "happy", "sad", "contempt", "anger", "disgust", "surprised", "fear"]]

    data_train, label_train, data_test, label_test = iterative_train_test_split(
        data_df[[modality_field]].values,
        label_df[["neutral", "happy", "sad", "contempt", "anger", "disgust", "surprised", "fear"]].values,
        test_size = 0.2
    )

    emotions = ['neutral', 'happy', 'sad', 'contempt', 'anger', 'disgust', 'surprised', 'fear']
    class_emotions = []
    train_rows = []
    val_rows = []

    for index, video in enumerate(data_train):
        for idx, emotion in enumerate(emotions):
            class_emotions.append(int(label_train[index][idx]))
            #if int(label_train[index][idx]) == 1:
            #    class_emotions.append(idx)

        
        items = " ".join(map(str, class_emotions))
        train_rows.append(f"{video[0]} {items}")
        class_emotions = []

    for index, video in enumerate(data_test):
        for idx, emotion in enumerate(emotions):
            class_emotions.append(int(label_test[index][idx]))
            #if int(label_test[index][idx]) == 1:
            #    class_emotions.append(idx)
            #else:
            #    class_emotions.append(idx)

        items = " ".join(map(str, class_emotions))
        val_rows.append(f"{video[0]} {items}")
        class_emotions = []

    with open(os.path.join(csv_path.parent, f"{csv_path.stem}_train.txt"), 'w') as f:
        for row in train_rows:
            f.write(f"{row}\n")
    
    with open(os.path.join(csv_path.parent, f"{csv_path.stem}_val.txt"), 'w') as f:
        for row in val_rows:
            f.write(f"{row}\n")

def parse_args():
    parser = argparse.ArgumentParser(
        description='Convert csv to annotation file')
    parser.add_argument('--csv_path', type=str, help='source video directory')
    parser.add_argument('--modality', type=str, default='video', help='Modality')
    args = parser.parse_args()

    return args


if __name__ == '__main__':
    args = parse_args()

    if not osp.exists(args.csv_path):
        print(f"File {args.csv_path} not exist")
        exit()
    
    convert_csv_to_ann(args.csv_path, args.modality)
