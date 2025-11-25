from PIL import Image
import cv2
import numpy as np
import os 
import uuid


class Vectorisator():

    def __init__(self):
        ...

    def vectorise(self,_path:str)->str:
        print(_path)
        temp_path = self._generate_tmp_path()+".svg"
        self.detailed_gray_svg(_path,temp_path)
        return temp_path
    
    def _generate_tmp_path(self)->str:
        image_folder= os.getenv("TEMP")
        image_name = str(uuid.uuid4())[-15:]
        path = image_folder+"/"+image_name
        return path
    
    def detailed_gray_svg(self,image_path, svg_path="output.svg",
                        num_shades=4, blur=1, edge_boost=True, simplify=0.0001):
        """
        Convert a grayscale or black-and-white image to a detailed gray-tone SVG.
        
        Args:
            image_path (str): Input image path.
            svg_path (str): Output SVG path.
            num_shades (int): Number of gray levels (4–8 recommended).
            blur (int): Gaussian blur radius to reduce noise (0 = none).
            edge_boost (bool): Apply edge sharpening to preserve lines.
            simplify (float): Simplification factor for contours (lower = more detail).
        """
        # Load grayscale
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise ValueError(f"Could not load image: {image_path}")

        # Optional blur to smooth noise
        if blur > 0:
            img = cv2.GaussianBlur(img, (blur*2+1, blur*2+1), 0)

        # Optional edge enhancement
        if edge_boost:
            edges = cv2.Laplacian(img, cv2.CV_8U)
            img = cv2.addWeighted(img, 1.2, edges, -0.3, 0)

        # Normalize and quantize
        img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
        levels = np.linspace(0, 255, num_shades+1, dtype=np.uint8)
        quantized = np.digitize(img, levels) - 1

        h, w = img.shape
        svg_lines = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}" shape-rendering="geometricPrecision">'
        ]

        # Iterate through tones (dark → light)
        for i in range(num_shades):
            mask = np.uint8(quantized == i) * 255
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            gray_val = int(255 * (i / (num_shades - 1)))
            hex_gray = f"#{gray_val:02x}{gray_val:02x}{gray_val:02x}"

            for cnt in contours:
                if len(cnt) < 5:
                    continue
                # Lower epsilon = more detail, higher = smoother
                epsilon = simplify * cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, epsilon, True)
                path_data = "M " + " L ".join(f"{x},{y}" for [[x, y]] in cnt) + " Z"
                svg_lines.append(f'<path d="{path_data}" fill="{hex_gray}" stroke="none"/>')

        svg_lines.append("</svg>")

        with open(svg_path, "w") as f:
            f.write("\n".join(svg_lines))

        print(f"✅ Saved detailed SVG to: {svg_path}")
