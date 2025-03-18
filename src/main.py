import sys
sys.path.insert(0,'P:/pipeline/extra_scripts/python_include')
from classes.ImageStamp import ImageStamp
from classes.ImageChecker import ImageChecker
from PIL import Image
import argparse
    
def main():
    print("ImageStamp")
    parser = argparse.ArgumentParser(prog='ImageStamp',description='add qrcode to image')
    parser.add_argument('-read','--read',action='store_true') 
    parser.add_argument('-find_qrcodes','--find_qrcodes',action='store_true') 
    parser.add_argument('-generate','--generate',action='store_true') 
    parser.add_argument('-combine','--combine',action='store_true') 
    parser.add_argument('-maximise','--maximise',action='store_true') 
    parser.add_argument('-check_image','--check_image',action='store_true') 
    parser.add_argument('-create_diff_map','--create_diff_map',action='store_true') 
    parser.add_argument('-add_text','--add_text') 
    parser.add_argument('-add_watermark','--add_watermark') 
    parser.add_argument('-add_overlay','--add_overlay') 
    parser.add_argument('-add_qrcode','--add_qrcode') 
    parser.add_argument('-apply_filter','--apply_filter') 
    parser.add_argument("-i","--input",action='append' ,required=True)
    parser.add_argument("-c","--code")
    parser.add_argument("-ct","--contrast")
    parser.add_argument("-tr","--transparency")
    parser.add_argument("-sf","--scale_factor")
    parser.add_argument("-st","--strategy")
    parser.add_argument("-gd","--grid_division")
    parser.add_argument("-o","--output_path")
    parser.add_argument("-oi","--output_image")
    parser.add_argument("-oj","--overlay_json")
    parser.add_argument("-s","--scale")
    parser.add_argument("-im","--integration_mode",default="all_corners")

    args = parser.parse_args()
    
    IS = ImageStamp()
    IC = ImageChecker()

    input_stream =args.input

    if args.read:
        data = IS.read(input_stream)
        return data
    
    if args.find_qrcodes and args.input and args.output_path:
        data = IS.find_qrcodes(input_stream,args.output_path)
        return data
    
    if args.add_overlay and args.input and args.overlay_json and args.output_path:
        data = IS.add_overlay(input_stream,args.overlay_json,args.output_path)
        return data

    if args.check_image:
        data = IC.check(input_stream)
        return data

    if args.combine:
        input_stream =IC.check(IS.combine(input_stream))

    if args.maximise:
        input_stream =IC.check(IS.maximise(input_stream))

    if args.create_diff_map:
        input_stream =IS.create_diff_map(input_stream[0],input_stream[1])

    # process on single images : 

    if isinstance(input_stream,list):
        input_stream = input_stream[0]
        
    if args.add_text:
        input_stream = IC.check(IS.add_text(input_stream,args.add_text))

    if args.add_watermark:
        input_stream = IC.check(IS.add_watermark(input_stream,args.add_watermark))

    if args.add_qrcode:
        code = args.add_qrcode
        integration_mode = "grid"
        strategy = "optimaly_hidden"
        if args.integration_mode:
            integration_mode = args.integration_mode
        if args.strategy:
            strategy = args.strategy
        # put hidden qrcodes
        input_stream =IS.add_qrcode(input_stream,code,integration_mode,strategy)

    if args.apply_filter:
        input_stream =IS.apply_filter(input_stream,args.apply_filter)

    if input_stream is None or input_stream == "":
        print("Image stream is None")
        sys.exit(0)

    im = Image.open(input_stream)
    #im.show()

    if args.output_image:
        im.save(args.output_image)
    else:
        im.save(args.input[0])

    IS.clean_temp()

    return input_stream
    
        
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
    python P:/pipeline/dev/a.cormier/core/decorators/image_stamp/repos/ImageStamp/src/main.py -i P:/projects/testa/users/a.cormier/test/image_stamp/my_image.png -add_watermark "this is a watemark"
    python P:/pipeline/dev/a.cormier/core/decorators/image_stamp/repos/ImageStamp/src/main.py -i P:/projects/billy/temp_no_backup/Sherif_temp/2024_11_22/download/attachment_ch_suzie_606866.png -i P:/projects/billy/temp_no_backup/Sherif_temp/2024_11_22/download/attachment_ch_suzie_606867.png -i P:/projects/billy/temp_no_backup/Sherif_temp/2024_11_22/download/attachment_ch_suzie_606868.png -i P:/projects/billy/temp_no_backup/Sherif_temp/2024_11_22/download/attachment_ch_suzie_606869.png -add_text "CH_SUZIE_CHARCATER-1" -apply_filter BW -oi P:/projects/billy/temp_no_backup/Sherif_temp/2024_11_22/pack_board/fe3d7/ep297_testboard_packboard_design_fe3d6/CH_SUZIE_CHARCATER-1.png
    python P:/pipeline/dev/a.cormier/core/decorators/image_stamp/repos/ImageStamp/src/main.py -combine -i P:/projects/billy/temp_no_backup/Sherif_temp/2024_11_25/download/attachment_ch_suzie_606866.png -i P:/projects/billy/temp_no_backup/Sherif_temp/2024_11_25/download/attachment_ch_suzie_606867.png -i P:/projects/billy/temp_no_backup/Sherif_temp/2024_11_25/download/attachment_ch_suzie_606868.png -i P:/projects/billy/temp_no_backup/Sherif_temp/2024_11_25/download/attachment_ch_suzie_606869.png -add_text "CH_SUZIE_CHARCATER-1" -apply_filter BW -oi P:/projects/billy/temp_no_backup/Sherif_temp/2024_11_25/pack_board/3fab7/ep297_testboard_packboard_design_3fab6/CH_SUZIE_CHARCATER-1.png
'''