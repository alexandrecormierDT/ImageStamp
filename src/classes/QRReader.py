import pyqrcode
from PIL import Image
from pyzbar.pyzbar import decode


class QRReader():
    
    def __init__(self):
        ...
        
    def read(self,_path):
        return self._decode_image(_path)
        
    def _decode_image(self,_path):
        data = decode(Image.open(_path))
        return data
    
    def _decode_video(self,_path):
        data = decode(Image.open(_path))
        return data


    
        



'''
python D:/1_TRAVAIL/WIP/CODING/repos/ImageStamp/main.py -generate -i D:/1_TRAVAIL/WIP/CODING/resources/images/png/dog.png -c TEST -o D:/1_TRAVAIL/WIP/CODING/repos/ImageStamp/output
python D:/1_TRAVAIL/WIP/CODING/repos/ImageStamp/main.py -generate -i D:/1_TRAVAIL/WIP/CODING/resources/images/png/dog.png -c 1897 -o D:/1_TRAVAIL/WIP/CODING/repos/ImageStamp/output

'''