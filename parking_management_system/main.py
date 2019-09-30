#import parking_management_system.license_plate_extraction
#import model
from parking_management_system import license_plate_extraction
training = True
recognize = True
save_path = "/Users/zhizhouqiu/desktop/web1127/plate_pic/original_licenseplate.png"
model_path = "/Users/zhizhouqiu/desktop/web1127/svc.pkl"
car_path = "/Users/zhizhouqiu/Desktop/web1127/car_pic/car5.jpg"

def extract_license_plate(car_path, save_path, model_path):
    license_plate_extraction.extraction.store_license_plate(car_path, save_path)
    license_id = str(license_plate_extraction.segmentation.character_recognization(save_path, model_path))
    license_id = license_id.replace("\n", "")
    license_id = license_id.replace(" ", "")
    license_id = license_id.replace("·", "")
    #license_id = license_id.replace()
    return license_id


if __name__ == '__main__':
	extract_license_plate(car_path, license_plate_path, model_path)
