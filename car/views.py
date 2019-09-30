import os
import datetime

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from car.utils import *
from car.models import CarsAll


def index(request):
    return render(request, 'index.html', {
            'car_img_path': '',
            'license_plate': '',
            'entry_time': '',
            'exit_time': '',
            'cost': 0,
        })


@csrf_exempt
def upload_img(request):
    if request.method == 'GET':
        return render(request, 'upload.html')
    elif request.method == 'POST':
        # 获取上传的文件对象
        car_img = request.FILES.get('file_data', None)
        if not car_img:
            # 如果没有上传，则重定向到首页
            return HttpResponseRedirect('/index/')
        else:
            # 修改上传的文件名为时间戳
            img_name = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + os.path.splitext(car_img.name)[1]
            car_img_path = os.path.join(CAR_IMG_DIR, img_name)
            # 保存文件
            with open(car_img_path, 'wb') as car_img_wb:
                for chunk in car_img.chunks():
                    car_img_wb.write(chunk)

            # 入库
            update_model(img_name)

            return JsonResponse({
                            'success': True,
                            'msg': 'Upload succeed'
                          })


def info(request):
    license_plate = request.GET.get('license_plate', '000000')
    query_result = CarsAll.objects.filter(license_id=license_plate)
    if query_result:
        car = query_result.order_by('-entry_time')[0]
        return render(request, 'info.html', {
            'car_img_path': '/car_img/' + os.path.basename(car.image_path),
            'license_plate': license_plate,
            'entry_time': car.entry_time.strftime("%Y-%m-%d %H:%M:%S"),
            'exit_time': car.exit_time.strftime("%Y-%m-%d %H:%M:%S") if car.exit_time.year != 1970 else '',
            'cost': '${0:.2f}'.format(cost(car.entry_time, car.exit_time)),
        })
    else:
        return JsonResponse({
            'error': True,
            'msg': 'No license plate was found',
        })


def car_img(request, img_name):
    with open(os.path.join(CAR_IMG_DIR, img_name), 'rb') as img:
        return HttpResponse(img.read())
