# JBSPDF_email_reminder
This is a repository where I am uploading the code to automate sending email reminders for JBSPDF members for posting the *thought_of_the_day*. The code accesses a google sheet which is a replica of the automated google sheet of *member responses* with some additional colums as follows: 
1. first name + last name
2. *thought_of_the_day* posting date assigned 
3. Sub-group by Admin assigned
4. First Reminder (Invitation)
5. Second Reminder (one week ago)
6. Third Reminder (one or two days prior)

The last three columns are booleans and automatically populated as the code is done sending mails. **date to post,mail id, name, admin assigned, whether the reminder is already sent**. We filter out people assigned to us (each admins). We send an invitation *a month prior* to the posting date, the second reminder *7 days prior* to the posting date and a third reminder *1-2 days prior* to the posting date. We keep the booleans and populate them automatically so that the same mail is not sent multiple times. We also **cc the concerned admin** in each such mails.


## Protocol we use
The code uses SMTP protocol. Hence in order to use it, please switch to 'less secure app access' from google account settings.

## Data format in .csv
We use a library named gspread and use the standard Google Drive API to access the google sheet directly. We Oauth using a .json file that is omitted from this repo. To study more on this, read [here](https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html)

##Data Format in credentials
We keep a text file and put our mail credentials there. The format is as follows:
```text
Mail ID
Mail Password
```

## How to run?
```bash
pip install pandas DateTime smtplib ssl
python send_email.py
```

~Arghya.
