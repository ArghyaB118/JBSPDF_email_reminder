# JBSPDF_email_reminder
This is a repository where I am uploading the code to automate sending email reminders for JBSPDF members. The code accesses a .csv file to know people assigned to me (one of the admins) and within 7 days from today it sends an automated reminder to post the #thought_of_the_day for the Slack forum of JBSPDF (Jagadish Bose Scholars Professional Development Forum). 

## Protocol we use
The code uses SMTP protocol. Hence in order to use it, please switch to 'less secure app access' from google account settings.

## Data format in .csv
```text
day_assigned,mail_id,name,admin,mail_sent
2020-10-10,confidentrana118@gmail.com,Arghya Bhattacharya,Arghya,FALSE
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

Note: please type in your mail ID and password on line 1 and 2.
~Arghya.