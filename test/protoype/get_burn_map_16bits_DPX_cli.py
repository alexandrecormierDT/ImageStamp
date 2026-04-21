import numpy as np
import cv2
import os
import argparse
import imageio.v2 as imageio
import tempfile
import uuid
import platform
import subprocess

HIGH_PERCENT = 0.98
LOW_PERCENT = 0.02



def detect_bit_depth(img):
    max_val = img.max()
    if max_val <= 255:
        return 8, 255
    elif max_val <= 1023:
        return 10, 1023
    elif max_val <= 4095:
        return 12, 4095
    elif max_val <= 65535:
        return 16, 65535
    else:
        raise ValueError("Unsupported bit depth")

def create_burn_map_8bit(img):
    bit_depth, max_code = detect_bit_depth(img)
    high_threshold = int(max_code * HIGH_PERCENT)
    low_threshold = int(max_code * LOW_PERCENT)

    burn_map = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]

    burn_map[R >= high_threshold, 0] = 255
    burn_map[G >= high_threshold, 1] = 255
    burn_map[B >= high_threshold, 2] = 255

    burn_map[R <= low_threshold, 0] = 128
    burn_map[G <= low_threshold, 1] = 128
    burn_map[B <= low_threshold, 2] = 128

    return burn_map

def load_image(path):
    img = imageio.imread(path)
    if img.ndim != 3 or img.shape[2] < 3:
        raise ValueError(f"Image must be RGB: {path}")
    if img.shape[2] > 3:
        img = img[:, :, :3]
    return img

def open_folder(path):
    system = platform.system()
    try:
        if system == "Windows":
            os.startfile(path)
        elif system == "Darwin":  # macOS
            subprocess.Popen(["open", path])
        else:  # Linux
            subprocess.Popen(["xdg-open", path])
    except Exception as e:
        print(f"Could not open folder automatically: {e}")

def process_folder(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    valid_exts = (".png", ".jpg", ".jpeg", ".tif", ".tiff", ".dpx", ".exr")
    files = sorted([f for f in os.listdir(input_folder) if f.lower().endswith(valid_exts)])

    if not files:
        raise FileNotFoundError(f"No image files found in {input_folder}")

    skipped = 0
    processed = 0

    for idx, file in enumerate(files, 1):
        input_path = os.path.join(input_folder, file)
        try:
            img = load_image(input_path)
        except Exception as e:
            print(f"Skipping {file}: {e}")
            skipped += 1
            continue

        burn_map = create_burn_map_8bit(img)

        if not np.any(burn_map):
            print(f"Skipping {file}: burn map is all black")
            skipped += 1
            continue

        output_path = os.path.join(output_folder, os.path.splitext(file)[0] + "_burn.png")
        cv2.imwrite(output_path, cv2.cvtColor(burn_map, cv2.COLOR_RGB2BGR))
        processed += 1

        if idx % 10 == 0 or idx == len(files):
            print(f"Processed {idx}/{len(files)} images...")

    print(f"\nFinished processing. {processed} burn maps created, {skipped} images skipped.")
    print(f"Burn maps saved to: {output_folder}")
    open_folder(output_folder)

def main():
    parser = argparse.ArgumentParser(description="Create burn maps for images in a folder (supports DPX/16-bit).")
    parser.add_argument("input_folder", help="Folder containing input images")
    parser.add_argument("-o", "--output", help="Folder to save burn maps")
    args = parser.parse_args()

    if not os.path.exists(args.input_folder):
        raise FileNotFoundError(f"Input folder not found: {args.input_folder}")

    if args.output:
        output_folder = args.output
    else:
        temp_root = tempfile.gettempdir()
        unique_id = str(uuid.uuid4())[:8]
        output_folder = os.path.join(temp_root, "burn_map", unique_id)

    process_folder(args.input_folder, output_folder)

if __name__ == "__main__":
    main()

'''

P:/projects/riv/render/dpx/shots/ep109_rivlm/ep109_sq004/ep109_pl641

python P:/pipeline/dev/a.cormier/core/decorators/image_stamp/repos/ImageStamp/test/protoype/get_burn_map_16bits_DPX_cli.py P:/projects/riv/render/dpx/shots/ep109_rivlm/ep109_sq004/ep109_pl641 -o P:/pipeline/dev/a.cormier/core/decorators/image_stamp/repos/ImageStamp/test/output/burn_map


'''