import smtplib

def notify(server, port, login, password, sender_name, sender_email,
        recipients, subject, message):
    """Send email to notify recipients

    :Parameters:
      - `server`: smtp server hostname
      - `port`: smtp server port
      - `login`: smtp server login
      - `password`: smtp server password
      - `sender_name`: sender name, e.g. 'Flights Notifier'
      - `sender_email`: email sender email
      - `recipients`: comma separated email addresses
      - `subject`: email subject
      - `message`: email message
    """
    server = smtplib.SMTP(server, port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(login, password)
    for email in recipients.split(','):
        server.sendmail(sender_email, email,
                'From: %s <%s>\n'
                'To: %s\n'
                'Subject: %s\n\n%s' % (
                    sender_name, sender_email, email, subject, message))
    server.close()
