import pyautogui  # Import the pyautogui library for automating mouse and keyboard actions
import time  # Import the time library for adding delays
import logging  # Import the logging library for logging messages
import yaml  # Import the yaml library for parsing YAML configuration files
import smtplib  # Import the smtplib library for sending emails
import argparse  # Import the argparse library for parsing command-line arguments
from email.mime.text import MIMEText  # Import MIMEText for email text content
from email.mime.multipart import MIMEMultipart  # Import MIMEMultipart for email multipart content
from email.mime.application import MIMEApplication  # Import MIMEApplication for email attachments
from PIL import Image  # Import the PIL library for image processing and compression
from datetime import datetime  # Import datetime for generating timestamps

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
    sender_email = "oussamaayari2014@gmail.com"  # Sender's email address
    receiver_email = "jnt8yyw9@spymail.one"  # Receiver's email address
    password = "kcqd dpeu kqee vunm"  # Sender's email password or app-specific password
    smtp_server = "smtp.gmail.com"  # SMTP server for sending the email
    smtp_port = 465  # Port for SSL

    msg = MIMEMultipart()  # Create a multipart email message
    msg['From'] = sender_email  # Set the sender email
    msg['To'] = receiver_email  # Set the receiver email
    msg['Subject'] = subject  # Set the subject of the email

    msg.attach(MIMEText(body, 'plain'))  # Attach the email body

    for file in attachments:
        with open(file, 'rb') as f:  # Open each file to be attached
            part = MIMEApplication(f.read(), Name=file)  # Read the file content
        part['Content-Disposition'] = f'attachment; filename="{file}"'  # Set the content disposition
        msg.attach(part)  # Attach the file to the email

    for attempt in range(3):  # Retry mechanism, try sending the email up to 3 times
        try:
            if smtp_port == 465:
                # Using SSL
                server = smtplib.SMTP_SSL(smtp_server, smtp_port)  # Connect to the SMTP server using SSL
            else:
                # Using TLS
                server = smtplib.SMTP(smtp_server, smtp_port)  # Connect to the SMTP server using TLS
                server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
            
            server.login(sender_email, password)  # Log in to the SMTP server
            server.sendmail(sender_email, receiver_email, msg.as_string())  # Send the email
            server.quit()  # Disconnect from the SMTP server
            logging.info(f'Email sent to {receiver_email}')  # Log success message
            break  # Exit the retry loop if the email was sent successfully
        except Exception as e:
            logging.error(f'Failed to send email (attempt {attempt + 1}): {e}')  # Log error message
            time.sleep(5)  # Wait 5 seconds before retrying

# Function to take and compress a screenshot
def take_screenshot(step):
    filename = f'screenshot_{step}.png'  # Filename for the original screenshot
    compressed_filename = f'compressed_screenshot_{step}.png'  # Filename for the compressed screenshot
    pyautogui.screenshot(filename)  # Take a screenshot and save it to the file
    
    # Compress the screenshot
    img = Image.open(filename)  # Open the screenshot image
    img.save(compressed_filename, optimize=True, quality=50)  # Save the compressed image
    
    logging.info(f'Compressed screenshot taken: {compressed_filename}')  # Log success message
    return compressed_filename  # Return the filename of the compressed screenshot

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
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Generate a timestamp
            text = f"{action['text']}_{timestamp}"  # Append timestamp to the text
            interval = action.get('interval', 0.05)
            logging.info(f'Step {step}: Writing text {text}')
            pyautogui.write(text, interval=interval)
        return take_screenshot(step)
    except Exception as e:
        logging.error(f'Step {step}: Error executing action: {e}')
        return None

# Execute actions from the configuration
screenshots = []
for idx, action in enumerate(config['actions']):
    step = f'{idx + 1}'  # Step number for logging
    screenshot = execute_action(action, step)  # Execute the action and take a screenshot
    if screenshot:
        screenshots.append(screenshot)  # Add the screenshot to the list

logging.info('Script finished')  # Log that the script has finished executing

# Select the last 5 screenshots to be sent via email
last_5_screenshots = screenshots[-5:]

# Send an email with the last 5 compressed screenshots
send_email('Automation Script Completed', 'The automation script has completed successfully.', last_5_screenshots)
