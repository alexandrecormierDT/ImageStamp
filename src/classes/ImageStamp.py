from classes.QRReader import QRReader
from classes.QRWriter import QRWriter


class ImageStamp : 
    
    _R:QRReader = QRReader()
    _W:QRWriter = QRWriter()
    
    def __init__(self):
        
        ...
        
    def generate(self,_source:str,_code:str,_output:str):
        return self._W.generate(_source,_code,_output)
    
    def read(self,_path:str):
        return self._R.read(_path)