import os
import cv2
import json
from tqdm import tqdm


def read_yolo_data(txt_path):
    yolo_data = []
    with open(txt_path, 'r') as file:
        for line in file:
            values = line.strip().split()
            class_id = int(values[0])
            x_center, y_center, bbox_width, bbox_height = map(float, values[1:])
            yolo_data.append((class_id, x_center, y_center, bbox_width, bbox_height))
    return yolo_data
 
def draw_bbox(image_path, yolo_data):
    img = cv2.imread(image_path)
    if img is None:
        print(image_path)
    height, width, _ = img.shape
 
    for ind, data in enumerate(yolo_data):
        #如果是yolox的xyxy格式不用再进行转化了
        class_id, x_center, y_center, bbox_width, bbox_height = data
        x_min = int((x_center - bbox_width / 2) * width)
        y_min = int((y_center - bbox_height / 2) * height)
        x_max = int((x_center + bbox_width / 2) * width)
        y_max = int((y_center + bbox_height / 2) * height)
 
        # cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

        box_image = img[y_min: y_max, x_min: x_max]
        save_file = os.path.join(save_folder, os.path.basename(image_path)+"_" + str(ind) + ".jpg")
        cv2.imwrite(save_file, box_image)

    return img
 

def main():
    for file in tqdm(os.listdir(txt_folder)):
        if file.endswith('.txt'):
            txt_path = os.path.join(txt_folder, file)
            yolo_data = read_yolo_data(txt_path)
 
            image_path = os.path.join(img_folder, file[:-4] + '.jpg')
            # print(image_path)

            img_with_bbox = draw_bbox(image_path, yolo_data)


if __name__ == "__main__":
    json_data = []
    img_folder = r'D:\qrcode\kuihuama\hand_label\images'
    txt_folder = r'D:\qrcode\kuihuama\hand_label\labels'
    save_folder = r'D:\qrcode\kuihuama\hand_label\temp'
    os.makedirs(save_folder, exist_ok=True)
    main()
