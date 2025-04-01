import os
import re
import subprocess

class ImageChecker():

    _max_nb_of_pixels:int = 178956970
    _max_heigth:int = 15000
    _max_width:int = 15000
    _image_magick_path = "P:/pipeline/extra_soft/ImageMagick-7.0.10-Q16/magick.exe"

    def __init__(self):
        ...

    def _get_image_infos(self,_path:str)->dict:
        args = [self._image_magick_path,"identify",_path]
        result =subprocess.run(args, stdout=subprocess.PIPE)
        string = result.stdout.decode('utf-8')
        # PNG image data, 782 x 602, 8-bit/color RGBA, non-interlaced
        width,heigth = self._get_resolution(string)

        return {
            "width":int(width),
            "heigth":int(heigth),
            "bitdepth":int(self._get_bitdepth(string)),
            "colorspace":self._get_colorspace(string),
            "image_format":self._get_image_format(string),
            "nb_pixels":int(width)*int(heigth)
        }   

    def get_max_width(self)->int:
        return self._max_width

    def _get_colorspace(self,_magic_string:str)->str:
        keys = ["sRGB","Yuv","Rec740"]
        for colorspace in keys:
            if colorspace not in _magic_string:
                continue
            return colorspace
        return ""
    
    def _get_bitdepth(self,_magic_string:str)->str:
        result = re.findall('(\d{1,2})-bit', _magic_string)
        if len(result)==0:
            return ""
        return result[0]
    
    def _get_resolution(self,_magic_string:str)->tuple:
        search = re.search(' ([0-9]+)x([0-9]+) ', _magic_string)
        if search is None:
            return None,None
        return search.groups()
    
    def _get_image_format(self,_magic_string:str)->str:
        return _magic_string.split(" ")[1].lower()

    def validate(self,_path:str):
        if isinstance(_path,str)==True:
            return self._validate(_path)
        if isinstance(_path,list)==False:
            return False
        for path in _path:
            if self._validate(path)==False:
                return False
        return True

    def _validate(self,_path:str):
        if os.path.exists(_path)==False:
            return False
        infos = self._get_image_infos(_path)
        print(f"[ImageChecker] {_path} ")
        print(f"[ImageChecker] {infos} ")
        nb_pixels = infos["nb_pixels"]
        width = infos["nb_pixels"]
        heigth = infos["nb_pixels"]
        if nb_pixels>self._max_nb_of_pixels:
            print(f"[ImageChecker] ERROR max nb of pixel {self._max_nb_of_pixels} reached ({nb_pixels})")
            return False
        if infos["width"]>self._max_width:
            print(f"[ImageChecker] ERROR max width {self._max_width} reached {width}")
            return False
        if infos["heigth"]>self._max_heigth:
            print(f"[ImageChecker] ERROR max heigth {self._max_heigth} reached ({heigth})")
            return False
        return True
    
    def check(self,_path_or_paths:str=None):
        if _path_or_paths is None:
            return None
        if self.validate(_path_or_paths)==False:
            return None
        return _path_or_paths
        



'''
python P:/pipeline/dev/a.cormier/core/decorators/image_stamp/repos/ImageStamp/src/main.py -combine -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0001.png" -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0002.png" -o "P:/projects/riv/temp_no_backup/image_stamp"
python P:/pipeline/dev/a.cormier/core/decorators/image_stamp/repos/ImageStamp/src/main.py -apply_filter "BW" -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0001.png" -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0002.png" -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0003.png" -add_text "this is my text" -o "P:/projects/riv/temp_no_backup/image_stamp" 

'''