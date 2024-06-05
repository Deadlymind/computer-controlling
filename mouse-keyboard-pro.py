import pyautogui  # Import the pyautogui library for controlling the mouse and keyboard
import time  # Import the time library for adding delays
import logging  # Import the logging library for logging information
import yaml  # Import the yaml library for parsing YAML configuration files
import smtplib  # Import the smtplib library for sending emails
import argparse  # Import the argparse library for parsing command-line arguments
from email.mime.text import MIMEText  # Import MIMEText for email text content
from email.mime.multipart import MIMEMultipart  # Import MIMEMultipart for email multipart content
from email.mime.application import MIMEApplication  # Import MIMEApplication for email attachments

# Configure logging to log messages to a file and the console
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger().addHandler(logging.FileHandler('script.log'))

# Parse command-line arguments for dynamic configuration
parser = argparse.ArgumentParser(description='Automate mouse movements and send email notifications.')
parser.add_argument('--config', type=str, default='config.yaml', help='Path to the configuration file')
args = parser.parse_args()

# Load configuration from the specified YAML file
config_path = args.config
with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

# Function to send email notifications
def send_email(subject, body, attachments=[]):
    sender_email = "oussamaayari2014@gmail.com"  # Your email address
    receiver_email = "biwdymuof@emlhub.com"  # Recipient email address
    password = "kcqd dpeu kqee vunm"  # Your email password or app-specific password
    smtp_server = "smtp.gmail.com"  # SMTP server for sending the email
    smtp_port = 465  # Port for SSL

    # Create a multipart email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

    # Attach any files to the email
    for file in attachments:
        with open(file, 'rb') as f:
            part = MIMEApplication(f.read(), Name=file)
        part['Content-Disposition'] = f'attachment; filename="{file}"'
        msg.attach(part)

    # Retry sending the email up to 3 times in case of failure
    for attempt in range(3):
        try:
            if smtp_port == 465:
                # Using SSL
                server = smtplib.SMTP_SSL(smtp_server, smtp_port)
            else:
                # Using TLS
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
            
            # Log in to the SMTP server and send the email
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            server.quit()
            logging.info(f'Email sent to {receiver_email}')
            break
        except Exception as e:
            logging.error(f'Failed to send email (attempt {attempt + 1}): {e}')
            time.sleep(5)  # Wait before retrying

# Function to take a screenshot and log the action
def take_screenshot(step):
    filename = f'screenshot_{step}.png'  # Filename for the screenshot
    pyautogui.screenshot(filename)  # Take a screenshot
    logging.info(f'Screenshot taken: {filename}')
    return filename

# Function to execute actions based on the configuration
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

# Execute actions defined in the configuration file
screenshots = []
for idx, action in enumerate(config['actions']):
    step = f'{idx + 1}'
    screenshot = execute_action(action, step)
    if screenshot:
        screenshots.append(screenshot)

logging.info('Script finished')

# Send an email with the screenshots attached
send_email('Automation Script Completed', 'The automation script has completed successfully.', screenshots)
