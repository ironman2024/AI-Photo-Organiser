from PIL import Image
import imagehash
import os

def remove_duplicates(main_folder):
    walker=os.walk(main_folder)
    print(walker)
    uniquefiles=dict()

    for folder,sub_folders,files in walker:
        for file in files:
            filepath=os.path.join(folder,file)
            image=Image.open(filepath)
            image_hash=imagehash.dhash(image)
            print(f" dhash value:{image_hash}")

            if image_hash  in uniquefiles:
               
                os.remove(filepath)
                print(f"{filepath} has been deleted")
                
            else:
                uniquefiles[image_hash]=filepath
            
main_folder=r"Images"
remove_duplicates(main_folder)
