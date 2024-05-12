import pyqrcode
from PIL import Image
from pyzbar.pyzbar import decode
import uuid
import os
import shutil
import sys
import argparse

def add_qrcode_to_image(_source_image:str,_code:str,_scale:float=2)->str:
    qrcode = generate_image_with_qr_code(str(_code),_scale)
    new_image = put_image_on_image(_source_image,qrcode)
    return new_image

def generate_image_with_qr_code(_code,_scale:float=2):
    qr = pyqrcode.create(_code)
    path = generate_qrcode_image_path(_code)
    qr.png(path, scale=_scale)
    return path
    
def put_image_on_image(_image_under,_image_over):
    copy = copy_image_to_temp(_image_under)
    img1 = Image.open(copy) 
    rgb_im1 = img1.convert('RGB')
    x_pixel_padding = 100
    for index in range(2):
        img2 = Image.open(_image_over) 
        rgb_im2 = img2.convert('RGB')
        y = 0
        x = index * x_pixel_padding
        rgb_im1.paste(rgb_im2, (x,y)) 
    rgb_im1.save(copy, quality=95)
    return copy
    
def copy_image_to_temp(_path):
    image_temp = os.getenv("TEMP")
    shutil.copy(_path, os.getenv("TEMP"))
    return image_temp+"/"+os.path.basename(_path)

def insert_suffix(_path,_suffix:str)->str:
    base = os.path.basename(_path)
    ext = base.split(".")[-1]
    name = base.split(".")[-2]
    return f"{name}{_suffix}.{ext}"
    
def copy_image_to_output(_path:str,_folder:str):
    shutil.copy(_path, _folder)
    return _folder+"/"+os.path.basename(_path)

def generate_qrcode_image_path(_code):
    serial = str(uuid.uuid4())[-8:]
    name = f"ImageStamp_{serial}_{_code}"
    return f"{os.getenv("TEMP")}/{name}.png"

def decode_image(_path):
    data = decode(Image.open(_path))
    return data

def generate(_source_image,_code,_output_folder)->bool:
    new_image = add_qrcode_to_image(_source_image,_code)
    final_path = copy_image_to_output(new_image,_output_folder)
    data = decode_image(final_path)
    print(data)
    if data == _code:
        return True
    return False
    
def read(_source_image):
    data = decode_image(_source_image)
    return data
    
def main():
    print("ImageStamp")
    parser = argparse.ArgumentParser(prog='ImageStamp',description='add qrcode to image')
    parser.add_argument('-read','--read',action='store_true') 
    parser.add_argument('-generate','--generate',action='store_true') 
    parser.add_argument("-i","--image_source",required=True)
    parser.add_argument("-c","--code")
    parser.add_argument("-o","--output_folder")
    parser.add_argument("-s","--scale")
    args = parser.parse_args()
    
    if args.generate:
        generate(args.image_source,args.code,args.output_folder)
        
    if args.read:
        read(args.image_source)
    
        
if __name__=="__main__":
    main()
    
    
        



'''
python D:/1_TRAVAIL/WIP/CODING/sandbox/read_qrcode/main.py generate -i D:/1_TRAVAIL/WIP/CODING/resources/images/png/dog.png -c TEST -o D:/1_TRAVAIL/WIP/CODING/sandbox/read_qrcode/output

'''