import cv2
import numpy as np
import pyautogui
from ultralytics import YOLO
import matplotlib.pyplot as plt
from PIL import Image

from world_nav.player_controller import PlayerController
from image_manip.mini_map import image_to_grid, draw_circle_at_grid_pos, draw_path, visualize_grid_overlay
from path_find.a_star import a_star_search
from path_find.path_to_actions import path_to_actions
from config import SILLY_STREET
import time

def main():

    player_loco = PlayerController()

    while True:

        time.sleep(1)
        # Capture a specific region of the screen
        # Replace the coordinates with the actual coordinates of your map in the game
        x, y, width, height = SILLY_STREET.region  # Example coordinates
        screenshot = pyautogui.screenshot(region=(x, y, width, height))

        # Convert the screenshot to a format suitable for OpenCV
        screenshot_cv = np.array(screenshot)
        screenshot_cv = cv2.cvtColor(screenshot_cv, cv2.COLOR_RGB2BGR)

        # Convert to grayscale and increase contrast
        gray = cv2.cvtColor(screenshot_cv, cv2.COLOR_BGR2GRAY)
        enhanced_image = cv2.convertScaleAbs(gray, alpha=1.5, beta=20)
        thresholded_image = cv2.adaptiveThreshold(
            enhanced_image,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            blockSize=5,  # Size of a pixel neighborhood that is used to calculate a threshold value
            C=-2  # Constant subtracted from the mean or weighted mean
        )

        # Convert back to PIL Image to display
        gray_image = Image.fromarray(gray)
        disp_thresholded_image = Image.fromarray(thresholded_image)


        # Display grayscale and thresholded images
        # gray_image.show()
        # disp_thresholded_image.show()

        cell_size = 10  # Adjust cell size as needed
        grid = image_to_grid(thresholded_image, cell_size)

        start, goal = SILLY_STREET.tunnel_entr, SILLY_STREET.tunnel_exit # Replace with actual start and goal positions

        visualized_image = cv2.cvtColor(thresholded_image, cv2.COLOR_GRAY2BGR)
        draw_circle_at_grid_pos(visualized_image, start, cell_size, (0, 255, 0), 5)  # Green for start
        draw_circle_at_grid_pos(visualized_image, goal, cell_size, (0, 0, 255), 5)   # Red for goal

        # Convert to PIL Image to display
        visualized_pil_image = Image.fromarray(visualized_image)
        # visualized_pil_image.show()

        visualize_grid_overlay(visualized_image, grid, cell_size, (0, 255, 255))  # Use a distinct color for the grid overlay

        path = a_star_search(grid, start, goal)
        print(path)

        if path:
            draw_path(visualized_image, path, cell_size, (255, 0, 0))  # Blue for path

            # Draw circles for start and goal on the visualized image
            draw_circle_at_grid_pos(visualized_image, start, cell_size, (0, 255, 0), 5)  # Green for start
            draw_circle_at_grid_pos(visualized_image, goal, cell_size, (0, 0, 255), 5)   # Red for goal

            # Convert to PIL Image to display
            visualized_pil_image = Image.fromarray(visualized_image)
            visualized_pil_image.show()
        else:
            print("No path found")

        #player_loco.press_up()

if __name__ == "__main__":
    main()