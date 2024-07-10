import pyqrcode
from PIL import Image
from pyzbar.pyzbar import decode
import uuid
import os
import shutil

class QRWriter ():
    
    def __init__(self):
        self._position = "all_corners" # all_corners , top_left  ect...
        ...

    def set_postion(self,_pos:str):
         self._position = _pos


    def generate(self,_source_image:str,_code:str)->str:
        if os.path.exists(_source_image)==False:
            return False
        new_image = self._add_qrcode_to_image(_source_image,_code)
        temp = self._generate_tmp_path()
        new_image.save(temp)
        return temp
    
    def _generate_tmp_path(self)->str:
        image_folder= os.getenv("TEMP")
        image_name = str(uuid.uuid4())[-15:]
        path = image_folder+"/"+image_name+".png"
        return path
    
    def _decode_image(self,_path):
        data = decode(Image.open(_path))
        return data
    
    def _calculate_qr_scale(self,_source_image):
        source = Image.open(_source_image)
        scale = source.width*0.0020
        return scale
        ...

    def _add_qrcode_to_image(self,_source_image:str,_code:str)->Image:
        qrcode = self._generate_image_with_qr_code(str(_code),self._calculate_qr_scale(_source_image))
        new_image = self._paste_image_in_corners(_source_image,qrcode)
        return new_image

    def _generate_image_with_qr_code(self,_code,_scale:float=8)->Image:
        qr = pyqrcode.create(_code)
        path = self._generate_qrcode_image_path(_code)
        qr.png(path, scale=_scale)
        return path

        
    def _paste_image_in_corners(self,_image_under,_image_over)->Image:
        under = Image.open(_image_under) 
        under_rgb = under.convert('RGB')

        over = Image.open(_image_over) 
        over_rgb = over.convert('RGB')

        with_qr_codes = self._paste_qrcodes(under_rgb,over_rgb,self._position)
        return with_qr_codes
    
    def _paste_qrcodes(self,_under:Image,_over:Image,_pos:str)->Image:

        uW = _under.width
        uH = _under.height
        
        oW = _over.width
        oH = _over.height
        
        x_pixel_padding = uW - oW
        y_pixel_padding = uH - oH
        
        if _pos == "top_left":
                y = 0 * y_pixel_padding
                x = 0 * x_pixel_padding
                _under.paste(_over, (x,y)) 

        if _pos == "top_right":
                y = 0 * y_pixel_padding
                x = 1 * x_pixel_padding
                _under.paste(_over, (x,y)) 

        if _pos == "bottom_right":
                y = 1 * y_pixel_padding
                x = 1 * x_pixel_padding
                _under.paste(_over, (x,y)) 

        if _pos == "bottom_left":
                y = 1 * y_pixel_padding
                x = 0 * x_pixel_padding
                _under.paste(_over, (x,y)) 

        if _pos == "all_corners":
            for i in range(2):
                for j in range(2):
                    y = j * y_pixel_padding
                    x = i * x_pixel_padding
                    _under.paste(_over, (x,y)) 

        return _under
    
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
        return f"{os.getenv('TEMP')}/{name}.png"


    