import cv2
from pyzbar.pyzbar import decode

def read_image(image_dir):
    image = cv2.imread(image_dir)

    codes = decode(image)

    if not codes:
        print("Nenhum código detectado")
    else:
        for c in codes:
            infos = c.data.decode("utf-8")
            bar_type = c.type
            print(f"{bar_type} -- {infos}")

read_image("backend/utils/temp_barcode/Teste.png")