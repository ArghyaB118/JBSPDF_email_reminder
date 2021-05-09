#switch on the 'less secure app access from google account settings'
#=TEXTJOIN(",",TRUE,K2,B2,J2,M2)
#maintain the datetime.date format the same as excel or vice versa
import smtplib, ssl
import datetime
import pandas as pd
import getpass
from termcolor import colored
today = datetime.date.today()
print "Operation done on", str(today)

import os

### First thing first: import the data from the google sheet
### Copy it in a csv named filename.csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def read_credentials():
	# Read the credentials from a text file: 'credentials.txt'
	# The file contains only two lines
	# Email ID
	# Password
	with open('credentials.txt', "r") as cred:
	    credentials = [line.rstrip() for line in cred]
	cred.close()
	sender_email = credentials[0]
	password = credentials[1]
	return sender_email, password

def input_credentials():
	try:
		sender_email = getpass.getpass(prompt="Enter email: ")
		password = getpass.getpass(prompt="Enter password: ")
	except Exception as error:
	    print('error', error)
	return sender_email, password


# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("JBSPDF Members for Slack 2010-2019").sheet1

# Extract and print all of the values
list_of_records = sheet.get_all_values()

with open('filename.csv', 'wb') as csvfile:
    csvfile.write(str('index' + ',' + 'day_assigned' + ',' + 'mail_id' + ',' + 'name' + ',' + 'admin' + ',' + 'first_mail_sent' + ',' + 'second_mail_sent' + ',' + 'third_mail_sent' + '\n'))
    for i in range(2,sheet.row_count + 1):
    	ind = str(str(i) + ',' + list_of_records[i-1][8]) + ',' + str(list_of_records[i-1][1]) + ',' + str(list_of_records[i-1][7]) + ',' + str(list_of_records[i-1][9]) + ',' + str(list_of_records[i-1][10]) + ',' + str(list_of_records[i-1][11]) + ',' + str(list_of_records[i-1][12]) + '\n'
    	csvfile.write(ind)
csvfile.close()

#getting the target dates for sending reminder
#dates may lie anywhere from 7 days to 30 days from now
target_dates_first = []
for i in range(9,31):
	target_dates_first.append(datetime.date.today() + datetime.timedelta(days=i))

target_dates_second = []
for i in range(3,9):
	target_dates_second.append(datetime.date.today() + datetime.timedelta(days=i))

target_dates_third = []
for i in range(1,3):
	target_dates_third.append(datetime.date.today() + datetime.timedelta(days=i))

#read the data file
data = pd.read_csv("filename.csv")

#sender_email, password = read_credentials()
sender_email, password = input_credentials()




#setting up the SMTP server 
smtp_server = "smtp.gmail.com"
port = 587  # For starttls

# Create a secure SSL context
context = ssl.create_default_context()

# Try to log in to server and send email
try:
	server = smtplib.SMTP(smtp_server,port)
	server.ehlo() # Can be omitted
	server.starttls() # Secure the connection
	server.ehlo() # Can be omitted
	server.login(sender_email, password)

	for ind in data.index:
		admin = str(data['admin'][ind])
		if admin == "Sudhakantha Girmohanta":
			admin_email = "sudhakantha5@gmail.com"
		elif admin == "Debarghya Sarkar":
			admin_email = "debarghyasarkar.ds@gmail.com"
		elif admin == "Sampurna Mukherjee":
			#admin = "Arghya Bhattacharya"
			#admin_email = "argbhattacha@cs.stonybrook.edu"
			admin_email = "sampurnamukherjeebiology@gmail.com" #For COVID
		elif admin == "Subhadeep Dasgupta":
			admin_email = "mastersubhadeep@gmail.com"
		elif admin == "Arghya Bhattacharya":
			admin_email = "jbspdf.ac@gmail.com"
		for target_date_first in target_dates_first:
			### first reminder setup
			if data['day_assigned'][ind] == str(target_date_first):
				if data['first_mail_sent'][ind] == 0:
					receiver_index = str(data['index'][ind])
					receiver_name = str(data['name'][ind])
					receiver_email = str(data['mail_id'][ind])
					receiver_emails = [data['mail_id'][ind]] + [admin_email]
					receiver_day = str(data['day_assigned'][ind])
					print "Mailing to: ", receiver_email, "for date:", receiver_day
					confirm = raw_input("Please confirm to send the first reminder (y/n): ")
					if confirm == "y":
						#compose the text
						message = """\
From: Arghya Bhattacharya
To: %s
CC: jbspdf.ac@gmail.com
Subject: JBSPDF invites your #thought_of_the_day on %s

Dear %s,

Hope this email finds you and your family well.

We would like to invite you to share your #thought_of_the_day in the #community channel of our Slack workspace on %s.

The #thought_of_the_day can be any interesting piece of science news, scientific concepts, science and society, and more than that communicated in a brief read to a broad scientific community.

We'll also send you a couple reminders closer to your posting date.

Looking forward to hearing your #thought_of_the_day from you soon!

Regards,
Arghya.
(On behalf of JBSPDF)

P.S.: Wondering what #thought_of_the_day can be like? Please check our webpage at https://sites.google.com/view/jbspdf/scholarly-activities/regular-communication/thought_of_the_day. 
For further queries, please slack me or reply here.

P.P.S.: 
(a) If you wish to acknowledge acceptance of this request, you may choose to do so by introducing yourself on the #greetings channel of jb-scholars.slack.com.
(b) If this date doesn't work for you, please let us know of an alternative better timeframe at https://forms.gle/1SB4xmi5Bm7gVNNf6.""" % (receiver_email, receiver_day, receiver_name, receiver_day)
							# TODO: Send email here
						server.sendmail(sender_email, receiver_emails, message)
						sheet.update_cell(receiver_index, 11, "TRUE")
		for target_date_second in target_dates_second:
			### second reminder setup
			if data['day_assigned'][ind] == str(target_date_second):
				if data['second_mail_sent'][ind] == 0:
					receiver_index = str(data['index'][ind])
					receiver_name = str(data['name'][ind])
					receiver_email = str(data['mail_id'][ind])
					receiver_emails = [data['mail_id'][ind]] + [admin_email]
					receiver_day = str(data['day_assigned'][ind])
					print "Mailing to: ", receiver_email, "for date:", receiver_day
					confirm = raw_input("Please confirm to send the second reminder (y/n): ")
					if confirm == "y":
						#compose the text
						message = """\
From: Arghya Bhattacharya
To: %s
CC: jbspdf.ac@gmail.com
Subject: Reminder for your #thought_of_the_day on %s

Dear %s,

This is a gentle reminder email that we'll expect your #thought_of_the_day in the #community channel of our Slack workspace on %s.

Just to reiterate, this can be a brief read for a broad scientific community on any "science communication" that you find interesting.

Please just include #thought_of_the_day in your post, so that everyone knows it's by invitation, and we can search and catalog them later if we wish.

We'll also send you another reminder a day or two prior to your posting date. Looking forward to hearing your #thought_of_the_day from you soon!

Regards,
Arghya.
(On behalf of JBSPDF)

P.S.: More questions on #thought_of_the_day? Please check our webpage at https://sites.google.com/view/jbspdf/scholarly-activities/regular-communication/thought_of_the_day. 
For further queries, please slack me or reply here.""" % (receiver_email, receiver_day, receiver_name, receiver_day)
							# TODO: Send email here
						server.sendmail(sender_email, receiver_emails, message)
						sheet.update_cell(receiver_index, 12, "TRUE")
		for target_date_third in target_dates_third:
			### third reminder setup
			if data['day_assigned'][ind] == str(target_date_third):
				if data['third_mail_sent'][ind] == 0:
					receiver_index = str(data['index'][ind])
					receiver_name = str(data['name'][ind])
					receiver_email = str(data['mail_id'][ind])
					#https://stackoverflow.com/questions/1546367/python-how-to-send-mail-with-to-cc-and-bcc
					receiver_emails = [data['mail_id'][ind]] + [admin_email]
					receiver_day = str(data['day_assigned'][ind])
					print "Mailing to: ", receiver_email, "for date:", receiver_day
					confirm = raw_input("Please confirm to send the third reminder (y/n): ")
					if confirm == "y":
						#compose the text
						message = """\
From: Arghya Bhattacharya
To: %s
CC: jbspdf.ac@gmail.com
Subject: Reminder for your #thought_of_the_day on %s

Dear %s,

This is another brief reminder email that we'll expect your #thought_of_the_day in the #community channel of our Slack workspace on %s.

Awaiting to hearing your #thought_of_the_day from you soon!

Regards,
Arghya.
(On behalf of JBSPDF)

P.S.: More questions on #thought_of_the_day? Please check our webpage at https://sites.google.com/view/jbspdf/scholarly-activities/regular-communication/thought_of_the_day. 
For further queries, please slack me or reply here.""" % (receiver_email, receiver_day, receiver_name, receiver_day)
							# TODO: Send email here
						server.sendmail(sender_email, receiver_emails, message)
						sheet.update_cell(receiver_index, 13, "TRUE")

	os.remove("filename.csv")
except Exception as e:
	# Print any error messages to stdout
	print(e)

finally:
	server.quit()