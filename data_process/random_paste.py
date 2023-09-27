import os
import cv2
import json
import random
from tqdm import tqdm


def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    if w>=1:
        w=0.99
    if h>=1:
        h=0.99
    return (x,y,w,h)


def random_paste(bg_image, paste_image):
    bh, bw, bc = bg_image.shape
    ph, pw, pc = paste_image.shape
    pos_x = random.randint(0, bw-pw)
    pos_y = random.randint(0, bh-ph)

    ran_p = random.uniform(0.05, 0.35)
    com = cv2.addWeighted(bg_image[pos_y:pos_y + ph, pos_x: pos_x+pw], ran_p, paste_image, 1- ran_p, 0)
    bg_image[pos_y:pos_y + ph, pos_x: pos_x+pw] = com

    box = [pos_x, pos_x+pw, pos_y, pos_y + ph]

    return bg_image, box



if __name__ == "__main__":

    image_dir = r"D:\qrcode\kuihuama\666\VOCdevkit\VOC2012\JPEGImages"
    image_files = os.listdir(image_dir)

    mask_dir = r"D:\qrcode\kuihuama\666\temp"
    mask_files = os.listdir(mask_dir)

    save_dir = r"D:\qrcode\kuihuama\666\dst"
    os.makedirs(save_dir, exist_ok=True)

    
    for file in tqdm(image_files[:5000]):
        bg_file = os.path.join(image_dir, file)
        bg_image = cv2.imread(bg_file)

        mask_file = random.choice(mask_files)
        mask_image = cv2.imread(os.path.join(mask_dir, mask_file), 1)

        ref_h = min(bg_image.shape[0], bg_image.shape[1])
        resize_h = random.randint(ref_h // 10, ref_h // 2)

        mask_image = cv2.resize(mask_image, [resize_h, resize_h])
        dst_image, box = random_paste(bg_image, mask_image)
        save_file = os.path.join(save_dir, "kuihuama_synth_" + os.path.basename(file))
        cv2.imwrite(save_file, dst_image)

        bb = convert((bg_image.shape[1], bg_image.shape[0]), box)
        with open(save_file.replace(".jpg", ".txt"), "w+" ,encoding='UTF-8') as out_file:
            out_file.write(str(2) + " " + " ".join([str(a) for a in bb]) + '\n')

