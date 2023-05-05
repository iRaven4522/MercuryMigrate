import imap_tools
import csv
import os
import logging
# import imaplib

# Configure logging
logging.basicConfig(filename=f"imported.log",
                    format='%(asctime)s %(levelname)s %(message)s',
                    filemode='a')
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# with open('Book1.csv') as csv_file:
#     csvreader = csv.reader(csv_file, delimiter=',')
#     header = []
#     header = next(csvreader) # skip header
#     for row in csvreader:
#         username = row[0]
#         password = row[1]
imapsrv = "mail.example.com"
sslcheck = False
emailfolder = "INBOX"
exportdir = 'conv/'

def processMbox(user, passwd):
    joineddir = os.path.join(exportdir, user)
    mbox = imap_tools.MailBoxUnencrypted(imapsrv, 143)
    mbox.login(user, passwd, initial_folder=emailfolder)
    log.info(f"signed on to {imapsrv} with {user}")
    print(f"signed on to {imapsrv} with {user}")
    for filename in os.listdir(joineddir):
        if filename.endswith(".eml"):
            joinedfile = os.path.join(joineddir, filename)
            with open(joinedfile, 'rb') as f:
                msg = imap_tools.MailMessage.from_bytes(f.read())  # *or use bytes instead MailMessage
                log.info(f'appending {filename} in {user}\'s mailbox')
                print(f'appending {filename} in {user}\'s mailbox')
                log.info(f'message details: {msg.subject}, date: {msg.date}, from {msg.from_}')
                mbox.append(msg, emailfolder, flag_set=[imap_tools.MailMessageFlags.SEEN], dt=msg.date)
        else:
            log.debug(f'{filename} is not an .eml file')
    mbox.logout() # log out of the current user when done


def dateTest(user):
    joineddir = os.path.join(exportdir, user)
    for filename in os.listdir(joineddir):
        if filename.endswith(".eml"):
            joinedfile = os.path.join(joineddir, filename)
            with open(joinedfile, 'rb') as f:
                log.debug(f'test was passed on {filename}, showing date:')
                msg = imap_tools.MailMessage.from_bytes(f.read())  # *or use bytes instead MailMessage
                print(f'date_str: {msg.date_str}')
                print(f'date: {msg.date}')
                exit() # don't do this for everything, just testing LOL

def addcomplete(user):
    with open ('users_complete.txt', 'a') as vlst:
        vlst.write(f"{user}\n")
        vlst.close()

def main():
    # --- questions
    imapsrv = input("Please enter the hostname or IP address of your IMAP server you want to connect to (defaults to mail.example.com): ")
    sslchecktemp = input("Does your IMAP server use SSL/TLS? (y/n)")
    sslchecktemp = sslchecktemp.lower.strip()
    if ("y" in sslchecktemp[0]):
        sslcheck = True
    # --- begin processing
    with open('Book1.csv') as csv_file:
        csvreader = csv.reader(csv_file, delimiter=',')
        header = []
        header = next(csvreader) # skip header
        for row in csvreader:
            username = row[0]
            password = row[1]
            # for names in uclts:
            #     if username == names:
            #         print(f'{username} \'s mailbox has already been imported into. not running for them.')
            #     else:
            print(f"Processing mailbox: {username}")
            log.info(f"Processing mailbox: {username}")
            processMbox(username, password)
            # dateTest(username)
            # usercomplete.append(username)
            # addcomplete(username)
        

main()