from PIL import Image
import imagehash
import os
main_folder=r"data_path"
images_folder=os.path.join(main_folder,'images_dataset')
images=[f for f in os.listdir(images_folder)if os.path.isfile(os.path.join(images_folder,f))]
images.sort()

for i in range(len(images)):
   image_path= os.path.join(images_folder,images[i])
   image=Image.open(image_path)
   hash_value_i=imagehash.dhash(image)
   print(f"Image: {images[i]} | dhash value :{hash_value_i}")
   for j in range(i+1,len(images)):
        image_path= os.path.join(images_folder,images[j])
        image=Image.open(image_path)
        hash_value_j=imagehash.dhash(image)
        if(hash_value_j==hash_value_i):
           print(f"Duplicate image Found:    {images[i]} | {images[j]}")
