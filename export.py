#!/usr/bin/env python
#
# Very simple Python script to dump all emails in an IMAP folder to files.  
# This code is released into the public domain.
#
# RKI Nov 2013 -- Original script for Python 2: https://gist.github.com/robulouski/7442321
#  ^ All credit goes to the above GitHub user for the original script that has been modified.
# Converted to work with Python 3.x by iRaven4522.
#
import sys
import imaplib
import getpass
import csv
import os
import logging
import time

# Configure logging
logging.basicConfig(filename=f"exported.log",
                    format='%(asctime)s %(levelname)s %(message)s',
                    filemode='a')
log = logging.getLogger()
log.setLevel(logging.DEBUG)

imapsrv = 'mail.example.com'
# with open('Book1.csv') as csv_file:
#     csvreader = csv.reader(csv_file, delimiter=',')
#     header = []
#     header = next(csvreader) # skip header
#     for row in csvreader:
#         username = row[0]
#         password = row[1]
EMAIL_FOLDER = "Inbox"
if not os.path.exists('conv/'):
    os.makedirs('conv/')
OUTPUT_DIRECTORY = 'conv/'

# PASSWORD = getpass.getpass()


def process_mailbox(M, name):
    # Dump all emails in the folder to files in output directory.

    if not os.path.exists(OUTPUT_DIRECTORY + name):
        os.makedirs(OUTPUT_DIRECTORY + name)

    outputdir = OUTPUT_DIRECTORY + name

    rv, data = M.search(None, "ALL")
    if rv != 'OK':
        print("No messages found!")
        return

    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print(f"ERROR getting message {num}")
            log.error(f"ERROR getting message {num}")
            return
        print(f"Writing message {num}")
        log.info(f"Writing message {num}")
        f = open(f'%s/%s.eml' %(outputdir, num), 'wb')
        f.write(data[0][1])
        f.close()

def main():
    imapsrv = input("Please enter the hostname or IP address of your IMAP server you want to connect to (defaults to mail.example.com): ")
    csvfilein = input("Please enter the name of the .csv file to be parsed through for user info to logon to the IMAP server. (default: Book1.csv): ")
    with open(csvfilein) as csv_file:
        csvreader = csv.reader(csv_file, delimiter=',')
        header = []
        header = next(csvreader) # skip header
        for row in csvreader:
            M = imaplib.IMAP4(imapsrv)
            username = row[0]
            password = row[1]
            log.info(f'Logging onto server with {username}')
            print(f'Logging onto server with {username}')
            M.login(username, password)
            rv, data = M.select(EMAIL_FOLDER)
            if rv == 'OK':
                print(f"Processing mailbox: {EMAIL_FOLDER}")
                log.info(f"Processing mailbox: {EMAIL_FOLDER}")
                process_mailbox(M, username)
                M.close()
            else:
                print(f"ERROR: Unable to open mailbox {rv}")
                log.info(f"ERROR: Unable to open mailbox {rv}")
            M.logout()
            log.info(f"{username} {EMAIL_FOLDER} was exported")
            print(f"{username} {EMAIL_FOLDER} was exported")

main()