import pyautogui


pyautogui.moveTo(x=-1150, y=393, duration=3)

pyautogui.click()
pyautogui.drag(150, 0,duration=1, button='left')
pyautogui.drag(0, -150,duration=1, button='left')
pyautogui.drag(-150, 0,duration=1, button='left')
pyautogui.drag(0, 150,duration=1, button='left')