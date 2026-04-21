import numpy as np
import imageio.v2 as imageio
import cv2

INPUT_PATH = "input.dpx"
OUTPUT_PATH = "burn_map.png"

HIGH_PERCENT = 0.98   # 98% of max code value
LOW_PERCENT = 0.02    # 2% of max code value


def load_dpx_native(path):
    img = imageio.imread(path)

    if img.ndim != 3 or img.shape[2] < 3:
        raise ValueError("Image must be RGB")

    # Drop alpha if present
    if img.shape[2] == 4:
        img = img[:, :, :3]

    return img


def detect_bit_depth(img):
    max_val = img.max()

    if max_val <= 1023:
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

    print(f"Detected {bit_depth}-bit DPX")
    print(f"High threshold: {high_threshold}")
    print(f"Low threshold: {low_threshold}")

    # Output is standard 8-bit RGB
    burn_map = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)

    R = img[:, :, 0]
    G = img[:, :, 1]
    B = img[:, :, 2]

    high_R = R >= high_threshold
    high_G = G >= high_threshold
    high_B = B >= high_threshold

    low_R = R <= low_threshold
    low_G = G <= low_threshold
    low_B = B <= low_threshold

    # Highlights → full intensity
    burn_map[high_R, 0] = 255
    burn_map[high_G, 1] = 255
    burn_map[high_B, 2] = 255

    # Shadows → half intensity (to distinguish from highlights)
    burn_map[low_R, 0] = 128
    burn_map[low_G, 1] = 128
    burn_map[low_B, 2] = 128

    return burn_map


def main():
    print("Loading DPX...")
    img = load_dpx_native(INPUT_PATH)

    print("Creating burn map...")
    burn_map = create_burn_map_8bit(img)

    print("Saving PNG...")
    cv2.imwrite(OUTPUT_PATH, cv2.cvtColor(burn_map, cv2.COLOR_RGB2BGR))

    print("Done!")


if __name__ == "__main__":
    main()
