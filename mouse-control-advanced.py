import pyautogui
import time
import logging
import yaml
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger().addHandler(logging.FileHandler('script.log'))

# Load configuration
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Function to send email notifications
def send_email(subject, body, attachments=[]):
    sender_email = "oussamaayari2014@gmail.com"
    receiver_email = "g433zmn3@flymail.tk"
    password = "kcqd dpeu kqee vunm"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    for file in attachments:
        with open(file, 'rb') as f:
            part = MIMEApplication(f.read(), Name=file)
        part['Content-Disposition'] = f'attachment; filename="{file}"'
        msg.attach(part)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        logging.info(f'Email sent to {receiver_email}')
    except Exception as e:
        logging.error(f'Failed to send email: {e}')

# Function to take a screenshot
def take_screenshot(step):
    filename = f'screenshot_{step}.png'
    pyautogui.screenshot(filename)
    logging.info(f'Screenshot taken: {filename}')
    return filename

# Function to move and click
def move_and_click(x, y, duration=3, step=''):
    try:
        logging.info(f'Step {step}: Moving to ({x}, {y}) over {duration} seconds')
        pyautogui.moveTo(x, y, duration=duration)
        pyautogui.click()
        logging.info(f'Step {step}: Clicked at ({x}, {y})')
        return take_screenshot(step)
    except Exception as e:
        logging.error(f'Step {step}: Error moving to ({x}, {y}): {e}')
        return None

# Execute actions from config
screenshots = []
for idx, action in enumerate(config['actions']):
    x = action['x']
    y = action['y']
    duration = action.get('duration', 3) + random.uniform(-0.5, 0.5)  # Randomize duration slightly
    step = f'{idx + 1}'
    screenshot = move_and_click(x, y, duration, step)
    if screenshot:
        screenshots.append(screenshot)
    time.sleep(1)  # Pause between actions for reliability

logging.info('Script finished')

# Send email with screenshots
send_email('Automation Script Completed', 'The automation script has completed successfully.', screenshots)
