from classes.QRReader import QRReader
from classes.QRIntegrator import QRIntegrator
from classes.Combiner import Combiner
from classes.TextWriter import TextWriter
from classes.ImageFilter import ImageFilter
from classes.ImageEditor import ImageEditor
from classes.Harmoniser import Harmoniser
from classes.PathManager import PathManager
from PIL import Image,ImageOps,ImageChops

import uuid
import os

class ImageStamp : 
    
    _R:QRReader = QRReader()
    _PM:PathManager = PathManager()
    _I:QRIntegrator = QRIntegrator()
    _C:Combiner = Combiner()
    _H:Harmoniser = Harmoniser()
    _T:TextWriter = TextWriter()
    _F:ImageFilter = ImageFilter()
    _E:ImageEditor = ImageEditor()
    def __init__(self):
        
        ...

    def add_qrcode(self,_source:str,_code:str,_integration_mode:str="grid",_strategy:str="adaptive"):
        self._I.set_strategy(_strategy)
        image = self._I.add_qrcode(_source,_code,_integration_mode)
        if image == "":
            return _source
        return image
    
    def set_qrcode_contrast(self,_v):
        self._W.set_contrast(_v)

    def set_qrcode_scale(self,_v):
        ...
        #self._W.set_scale_factor(_v)

    def set_grid_division(self,_v):
        self._W.set_grid_division(_v)
    
    def set_qrcode_transparency(self,_v):
        self._W.set_transparency(_v)

    def grayscale(self,_path:str)->str:
        return self._F.grayscale(_path)
    
    def read(self,_path:str)->str:
        return self._R.read(_path)
    
    def evaluate(self,_path:str,_minimum_qrcodes:int=2)->dict:
        return self._R.evaluate(_path,_minimum_qrcodes)
    
    def invert(self,_path:str)->str:
        return self._F.invert(_path)
    
    def combine(self,_paths:list,_axe:str="H")->str:
        self._C.set_axe(_axe)
        return self._C.combine(_paths)
    
    def maximise(self,_paths:list,_axe:str="H")->str:
        self._C.set_axe(_axe)
        return self._H.maximise(_paths)
    
    def add_text(self,_path:str,_text:str)->str:
        self._T.set_background_color("white")
        self._T.set_text_color("black")
        return self._T.add_text(_path,_text)
    
    def apply_filter(self,_path:str,_f:str)->str:
        self._F.set_filter(_f)
        return self._F.apply_filter(_path)
    
    def crop(self,_path:str,_x1:int=0,_x2:int=0,_y1:int=0,_y2:int=0)->Image:
        return self._E.crop(_path,_x1,_x2,_y1,_y2)
    
    def _get_temp_image_path(self)->str:
        return self._PM.get_temp_image_path()
    
    def split(self,_path:str,_value:int=2)->list:
        return self._E.split(_path,_value)
    
    def clean_temp(self):
        return self._PM.clean_temp()

    
    