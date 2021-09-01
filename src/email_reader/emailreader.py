#IMPORT EMAIL MODULES
import email
import imaplib
import os


# Class used to get Gmail Emails
class Gmail():

    def __init__(self):
        self.username = None
        self.password = None
        self.imap = None

    def login(self, username, password):
        self.username = username
        self.password = password
        self.imap = imaplib.IMAP4_SSL('gmail.com', port = 999)

        is_logged_in, details = self.imap.login(username, password)


# Class to store individual Emails
class Email():

    def __init__(self):
        self.sender = None
        self.subject = None
        self.content = None

