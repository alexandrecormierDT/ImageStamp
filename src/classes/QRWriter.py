import pyqrcode
from PIL import Image
from pyzbar.pyzbar import decode
import uuid
import os
import shutil
import random
from classes.MonochromaticSquareDetector import MonochromaticSquareDetector
import math 
from PIL import Image, ImageDraw, ImageEnhance
import PIL.ImageOps    


class QRWriter ():

    _MSD:MonochromaticSquareDetector = MonochromaticSquareDetector()
    
    def __init__(self):
        self._position = "all_corners" # all_corners , top_left  ect...
        self._under_path = ""
        self._over_path = ""
        self._scale_factor = 0.0020
        self._contrast = 5
        self._transparency = 1
        self._rgb_over:Image = None
        self._rgb_under:Image = None
        self._grid_division:int = 2

        ...

    def set_postion(self,_pos:str):
         self._position = _pos

    def set_scale_factor(self,_v:int):
        value = int(_v)
        self._scale_factor = value/10000

    def set_contrast(self,_v:int):
        value = int(_v)
        self._contrast= value

    def set_grid_division(self,_v:int):
        value = int(_v)
        self._grid_division= value

    def set_transparency(self,_v:int):
        v = int(_v)
        if v == 0:
             v=1
        value = float(100/int(v))
        self._transparency= value

    def generate(self,_source_image:str,_code:str,_mode:str="")->str:
        if os.path.exists(_source_image)==False:
            return False
        new_image = self._add_qrcode_to_image(_source_image,_code,_mode)
        if new_image == "":
             return ""
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
    
    def _calculate_qr_scale(self,_source_image)->float:
        source = Image.open(_source_image)
        factor = self._scale_factor
        scale = source.width*factor
        print("SCALE")
        print(scale)
        if scale <= 1:
             scale = 1
        return scale
        ...

    def _add_qrcode_to_image(self,_source_image:str,_code:str,_mode:str="")->Image:
        qrcode_scale = self._calculate_qr_scale(_source_image)
        qrcode_image = self._generate_image_with_qr_code(str(_code),qrcode_scale)
        if qrcode_image == "":
             return ""
        new_image = self._paste_image(_source_image,qrcode_image)
        return new_image

    def _generate_image_with_qr_code(self,_code,_scale:float=8)->Image:
        print("[QRWriter] code = "+_code)
        print("[QRWriter] scale "+str(_scale))
        qr = pyqrcode.create(_code)
        path = self._generate_qrcode_image_path(_code)
        print("[QRWriter] temp file = "+path)
        print(f"[QRWriter] {qr}")
        qr.png(path, scale=_scale)
        return path

        
    def _paste_image(self,_image_under:str,_image_over:str)->Image:
        self._under_path = _image_under
        self._over_path = _image_over
        under = Image.open(_image_under) 
        under_rgb = under.convert('RGB')

        over = Image.open(_image_over) 
        over_rgb = over.convert('RGB')

        with_qr_codes = self._paste_qrcodes(under_rgb,over_rgb,self._position)
        return with_qr_codes
    
    def _combine_images(self,_under:Image,_over:Image,_x:int=0,_y:int=0,_mask=None)->Image:
        if _mask is None:
            _under.paste(_over,(_x,_y))
            return _under
        _under.paste(_over,(_x,_y),_mask)
        return _under

    
    def _paste_qrcodes(self,_under:Image,_over:Image,_pos:str)->Image:

        uW = _under.width
        uH = _under.height
        
        oW = _over.width
        oH = _over.height
        
        x_pixel_padding = uW - oW
        y_pixel_padding = uH - oH

        result = None
        
        if _pos == "top_left":
                y = 0 * y_pixel_padding
                x = 0 * x_pixel_padding
                self._combine_images(_under,_over,x,y) 

        if _pos == "top_right":
                y = 0 * y_pixel_padding
                x = 1 * x_pixel_padding
                self._combine_images(_under,_over,x,y) 

        if _pos == "bottom_right":
                y = 1 * y_pixel_padding
                x = 1 * x_pixel_padding
                self._combine_images(_under,_over,x,y) 

        if _pos == "bottom_left":
                y = 1 * y_pixel_padding
                x = 0 * x_pixel_padding
                self._combine_images(_under,_over,x,y)  

        if _pos == "all_corners":
            margin = 20
            for i in range(2):
                for j in range(2):
                    y = (j * y_pixel_padding-margin)+margin
                    x = (i * x_pixel_padding-margin)+margin
                    result =self._combine_images(_under,_over,x,y) 

        if _pos == "grid":

            

            margin = 20

            grid_division = self._grid_division

            print(uW)
            print(uH)

            column_width = int(x_pixel_padding/grid_division)
            row_width = int(y_pixel_padding/grid_division)
            print(column_width)
            print(row_width)
            x=0
            y=0
            
            for i in range(grid_division+1):
                y =row_width*i
                for j in range(grid_division+1):
                    x = column_width*j
                    result =self._integrate(_under,_over,x,y)


        if _pos == "random":

            for i in range(30):
                random_position = self._random_position_in_rect(x_pixel_padding,x_pixel_padding)
                result = self._combine_images(_under,_over,random_position["x"],random_position["y"]) 

        if _pos == "blobs":

            _under = PIL.ImageOps.grayscale(_under)

            MCSD = MonochromaticSquareDetector(self._under_path)
            MCSD.set_square_padding(0)
            MCSD.set_pixel_approximation(3)
            MCSD.set_value_threshold(30)
            points = MCSD.get_squares_positions(oW)

            for pt in points:
                x = int(pt["x"])
                y = int(pt["y"])
                result = self._integrate(_under,_over,x,y)

            '''
            rgb_im = _under.convert('RGB')
            bbox = BD.get_blobs(self._under_path,oW,oW)
            adpated_over = _over
            for box in bbox:
                x1= box[0][0]
                y1= box[0][1]
                x2= box[1][0]
                y2= box[1][1]
                r, g, b = rgb_im.getpixel((x, y))
                shape = [(x1,y1),(x2,y2)] 
                img = Image.new("RGB", (50, 50)) 
                rectangle = ImageDraw.Draw(img)  
                rectangle.rectangle(shape, fill ="# ffff33") 
                result = self._combine_images(_under,rectangle,x1,y1) 
            
            '''
            
        return result
    
    def _integrate(self,_under:Image,_over:Image,_x:int=0,_y:int=0)->Image:

        if self._rgb_under == None:
             self._rgb_under = _under.convert('RGB')

        if self._rgb_over == None:
            rgb_over = _over.convert('RGB')
            # Image brightness enhancer
            inverted_over = PIL.ImageOps.invert(rgb_over)
            enhancer = ImageEnhance.Brightness(inverted_over)

            factor = self._transparency #gives original image
            tranparent_over = enhancer.enhance(factor)
            a_channel = tranparent_over.convert('L')
            rgb_over.putalpha(a_channel)
            self._rgb_over = rgb_over

        over_width= _over.width
        average_color = self._get_average_color_behind(self._rgb_under,_x,_y,over_width)
        displayed_color = self._display_color(average_color)
        hex = '#%02x%02x%02x' % (displayed_color, displayed_color, displayed_color)
        background = Image.new('RGB',(over_width,over_width),hex)
        result = self._combine_images(_under,background,_x,_y,self._rgb_over)
        return result


    def _get_average_color_behind(self,_image,_x,_y,_width):
        count = 1
        sum = 0
        average = 0
        w,h = _image.size
        for y in range(_y, _y+_width):
            if y > h :
                 continue
            for x in range(_x,_x+_width):
                if x > w :
                    continue
                r, g, b = _image.getpixel((x,y))
                count+=1
                sum+=r
        average = round(sum/count)
        return average
    
    def _display_color(self,_value):
        gap = self._contrast
        half_tone = 80
        new_color = _value
        if _value == 255:
              new_color = _value-gap
        if _value == 0:
              new_color = _value+gap
        if _value >= half_tone and _value < 255-gap:
              new_color = _value-gap
        if _value <= half_tone:
              new_color = _value+gap
        if new_color > 255:
             return 255
        if new_color < 0:
             return 0
        return new_color
    
    def _get_hex_value_of_pixel(_image:Image,_x,_y)->str:
        rgb_im = _image.convert('RGB')
        r, g, b = rgb_im.getpixel((_x, _y))
        return '#%02x%02x%02x' % (r, g, b)
    

    def _random_position_in_rect(self,_W:int,_H:int)->dict:
        pos = {
            "x": int(random.uniform(0, _W)),
            "y": int(random.uniform(0, _H))
        }
        return pos

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


    