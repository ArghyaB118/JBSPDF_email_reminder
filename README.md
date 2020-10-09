# JBSPDF_email_reminder
This is a repository where I am uploading the code to automate sending email reminders for JBSPDF members. The code accesses a .csv file to which has **date to post,mail id, name, admin assigned, whether the reminder is already sent**. We filter out people assigned to us (each admins) and within 7 days from today we send an automated reminder **if the mail is not already sent** to post the **#thought_of_the_day** for the Slack forum of JBSPDF (Jagadish Bose Scholars Professional Development Forum). 

## Protocol we use
The code uses SMTP protocol. Hence in order to use it, please switch to 'less secure app access' from google account settings.

## Data format in .csv
```text
day_assigned,mail_id,name,admin,mail_sent
2020-10-10,someone@gmail.com,Firstname Surname,Arghya,FALSE
```

##Data Format in credentials
```text
Mail ID
Mail Password
First Name
```

## How to run?
```bash
pip install pandas DateTime smtplib ssl
python send_email.py
```

~Arghya.
