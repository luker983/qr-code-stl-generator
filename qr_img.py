import qrcode
from PIL import Image
import qrcode.image.svg


# generate png

def generate_png(data, icon_path, output_path='qr.png', box_size=20, icon_size=200):
    icon = Image.open(icon_path)

    qr = qrcode.QRCode(
        error_correction = qrcode.constants.ERROR_CORRECT_H,
        box_size = box_size
    )

    qr.add_data(data)
    qr.make(fit=True)
    qr_code = qr.make_image()

    width, height = qr_code.size

    xmin = ymin = int((width / 2) - (icon_size / 2))
    xmax = ymax = int((width / 2) + (icon_size / 2))

    icon = icon.resize((xmax - xmin, ymax-ymin))

    canvas = Image.new('RGBA', qr_code.size, (0, 0, 0, 0))
    canvas.paste(qr_code, (0,0))
    canvas.paste(icon, (xmin, ymin, xmax, ymax), mask=icon)
    canvas.save(output_path, format='png')
    # canvas.show()

# generate svg

def generate_svg(data, output_path='qr.svg', box_size=20):
    qr = qrcode.QRCode(
        error_correction = qrcode.constants.ERROR_CORRECT_H,
        box_size = box_size,
        image_factory = qrcode.image.svg.SvgImage
    )

    qr.add_data(data)
    qr.make(fit=True)
    qr_code = qr.make_image()
    qr_code.save(output_path)
