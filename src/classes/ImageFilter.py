'''

'''

from PIL import Image
import os
import uuid

class ImageFilter():
    
    def __init__(self):
        self._current_filter = "BW"
        ...

    def set_filter(self,_filter_name:str):
        self._current_filter = _filter_name
        return self
        ...

    def apply_filter(self,_path:str)->str:

        image_file = Image.open(_path) # open colour image
        if self._current_filter == "BW":
            image_file = image_file.convert('L') # convert image to black and white
        temp = self._generate_tmp_path()+".png"
        image_file.save(temp)
        return temp
        ...


    def _generate_tmp_path(self)->str:
        image_folder= os.getenv("TEMP")
        image_name = str(uuid.uuid4())[-15:]
        path = image_folder+"/"+image_name
        return path

       


'''
python P:/pipeline/dev/a.cormier/core/decorators/image_stamp/repos/ImageStamp/src/main.py -combine -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0001.png" -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0002.png" -o "P:/projects/riv/temp_no_backup/image_stamp"
python P:/pipeline/dev/a.cormier/core/decorators/image_stamp/repos/ImageStamp/src/main.py -apply_filter "BW" -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0001.png" -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0002.png" -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0003.png" -add_text "this is my text" -o "P:/projects/riv/temp_no_backup/image_stamp" 

'''