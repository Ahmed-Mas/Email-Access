'''
Created on Feb 8, 2018

@author: ahmed
'''

import smtplib, pyzmail, imaplib, imapclient

class emailBot:
    def __init__(self, userName, pswd):
        self.authAccounts = []  # put authorized accounts
        self.userName = userName
        self.pswd = pswd

    def __loginToSMTP(self):
        try:
            self.server = smtplib.SMTP("smtp.gmail.com", 587)
            self.server.ehlo()
            self.server.starttls()

            self.server.login(self.userName, self.pswd)
            print("SMTP login successful..")
        except:
            print("There was an error connecting to smtp..")

    def __loginIMAP(self):
        try:
            self.imapObj = imapclient.IMAPClient("imap.gmail.com", ssl=True)
            self.imapObj.login(self.userName, self.pswd)
            print("IMAP login successful..")
        except:
            print("There was an error connecting to IMAP..")

    def __sendMail(self, toEmail, subject, body):
        self.__loginToSMTP()
        msg = "\r\n".join([
        "From: %s" % (self.userName),
        "To: %s" % (toEmail),
        "Subject: %s" % (subject),
        "",
        "%s" % (body)
        ])

        try:
            self.server.sendmail(self.userName, toEmail, msg)
            print("Email sent..")
        except:
            print("An error occured sending email..")

    def checkUnread(self):
        imaplib._MAXLINE = 10000000

        self.__loginIMAP()
        self.imapObj.select_folder("INBOX", readonly=False)
        self.UIDs = self.imapObj.search("UNSEEN")
        if not self.UIDs:
            print("Nothing to send..")
            self.imapObj.logout()
            print("IMAP connection closed..")
        else:
            while self.UIDs:
                self.rawMSG = self.imapObj.fetch([self.UIDs[0]], ["BODY[]"])
                self.message = pyzmail.PyzMessage.factory(self.rawMSG[self.UIDs[0]][b"BODY[]"])
                self.fromAdd = self.message.get_address("from")[1]

                if self.fromAdd not in self.authAccounts:
                    self.__sendMail(self.fromAdd, "Unauthorized Access", "Go away please.")
                    self.UIDs.pop()
                else:
                    self.__replyEmail()
                    self.UIDs.pop(0)
            self.server.quit()
            print("SMTP connection closed..")
            self.imapObj.logout()
            print("IMAP connection closed..")

    def __replyEmail(self):
        self.subject = self.message.get_subject()

        # Below is the cases, requests should be made in subject lines
        # Whats replied can be taken from any source (excel, text, in-file info ect..)
        # Can also be used to launch system apps, start other programs, all from email

        if self.subject == "emails":
            self.__sendMail(self.fromAdd, "Your request", "emailsTest")
        elif self.subject == "accounts":
            self.__sendMail(self.fromAdd, "Your request", "accountsTest")
        else:
            self.__sendMail(self.fromAdd, "Error", "Could not understand the request")
