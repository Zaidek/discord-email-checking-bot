#IMPORT EMAIL MODULES
import email
import imaplib
import os


# Class used to get Gmail Emails
class Gmail():

    def __init__(self):
        self.username = None
        self.password = None
        self.imap_client = None

    def login(self, username, password):
        
        # Get details
        self.username = username
        self.password = password
        self.imap = imaplib.IMAP4_SSL(host = 'imap.gmail.com', port = 993)

        # Try connect to Gmail
        is_logged_in, details = self.imap_client.login(username, password)
        if not is_logged_in: print("Login Failed")
        else:
            print("Login Successful!")

    def inbox(self, readonly = True):
        self.imap_client.select('inbox')

    def get_unseen_mail(self):
        _, data = self.imap_client.search(None, 'UNSEEN')
        emails = extract_email_message(data)
        return emails
        
    def get_all_mail(self):
        _, data = self.imap.client.search(None, "ALL")
        emails = extract_email_message(data)
        return emails
        
    def extract_email_message(self, data):
        emails = []
        for email_number in data[0].split():
            _, email_data = self.imap_client.fetch(email_number, '(RFC822)')
            _, email_in_bytes = email_data[0]
            email_in_text = email.message_from_bytes(email_in_bytes)
            new_email = Email()
            new_email.get_mail(email_in_text)
            emails.append(new_email)
        return emails
    

    def main(self, username, password):
        self.login(username, password)
        self.inbox()
        self.get_unseen_mail()


# Class to store individual Emails
class Email():

    def __init__(self):
        self.sender = None
        self.receiver = None
        self.subject = None
        self.content = None
        self.date = None

    def get_mail(self, email):
        self.sender = email['from']
        self.receiver =  email['to']
        self.subject = email['subject']
        self.date = email['date']

        for section in email.walk():
            if section.get_content_type() == "text/plain":
                content = section.get_payload(decode = True)
                self.content = content.decode()
            
               
# Starter function 
if __name__ == '__main__':
    obj = Gmail()
    obj.main('zajdektestmail@gmail.com', 'testPASS123456')