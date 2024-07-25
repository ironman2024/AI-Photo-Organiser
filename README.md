# AI Photo Organiser

## Image Processing Server
**Problem statement** : 
Create an AI based solution that separates duplicates, blur photos from a given set of photos and logically organizes photos based on location, date etc. This can help create photo albums automatically based on different attributes from the huge number of photos available.

**Overview** : 
The Image Processing Server is a web application that allows users to upload images, process them, and download the processed results. The server performs various image processing tasks, including duplicate removal, blur detection, and location-based sorting.

**Features**
1. Image Upload: Users can upload images through a web interface.
2. Duplicate Removal: The server identifies and removes duplicate images from the uploaded files.
3. Blur Detection: Images are scanned for blur, and blurry images are identified and separated.
4. Location-based Sorting: Images are sorted into folders based on their geographical location, if available in the image metadata.
5. Output Zip Creation: The processed images are packaged into a zip file for easy download by the user.
6. Clean-up: After processing, the server clears uploaded images and processed results to conserve disk space.

**Installation**
1. Clone the repository to your local machine.
2. Install the required dependencies by running npm install in the project directory.
3. Make sure Python is installed on your system, as the server relies on Python scripts for image processing tasks.
4. Run the server by executing node server.js.
5. Access the server through your web browser at http://localhost:3001.

**Usage**
1. Navigate to the upload page on the web interface.
2. Select one or more images to upload.
3. Submit the upload form to start image processing.
4. After processing, the server will generate a zip file containing the processed images.
5. Download the zip file from the provided link.
6. The server will automatically clean up uploaded images and processed results to maintain disk space.

**System Architecture**
![Research and design](https://github.com/ironman2024/Hacksprintv5.o_AIML02_CtrlShiftHack/assets/113116636/e858fdec-2986-446e-89d1-9fffc12a9334)


**Dependencies**
1. Node.js
2. Express.js
3. Multer
4. Archiver
5. Python (with required libraries for image processing)


**Authors**
1. Atharva Karval
2. Samarth Patil
3. Shweta Ingole
4. Swarali Kulkarni

*Acknowledgements*: Special thanks to Anushka Vaidya for their contributions to this project.
