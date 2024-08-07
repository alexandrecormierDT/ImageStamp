from classes.QRReader import QRReader
from classes.QRWriter import QRWriter
from classes.Combiner import Combiner
from classes.TextWriter import TextWriter
from classes.ImageFilter import ImageFilter
from classes.Harmoniser import Harmoniser
from PIL import Image

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
    
    