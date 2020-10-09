#switch on the 'less secure app access from google account settings'
#=TEXTJOIN(",",TRUE,K2,B2,J2,M2)
#maintain the datetime.date format the same as excel or vice versa
import smtplib, ssl
import datetime
import pandas as pd
today = datetime.date.today()
print "Operation done on", str(today)

#getting the target dates for sending reminder
#dates may lie anywhere within a week from now
target_dates = []
for i in range(1,8):
	target_dates.append(datetime.date.today() + datetime.timedelta(days=i))

#read the data file
data = pd.read_csv("filename.csv")

#read the credentials from a text file
with open('credentials.txt', "r") as cred:
    credentials = [line.rstrip() for line in cred]

sender_email = credentials[0]
password = credentials[1]
admin = credentials[2]

print sender_email, password, admin
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
		for target_date in target_dates:
			if data['day_assigned'][ind] == str(target_date):
				if data['admin'][ind] == admin:
					if data['mail_sent'][ind] == 0:
						receiver_name = str(data['name'][ind])
						receiver_email = str(data['mail_id'][ind])
						receiver_day = str(data['day_assigned'][ind])
						print "Mailing to: ", receiver_email, "for date:", receiver_day
						confirm = raw_input("Please confirm by saying 'yes' or 'no: ")
						if confirm == "yes":
							#compose the text
							message = """\
Subject: Invitation to post #thought_of_the_day on JBSPDF Slack forum

Hi %s!

You probably have received an email from JBSPDF about the initiative that has been taken to encourage members, especially younger scholars like you to post the #thought_of_the_day. As was mentioned in the email, it can be any "science communication" that you find interesting. This can include latest science news, important scientific concepts, some scientific proof, and more than that. We would like to invite you to post your #thought_of_the_day on %s.

Best,
%s.""" % (receiver_name, receiver_day, admin)
							# TODO: Send email here
							server.sendmail(sender_email, receiver_email, message)
except Exception as e:
	# Print any error messages to stdout
	print(e)

finally:
	server.quit() 