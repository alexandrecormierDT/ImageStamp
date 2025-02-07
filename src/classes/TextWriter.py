from PIL import Image,ImageDraw,ImageFont
import os
import shutil
import uuid
from classes.ImageChecker import ImageChecker

class TextWriter():

    _IC = ImageChecker()
    
    def __init__(self):
        self._text_color = self._get_color("white")
        self._background_color = self._get_color("gray")
        self._use_background = False
        ...

    def set_text_color(self,_color_name):
        self._text_color = self._get_color(_color_name)
        ...

    def set_background_color(self,_color_name):
        self._background_color = self._get_color(_color_name)
        self._use_background = True
        ...

    def _get_color(self,_color_name):
        table ={
            "white":(255, 255, 255),
            "black":(0, 0, 0),
            "gray":(100, 100, 100),
            "red":(255, 0, 0)
        }
        if _color_name in table.keys():
            return table[_color_name]
        return table["white"]
    
    def _filter_text(self,_text:str)->str:
        return _text
    
        
    def add_watermark(self,_path:str,_text:str)->str:

        im = Image.open(_path)
        width, height = im.size
        draw = ImageDraw.Draw(im)
        font_size = round(height/40)
        font = ImageFont.truetype("arial.ttf",font_size)
        padding = round(font_size/3)
        position = (0,0)

        #bounding box of the texte
        left, top, right, bottom = draw.textbbox(position, _text, font=font)
        draw = ImageDraw.Draw(im)

        try:
            # draw rectancle behind the text
            draw.rectangle((left-padding, top-padding, right+padding, bottom+round(padding*0.8)), fill="white")
            draw.text(position, _text, self._text_color, font=font)
        except:
            print(f"[TextWriter] Exeption occured ,  problem with adding text to {_path}")

        temp = self._generate_tmp_path()+".png"
        im.save(temp)
        return temp        
        
    def add_text(self,_path:str,_text:str)->str:

        if self._IC.check(_path)==None:
            return ""

        im = Image.open(_path)
        width, height = im.size
        draw = ImageDraw.Draw(im)
        font_size = round(height/20)
        font = ImageFont.truetype("arial.ttf",font_size)
        padding = round(font_size/3)
        position = (padding+5,padding+5)
        left, top, right, bottom = draw.textbbox(position, _text, font=font)
        text_h = ((bottom-top)+padding*2)*2
        image_with_text = Image.new("RGBA", (width, height+text_h))
        draw = ImageDraw.Draw(image_with_text)
        image_with_text.paste(im, (0,text_h))

        if self._use_background == True:
            draw.rectangle((left-padding, top-padding, right+padding, bottom+round(padding*0.8)), fill=self._background_color)

        draw.text(position, _text, self._text_color, font=font)
        temp = self._generate_tmp_path()+".png"
        image_with_text.save(temp)
        return temp
        ...


    def _generate_tmp_path(self)->str:
        image_folder= os.getenv("TEMP")
        image_name = str(uuid.uuid4())[-15:]
        path = image_folder+"/"+image_name
        return path

       


'''
python P:/pipeline/dev/a.cormier/core/decorators/image_stamp/repos/ImageStamp/src/main.py -combine -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0001.png" -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0002.png" -o "P:/projects/riv/temp_no_backup/image_stamp"
python P:/pipeline/dev/a.cormier/core/decorators/image_stamp/repos/ImageStamp/src/main.py -combine -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0001.png" -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0002.png" -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0003.png" -add_text "this is my text" -o "P:/projects/riv/temp_no_backup/image_stamp" 

'''