from classes.QRReader import QRReader
from classes.QRWriter import QRWriter
from classes.Combiner import Combiner
from classes.TextWriter import TextWriter
from classes.ImageFilter import ImageFilter
from classes.Harmoniser import Harmoniser
from PIL import Image
import uuid
import os

class ImageStamp : 
    
    _R:QRReader = QRReader()
    _W:QRWriter = QRWriter()
    _C:Combiner = Combiner()
    _H:Harmoniser = Harmoniser()
    _T:TextWriter = TextWriter()
    _F:ImageFilter = ImageFilter()
    
    def __init__(self):
        
        ...
        
    def generate(self,_source:str,_code:str,_position="all_corners")->str:
        self._W.set_postion(_position)
        image = self._W.generate(_source,_code)
        if image == "":
            return _source
        return image
    
    def set_contrast(self,_v):
        self._W.set_contrast(_v)

    def set_scale(self,_v):
        ...
        #self._W.set_scale_factor(_v)

    def set_grid_division(self,_v):
        self._W.set_grid_division(_v)
    
    def set_transparency(self,_v):
        self._W.set_transparency(_v)
    
    def read(self,_path:str)->str:
        return self._R.read(_path)
    
    def combine(self,_paths:list,_axe:str="H")->str:
        self._C.set_axe(_axe)
        return self._C.combine(_paths)
    
    def maximise(self,_paths:list,_axe:str="H")->str:
        return self._H.maximise(_paths)
    
    
    def add_text(self,_path:str,_text:str)->str:
        self._T.set_background_color("white")
        self._T.set_text_color("black")
        return self._T.add_text(_path,_text)
    
    def apply_filter(self,_path:str,_f:str)->str:
        self._F.set_filter(_f)
        return self._F.apply_filter(_path)
    
    def crop(self,_path:str,_x1:int=0,_x2:int=0,_y1:int=0,_y2:int=0)->Image:
                # Opens a image in RGB mode
        im = Image.open(_path)
        
        # Cropped image of above dimension
        # (It will not change original image)
        cropped = im.crop((_x1, _y1, _x2, _y2))
        
        # Shows the image in image viewer
        return cropped
    
    def _get_temp_image_path(self):
        serial = str(uuid.uuid4())[-8:]
        name = f"ImageStamp_{serial}"
        return f"{os.getenv('TEMP')}/{name}.png"
    
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
                path = self._get_temp_image_path()
                croped.save(path)
                split.append(path)

        

        # Shows the image in image viewer
        return split
    
    