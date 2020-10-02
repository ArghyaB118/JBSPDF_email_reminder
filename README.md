# JBSPDF_email_reminder
This is a repository where I am uploading the code to automate sending email reminders for JBSPDF members. The code accesses a csv to know people assigned to me (one of the admins) and before 7 days it sends an automated reminder to post the thought of the day for the Slack forum of JBSPDF (jagadish Bose Scholars Professional Development Forum). The code uses SMTP protocol. Hence in order to use it, please switch to 'less secure app access' from google account settings.

##How to run?
```bash
pip install pandas
python send_email.py
```

