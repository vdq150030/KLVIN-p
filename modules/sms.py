""" Separate module for sms service """

# Send an HTML email with an embedded image and a plain text message for
# email clients that don't want to display the HTML.
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

import smtplib
import time
import json

class SMS(object):

    sms = None # SMTP object
    username=""
    password=""

    # the email objects
    replyto="" # where a reply to will go
    sendto=[] # list to send to

    datafile = "./info.json"
    data = None 

    def __init__(self, recipients = ""):

        print ('Initializing SMS service module.')
        #TODO: Test login - log out from the account - maybe event send a test message
        #TODO: add repcipents 
        try:
            # Test login SMS service
            #self.__sms_login(self.username, self.password)
            # logout
            #time.sleep(2000)
            #print (self.sms.quit())

            #get login data from a file
            with open(self.datafile) as fp:
                self.data = json.load(fp)

            self.username= self.data["user"]["username"]
            self.password= self.data["user"]["password"]

            # the email objects
            self.replyto= self.username # where a reply to will go
            self.sendto= self.data["user"]["recipients"] # list to send to

            # append list of recipients
            if (recipients): 
                self.sendto.extend(recipients)
            pass

        except Exception as e:    
            data = {}
            print ("Failed to initalize SMS Service Module: {}".format(e))
            raise e

    def show_recipients(self):
        return self.sendto

    def __sms_login(self, user, password):
        """ Login SMS server with supplied username and password """
        # start talking to the SMTP server for Gmail
        self.sms = smtplib.SMTP('smtp.gmail.com', 587)
        self.sms.starttls()
        self.sms.ehlo()
        # now login as my gmail user
        self.sms.login(user,password)

    def __wrap_message(self, msgRoot: MIMEMultipart, text = "#selfies.", url = "./resources/pi.jpg") -> MIMEMultipart:
        """ wrap contents, images, etc and return a MIMEMultipart object """
        # Encapsulate the plain and HTML versions of the message body in an
        # 'alternative' part, so message agents can decide which they want to display.
        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)
        
        # attach string content 
        msgText = MIMEText(text)
        msgAlternative.attach(msgText)
        
        # We reference the image in the IMG SRC attribute by the ID we give it below
        msgText = MIMEText('<b>Some <i>HTML</i> text</b> and an image.<br><img src="cid:image1"><br>Nifty!', 'html')
        msgAlternative.attach(msgText)
        
        # This example assumes the image is in the current directory
        fp = open( url, 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        
        # Define the image's ID as referenced above
        msgImage.add_header('Content-ID', '<image1>')
        msgRoot.attach(msgImage)

        return msgRoot

    def send_sms_image(self, text = '#selfies.', url = './resources/pi.jpg', subject = 'Pi977'):

        print ("sending sms")
        self.__sms_login(self.username,self.password)

        # Create the root message and fill in the from, to, and subject headers
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = 'Pi977'
        msgRoot['From'] = self.replyto
        if (len(self.sendto) == 1):
            msgRoot['To'] = self.sendto[0]
        else:
            msgRoot['To'] = self.sendto
        msgRoot.preamble = 'This is a multi-part message in MIME format.'

        msgRoot = self.__wrap_message(msgRoot,text,url)

        if (len(self.sendto) == 1):
            self.sms.sendmail(self.replyto, self.sendto[0], msgRoot.as_string())
        else:
            self.sms.sendmail(self.replyto, self.sendto, msgRoot.as_string()) 

        # logout
        rslt=self.sms.quit()
        # print the result
        print('Sendmail result=' + str(rslt[1]))

        pass




