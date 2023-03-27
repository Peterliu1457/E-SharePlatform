from google.cloud import storage
import json
from Google import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os.path

# 設定API參數
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'C:/Users/210241841/PycharmProjects/pythonProject/cloudfunction/gmailAPI/peterproject-364114-be614bbe8393.json'
GOOGLE_APPLICATION_CREDENTIALS="peterproject-364114-be614bbe8393.json"
CLIENT_SECRET_FILE = 'client_secret_878467896519-9fvu5068lqc4bpu61bidi0akf3clms99.apps.googleusercontent.com.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

# 建立API服務
service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

# 連接Storage bucket
client = storage.Client()
bucket = client.bucket('processedjson')

# 從bucket中取得JSON檔案
blob = bucket.blob('processed.txt')
json_str = blob.download_as_string()
#print(json_str)
encoding = 'utf-8'
json_str = str(json_str, encoding)
#print(json_str)
#json_str = "{'StudentName': 'Chan Tai Man', 'DateOfBirth': '11/07/2007', 'Age': '15', 'StudentID': '20712773', 'EmailAddress': 'peterliu202347@gmail.com', 'PhoneNumber': '97865201', 'HomeAddress': '30 Fortress Hill Road North Point HK', 'NameOSchool': 'Clementi Secondary School', 'SchoolAddress': 'Clementi Secondary School', 'NameOTeacher': 'Ms.Chan', 'PhoneOfTeacher': '97022556', 'EmailOfTeacher': 'teacher@gmail.com', 'NameOfParent': 'Chan Tai Man', 'ParentPhoneNumber': '95705632'}"
json_str = json_str.replace("'", '"')

# 解析JSON檔案，並抽取email
data = json.loads(json_str)
email = data['EmailAddress']

print("Email send to: " + email)

# 建立郵件內容
emailMsg = 'Apply Sucessful!\n申請成功！'
mimeMessage = MIMEMultipart()
mimeMessage['to'] = email
mimeMessage['subject'] = '申請成功！'
mimeMessage.attach(MIMEText(emailMsg, 'plain'))
raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

# 發送郵件
message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
print(message)

"""
def main():
    #Shows basic usage of the Gmail API.
    #Lists the user's Gmail labels.
    
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(CLIENT_SECRET_FILE):
        creds = Credentials.from_authorized_user_file(CLIENT_SECRET_FILE, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                GOOGLE_APPLICATION_CREDENTIALS, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(CLIENT_SECRET_FILE, 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])

if __name__ == '__main__':
    main()"""
