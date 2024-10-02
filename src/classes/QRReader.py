import pyqrcode
from PIL import Image
from pyzbar.pyzbar import decode
from classes.ImageEditor import ImageEditor
from classes.ImageFilter import ImageFilter

class QRReader():


    _IE:ImageEditor = ImageEditor()
    _IF:ImageFilter = ImageFilter()
    _minimum_detected_qrcode = 1
    
    def __init__(self):

        ...

    def find(self,_path:str)->list:

        #split the image in sub parts and look fo qrcodes
        split_division = 2
        split = self._IE.split(_path,split_division)
        split.append(_path)
        split.extend(self._IE.split(_path,split_division+1))

        for image_part in split:
            split_data = self.read(image_part)
            if len(split_data)>0:
                return split_data
            # test on inverted image
            inverted_image= self._IF.invert(image_part)
            split_data=self.read(inverted_image)
            if len(split_data)>0:
                return split_data
            
        return []
        
    def read(self,_path)->list:
        # can you see a qrcode ? 
        return self._decode_image(_path)
    
    def evaluate(self,_path:str,_min_qrcodes:int=3)->bool:

        # check if the image have some minimum detectable qrcodes even if it's croped

        #split the image in sub parts and test the qrcodes
        split_division = 2
        split = self._IE.split(_path,split_division)
        split.append(_path)
        split.extend(self._IE.split(_path,split_division+2))

        match = 0

        for image_part in split:
            image_data = self.read(image_part)
            if len(image_data)>=self._minimum_detected_qrcode:
                print(f"--------- MATCH {len(image_data)}")
                match+=1
            #testing on inveted image
            inverted_image= self._IF.invert(image_part)
            image_data=self.read(inverted_image)
            if len(image_data)>=self._minimum_detected_qrcode:
                print(f"---------INVERTED MATCH {len(image_data)}")
                match+=1

        if match < _min_qrcodes:
            return False
        
        return True
        
    def _decode_image(self,_path):
        data = decode(Image.open(_path))
        return data
    
    def _decode_video(self,_path:str):

        data = decode(Image.open(_path))
        return data


    
        



'''
python D:/1_TRAVAIL/WIP/CODING/repos/ImageStamp/main.py -generate -i D:/1_TRAVAIL/WIP/CODING/resources/images/png/dog.png -c TEST -o D:/1_TRAVAIL/WIP/CODING/repos/ImageStamp/output
python D:/1_TRAVAIL/WIP/CODING/repos/ImageStamp/main.py -generate -i D:/1_TRAVAIL/WIP/CODING/resources/images/png/dog.png -c 1897 -o D:/1_TRAVAIL/WIP/CODING/repos/ImageStamp/output

'''