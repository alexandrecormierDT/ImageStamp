import numpy as np
import imageio.v2 as imageio
import cv2

INPUT_PATH = "input.dpx"
OUTPUT_PATH = "burn_map.png"

HIGH_THRESHOLD = 250
LOW_THRESHOLD = 5

def load_image(path):
    """
    Load DPX or other formats.
    Converts to 8-bit RGB if necessary.
    """
    img = imageio.imread(path)

    # If 16-bit or float, normalize to 0–255
    if img.dtype == np.uint16:
        img = (img / 257).astype(np.uint8)
    elif img.dtype == np.float32 or img.dtype == np.float64:
        img = np.clip(img * 255, 0, 255).astype(np.uint8)

    # Ensure RGB (drop alpha if present)
    if img.shape[-1] == 4:
        img = img[:, :, :3]

    return img

def create_burn_map(img):
    h, w, _ = img.shape
    burn_map = np.zeros((h, w, 3), dtype=np.uint8)

    R = img[:, :, 0]
    G = img[:, :, 1]
    B = img[:, :, 2]

    high_R = R > HIGH_THRESHOLD
    high_G = G > HIGH_THRESHOLD
    high_B = B > HIGH_THRESHOLD

    low_R = R < LOW_THRESHOLD
    low_G = G < LOW_THRESHOLD
    low_B = B < LOW_THRESHOLD

    # High burns
    burn_map[high_R, 0] = 255
    burn_map[high_G, 1] = 255
    burn_map[high_B, 2] = 255

    # Low crush (dim color to differentiate)
    burn_map[low_R, 0] = 128
    burn_map[low_G, 1] = 128
    burn_map[low_B, 2] = 128

    return burn_map

def main():
    print("Loading image...")
    img = load_image(INPUT_PATH)

    print("Creating burn map...")
    burn_map = create_burn_map(img)

    print("Saving result...")
    cv2.imwrite(OUTPUT_PATH, cv2.cvtColor(burn_map, cv2.COLOR_RGB2BGR))

    print("Done!")

if __name__ == "__main__":
    main()
