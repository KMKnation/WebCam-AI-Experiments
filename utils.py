from keras.utils import np_utils
from keras_preprocessing.image import ImageDataGenerator
from scipy.io import loadmat
from datetime import datetime
import os
import cv2


def calc_age(taken, dob):
    birth = datetime.fromordinal(max(int(dob) - 366, 1))

    # assume the photo was taken in the middle of the year
    if birth.month < 7:
        return taken - birth.year
    else:
        return taken - birth.year - 1


def get_meta(mat_path, db):
    meta = loadmat(mat_path)
    full_path = meta[db][0, 0]["full_path"][0]
    dob = meta[db][0, 0]["dob"][0]  # Matlab serial date number
    gender = meta[db][0, 0]["gender"][0]
    photo_taken = meta[db][0, 0]["photo_taken"][0]  # year
    face_score = meta[db][0, 0]["face_score"][0]
    second_face_score = meta[db][0, 0]["second_face_score"][0]
    age = [calc_age(photo_taken[i], dob[i]) for i in range(len(dob))]

    return full_path, dob, gender, photo_taken, face_score, second_face_score, age


def load_data(mat_path):
    d = loadmat(mat_path)
    data = d['wiki']
    d = { n : data[n][0,0] for n in data.dtype.names}

    return d["image"], d["gender"][0], d["age"][0], d["db"][0], d["img_size"][0, 0], d["min_score"][0, 0]

import pandas as pd
import re
def load_imdb(df_path):
    df = pd.read_csv(df_path)
    wikipath = os.path.join(folder, 'data')
    trainpath = os.path.join(wikipath, 'train')
    testpath = os.path.join(wikipath, 'test')
    X = []
    genders = []
    ages = []
    for index, rows in df.iterrows():
        if index == 0:
            continue
        imagename = rows['imagepath'].split('/')[1]
        img = None
        img = process_adience(os.path.join(trainpath, imagename))
        if type(img) == type(None):
            img = process_adience(os.path.join(testpath, imagename))

        print(index)
        X.append(img)
        genders.append(rows['gender'])
        ages.append(rows['age'])

    return X, genders, ages, None, 62, 0


import re

image = None
def process_adience(path):
    image = cv2.imread(path)
    image = cv2.resize(image, (62,62), cv2.INTER_AREA)
    image = image / 255
    return image


pattern = re.compile("[a-z]\w*\.\d{1,4}\.")


def get_age(mainDf, path):
    imagename = path.split('/')[-1]
    a = re.findall(pattern, imagename)
    imagename = imagename.replace(a[0], '')

    mainDf = mainDf[mainDf.loc[:, 'original_image'] == imagename]
    for index, row in mainDf.iterrows():
        try:
            return int(row['mod_age'])
        except Exception as err:
            print(err)
            return 0

    return 0


folder = '/run/user/1000/gvfs/smb-share:server=192.168.43.124,share=project_phase2'
import pickle
# import gc
def load_adience_data():
    trdata = ImageDataGenerator(width_shift_range=0.1,
                                height_shift_range=0.1,
                                horizontal_flip=True,
                                rescale=1. / 255)
    traindata = trdata.flow_from_directory(directory=os.path.join(folder, 'Adience/faces/train'),
                                           target_size=(224, 224), batch_size=32, shuffle=True)
    # tsdata = ImageDataGenerator(width_shift_range=0.1,
    #                             height_shift_range=0.1,
    #                             horizontal_flip=True,
    #                             rescale=1. / 255)
    # testdata = tsdata.flow_from_directory(directory=os.path.join(folder, 'Adience/faces/test'), target_size=(224, 224),
    #                                       batch_size=32, shuffle=True)

    X = []
    gender = []
    age = []

    mainDF = pd.read_csv(os.path.join(folder, 'Adience_dataset_processed.csv'))

    counter = 0
    for (data, label) in zip(traindata.filepaths, traindata.labels):
        print((data, label))
        X.append(process_adience(data))
        global image
        image = None
        # gc.collect()

        gender.append(label)
        ag = get_age(mainDF, data)
        age.append(ag)
        counter = counter + 1
        if counter == 10:
            break

    mainDF = None
    return X, gender, age, None, 62, 0


def mk_dir(dir):
    try:
        os.mkdir(dir)
    except OSError:
        pass



# print(gender)


def get_input(files):
    img = cv2.imread(files)

    img = cv2.resize(img, (62, 62))
    return img


def get_output(files):
    age = files.split('_')[0]

    return age


import random

import numpy as np
def image_generator(path, batch_size=52):
    while (True):

        batch_input = []
        ages = []
        genders = []

        for i in range(batch_size):
            folder_indexes = os.listdir(path)
            random_folder = random.randint(0, 1)
            gender = folder_indexes[random_folder]
            folderpath = os.path.join(path, folder_indexes[random_folder])

            files = os.listdir(folderpath)
            random.shuffle(files)
            batch_path = np.random.choice(a=files, size=batch_size)
            for input_path in batch_path:
                gendereye = np.zeros(2)
                ageeye = np.zeros(47)

                image_full_path = os.path.join(folderpath, input_path)
                inputs = get_input(image_full_path)
                age = get_output(input_path)

                batch_input.append(inputs)
                # ageeye[int(age)] = 1
                # ages.append(ageeye)
                ages.append(age)

                # gendereye[random_folder] = 1
                # genders.append(gendereye)
                genders.append(random_folder)
                break

        batch_x = np.array(batch_input)

        y_data_g = np_utils.to_categorical(genders, 2)
        y_data_a = np_utils.to_categorical(ages, 47)

        # genders = np.array(genders)
        # ages = np.array(ages)
        yield ((np.array(batch_x)), [y_data_g, y_data_a])
