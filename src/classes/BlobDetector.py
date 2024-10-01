import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import math

class BlobDetector:

    def __init__(self) -> None:

        pass

    def _get_contrast_points(self,_image_path)->list:
        # read image
        img = cv2.imread(_image_path)

        # convert img to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # do adaptive threshold on gray image
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 101, 3)

        # apply morphology open then close
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
        blob = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9,9))
        blob = cv2.morphologyEx(blob, cv2.MORPH_CLOSE, kernel)


        cv2.imwrite("doco3_contour.jpg", blob)
        cv2.imshow("IMAGE", blob)
        cv2.waitKey(0)

    
        image = Image.open("doco3_contour.jpg")

    def _unsgined(self,_int:int)->int:
        if _int < 0:
            return _int*-1
        return _int
    

    def _square_color_variation_is_bellow_thres(self,_image:cv2.typing.MatLike,_top_x:int,_top_y:int,_width:int,_thres:int):



    def _pixels_color_variation_is_bellow_thres(self,_image:cv2.typing.MatLike,_pixels:list[list],_start_value:int=0,_thres:int=100)->bool:
        last_value = _start_value
        for pix in _pixels:
            value = _image[pix["y"],pix["x"]] 
            value_distance = self._unsgined(last_value -value )
            if value_distance > _thres:
                return False
            last_value = value
        return True


    def _detect_contrast_points(self,_image_path:str,_width)->list:

        image = cv2.imread(_image_path)

        # grab the image dimensions
        h = image.shape[0]
        w = image.shape[1]

        # convert img to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # do adaptive threshold on gray image
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 101, 3)

        #cv2.imshow("IMAGE", thresh)
        #cv2.waitKey(0)

        last_h_value = 0
        thres = 200
        points = []
        aproximation = 1
        last_x_value = 0
        last_y_value = 0
        x_distance = 0

        max_points = 300
        
        # loop over the image, pixel by pixel

        padding = 5

        final_with = _width+padding

        for y in range(0, h):
            if y % final_with != 0:
                continue
            for x in range(0, w):
                if x % aproximation != 0:
                    continue
                value = thresh[y, x]
                value_distance = self._unsgined(last_h_value -value )
                last_h_value = value

                '''
                    distance_sum +=distance
                    distance_count+=1

                    average_distance = int(distance_sum/distance_count)
                    print(average_distance)
                '''
                # does the gray value changed ? 
                if value_distance > thres:
                    # strat mesuring from this point
                    last_x_value = x
                    last_y_value = y

                # mesure the distance where the gray  value of pixels are the same
                x_distance = self._unsgined(last_x_value -x)
                y_distance = self._unsgined(last_y_value -y)

                # is there room for the qr code in this distance ? 
                if x == 0:
                    last_x_value = x
                    last_y_value = y

                if x_distance >= final_with :
                    #does the qr code will be cut by the image border ? 
                    if last_x_value+final_with > w:
                        continue
                    points.append({"x":last_x_value,"y":last_y_value})
                    last_x_value = x
                    last_y_value = y

        return points


    def _get_pixel_value(self,_image:Image,_x,_y):
        im = Image.open('image.gif')
        rgb_im = im.convert('RGB')
        r, g, b = rgb_im.getpixel((_x, _y))
        return r
        print(r, g, b)
        (65, 100, 137)


    def get_blobs(self,_image_path:str,_min=200,_max=8000)->list:

        return self._detect_contrast_points(_image_path,_min)

        # read image
        img = cv2.imread(_image_path)

        # convert img to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # do adaptive threshold on gray image
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 101, 3)

        # apply morphology open then close
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
        blob = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9,9))
        blob = cv2.morphologyEx(blob, cv2.MORPH_CLOSE, kernel)

        # invert blob
        blob = (255 - blob)

        # Get contours
        cnts = cv2.findContours(blob, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        #big_contour = max(cnts, key=cv2.contourArea)

        filtered_contours = []
        bounding_boxes = []

        min = 100
        max = 300000
        for contour in cnts:
            blob_area = cv2.contourArea(contour)
            if blob_area < min:
                continue
            if blob_area > max:
                continue
            filtered_contours.append(contour)
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            bounding_boxes.append(box)
            print(box)
            ...

        result = img.copy()

        cv2.drawContours(result, filtered_contours, -1, (0,0,255), 1)
        for box in bounding_boxes:
            cv2.drawContours(result,[box],0,(0,255,0),2)

        cv2.imwrite("doco3_contour.jpg", result)
        cv2.imshow("RESULT", result)
        cv2.waitKey(0)
        return bounding_boxes

        # test blob size
        blob_area = cv2.contourArea(big_contour)
        if blob_area < blob_area_thresh:
            print("Blob Is Too Small")

        # draw contour
        result = img.copy()
        cv2.drawContours(result, [big_contour], -1, (0,0,255), 1)

        # write results to disk
        cv2.imwrite("doco3_threshold.jpg", thresh)

        # display it
        return
        cv2.imshow("IMAGE", img)
        cv2.imshow("THRESHOLD", thresh)