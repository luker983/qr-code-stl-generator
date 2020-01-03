#!/usr/local/bin/python3

import qr_img
import subprocess

blender_path = '/Applications/Blender.app/Contents/MacOS/Blender'

auth_type = 'WPA'
ssid = 'SSID_GOES_HERE'
password = 'PASSWORD_GOES_HERE'

data = 'WIFI:T:%s;S:%s;P:%s;;'%(auth_type, ssid, password)

qr_img.generate_png(data=data, icon_path='files/wifi.png', output_path='files/qr.png')
qr_img.generate_svg(data=data, output_path='files/qr.svg')
subprocess.run([blender_path, '--background', '--python', 'qr_blend.py'])
