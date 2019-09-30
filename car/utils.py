# coding:utf-8
import os
import datetime
from math import ceil

from car.models import CarsAll, CarsIn
from parking_management_system.main import extract_license_plate


# 获取car文件夹下的car_img文件夹的地址
CAR_IMG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'car_img')


def update_model(img_name):
    plate_name = '%s_plate%s' % os.path.splitext(img_name)
    # 准备参数
    car_img_path = os.path.join(CAR_IMG_DIR, img_name)
    license_plate_path = os.path.join(CAR_IMG_DIR, plate_name)
    # 提取车牌号
    car_license_plate = extract_license_plate(car_img_path,
                                              license_plate_path,
                                              '/Users/gangwei/desktop/web1127/svc.pkl')

    # 从图片名中获取拍摄时间
    year, month, day, hour, minute, second = map(int, os.path.splitext(img_name)[0].split('_'))
    upd_time = datetime.datetime(year, month, day, hour, minute, second)

    # 查询对应的车是否已经存在数据表cars_all中，没有的话，此次为入库，有的话此次为出库
    query_result = CarsAll.objects.filter(license_id=car_license_plate).filter(exit_time=datetime.datetime(1970, 1, 1))
    if query_result:
        # 出库
        query_result.update(exit_time=upd_time, image_path=car_img_path)
        CarsIn.objects.filter(license_id=car_license_plate).delete()
    else:
        # 入库
        CarsAll.objects.create(license_id=car_license_plate,
                               entry_time=upd_time,
                               exit_time=datetime.datetime(1970, 1, 1),
                               image_path=car_img_path)
        CarsIn.objects.create(license_id=car_license_plate, entry_time=upd_time)


def cost(entry_time, exit_time):
    """
    根据入库和出库时间计算停车费用，每分钟$1/60，不满一分钟，按照一分钟算
    :param entry_time: datetime.datetime 入库时间，UTC
    :param exit_time: datetime.datetime 出库时间，当出库时间为1970年时，出库时间设定为timezone.now() UTC
    :return: float 停车费用
    """
    if exit_time.year == 1970:
        exit_time = datetime.datetime.now()
    return ceil((exit_time - entry_time).total_seconds() / 60) * (1 / 60)
