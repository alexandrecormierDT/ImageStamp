from PIL import Image
import os
import shutil
import uuid

class Harmoniser():
    
    def __init__(self):
        self._output_folder = None
        ...

    def use_output_folder(self,_of:str):
        self._output_folder = _of
        
    def maximise(self,_paths:list)->str:
        print(_paths)
        images = [Image.open(x) for x in _paths]
        widths, heights = zip(*(i.size for i in images))
        max_width = max(widths)
        max_heigth = max(heights)

        new_images = []

        for path in _paths:
            img = Image.open(path)
            new_blank_img = Image.new('RGBA', (max_width,max_heigth))
            new_blank_img.paste(img, (0,0))
            new_path = path
            if self._output_folder is not None:
                new_folder = self._output_folder
                new_path = new_folder+"/"+os.path.basename(path)
                if os.path.exists(new_folder)==False:
                    os.mkdir(new_folder)
            new_blank_img.save(new_path)
            new_images.append(new_path)

        return new_images



'''
python P:/pipeline/dev/a.cormier/core/decorators/image_stamp/repos/ImageStamp/src/main.py -maximise -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0001.png" -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0002.png" -o "P:/projects/riv/temp_no_backup/image_stamp"

'''