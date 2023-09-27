import os
import glob
import shutil
import random
from tqdm import tqdm
from tqdm.contrib import tzip


images_dir = "qrcode/all/images"
labels_dir = "qrcode/all/labels"

images_val_dir = "qrcode/all/images_val"
labels_val_dir = "qrcode/all/labels_val"
os.makedirs(images_val_dir, exist_ok=True)
os.makedirs(labels_val_dir, exist_ok=True)

image_files = glob.glob(images_dir + "/*")
label_files = glob.glob(labels_dir + "/*")

train_txt = open("qrcode/train.txt", 'w')
val_txt = open("qrcode/val.txt", 'w')

# split train and val
random.seed(1024)
random.shuffle(image_files)
for index, image_file in enumerate(image_files):
    image_name = os.path.splitext(os.path.basename(image_file))[0]
    img_path = image_file
    info = os.path.abspath(img_path) + "\n"
    if index <= int(0.1*len(image_files)):
        val_txt.write(info)
        shutil.copy2(image_file, images_val_dir)
        shutil.copy2(os.path.join(labels_dir, image_name + '.txt'), labels_val_dir)
    else:
        train_txt.write(info)

train_txt.close()
val_txt.close()

