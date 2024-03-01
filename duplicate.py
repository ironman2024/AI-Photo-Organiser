from PIL import Image
import imagehash
import os
main_folder=r"path"
images_folder=os.path.join(main_folder,'images_dataset')
dhash_threshold=5

images=[f for f in os.listdir(images_folder)if os.path.isfile(os.path.join(images_folder,f))]

duplicate_count=0

for i in range(len(images)):
   image_path= os.path.join(images_folder,images[i])
   image=Image.open(image_path)
   hash_value_i=imagehash.dhash(image)
   print(f"Image: {images[i]} | dhash value :{hash_value_i}")
   for j in range(i+1,len(images)):
        image_path= os.path.join(images_folder,images[j])
        image=Image.open(image_path)
        hash_value_j=imagehash.dhash(image)
        if abs(hash_value_j-hash_value_i) <= dhash_threshold:
                print(f"Duplicate image Found using dhash:    {images[i]} | {images[j]}")
                duplicate_count+=1
print(f"Total number of duplicate counts are: {duplicate_count}")
