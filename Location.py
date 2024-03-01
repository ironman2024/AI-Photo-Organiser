import os
import exifread
from datetime import datetime
from PIL import Image

def get_image_metadata(image_path):
    try:
        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f)

            gps_latitude = tags.get('GPS GPSLatitude')
            gps_longitude = tags.get('GPS GPSLongitude')
            
            if gps_latitude and gps_longitude:
                lat_degrees = gps_latitude.values[0].num / gps_latitude.values[0].den
                lat_minutes = gps_latitude.values[1].num / gps_latitude.values[1].den
                lat_seconds = gps_latitude.values[2].num / gps_latitude.values[2].den
                latitude = lat_degrees + lat_minutes / 60 + lat_seconds / 3600

                lon_degrees = gps_longitude.values[0].num / gps_longitude.values[0].den
                lon_minutes = gps_longitude.values[1].num / gps_longitude.values[1].den
                lon_seconds = gps_longitude.values[2].num / gps_longitude.values[2].den
                longitude = lon_degrees + lon_minutes / 60 + lon_seconds / 3600

                gps_location = (latitude, longitude)
            else:
                gps_location = None
            date_time = tags.get('EXIF DateTimeOriginal')
            if date_time:
                date_time_str = str(date_time)
                date_obj = datetime.strptime(date_time_str, '%Y:%m:%d %H:%M:%S')
                day_date = date_obj.strftime('%Y-%m-%d')
            else:
                day_date = None

        return gps_location, day_date

    except (IOError, OSError, exifread.ExifReadError, ValueError) as e:
        print(f"Error processing {image_path}: {e}")
        return None, None

def process_files_in_directory(source_directory, destination_directory, no_metadata_directory):
    for filename in os.listdir(source_directory):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            file_path = os.path.join(source_directory, filename)
            gps_location, day_date = get_image_metadata(file_path)

            if day_date and gps_location:
                date_folder = os.path.join(destination_directory, day_date)
                location_folder = os.path.join(date_folder, f"{gps_location[0]}, {gps_location[1]}")

                os.makedirs(location_folder, exist_ok=True)

                new_file_path = os.path.join(location_folder, filename)
                os.rename(file_path, new_file_path)
            else:

                no_metadata_folder = os.path.join(no_metadata_directory, "NoMetadata")
                os.makedirs(no_metadata_folder, exist_ok=True)

                new_file_path = os.path.join(no_metadata_folder, filename)
                os.rename(file_path, new_file_path)

source_directory = r"D:\iphone"

destination_directory = r"D:\SortedPhotos"

no_metadata_directory = r"D:\NoMetadataPhotos"

process_files_in_directory(source_directory, destination_directory, no_metadata_directory)
