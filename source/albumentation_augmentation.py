# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import time
import cv2
import random
import glob
import shutil
import os
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
from albumentations import (
    HorizontalFlip, IAAPerspective, ShiftScaleRotate, CLAHE, RandomRotate90, RandomGamma, VerticalFlip,
    Transpose, ShiftScaleRotate, Blur, OpticalDistortion, GridDistortion, HueSaturationValue, 
    IAAAdditiveGaussianNoise, GaussNoise, MotionBlur, MedianBlur, RandomBrightnessContrast, IAAPiecewiseAffine,
    IAASharpen, IAAEmboss, Flip, OneOf, Compose, Rotate, RandomContrast, RandomBrightness, RandomCrop, Resize, OpticalDistortion
)


def aug_options(p=1):
    return Compose([
        Resize(224, 224),
RandomCrop(224,224, p=0.5),  # 위에꺼랑 세트
        
        OneOf([
        RandomContrast(p=1, limit=(-0.5,2)),   # -0.5 ~ 2 까지가 현장과 가장 비슷함  -- RandomBrightnessContrast
        RandomBrightness(p=1, limit=(-0.2,0.4)),
        RandomGamma(p=1, gamma_limit=(80,200)),
        ], p=0.6),
            
        OneOf([
            Rotate(limit=30, p=0.3),
            RandomRotate90(p=0.3),
            VerticalFlip(p=0.3)
        ], p=0.3),
    
        MotionBlur(p=0.2),   # 움직일때 흔들리는 것 같은 이미지
        ShiftScaleRotate(shift_limit=0.001, scale_limit=0.1, rotate_limit=30, p=0.3, border_mode=1),
        Resize(224,224, p=1),
        ],
        p=p)


def apply_aug(aug, image):
    image = aug(image=image)['image']
    return image


def show_img_distribution(img_df):
    print(img_df)
    print(img_df['label'].value_counts().sort_index())

    # plt.figure(figsize=(14, 6))
    img_df['label'].value_counts().sort_index().plot.barh(figsize=(14,10), title='Num of images Distribution')
    plt.xlabel('NUM OF IMAGES')
    plt.ylabel('CLASS_NAMES')
    plt.show()

    os.system("clear")

def show_splited_datasets(train_set, valid_set):
    labels = train_set['label'].sort_index()
    train_set_imgs = train_set['label'].value_counts().sort_index()
    valid_set_imgs = valid_set['label'].value_counts().sort_index()

    print("Train Set Distribution \n", train_set_imgs)
    print('=======================================================================')
    print("Validation Set Distribution \n", valid_set_imgs)

    index = []
    for l in labels:
        if l in index:
            pass
        else:
            index.append(l)

    train_imgs_num = []
    valid_imgs_num = []

    for i in train_set_imgs:
        train_imgs_num.append(i)

    for i in valid_set_imgs:
        valid_imgs_num.append(i)

    df = pd.DataFrame({'train imgs':train_imgs_num, 'valid imgs':valid_imgs_num}, index=index)

    df.plot.barh(title='Num of images Distribution', figsize=(14, 10))
    plt.show()
    

def show_aug_sampels(path):
    print("Show augmented image samples")
    imgs = glob.glob(path + '/*/*.jpg')
    idx = random.randint(0, len(imgs))

    for i in range(0, 10):
        image = cv2.imread(imgs[idx])
        aug = aug_options(p=1)
        aug_img = apply_aug(aug, image)

        numpy_horizontal = np.hstack((image, aug_img))
        numpy_horizontal_concat = np.concatenate((image, aug_img), axis=1)
        numpy_horizontal_concat = cv2.resize(numpy_horizontal_concat, (1280, 720))

        cv2.imshow('Original / Augmentation', numpy_horizontal_concat)
        cv2.waitKey(300)
    cv2.destroyAllWindows()

    os.system('clear')


def aug_processing(data_set, output_path, is_train):
    img_path = data_set['image_path'].sort_index()

    if is_train == True:
        output_path = output_path + '/train'

    else:
        output_path = output_path + '/valid'
    
    for img in img_path:
        file_name = img.split('/')[-1]
        class_name = img.split('/')[-2]

        print(class_name, file_name)
        image = cv2.imread(img)
        aug = aug_options(p=1)

        if not (os.path.isdir(output_path + '/' + class_name)):
            os.makedirs(output_path + '/' + class_name)

        else:
            pass

        idx = 0
        for i in range(0, 10):
            aug_img = apply_aug(aug, image)
            cv2.imwrite(output_path + '/' + class_name + '/' + str(idx) + '_' + file_name , aug_img)

if __name__ == "__main__":
    # Dataset Path define
    path = '/data/backup/pervinco_2020/datasets/test'
    dataset_name = path.split('/')[-1]
    output_path = '/data/backup/pervinco_2020/Auged_dataset/' + dataset_name

    # Dataset Load & visualization
    result = []
    idx = 0
    label_list = sorted(os.listdir(path))

    for label in label_list:
        file_list = glob.glob(os.path.join(path,label,'*'))
        
        for file in file_list:
            result.append([idx, label, file])
            idx += 1
            
    img_df = pd.DataFrame(result, columns=['idx','label','image_path'])
    show_img_distribution(img_df)

    # Split Train set, Validation set + Visualization
    train_set, test_set = train_test_split(img_df, test_size=0.2, shuffle=True)
    show_splited_datasets(train_set, test_set)

    aug_processing(train_set, output_path, is_train=True)
    aug_processing(test_set, output_path, is_train=False)

    