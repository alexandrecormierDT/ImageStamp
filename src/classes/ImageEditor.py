'''

'''

from PIL import Image
import os
from classes.PathManager import PathManager

class ImageEditor():

    _PM:PathManager = PathManager()
    
    def __init__(self):
        self._current_filter = "BW"
        ...

    def crop(self,_path:str,_x1:int=0,_x2:int=0,_y1:int=0,_y2:int=0)->Image:
        # Opens a image in RGB mode
        im = Image.open(_path)
        
        # Cropped image of above dimension
        # (It will not change original image)
        cropped = im.crop((_x1, _y1, _x2, _y2))
        
        # Shows the image in image viewer
        return cropped
    
    def resize_by_width(self,_path:str,_width:int=0)->str:
        img = Image.open(_path)
        wpercent = (_width / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        resized = img.resize((_width, hsize), Image.Resampling.LANCZOS)
        path = self._PM.get_temp_image_path()
        resized.save(path)
        return  path

    def split(self,_path:str,_value:int=2)->list:

        im = Image.open(_path)
        width, height = im.size
        chunk_x = int(width/_value)
        chunk_y = int(height/_value)
        split = []

        for i in range(0,_value):
            x1 = chunk_x*i
            x2 = chunk_x*(i+1)
            for j in range(0,_value):
                y1 = chunk_y*j
                y2 = chunk_y*(j+1)
                croped = self.crop(_path,x1,x2,y1,y2)
                path = self._PM.get_temp_image_path()
                croped.save(path)
                split.append(path)

        # Shows the image in image viewer
        return split       


'''
python P:/pipeline/dev/a.cormier/core/decorators/image_stamp/repos/ImageStamp/src/main.py -combine -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0001.png" -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0002.png" -o "P:/projects/riv/temp_no_backup/image_stamp"
python P:/pipeline/dev/a.cormier/core/decorators/image_stamp/repos/ImageStamp/src/main.py -apply_filter "BW" -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0001.png" -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0002.png" -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0003.png" -add_text "this is my text" -o "P:/projects/riv/temp_no_backup/image_stamp" 

'''