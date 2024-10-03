from PIL import Image
from classes.QRWriter import QRWriter
from classes.ImageFilter import ImageFilter
from classes.QRReader import QRReader

class QRIntegrator ():

    _W:QRWriter = QRWriter()
    _F:ImageFilter = ImageFilter()
    _R:QRReader = QRReader()
    _max_trials = 30
    
    def __init__(self):
        self._strategy = "optimaly_hidden" # visible
        ...

    def set_strategy(self,_s:str):
        self._strategy = str(_s)

    def set_integration_mode(self,_im:str):
        self._W.set_integration_mode(_im)

    def set_scale_factor(self,_v:int):
        self._W.set_scale_factor(_v)

    def set_contrast(self,_v:int):
        self._W.set_contrast(_v)

    def set_grid_division(self,_v:int):
        self._W.set_grid_division(_v)

    def set_transparency(self,_v:int):
        self._W.set_transparency(_v)

    def add_qrcode(self,_source_image:str,_code:str,_integration_mode:str="grid")->str:
        if self._strategy == "optimaly_hidden":
            return self._add_qrcode_optimaly_hidden(_source_image,_code,_integration_mode)
        if self._strategy == "visible":
            return self._add_qrcode_visible(_source_image,_code,_integration_mode)
        return self._W.add_qrcode(_source_image,_code,_integration_mode)
    
    def _add_qrcode_visible(self,_source_image:str,_code:str,_integration_mode:str="grid")->str:
        self._W.set_grid_division(1)
        self._W.set_blend_mode("over")
        return self._W.add_qrcode(_source_image,_code,_integration_mode)
    
    def _add_qrcode_optimaly_hidden(self,_source_image:str,_code:str,_integration_mode:str="grid"):

        self._W.reset()
        contrast = 5
        scale = 20
        code = _code
        transparency = 1
        grid_division = 4
        integration_mode = _integration_mode

        max_trial = self._max_trials

        increment_table = {
            "contrast":int(100/max_trial),
            "grid_division":0.3
        }

        image_stream =self._F.grayscale(_source_image)
        original_image = image_stream

        self._W.set_grid_division(grid_division)
        self._W.set_scale_factor(scale)
        self._W.set_transparency(transparency)
        self._W.set_contrast(contrast)

        match_target = 3

        for trial in range(0,max_trial):

            if self._R.evaluate(image_stream,match_target)==True:
                print(f"REQUIRED MINIMUM OF VISIBLE {match_target} QRCODE REACHED ")
                break
            print("QR CODE NOT VISIBLE -- TRIAL "+str(trial))
            contrast+=increment_table["contrast"]
            grid_division+=round(increment_table["grid_division"])
            self._W.set_grid_division(grid_division)
            self._W.set_contrast(contrast)
            image_stream =self._W.add_qrcode(original_image,code,integration_mode)

        if match_target < 3:
            #for safety we had realy visible qrcodes in the corners
            return self._add_qrcode_visible(image_stream,_code,_integration_mode)

        return image_stream

    