import pyqrcode
from PIL import Image
from pyzbar.pyzbar import decode
import uuid
import os
import shutil

class QRWriter ():
    
    def __init__(self):
        
        ...
    def generate(self,_source_image,_code,_output_folder)->bool:
        new_image = self.add_qrcode_to_image(_source_image,_code)
        final_path = self.copy_image_to_output(new_image,_output_folder)
        data = self._decode_image(final_path)
        for qr in list(data):
            print(qr)
        if data == _code:
            return True
        return False
    
    def _decode_image(self,_path):
        data = decode(Image.open(_path))
        return data

    def _add_qrcode_to_image(self,_source_image:str,_code:str,_scale:float=2)->str:
        qrcode = self._generate_image_with_qr_code(str(_code),_scale)
        new_image = self._paste_image_in_corners(_source_image,qrcode)
        return new_image

    def _generate_image_with_qr_code(self,_code,_scale:float=2):
        qr = pyqrcode.create(_code)
        path = self._generate_qrcode_image_path(_code)
        qr.png(path, scale=_scale)
        return path

        
    def _paste_image_in_corners(self,_image_under,_image_over):
        copy = self.copy_image_to_temp(_image_under)
        under = Image.open(copy) 
        under_rgb = under.convert('RGB')
        uW = under.width
        uH = under.height
        
        over = Image.open(_image_over) 
        over_rgb = over.convert('RGB')
        oW = over.width
        oH = over.height
        
        
        x_pixel_padding = uW - oW
        y_pixel_padding = uH - oH
        
        print(x_pixel_padding)
        print(y_pixel_padding)
        print(uW,uH,oW,oH)
        
        for i in range(2):
            for j in range(2):
                y = j * y_pixel_padding
                x = i * x_pixel_padding
                under_rgb.paste(over_rgb, (x,y)) 
        under_rgb.save(copy, quality=95)
        return copy
    
    def _copy_image_to_temp(self,_path):
        image_temp = os.getenv("TEMP")
        shutil.copy(_path, os.getenv("TEMP"))
        return image_temp+"/"+os.path.basename(_path)

    def _insert_suffix(self,_path,_suffix:str)->str:
        base = os.path.basename(_path)
        ext = base.split(".")[-1]
        name = base.split(".")[-2]
        return f"{name}{_suffix}.{ext}"
        
    def _copy_image_to_output(self,_path:str,_folder:str):
        shutil.copy(_path, _folder)
        return _folder+"/"+os.path.basename(_path)

    def _generate_qrcode_image_path(self,_code):
        serial = str(uuid.uuid4())[-8:]
        name = f"ImageStamp_{serial}_{_code}"
        return f"{os.getenv("TEMP")}/{name}.png"


    