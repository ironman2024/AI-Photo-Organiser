import PIL.Image
import PIL.ExifTags

img = PIL.Image.open("Test.jpg")

if hasattr(img, "_getexif") and callable(getattr(img, "_getexif")):
    exif = {
        PIL.ExifTags.TAGS[k]: v
        for k, v in img._getexif().items()
        if k in PIL.ExifTags.TAGS
    }
    print(exif)
else:
    print("NO data Found!")
