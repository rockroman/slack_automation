import gspread
from oauth2client.service_account import ServiceAccountCredentials
from refactored_slack import Conversations
import os
import time
import time
import datetime
from datetime import datetime
import json

from timestap_utils import load_timestamp,format_timestamp,save_timestamp

timestamp = load_timestamp()


# connect to Google Sheets
scope = ["https://spreadsheets.google.com/feeds", 
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]

# creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
# client = gspread.authorize(creds)
# Load Google credentials from environment variable
# google_creds_json = os.environ.get('GOOGLE_CREDENTIALS')
# if not google_creds_json:
#     raise ValueError("GOOGLE_CREDENTIALS environment variable is not set")
# Load Google credentials from credentials.json
with open('credentials.json') as f:
    creds_dict = json.load(f)

# Parse the JSON string into a dictionary
# creds_dict = json.loads(google_creds_json)

# Create credentials object
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

# Authorize the client
client = gspread.authorize(creds)

sheet = client.open("Roman Rakic_test").get_worksheet(2)



def find_first_empty_row():
    #  all values in the first column
    col_values = sheet.col_values(1)  
    print("first empty row ", len(col_values)+1)
    return len(col_values) + 1




slack_convos = Conversations(timestamp=timestamp, limit=6)
results = slack_convos.fetch_conversations_after_timestamp(timestamp)

# F first empty row
first_empty_row = find_first_empty_row()

def convert_date_format(date_str):
    print("date string passed to conv format date func = ",date_str)
    date_formats = ['%d/%m/%Y', '%Y-%m-%d', '%m/%d/%Y']
    for fmt in date_formats:
        try:
            date_obj = datetime.strptime(date_str, fmt)
            print("date object returned from convert date funct",date_obj.strftime('%d/%m/%Y'))
            return date_obj.strftime('%d/%m/%Y')
        except ValueError:
            continue
    return date_str 

# Updating the sheet
for i, result in enumerate(results):
    row = first_empty_row + i
    # date = result['date']
    date = convert_date_format(result['date'])
    print("data to be inserted ", date)
    link = result['link']
    first_response_time = result['first_response_time']
    
    # Update Date column  A
    sheet.update_cell(row, 1, date)
    
    # Update Time to first response  column E
    sheet.update_cell(row, 5, first_response_time)
    
    # Update Link  column F
    sheet.update_cell(row, 6, link)
    
if slack_convos.latest_timestamp > timestamp:
    save_timestamp(slack_convos.latest_timestamp)
    print(f"New ending timestamp: {format_timestamp(slack_convos.latest_timestamp)}")
else:
    print("No new messages, timestamp not updated.")

print(f"Final timestamp: {format_timestamp(load_timestamp())}")

print(f"Updated {len(results)} rows in the sheet.")