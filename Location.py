from PIL import Image

# Open the image file
image_path = r"C:\Users\Lenovo\Downloads\image_67186177.JPG"  # Replace with the path to your image
image = Image.open(image_path)

# Get image metadata
metadata = image.info

# Print metadata
print("Image Metadata:")
for key, value in metadata.items():
    print(f"{key}: {value}")

# Extract the threshold value (if available)
threshold = metadata.get('threshold')
if threshold is not None:
    print(f"Threshold value: {threshold}")
else:
    print("Threshold value not found in metadata.")
