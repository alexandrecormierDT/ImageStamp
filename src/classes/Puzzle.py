import cv2
import numpy as np
from PIL import Image
from typing import List 
import tempfile
import os
import uuid

class Puzzle:

    def __init__(self) -> None:
        pass

    def unpuzzle(self,image_paths:List[str])->Image:
        '''
        Combine overlapping images into one large image.

        Args:
            image_paths (list[str]): paths to overlapping images

        Returns:
            str: path to the stitched image (temp file)
        '''

        if not image_paths:
            raise ValueError("UnPuzzle requires at least one image path")

        # Load images
        images = []
        for path in image_paths:
            img = cv2.imread(path, cv2.IMREAD_COLOR)
            if img is None:
                raise IOError(f"Failed to load image: {path}")
            images.append(img)

        base_img = images[0]
        orb = cv2.ORB_create(5000)

        for next_img in images[1:]:
            gray_base = cv2.cvtColor(base_img, cv2.COLOR_BGR2GRAY)
            gray_next = cv2.cvtColor(next_img, cv2.COLOR_BGR2GRAY)

            kp1, des1 = orb.detectAndCompute(gray_base, None)
            kp2, des2 = orb.detectAndCompute(gray_next, None)

            if des1 is None or des2 is None:
                continue

            matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            matches = matcher.match(des1, des2)

            if len(matches) < 10:
                continue

            matches = sorted(matches, key=lambda x: x.distance)
            good_matches = matches[:50]

            pts1 = np.float32([kp1[m.queryIdx].pt for m in good_matches])
            pts2 = np.float32([kp2[m.trainIdx].pt for m in good_matches])

            H, mask = cv2.findHomography(pts2, pts1, cv2.RANSAC, 5.0)
            if H is None:
                continue

            h1, w1 = base_img.shape[:2]
            h2, w2 = next_img.shape[:2]

            corners = np.float32([
                [0, 0], [0, h2], [w2, h2], [w2, 0]
            ]).reshape(-1, 1, 2)

            warped_corners = cv2.perspectiveTransform(corners, H)

            all_corners = np.concatenate((
                warped_corners,
                np.float32([[0, 0], [0, h1], [w1, h1], [w1, 0]]).reshape(-1, 1, 2)
            ))

            xmin, ymin = np.int32(all_corners.min(axis=0).ravel() - 0.5)
            xmax, ymax = np.int32(all_corners.max(axis=0).ravel() + 0.5)

            T = np.array([
                [1, 0, -xmin],
                [0, 1, -ymin],
                [0, 0, 1]
            ])

            result = cv2.warpPerspective(
                next_img, T @ H, (xmax - xmin, ymax - ymin)
            )

            result[-ymin:h1 - ymin, -xmin:w1 - xmin] = base_img
            base_img = result

        # Write to temp file
        filename = f"unpuzzle_{uuid.uuid4().hex}.png"
        temp_path = os.path.join(os.getenv("TEMP"), filename)

        cv2.imwrite(temp_path, base_img)

        return temp_path

