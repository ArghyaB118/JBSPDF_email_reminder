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
#sender_email = input("Type your own email ID and press enter: ")
sender_email = "write your mail ID here"
#password = input("Type your password and press enter: ")
password = "write your password here"

#receiver_email = "confidentrana118@gmail.com"
#message = "Subject: Hi there Hi " + receiver_name + ", Please post the thought of the day on " + receiver_day
message = """\
Subject: thought of the day for JBSPDF Slack forum

Hi %s, This is just a gentle reminder to post the thought of the day on %s""" % (receiver_name, receiver_day)

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