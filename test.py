import pyautogui
import cv2
import numpy as np
import heapq
from PIL import Image
import time
from config import SILLY_STREET

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

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(grid, start, goal):
    neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 4-way movement
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []

    heapq.heappush(oheap, (fscore[start], start))
    
    while oheap:
        current = heapq.heappop(oheap)[1]

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data[::-1]

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j            
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            if 0 <= neighbor[0] < len(grid):
                if 0 <= neighbor[1] < len(grid[0]):
                    if grid[neighbor[0]][neighbor[1]] == 1:
                        continue
                else:
                    continue
            else:
                continue

            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue

            if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(oheap, (fscore[neighbor], neighbor))
    
    return False

def path_to_actions(path):
    actions = []
    for i in range(1, len(path)):
        x1, y1 = path[i - 1]
        x2, y2 = path[i]
        if x2 > x1:
            actions.append('move right')
        elif x2 < x1:
            actions.append('move left')
        if y2 > y1:
            actions.append('move down')
        elif y2 < y1:
            actions.append('move up')
    return actions

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

time.sleep(3)

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
visualized_pil_image.show()

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
# actions = path_to_actions(path)
# print(actions)