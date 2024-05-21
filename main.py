from QRReader import QRReader
from QRWriter import QRWriter
    
def main():
    print("ImageStamp")
    parser = argparse.ArgumentParser(prog='ImageStamp',description='add qrcode to image')
    parser.add_argument('-read','--read',action='store_true') 
    parser.add_argument('-generate','--generate',action='store_true') 
    parser.add_argument("-i","--image_source",required=True)
    parser.add_argument("-c","--code")
    parser.add_argument("-o","--output_folder")
    parser.add_argument("-s","--scale")
    args = parser.parse_args()
    
    if args.generate:
        writer = QRWriter()
        writer.generate(args.image_source,args.code,args.output_folder)
        
    if args.read:
        reader = QRReader()
        reader(args.image_source)
    
        
if __name__=="__main__":
    main()
    
    
        



'''
python D:/1_TRAVAIL/WIP/CODING/repos/ImageStamp/main.py -generate -i D:/1_TRAVAIL/WIP/CODING/resources/images/png/dog.png -c TEST -o D:/1_TRAVAIL/WIP/CODING/repos/ImageStamp/output
python D:/1_TRAVAIL/WIP/CODING/repos/ImageStamp/main.py -generate -i D:/1_TRAVAIL/WIP/CODING/resources/images/png/dog.png -c 1897 -o D:/1_TRAVAIL/WIP/CODING/repos/ImageStamp/output

'''