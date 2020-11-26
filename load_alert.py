#!/usr/bin/env python

import subprocess
import smtplib
from email.mime.text import MIMEText
import socket

def email_alert(uptime, top):
    """Email alert"""
    body = uptime + '\n\n' + top + '\n'
    email_sender = "root@" + get_hostname()
    email_receiver = ''
    smtp_server = ''
    msg = MIMEText(body)
    msg['Subject'] = "Load Alert"
    msg['From'] = email_sender
    msg['To'] = email_receiver
    s = smtplib.SMTP(smtp_server)
    s.sendmail(email_sender, [email_receiver], msg.as_string())
    s.quit()

def get_hostname():
    """Get Local Hostname"""
    hostname = socket.getfqdn()
    return hostname

def main():

    u = subprocess.Popen(["uptime"], stdout=subprocess.PIPE)
    uptime, err = u.communicate()
    t = subprocess.Popen(["top", "-n", "1", "-b"], stdout=subprocess.PIPE)
    top, err = t.communicate()
    load = uptime.split('average:')[1].split(',')
    load_float = [ float(x) for x in load ]

    for i in load_float:
        if i > 1.5:
            email_alert(uptime, top)
            break

if __name__ == '__main__':
    main()