import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import math

class MonochromaticSquareDetector:

    def __init__(self,_image_path:str="") -> None:
        self._image:cv2.typing.MatLike = None
        self._image_width = None
        self._image_heigth = None   
        self._graycale= None
        self._high_contrast_image= None
        self._value_threshold = 100
        self._pixel_approximation=1
        self._square_padding = 1
        self._max_squares = 300
        self._square_table = []
        self._square_min_width = 20
        self._square_max_width = 30
        if _image_path!="":
            self.load(_image_path)
        pass

    def load(self,_image_path:str):
        self._image:cv2.typing.MatLike = cv2.imread(_image_path)
        self._image_heigth = self._image.shape[0]
        self._image_width = self._image.shape[1]      
        self._graycale= cv2.cvtColor(self._image, cv2.COLOR_BGR2GRAY)
        self._high_contrast_image= self._get_high_contrast_image(self._image)    
        return self

    def _get_high_contrast_image(self,_image:cv2.typing.MatLike)->cv2.typing.MatLike:
        # do adaptive threshold on gray image
        gray = cv2.cvtColor(_image, cv2.COLOR_BGR2GRAY)
        return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 101, 3)
    
    def set_value_threshold(self,_value:int):
        self._value_threshold = _value

    def set_pixel_approximation(self,_value:int):
        # ignore pixels to gain speed (a value of 5 means : ignore 4 pixels out of 5 . ect... )
        self._pixel_approximation= _value

    def set_max_squares(self,_value:int):
        # WIP : ingore some squares 
        self._max_squares =_value

    def set_square_padding(self,_value:int):
        # space between square , it's like an extra width on the square to detect
        self._square_padding= _value

    def set_square_min_width(self,_value:int):
        # WIP , scale the square but not bellow this _image_width
        self._square_min_image_width= _value

    def _validate_square(self,_square:dict)->bool:
        if _square["width"] == 0:
            return False
        if self._overlap_detected_square(_square)==True:
            return False
        return True

    def _overlap_detected_square(self,_square:dict)->bool:
        return False

    def get_squares_positions(self,_width:int)->list:
        return self._get_monochromatic_squares(_width)

    def _unsigned(self,_int:int)->int:
        if int(_int) < 0:
            return int(_int)*-1
        return int(_int)
    

    def _get_monochromatic_squares(self,_width):
        
        thresh = self._high_contrast_image

        h = self._image_heigth
        w = self._image_width

        last_v_value = 0
        points = []
        thres = self._value_threshold
        aproximation = self._pixel_approximation
        last_x_value = 0
        last_y_value = 0
        x_distance = 0
        padding = self._square_padding

        final_with = _width+padding

        for y in range(0, h):

            if y % final_with != 0:
                continue

            for x in range(0, w):

                if x % aproximation != 0:
                    continue
                
                value = thresh[y, x]
                value_distance = self._unsigned(last_v_value -value )
                last_v_value = value

                '''
                    distance_sum +=distance
                    distance_count+=1

                    average_distance = int(distance_sum/distance_count)
                    print(average_distance)
                '''

                # does the gray value changed on x axis ? 
                if value_distance > thres:
                    # strat again mesuring from this point
                    last_x_value = x
                    last_y_value = y
                    

                # does the gray value changed on y axis below the x  ? 
                y_distance_to_contrast =self._get_y_distance_to_contrast(thresh,x,y)
                if y_distance_to_contrast < final_with:
                    #there is no room under this point to fit the square
                    # strat again mesuring from this point
                    last_x_value = x
                    last_y_value = y
                    continue

                if x == 0:
                    last_x_value = x
                    last_y_value = y

                # mesure the distance where the gray  value of pixels are the same
                x_distance = self._unsigned(last_x_value-x)

                # is there room for the qr code in this distance ? 
                if x_distance < final_with :
                    continue

                #does the qr code will be cut by the image border ? 
                if last_x_value+final_with > w:
                    continue
                if last_y_value+final_with > h:
                    continue
                points.append({"x":last_x_value,"y":last_y_value})
                last_x_value = x
                last_y_value = y


        return points
    
    def _get_y_distance_to_contrast(self,_image:cv2.typing.MatLike,_from_x:int,_from_y:int):

        last_h_value = _image[_from_y, _from_x]
        thres = self._value_threshold
        last_y = 0
        for y in range(_from_y, self._image_heigth):

            if y % self._pixel_approximation != 0:
                continue

            absolute_y = _from_y+y
            if absolute_y >= self._image_heigth:
                absolute_y = self._image_heigth-1
            value = _image[absolute_y, _from_x]
            value_distance = self._unsigned(last_h_value - value )
            last_h_value = value
            last_y = y
            if value_distance > thres:
                break
        return last_y
    
    def _get_monochromic_square(self,_image:cv2.typing.MatLike,_top_x:int,_top_y:int,_width:int=0)->dict:
        
        width = _width
        if width==0:
            width=self._square_min_width

        y_distance_to_contrast = 0
        x_distance_to_contrast = 0

        last_h_value = _image[_top_y,_top_x] 
        last_v_value = _image[_top_y,_top_x] 

        square = {
            "x":_top_x,
            "y":_top_y,
            "width":0
        }
            
        # y axis first
        for y in range(_top_y,self._image_heigth):

            h_value = _image[y,_top_x] 

            if y % self._pixel_approximation != 0:
                continue        

            h_distance = self._unsigned(last_h_value -h_value )
            y_distance = self._unsigned(y-_top_y)
            print(y_distance)
            if h_distance>self._value_threshold:
                #contrast detected
                y_distance_to_contrast = y_distance
                # we got the max heigth
                break
            if y_distance > self._square_max_width:
                y_distance_to_contrast = y_distance
                break


        # x axis 
        for y in range(_top_y,y_distance_to_contrast):

            if y % self._pixel_approximation != 0:
                continue        

            for x in range(_top_x, self._image_width):

                if x % self._pixel_approximation != 0:
                    continue        

                v_value = _image[y,x] 

                v_distance = self._unsigned(last_v_value -v_value )
                x_distance = self._unsigned(x-_top_x)
                if h_distance>self._value_threshold:
                    #contrast detected
                    x_distance_to_contrast = x_distance
                    # we got the max heigth
                    break
                if x_distance > self._square_max_width:
                    #contrast detected
                    x_distance_to_contrast = x_distance
                    # we got the max width
                    break

        #choosing a maximum square in the low contrast rectangular area 
        max_width = 0
        if x_distance_to_contrast == y_distance_to_contrast:
            # by chance it's actualy a square
            max_width = x_distance_to_contrast
        if x_distance_to_contrast < y_distance_to_contrast:
            # the rectangle is more high than large
            max_width = x_distance_to_contrast
        if y_distance_to_contrast < x_distance_to_contrast:
            # the rectangle is more large than high
            max_width = y_distance_to_contrast

        print(max_width)

        square = {
            "x":_top_x,
            "y":_top_y,
            "width":max_width
        }
                
        # every pixel value in the square is bellow threshold 
        return square
        
        ...

    def _pixels_color_variation_is_bellow_thres(self,_image:cv2.typing.MatLike,_pixels:list[list],_start_value:int=0,_thres:int=100)->bool:
        last_value = _start_value
        for pix in _pixels:
            value = _image[pix["y"],pix["x"]] 
            value_distance = self._unsigned(last_value -value )
            if value_distance > _thres:
                return False
            last_value = value
        return True

