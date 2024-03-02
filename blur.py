import cv2
import os
import sys
import shutil

def is_blurry(image_path, threshold=80):
    image = cv2.imread(image_path)

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    saturation = hsv[:,:,1]

    mean_saturation = saturation.mean()
    # Adjust threshold based on image type
    if image_path.endswith('.jpg') or image_path.endswith('.jpeg'):
        threshold = 100
    elif image_path.endswith('.png'):
        threshold = 200

    if  mean_saturation > threshold:
        return True
    else:
        return False


def detect_blurry_images(input_folder, output_folder):
    blurry_images = []
    blur_folder = 'Blur'

    # Create Blur folder if not exist
    if not os.path.exists(blur_folder):
        os.mkdir(blur_folder)

    for filename in os.listdir(input_folder):
        image_path = os.path.join(input_folder, filename)
        if is_blurry(image_path):
            blurry_images.append(filename)
            # Copy the blurry image to Blur folder
            shutil.copy(image_path, os.path.join(blur_folder, filename))
    return blurry_images

if __name__ == "__main__":
    input_folder = sys.argv[1]
    output_folder = 'Blur'

    blurry_images = detect_blurry_images(input_folder, output_folder)
    print("Blurry images:", blurry_images)
