#switch on the 'less secure app access from google account settings'
#=TEXTJOIN(",",TRUE,K2,B2,J2,M2)
#maintain the datetime.date format the same as excel or vice versa
import smtplib, ssl
import datetime
import pandas as pd
today = datetime.date.today()
print "Operation done on", str(today)

import os

### First thing first: import the data from the google sheet
### Copy it in a csv named filename.csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

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
for i in range(5,7):
	target_dates_first.append(datetime.date.today() + datetime.timedelta(days=i))

target_dates_second = []
for i in range(3,5):
	target_dates_second.append(datetime.date.today() + datetime.timedelta(days=i))

target_dates_third = []
for i in range(1,3):
	target_dates_third.append(datetime.date.today() + datetime.timedelta(days=i))

#read the data file
data = pd.read_csv("filename.csv")

#read the credentials from a text file
with open('credentials.txt', "r") as cred:
    credentials = [line.rstrip() for line in cred]

sender_email = credentials[0]
password = credentials[1]

cred.close()

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
			admin_email = "sampurnamukherjeebiology@gmail.com"
		elif admin == "Subhadeep Dasgupta":
			admin_email = "mastersubhadeep@gmail.com"
		elif admin == "Arghya Bhattacharya":
			admin_email = "iamarghya.1@gmail.com"
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
From: jbspdf.ac@gmail.com
To: %s
CC: %s
Subject: JBSPDF invites your #thought_of_the_day on %s

Dear %s,

Hope this email finds you and your family well.

You must have received an email from JBSPDF about the initiative that has been taken to encourage members, especially younger scholars like you to post the #thought_of_the_day.

We would like to invite you to share your #thought_of_the_day in the #community channel of our Slack workspace on %s.

And there's no boundary or guidelines for what this can be about - any "science communication" that you find interesting. This can include latest science news, important scientific concepts, some scientific proof, and more than that. The only "rule" is to include the phrase #thought_of_the_day in the post, so that everyone knows it's by invitation, and we can search and catalog them later if we wish. Some of our members have already posted their #thoughts_of_the_day which you may want to check out if you missed them earlier.

%s (cc-ed) is your primary point of contact, so if you want to discuss some specific topics about the forum including #thought_of_the_day, please feel free to do so with %s personally or anyone else in the forum. 

At this point, can you please confirm on the #messages_to_admins channel on Slack (ideally) or by replying to this email that you are accepting this invitation and are willing to post on that day? Please note that this date will be reserved for your #thought_of_the_day posting, and we'll await your post even if you miss to confirm now.

We'll also send you a couple reminders closer to your posting date.

Looking forward to hearing your #thought_of_the_day from you soon!

Regards,
Your Friends at JBSPDF""" % (receiver_email, admin_email, receiver_day, receiver_name, receiver_day, admin, admin)
							# TODO: Send email here
						server.sendmail(sender_email, receiver_email, message)
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
From: jbspdf.ac@gmail.com
To: %s
CC: %s
Subject: Reminder for your #thought_of_the_day on %s

Dear %s,

This is a gentle reminder email that we'll expect your #thought_of_the_day in the #community channel of our Slack workspace on %s.

Just to reiterate, there's no boundary or guidelines for what this can be about - any "science communication" that you find interesting. This can include latest science news, important scientific concepts, some scientific proof, and more than that. The only "rule" is to include the phrase #thought_of_the_day in the post, so that everyone knows it's by invitation, and we can search and catalog them later if we wish. Some of our members have already posted their #thoughts_of_the_day which you may want to check out if you missed them earlier.

We'll also send you another reminder a day or two prior to your posting date. Looking forward to hearing your #thought_of_the_day from you soon!

Regards,
Your Friends at JBSPDF""" % (receiver_email, admin_email, receiver_day, receiver_name, receiver_day)
							# TODO: Send email here
						server.sendmail(sender_email, receiver_email, message)
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
From: jbspdf.ac@gmail.com
To: %s
CC: %s
Subject: Reminder for your #thought_of_the_day on %s

Dear %s,

This is another brief reminder email that we'll expect your #thought_of_the_day in the #community channel of our Slack workspace on %s.

%s (cc-ed) is your primary point of contact, so if you want to discuss some specific topics about the forum including #thought_of_the_day, please feel free to do so with %s personally or anyone else in the forum. 

Awaiting to hearing your #thought_of_the_day from you soon!

Regards,
Your Friends at JBSPDF""" % (receiver_email, admin_email, receiver_day, receiver_name, receiver_day, admin, admin)
							# TODO: Send email here
						server.sendmail(sender_email, receiver_emails, message)
						sheet.update_cell(receiver_index, 13, "TRUE")

	os.remove("filename.csv")
except Exception as e:
	# Print any error messages to stdout
	print(e)

finally:
	server.quit()