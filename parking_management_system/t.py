# coding: utf-8
from license_image_extraction import extraction
from recognize_license_id import text

#export GOOGLE_APPLICATION_CREDENTIALS="/Users/zhizhouqiu/Desktop/web1127/parking_management_system/EC601MiniProject1.json"
car_path = "car10.jpg"
license_plate_path = 'license.jpg'
json_path = "EC601MiniProject1.json"


def extract_license_plate(car_pic_path, license_plate_path, json_path):
    upd_time = extraction.time_extraction(car_path)
    extraction.store_license_plate(car_path, license_plate_path)
    license_id = str(text.recognize(license_plate_path, json_path))
    license_id = license_id.replace("\n","")
    license_id = license_id.replace(" ","")
    license_id = license_id.replace("·","")
    #license_id = 'LEM446AA'
    return license_id


