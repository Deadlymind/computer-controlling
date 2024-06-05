import pyautogui
import time



position = pyautogui.position()
print(position)

pyautogui.doubleClick(x=1907, y=300, duration=3)
time.sleep(1)
pyautogui.press('down')
pyautogui.press('enter')
pyautogui.write('hello, i am computer controller this script is created by Oussama to control the computer for smp team \nlets start now with Web Email Extractor Pro', interval=0.05)

pyautogui.hotkey('ctrl', 'a')
pyautogui.hotkey('ctrl', 'c')
pyautogui.press('del')
pyautogui.hotkey('ctrl', 'v')
