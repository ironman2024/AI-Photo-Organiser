import cv2
import os

def is_blurry(image_path, threshold=50):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Extract the saturation channel
    saturation = hsv[:,:,1]

    # Compute the mean saturation value
    mean_saturation = saturation.mean()

    # Check if the mean saturation is below the threshold
    if mean_saturation < threshold:
        return True
    else:
        return False

def detect_blurry_images(folder_path):
    blurry_images = []
    for filename in os.listdir(folder_path):
        image_path = os.path.join(folder_path, filename)
        if is_blurry(image_path):
            blurry_images.append(filename)
    return blurry_images

# Folder path containing images
folder_path = "pictures"

# Detect blurry images
blurry_images = detect_blurry_images(folder_path)
print("Blurry images:", blurry_images)
