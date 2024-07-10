from PIL import Image
import os
import shutil
import uuid

class Combiner():
    
    def __init__(self):
        ...
        
    def combine(self,_paths:list)->str:
        print(_paths)
        cropped_images = []
        for path in _paths:
            cropped_images.append(self._crop_to_bbox(path))
        temp = self._generate_tmp_path()+".png"
        final_image = self._combine_images(cropped_images,temp)
        return temp

    def _combine_images(self,_paths,_output,_padding=100):
        images = [Image.open(x) for x in _paths]
        widths, heights = zip(*(i.size for i in images))

        total_width = sum(widths)+(_padding*(len(_paths)+1))
        max_height = max(heights)

        new_im = Image.new('RGBA', (total_width, max_height))

        x_offset =_padding
        for im in images:
            new_im.paste(im, (x_offset,0))
            x_offset += im.size[0]+_padding

        new_im.save(_output)
        return new_im

    def _crop_to_bbox(self,_path:str)->str:

        # Opens a image in RGB mode
        im = Image.open(_path)
        bbox = im.getbbox()

        # Size of the image in pixels (size of original image)
        # (This is not mandatory)
        width, height = im.size
        
        # Cropped image of above dimension
        # (It will not change original image)
        im1 = im.crop(bbox)
        
        # Shows the image in image viewer
        temp = self._generate_tmp_path()
        ext = "."+_path.split(".")[-1]
        im1.save(temp+ext)
        return temp+ext

    def _generate_tmp_path(self)->str:
        image_folder= os.getenv("TEMP")
        image_name = str(uuid.uuid4())[-15:]
        path = image_folder+"/"+image_name
        return path

    def _copy_image_to_temp(self,_path):
        image_temp = os.getenv("TEMP")
        shutil.copy(_path, os.getenv("TEMP"))
        return image_temp+"/"+os.path.basename(_path)        


'''
python P:/pipeline/dev/a.cormier/core/decorators/image_stamp/repos/ImageStamp/src/main.py -combine -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0001.png" -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0002.png" -o "P:/projects/riv/temp_no_backup/image_stamp"
python P:/pipeline/dev/a.cormier/core/decorators/image_stamp/repos/ImageStamp/src/main.py -combine -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0001.png" -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0002.png" -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0003.png" -o "P:/projects/riv/temp_no_backup/image_stamp"

'''