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
    parser.add_argument('-add_text','--add_text') 
    parser.add_argument("-i","--image_source",action='append' ,required=True)
    parser.add_argument("-c","--code")
    parser.add_argument("-o","--output_folder")
    parser.add_argument("-oi","--output_image")
    parser.add_argument("-s","--scale")
    parser.add_argument("-p","--position")

    args = parser.parse_args()
    
    IS = ImageStamp()
    image_stream =args.image_source

    if args.read:
        data = IS.read(image_stream)
        return data

    if args.combine:
        image_stream =IS.combine(image_stream)

    if args.add_text:
        image_stream = IS.add_text(image_stream,args.add_text)

    if args.generate and args.code:
        position = "all_corners"
        if args.position:
            position = args.position
        image_stream =IS.generate(image_stream,args.code,position)

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

'''