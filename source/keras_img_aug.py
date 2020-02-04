import tensorflow as tf
import numpy as np
import glob
import os

path = sorted(glob.glob('/home/barcelona/pervinco/datasets/four_shapes/train_no_bg/*'))
output_path = '/home/barcelona/pervinco/datasets/four_shapes/train_no_bg_aug/'
print('label num : ', len(path))

data_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255,
                                                                 rotation_range=360,
                                                                 width_shift_range=0.2,
                                                                 height_shift_range=0.2,
                                                                 zoom_range=0.1)


path = sorted(glob.glob('/home/barcelona/pervinco/datasets/four_shapes/train_no_bg/*/*.png'))
print(len(path))

for image in path:
    folder = image.split('/')[-2]
    print('processing', folder, image)
    image = tf.keras.preprocessing.image.load_img(image)
    image = tf.keras.preprocessing.image.img_to_array(image)
    image = tf.image.resize(image, (224, 224))
    image = np.expand_dims(image, 0)
    data_generator.fit(image)

    if not (os.path.isdir(output_path + folder)):
        os.makedirs(output_path + folder)

    for x, val in zip(data_generator.flow(image, save_to_dir=output_path + folder, save_prefix=folder, save_format='jpg'), range(30)):
        pass