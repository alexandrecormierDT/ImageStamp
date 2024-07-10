from classes.QRReader import QRReader
from classes.QRWriter import QRWriter
from classes.Combiner import Combiner
from classes.TextWriter import TextWriter
from PIL import Image

class ImageStamp : 
    
    _R:QRReader = QRReader()
    _W:QRWriter = QRWriter()
    _C:Combiner = Combiner()
    _T:TextWriter = TextWriter()
    
    def __init__(self):
        
        ...
        
    def generate(self,_source:str,_code:str,_position="all_corners")->str:
        self._W.set_postion(_position)
        return self._W.generate(_source,_code)
    
    def read(self,_path:str)->str:
        return self._R.read(_path)
    
    def combine(self,_paths:list)->str:
        return self._C.combine(_paths)
    
    
    def add_text(self,_path,_text)->str:
        self._T.set_background_color("white")
        self._T.set_text_color("black")
        return self._T.add_text(_path,_text)
    
    