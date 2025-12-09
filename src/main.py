import sys
import os
import argparse
from PIL import Image

# Ensure your modules are importable
sys.path.insert(0, 'P:/pipeline/extra_scripts/python_include')
from classes.ImageStamp import ImageStamp
from classes.ImageChecker import ImageChecker


def process_input_images(input_images, checker: ImageChecker):
    """
    Validate input images and reduce to a single image if needed.
    """
    valid_images = []
    for img in input_images:
        result = checker.check([img])
        if result:
            valid_images.append(img)
    if not valid_images:
        print("[Error] No valid images found after checking.")
        sys.exit(1)
    return valid_images[0] if len(valid_images) == 1 else valid_images


def main():
    parser = argparse.ArgumentParser(
        prog='ImageStamp',
        description='Add QR codes, overlays, text, watermark, and filters to images'
    )

    # Boolean flags
    parser.add_argument('--read', action='store_true')
    parser.add_argument('--find_qrcodes', action='store_true')
    parser.add_argument('--generate', action='store_true')
    parser.add_argument('--combine', action='store_true')
    parser.add_argument('--maximise', action='store_true')
    parser.add_argument('--check_image', action='store_true')
    parser.add_argument('--create_diff_map', action='store_true')

    # Parameters with values
    parser.add_argument('--add_text')
    parser.add_argument('--add_watermark')
    parser.add_argument('--add_overlay')
    parser.add_argument('--add_qrcode')
    parser.add_argument('--apply_filter')
    parser.add_argument('--input', '-i', action='append', required=True)
    parser.add_argument('--code', '-c')
    parser.add_argument('--contrast', '-ct')
    parser.add_argument('--transparency', '-tr')
    parser.add_argument('--scale_factor', '-sf')
    parser.add_argument('--strategy', '-st')
    parser.add_argument('--grid_division', '-gd')
    parser.add_argument('--output_path', '-o')
    parser.add_argument('--output_image', '-oi')
    parser.add_argument('--overlay_json', '-oj')
    parser.add_argument('--scale', '-s')
    parser.add_argument('--integration_mode', '-im', default='all_corners')

    args = parser.parse_args()

    IS = ImageStamp()
    IC = ImageChecker()

    input_stream = args.input

    # --- Early operations ---
    if args.read:
        return IS.read(input_stream)

    if args.find_qrcodes:
        if not args.output_path:
            print("[Error] --output_path required for --find_qrcodes")
            sys.exit(1)
        return IS.find_qrcodes(input_stream, args.output_path)

    if args.add_overlay:
        if not args.output_path or not args.overlay_json:
            print("[Error] --output_path and --overlay_json required for --add_overlay")
            sys.exit(1)
        return IS.add_overlay(input_stream, args.overlay_json, args.output_path)

    if args.check_image:
        return IC.check(input_stream)

    # --- Image transformations ---
    if args.combine:
        input_stream = IC.check(IS.combine(input_stream))

    if args.maximise:
        input_stream = IC.check(IS.maximise(input_stream))

    if args.create_diff_map:
        if isinstance(input_stream, list) and len(input_stream) >= 2:
            input_stream = IS.create_diff_map(input_stream[0], input_stream[1])
        else:
            print("[Error] At least 2 images required for diff map")
            sys.exit(1)

    # Reduce input stream to a single image for single-image operations
    if isinstance(input_stream, list):
        input_stream = process_input_images(input_stream, IC)

    # --- Apply operations on single images ---
    if args.add_text:
        input_stream = IC.check(IS.add_text(input_stream, args.add_text))

    if args.add_watermark:
        input_stream = IC.check(IS.add_watermark(input_stream, args.add_watermark))

    if args.add_qrcode:
        code = args.add_qrcode
        integration_mode = args.integration_mode or "grid"
        strategy = args.strategy or "optimaly_hidden"
        input_stream = IS.add_qrcode(input_stream, code, integration_mode, strategy)

    if args.apply_filter:
        input_stream = IS.apply_filter(input_stream, args.apply_filter)

    # --- Save the final image ---
    if not input_stream:
        print("[Error] Image stream is None or empty")
        sys.exit(1)

    im = Image.open(input_stream)
    output_file = args.output_image or args.input[0]
    im.save(output_file)
    print(f"[Info] Image saved to: {output_file}")

    # Clean temporary files
    IS.clean_temp()

    return input_stream


if __name__ == "__main__":
    result = main()
    print(result)
