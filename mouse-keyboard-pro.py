import pyautogui
import time
import logging
import yaml
import smtplib
import argparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from PIL import Image

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger().addHandler(logging.FileHandler('script.log'))

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Automate mouse movements and send email notifications.')
parser.add_argument('--config', type=str, default='config.yaml', help='Path to the configuration file')
args = parser.parse_args()

# Load configuration
config_path = args.config
with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

# Function to send email notifications
def send_email(subject, body, attachments=[]):
    sender_email = "oussamaayari2014@gmail.com"
    receiver_email = "jnt8yyw9@spymail.one"
    password = "kcqd dpeu kqee vunm"
    smtp_server = "smtp.gmail.com"
    smtp_port = 465  # Update based on your provider

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

    for attempt in range(3):  # Retry mechanism
        try:
            if smtp_port == 465:
                # Using SSL
                server = smtplib.SMTP_SSL(smtp_server, smtp_port)
            else:
                # Using TLS
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
            
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            server.quit()
            logging.info(f'Email sent to {receiver_email}')
            break
        except Exception as e:
            logging.error(f'Failed to send email (attempt {attempt + 1}): {e}')
            time.sleep(5)  # Wait before retrying

# Function to take and compress a screenshot
def take_screenshot(step):
    filename = f'screenshot_{step}.png'
    compressed_filename = f'compressed_screenshot_{step}.png'
    pyautogui.screenshot(filename)
    
    # Compress the screenshot
    img = Image.open(filename)
    img.save(compressed_filename, optimize=True, quality=50)  # Adjust quality as needed
    
    logging.info(f'Compressed screenshot taken: {compressed_filename}')
    return compressed_filename

# Function to execute actions
def execute_action(action, step):
    try:
        if action['action'] == 'move_click':
            x, y, duration = action['x'], action['y'], action.get('duration', 3)
            logging.info(f'Step {step}: Moving to ({x}, {y}) over {duration} seconds')
            pyautogui.moveTo(x, y, duration=duration)
            pyautogui.click()
        elif action['action'] == 'press':
            key, duration = action['key'], action.get('duration', 3)
            logging.info(f'Step {step}: Pressing {key}')
            pyautogui.press(key)
            time.sleep(duration)
        elif action['action'] == 'hotkey':
            keys, duration = action['keys'], action.get('duration', 3)
            logging.info(f'Step {step}: Pressing hotkeys {keys}')
            pyautogui.hotkey(*keys)
            time.sleep(duration)
        elif action['action'] == 'write':
            text, interval = action['text'], action.get('interval', 0.05)
            logging.info(f'Step {step}: Writing text {text}')
            pyautogui.write(text, interval=interval)
        return take_screenshot(step)
    except Exception as e:
        logging.error(f'Step {step}: Error executing action: {e}')
        return None

# Execute actions from config
screenshots = []
for idx, action in enumerate(config['actions']):
    step = f'{idx + 1}'
    screenshot = execute_action(action, step)
    if screenshot:
        screenshots.append(screenshot)

logging.info('Script finished')

# Send email with compressed screenshots
send_email('Automation Script Completed', 'The automation script has completed successfully.', screenshots)
