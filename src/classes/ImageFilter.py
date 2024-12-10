'''

'''

from PIL import Image,ImageOps,ImageChops
import os
import uuid
from classes.PathManager import PathManager
from PIL import Image, ImageEnhance

class ImageFilter():

    _PM:PathManager = PathManager()
    
    def __init__(self):
        self._current_filter = "BW"
        ...

    def set_filter(self,_filter_name:str):
        self._current_filter = _filter_name
        return self
        ...

    def apply_filter(self,_path:str)->str:

        # Read the image
        image = self._open_rgb_image(_path)
        if image is None:
            return _path
        if self._current_filter == "BW":
            image = image.convert('L') # convert image to black and white
        temp = self._generate_tmp_path()+".png"
        image.save(temp)
        return temp
        ...

    def increase_contrast(self,_path:str,_value:1.5)->str:

        # Read the image
        image = self._open_rgb_image(_path)
        if image is None:
            return _path
        # Image brightness enhancer
        enhancer = ImageEnhance.Contrast(image)
        path = self._PM.get_temp_image_path()

        factor = _value #increase contrast
        im_output = enhancer.enhance(factor)
        im_output.save(path)
        return path
    
    def _open_rgb_image(self,_path:str)->Image:
        try:
            image = Image.open(_path).convert("RGB")
            return image
        except():
            print("ERROR can't parse image path "+_path)
            return None   

    def grayscale(self,_path:str)->str:
        image = self._open_rgb_image(_path)
        if image is None:
            return _path
        grayscale = ImageOps.grayscale(image)
        path = self._PM.get_temp_image_path()
        grayscale.save(path)
        return path
    
    def invert(self,_path:str)->str:
        image = self._open_rgb_image(_path)
        if image is None:
            return _path
        inverted_image =ImageChops.invert(image)
        path = self._PM.get_temp_image_path()
        inverted_image.save(path)
        return path
    
    
    def _generate_tmp_path(self)->str:
        image_folder= os.getenv("TEMP")
        image_name = str(uuid.uuid4())[-15:]
        path = image_folder+"/"+image_name
        return path

       


'''
python P:/pipeline/dev/a.cormier/core/decorators/image_stamp/repos/ImageStamp/src/main.py -combine -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0001.png" -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0002.png" -o "P:/projects/riv/temp_no_backup/image_stamp"
python P:/pipeline/dev/a.cormier/core/decorators/image_stamp/repos/ImageStamp/src/main.py -apply_filter "BW" -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0001.png" -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0002.png" -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0003.png" -add_text "this is my text" -o "P:/projects/riv/temp_no_backup/image_stamp" 

'''