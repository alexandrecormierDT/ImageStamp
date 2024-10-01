import sys
sys.path.insert(0,'P:/pipeline/extra_scripts/python_include')
from classes.ImageStamp import ImageStamp
from PIL import Image
import argparse
    
def main():
    print("ImageStamp")
    parser = argparse.ArgumentParser(prog='ImageStamp',description='add qrcode to image')
    parser.add_argument('-read','--read',action='store_true') 
    parser.add_argument('-generate','--generate',action='store_true') 
    parser.add_argument('-combine','--combine',action='store_true') 
    parser.add_argument('-maximise','--maximise',action='store_true') 
    parser.add_argument('-add_text','--add_text') 
    parser.add_argument('-add_qrcode','--add_qrcode') 
    parser.add_argument('-apply_filter','--apply_filter') 
    parser.add_argument("-i","--image_source",action='append' ,required=True)
    parser.add_argument("-c","--code")
    parser.add_argument("-ct","--contrast")
    parser.add_argument("-tr","--transparency")
    parser.add_argument("-sf","--scale_factor")
    parser.add_argument("-gd","--grid_division")
    parser.add_argument("-o","--output_folder")
    parser.add_argument("-oi","--output_image")
    parser.add_argument("-s","--scale")
    parser.add_argument("-p","--position",default="all_corners")

    args = parser.parse_args()
    
    IS = ImageStamp()
    image_stream =args.image_source

    if args.read:
        data = IS.read(image_stream)
        return data

    if args.combine:
        image_stream =IS.combine(image_stream)

    if args.maximise:
        image_stream =IS.maximise(image_stream)

    if isinstance(image_stream,list):
        image_stream = image_stream[0]
        
    if args.add_text:
        image_stream = IS.add_text(image_stream,args.add_text)

    if args.add_qrcode:
        image_stream =IS.generate(image_stream,args.add_qrcode,args.position)


    if args.apply_filter:
        image_stream =IS.apply_filter(image_stream,args.apply_filter)

    if args.generate and args.code:

        contrast = 5
        scale = 25
        code = args.code
        transparency = 1
        grid_division = 4

        if args.contrast:
            contrast =args.contrast
        if args.grid_division:
            grid_division =args.grid_division
        if args.scale_factor:
            scale_factor=args.scale_factor
        if args.position:
            position = args.position
        if args.transparency:
            transparency = args.transparency

        max_trial = 30

        increment_table = {
            "contrast":int(100/max_trial),
            "scale":int(100/max_trial),
            "transparency":0,
            "division":0
        }

        data = []
        minimum_detected_qrcode = 1

        image_stream =IS.grayscale(image_stream)
        original_image = image_stream

        IS.set_grid_division(grid_division)
        IS.set_scale(scale)
        IS.set_transparency(transparency)
        IS.grayscale(image_stream)


        for trial in range(0,max_trial):


            #split the image in sub parts and test the qrcodes
            split_division = 2
            split = IS.split(image_stream,split_division)
            split.append(image_stream)
            split.extend(IS.split(image_stream,split_division+2))

            image_data = []

            match = 0
            for image_part in split:
                image_data = IS.read(image_part)
                if len(image_data)>=minimum_detected_qrcode:
                    print("--------- MATCH")
                    match+=1
                    data = image_data
                #testing on inveted image
                inverted_image= IS.invert(image_part)
                image_data=IS.read(inverted_image)
                if len(image_data)>=minimum_detected_qrcode:
                    print("---------INVERTED MATCH")
                    match+=1
                    data = image_data

            # if qrcodes where detected in all the parts : 
            match_target = (split_division*2)+1

            if match>=match_target:
                print(f"REQUIRED MINIMUM OF VISIBLE {match_target} QRCODE REACHED = {match} ")
                break
             
            print("QR CODE NOT VISIBLE -- TRIAL "+str(trial))
            IS.set_contrast(contrast)
            IS.set_transparency(transparency)
            image_stream =IS.generate(original_image,code,"grid")
            contrast+=increment_table["contrast"]
            scale+=increment_table["scale"]
            transparency+=increment_table["transparency"]

        print(data)


    im = Image.open(image_stream)
    im.show()

    if args.output_image:
        im.save(args.output_image)

    return image_stream
    
        
if __name__=="__main__":
    result = main()
    print(result)


'''

    python P:/pipeline/dev/a.cormier/core/decorators/image_stamp/repos/ImageStamp/src/main.py -generate -i "P:/projects/billy/library/boxanim/assets/Character/ch_biff_le_borgne/png/ch_biff_le_borgne.png" -c 1897 -o "P:/projects/riv/temp_no_backup/image_stamp"
    python P:/pipeline/dev/a.cormier/core/decorators/image_stamp/repos/ImageStamp/src/main.py -generate -i "P:/projects/billy/library/boxanim/assets/Character/ch_billy/png/ch_billy.png" -c 1897 -o "P:/projects/riv/temp_no_backup/image_stamp"
    python P:/pipeline/dev/a.cormier/core/decorators/image_stamp/repos/ImageStamp/src/main.py -combine -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0001.png" -i "P:/projects/billy/render/png/assets/library/master/ch_billy/t-0002.png" -add_text "this is my text" -o "P:/projects/riv/temp_no_backup/image_stamp" -generate -c "mycode"
    python P:/pipeline/dev/a.cormier/core/decorators/image_stamp/repos/ImageStamp/src/main.py -add_text "test" -i "P:/projects/testa/temp_no_backup/render/packboard/download/bg_bil_ext_m_a1_multipl.png" -oi "P:/projects/testa/temp_no_backup/render/packboard/test/add_text.png"
    python P:/pipeline/dev/a.cormier/core/decorators/image_stamp/repos/ImageStamp/src/main.py -add_text "test" -add_qrcode "my_code" -i "P:/projects/testa/temp_no_backup/render/packboard/download/bg_bil_ext_m_a1_multipl.png" -oi "P:/projects/testa/temp_no_backup/render/packboard/test/add_text.png"
    python P:/pipeline/dev/a.cormier/core/decorators/image_stamp/repos/ImageStamp/src/main.py -apply_filter "BW"  -i "P:/projects/testa/temp_no_backup/render/packboard/download/bg_bil_ext_m_a1_multipl.png" -oi "P:/projects/testa/temp_no_backup/render/packboard/test/add_text.png"

    
    python P:/pipeline/dev/a.cormier/core/decorators/image_stamp/repos/ImageStamp/src/main.py -generate -i "P:/projects/billy/library/boxanim/assets/Character/ch_billy/png/ch_billy.png" -c 1897 -o "P:/projects/riv/temp_no_backup/image_stamp"
    
    
    '''