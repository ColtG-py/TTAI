import pyautogui

class PlayerController:
    def __init__(self):
        # Optional: set a default delay between commands
        pyautogui.PAUSE = 0.05

    def press_left(self):
        pyautogui.keyDown('left')

    def release_left(self):
        pyautogui.keyUp('left')

    def press_right(self):
        pyautogui.keyDown('right')

    def release_right(self):
        pyautogui.keyUp('right')

    def press_up(self):
        pyautogui.keyDown('up')

    def release_up(self):
        pyautogui.keyUp('up')

    def press_down(self):
        pyautogui.keyDown('down')

    def release_down(self):
        pyautogui.keyUp('down')

    def press_jump(self):
        pyautogui.keyDown('ctrl')

    def release_jump(self):
        pyautogui.keyUp('ctrl')

    def press_alt(self):
        pyautogui.keyDown('alt')

    def release_alt(self):
        pyautogui.keyUp('alt')
