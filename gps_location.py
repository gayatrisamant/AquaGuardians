import exifread
import os
from tabulate import tabulate

def get_gps_from_image(image_path):
    with open(image_path, 'rb') as f:
        tags = exifread.process_file(f, details=False)
    if 'GPS GPSLatitude' in tags and 'GPS GPSLongitude' in tags:
        latitude_dms = tags['GPS GPSLatitude'].values
        longitude_dms = tags['GPS GPSLongitude'].values
        latitude_ref = str(tags['GPS GPSLatitudeRef'])
        longitude_ref = str(tags['GPS GPSLongitudeRef'])

        latitude = convert_dms_to_dd(latitude_dms, latitude_ref)
        longitude = convert_dms_to_dd(longitude_dms, longitude_ref)

        return latitude, longitude

    return None

def convert_dms_to_dd(dms_tuple, ref):
    degrees = dms_tuple[0].num / dms_tuple[0].den
    minutes = dms_tuple[1].num / dms_tuple[1].den
    seconds = dms_tuple[2].num / dms_tuple[2].den

    decimal_degrees = degrees + (minutes / 60) + (seconds / 3600)

    if ref in ['S', 'W']:
        decimal_degrees = -decimal_degrees

    return decimal_degrees

def get_google_maps_link(latitude, longitude):
    google_maps_url = f'https://www.google.com/maps/search/?api=1&query={latitude},{longitude}'
    return google_maps_url




directory_path = 'C:/Users/GayatriSamant/OneDrive - kyndryl/Desktop/AI hack/AI Hackathon REVA University/Predict/'

# Create an empty list to store the file names
file_names = []

# Iterate over all files in the directory
for filename in os.listdir(directory_path):
    if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
        file_names.append(filename)

# Create an empty list to store the table rows
table_rows = []

# Iterate over the file names list and retrieve GPS info if available
for filename in file_names:

    image_path = os.path.join(directory_path, filename)
    gps_info = get_gps_from_image(image_path)

    if gps_info is not None:
        latitude, longitude = gps_info
        google_maps_link = get_google_maps_link(latitude, longitude)
        table_rows.append([filename, google_maps_link])

    else:
        print('No GPS information found in the image.')

# Print the table
table_headers = ["File Name", "GPS Info"]
table = tabulate(table_rows, headers=table_headers, tablefmt="grid")
print(table)
