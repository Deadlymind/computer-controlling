import pyautogui
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to move and click
def move_and_click(x, y, duration=3):
    try:
        logging.info(f'Moving to ({x}, {y}) over {duration} seconds')
        pyautogui.moveTo(x, y, duration=duration)
        pyautogui.click()
        logging.info(f'Clicked at ({x}, {y})')
    except Exception as e:
        logging.error(f'Error moving to ({x}, {y}): {e}')

# Get current mouse position
position = pyautogui.position()
logging.info(f'Current mouse position: {position}')

# Sequence of actions
actions = [
    (465, 171, 3),
    (1680, 307, 3),
    (447, 1357, 30),
    (1305, 777, 3),
    (1603, 355, 3),
    (770, 630, 3),
    (939, 840, 3),
    (777, 756, 3),
    (1476, 1066, 3)
]

# Execute actions
for action in actions:
    x, y, duration = action
    move_and_click(x, y, duration)
    time.sleep(1)  # Pause between actions for reliability

logging.info('Script finished')
