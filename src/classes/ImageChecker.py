import os
import re
import subprocess

class ImageChecker():

    _max_heigth:int = 18000
    _max_width:int = 18000
    _max_nb_of_pixels:int = 18000*18000
    _image_magick_path = "P:/pipeline/extra_soft/ImageMagick-7.0.10-Q16/magick.exe"

    def __init__(self):
        ...

    def _get_image_infos(self, _path: str) -> dict:
        args = [self._image_magick_path, "identify", _path]
        result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0:
            # Identify failed — catch the error *early*
            stderr_msg = result.stderr.decode('utf-8', errors='replace')
            raise RuntimeError(
                f"ImageMagick identify failed for {_path!r}: {stderr_msg!r}"
            )

        string = result.stdout.decode('utf-8', errors='replace')

        width, height = self._get_resolution(string)
        bitdepth = self._get_bitdepth(string)

        return {
            "width": int(width),
            "height": int(height),
            "bitdepth": int(bitdepth),
            "colorspace": self._get_colorspace(string),
            "image_format": self._get_image_format(string),
            "nb_pixels": int(width) * int(height)
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
    
    def _get_resolution(self, _magic_string: str) -> tuple[int, int]:
        result = re.search(r'(\d+)x(\d+)', _magic_string)
        if not result:
            raise ValueError(
                f"Could not parse resolution from ImageMagick output:{_magic_string!r}"
            )
        return result.groups()
    
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

    def _validate(self, _path: str):
        # --- 1) Check if file exists ---
        if not os.path.exists(_path):
            print(f"[ImageChecker] ERROR file does not exist: {_path}")
            return False

        # --- 2) Check if file is empty (0 bytes) ---
        if os.path.getsize(_path) == 0:
            print(f"[ImageChecker] ERROR file is empty (0 bytes): {_path}")
            return False

        # --- 3) Get image infos, catch ImageMagick errors ---
        try:
            infos = self._get_image_infos(_path)
        except RuntimeError as e:
            print(f"[ImageChecker] ERROR corrupted or unreadable image: {_path}\n{e}")
            return False

        print(f"[ImageChecker] {_path}")
        print(f"[ImageChecker] {infos}")

        nb_pixels = infos["nb_pixels"]
        width = infos["width"]
        height = infos["height"]

        # --- 4) Validate dimensions & pixel count ---
        if nb_pixels > self._max_nb_of_pixels:
            print(f"[ImageChecker] ERROR max nb of pixels {self._max_nb_of_pixels} reached ({nb_pixels})")
            return False

        if width > self._max_width:
            print(f"[ImageChecker] ERROR max width {self._max_width} reached ({width})")
            return False

        if height > self._max_heigth:
            print(f"[ImageChecker] ERROR max height {self._max_heigth} reached ({height})")
            return False

        return True
    
    def check(self,_path_or_paths:str=None):
        if _path_or_paths is None:
            return None
        if self.validate(_path_or_paths)==False:
            return None
        return _path_or_paths
        
    def check_svg(self,_path_or_paths:str=None):
        # wip
        return _path_or_paths
        



'''
python P:/pipeline/dev/a.cormier/core/decorators/image_stamp/repos/ImageStamp/src/main.py -combine -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0001.png" -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0002.png" -o "P:/projects/riv/temp_no_backup/image_stamp"
python P:/pipeline/dev/a.cormier/core/decorators/image_stamp/repos/ImageStamp/src/main.py -apply_filter "BW" -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0001.png" -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0002.png" -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0003.png" -add_text "this is my text" -o "P:/projects/riv/temp_no_backup/image_stamp" 

'''