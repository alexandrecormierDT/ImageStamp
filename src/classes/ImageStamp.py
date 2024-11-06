from classes.QRReader import QRReader
from classes.QRIntegrator import QRIntegrator
from classes.Combiner import Combiner
from classes.TextWriter import TextWriter
from classes.ImageFilter import ImageFilter
from classes.ImageEditor import ImageEditor
from classes.Harmoniser import Harmoniser
from classes.PathManager import PathManager
from classes.VideoEditor import VideoEditor
from PIL import Image,ImageOps,ImageChops
import json

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
    _V:VideoEditor = VideoEditor()

    def __init__(self):
        
        ...

    def add_qrcode(self,_source:str,_code:str,_integration_mode:str="grid",_strategy:str="optimaly_hidden"):
        self._I.set_strategy(_strategy)
        image = self._I.add_qrcode(_source,_code,_integration_mode)
        if image == "":
            return _source
        return image
    
    def set_qrcode_contrast(self,_v):
        self._I.set_contrast(_v)

    def set_qrcode_scale(self,_v):
        self._I.set_scale_factor(_v)

    def set_grid_division(self,_v):
        self._I.set_grid_division(_v)
    
    def set_qrcode_transparency(self,_v):
        self._I.set_transparency(_v)

    def grayscale(self,_path:str)->str:
        return self._F.grayscale(_path)
    
    def read(self,_path:str)->str:
        return self._R.read(_path)
    
    def find_qrcodes(self,_path:str,_output:str="")->dict:
        frames = self._V.extract_frames(_path[0])
        skip_rate = 1
        index = 0
        frame_table = {}
        code_table = {}
        search_list = []
        for frame_path in frames:
            index+=1
            if index % skip_rate !=0:
                continue
            print(frame_path)
            found = self._R.find(frame_path)
            if len(found)==0:
                continue
            data = [item.data.decode('utf-8') for item in found]
            #unique codes 
            data = list(set(data))
            first_code = data[0]
            frame_table[str(index)] = data
            if first_code not in code_table.keys():
                code_table[first_code] = []
                search_list.append(first_code)
            code_table[first_code].append(index)
            print(f" FRAME {index} === {data}")
        result = {
            "input_path":_path,
            "frame_table":frame_table,
            "code_table":code_table,
            "search":search_list, # will be used to cominucate with sgrequest
            "result":{}
        }

        with open(_output,"w") as file:
            file.write(json.dumps(result))
        return result
    
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
    
    def add_watermark(self,_path:str,_text:str)->str:
        self._T.set_text_color("gray")
        return self._T.add_watermark(_path,_text)
    
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

    
    