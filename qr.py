#!/usr/local/bin/python3

import qr_img
import subprocess
import qrcode

### you probably need to change these fields!
## default Ubuntu Store Blender location
# blender_path = '/snap/bin/blender'
## default MacOS Blender location
blender_path = '/Applications/Blender.app/Contents/MacOS/Blender'
## default Windows Blender location
# blender_path = 'C:/Program Files/Blender Foundation/Blender/blender.exe'

auth_type = 'WPA' # WPA or WEP or '' 
ssid = "SSID GOES HERE" # name of your wifi network 
password = 'PASSWORD GOES HERE' # wifi password

# experimental multi-material option
multi = True 

# if you don't want to make a wifi qr code, change this to whatever you do want
# data = 'https://example.com'
data = 'WIFI:T:%s;S:%s;P:%s;;'%(auth_type, ssid, password)

# generate png, using icon_path for icon and placing result at output_path, not necessary for STL
qr_img.generate_png(data=data, icon_path='files/wifi.png', output_path='files/qr.png')

# generate svg and placing at output_path, necessary if you don't already have an SVG
qr_img.generate_svg(data=data, output_path='files/qr.svg')

if multi:
    qr_img.generate_svg(data=data, output_path='files/qr_multi.svg', factory=qrcode.image.svg.SvgPathFillImage) 

# generate STL
subprocess.run([blender_path, '--background', '--python', 'qr_blend.py'])
