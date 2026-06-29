import cv2
import numpy as np
import os

def process_track(input_path="track.png", output_path="track_mask.png"):
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found. Please save your track image here.")
        return False

    # Read the image
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

    # Threshold to get black lines as white, white background as black
    # Assuming the track is drawn with black lines on white background
    _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    
    # Create a blank black image
    mask = np.zeros_like(thresh)
    
    # Draw only the large contours (main track boundaries)
    # This filters out the smaller start/end grid lines and middle lines
    for cnt in contours:
        if len(cnt) > 1000:  # Adjust this threshold if needed
            cv2.drawContours(mask, [cnt], -1, 255, thickness=15)

    # Save the mask
    cv2.imwrite(output_path, mask)
    print(f"Successfully processed {input_path} and saved collision mask to {output_path}")
    return True


if __name__ == "__main__":
    process_track()
