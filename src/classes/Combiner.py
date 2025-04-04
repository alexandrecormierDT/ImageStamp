from PIL import Image
import os
import shutil
import uuid
from classes.ImageChecker import ImageChecker
from classes.ImageEditor import ImageEditor

class Combiner():

    _IC = ImageChecker()
    _IE:ImageEditor = ImageEditor()
    
    def __init__(self):
        self._axe= "H"
        self._crop = True
        ...
        
    def combine(self,_paths:list)->str:
        print(_paths)
        images = _paths
        if self._crop:
            images = []
            for path in _paths:
                if self._IC.check(path)==None:
                    return 
                images.append(self._crop_to_bbox(path))
        temp = self._generate_tmp_path()+".png"
        if self._axe == "H":
            self._combine_images_horizontaly(images,temp)
        if self._axe == "V":
            self._combine_images_verticaly(images,temp)
        return temp
    
    def set_axe(self,_axe:str):
        self._axe = _axe
        return self
    
    def set_crop(self,_c:bool):
        self._crop = _c
        return self
    
    def _combine_images_verticaly(self,_paths,_output,_padding=100):
        for path in _paths:
            if self._IC.check(path) is None:
                return 
        images = [Image.open(x) for x in _paths]
        widths, heights = zip(*(i.size for i in images))

        total_height = sum(heights)+(_padding*(len(_paths)+1))
        max_width = max(widths)

        new_im = Image.new('RGBA', (max_width,total_height))
        path = self._IE.resize_by_width(self._IC.get_max_width())

        x_offset = 0
        y_offset = _padding

        for im in images:
            new_im.paste(im, (x_offset,y_offset))
            x_offset += im.size[1]+_padding

        new_im.save(_output)
        return new_im
    
    def _conform_images_width(self,_paths,_total_width)->list:
        # check if the combined image is not too hudge (will cause errors on PIL side)
        max_auhorised_width = self._IC.get_max_width()
        conformed_paths = _paths
        if _total_width >= max_auhorised_width:
            print("[Combiner] WARNING ! final width is too high , resizing images ! ")
            conformed_paths = []
            forced_equal_width = int((max_auhorised_width/len(_paths))*0.95)
            for path in _paths:
                resized_image = self._IE.resize_by_width(path,forced_equal_width)
                conformed_paths.append(resized_image)
        return conformed_paths
    
    def _combine_images_horizontaly(self,_paths,_output,_padding=100):
        for path in _paths:
            if self._IC.check(path)==None:
                return 
            
        # original width sum  and max heigth 
        images = [Image.open(x) for x in _paths]
        widths, heights = zip(*(i.size for i in images))
        total_width = sum(widths)+(_padding*(len(_paths)+1))
        max_height = max(heights)

        #width check
        conformed_paths = self._conform_images_width(_paths,total_width)
        conformed_images = [Image.open(x) for x in conformed_paths]

        # conformed width sum  and max heigth 
        widths, heights = zip(*(i.size for i in conformed_images))
        total_width = sum(widths)+(_padding*(len(_paths)+1))
        max_height = max(heights)

        new_im = Image.new('RGBA', (total_width, max_height))
        max_height = max(heights)

        x_offset =_padding
        y_offset = 0

        for im in conformed_images:
            new_im.paste(im, (x_offset,y_offset))
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