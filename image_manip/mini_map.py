import pyautogui
import cv2
import numpy as np
import heapq
from PIL import Image

def image_to_grid(image, cell_size):
    grid = []
    h, w = image.shape

    for y in range(0, h, cell_size):
        row = []
        for x in range(0, w, cell_size):
            # Check if all pixels in the cell are white (walkable)
            cell_area = image[y:y+cell_size, x:x+cell_size]
            cell = 0 if np.all(cell_area == 255) else 1  # Walkable if all pixels are white (255)
            row.append(cell)
        grid.append(row)

    return grid

def draw_circle_at_grid_pos(image, grid_pos, cell_size, color, radius):
    # Convert grid position to pixel coordinates
    pixel_x = int(grid_pos[1] * cell_size + cell_size / 2)
    pixel_y = int(grid_pos[0] * cell_size + cell_size / 2)
    # Draw the circle on the image
    cv2.circle(image, (pixel_x, pixel_y), radius, color, -1)

def draw_path(image, path, cell_size, color):
    # Iterate over the path points and draw lines between each consecutive point
    for i in range(1, len(path)):
        start_point = path[i - 1]
        end_point = path[i]
        start_pixel = (int(start_point[1] * cell_size + cell_size / 2), int(start_point[0] * cell_size + cell_size / 2))
        end_pixel = (int(end_point[1] * cell_size + cell_size / 2), int(end_point[0] * cell_size + cell_size / 2))
        cv2.line(image, start_pixel, end_pixel, color, 2)

def visualize_grid_overlay(image, grid, cell_size, color):
    h, w = image.shape[:2]
    # Draw grid lines
    for y in range(0, h, cell_size):
        cv2.line(image, (0, y), (w, y), color, 1)
    for x in range(0, w, cell_size):
        cv2.line(image, (x, 0), (x, h), color, 1)
    
    # Fill non-walkable cells
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == 1:  # Non-walkable
                top_left = (j * cell_size, i * cell_size)
                bottom_right = ((j + 1) * cell_size, (i + 1) * cell_size)
                cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)