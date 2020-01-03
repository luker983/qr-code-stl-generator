#!/usr/local/bin/python3

import qr_img
import subprocess

blender_path = '/Applications/Blender.app/Contents/MacOS/Blender'

qr_img.generate_png(data='test', icon_path='files/wifi.png', output_path='files/qr.png')
qr_img.generate_svg(data='Thisfhdaoisdfhoasidhfoasdihfoasidhvlsidohgvsd', output_path='files/qr.svg')
subprocess.run([blender_path, '--background', '--python', 'qr_blend.py'])
