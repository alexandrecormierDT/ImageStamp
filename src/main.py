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
    parser.add_argument('-add_qrcode','--add_qrcode') 
    parser.add_argument('-apply_filter','--apply_filter') 
    parser.add_argument("-i","--image_source",action='append' ,required=True)
    parser.add_argument("-c","--code")
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

    if isinstance(image_stream,list):
        image_stream = image_stream[0]
        
    if args.add_text:
        image_stream = IS.add_text(image_stream,args.add_text)

    if args.add_qrcode:
        image_stream =IS.generate(image_stream,args.add_qrcode,args.position)

    if args.apply_filter:
        image_stream =IS.apply_filter(image_stream,args.apply_filter)

    #obsolete
    if args.generate and args.code:
        image_stream =IS.generate(image_stream,args.code,args.position)


    im = Image.open(image_stream)

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

    
    
    
    '''