sender_email = "your mail ID"
password = "your password for mail"
#switch on the 'less secure app access from google account settings'
#=TEXTJOIN(",",TRUE,K2,B2,J2)
#maintain the datetime.date format the same as excel or vice versa
import smtplib, ssl
import datetime
import pandas as pd
today = datetime.date.today() + datetime.timedelta(days=7)
print(today)
data = pd.read_csv("filename.csv")
print(data.size)

for ind in data.index:
	if data['day_assigned'][ind] == str(today):
		if data['admin'][ind] == "Arghya":
			receiver_name = str(data['name'][ind])
			receiver_email = str(data['mail_id'][ind])
			receiver_day = str(data['day_assigned'][ind])
			print(data['mail_id'][ind], data['day_assigned'][ind])

smtp_server = "smtp.gmail.com"
port = 587  # For starttls

message = """\
Subject: Invitation to post #thought_of_the_day on JBSPDF Slack forum

Hi %s!

You probably have received an email from jbspdf about the initiative that has been taken to encourage members, especially younger scholars like you to post the #thought_of_the_day. As was mentioned in the email, it can be any "science communication" that you find interesting. This can include latest science news, important scientific concepts, some scientific proof, and more than that. We would like to invite you to post your #thought_of_the_day on %s.

Best,
Arghya.""" % (receiver_name, receiver_day)


#message = """\ 
#Subject: Invitation to post #thought_of_the_day on JBSPDF Slack forum

#Hi %s, This is just a gentle reminder to post the thought of the day on %s""" % (receiver_name, receiver_day)

# Create a secure SSL context
context = ssl.create_default_context()

# Try to log in to server and send email
try:
	server = smtplib.SMTP(smtp_server,port)
	server.ehlo() # Can be omitted
	server.starttls() # Secure the connection
	server.ehlo() # Can be omitted
	server.login(sender_email, password)
	server.sendmail(sender_email, receiver_email, message)
	# TODO: Send email here
except Exception as e:
	# Print any error messages to stdout
	print(e)
finally:
	server.quit() 