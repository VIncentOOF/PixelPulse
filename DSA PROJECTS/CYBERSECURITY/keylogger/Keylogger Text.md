# **Keylogger and Email Sender - Python Script**

This Python script records keystrokes, logs them to a file, and periodically sends the log file to a specified email address. The script handles special keys and formats the output for readability.

## **Features**

- **Keystroke Logging**:
  - Records all keystrokes with timestamps.
  - Handles special keys like space, enter, backspace, shift, etc.
  
- **Email Sending**:
  - Periodically sends the log file to a specified email address.
  - Configurable email credentials and SMTP server details.

- **Log Processing**:
  - Processes the log file to provide readable output.
  - Handles shift keys to capture uppercase letters correctly.

**Usage**:
Run keylogger.py on victims machine 
Run keylogger decoder.py in attackers machine