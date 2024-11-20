import gspread
from oauth2client.service_account import ServiceAccountCredentials
from extract_from_link import calc_time
import time
import json

# Authenticate and connect to Google Sheets
scope = ["https://spreadsheets.google.com/feeds", 
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]

with open('credentials.json') as f:
    creds_dict = json.load(f)


# Create credentials object
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

# Authorize the client
client = gspread.authorize(creds)

sheet = client.open("Roman Rakic_test").get_worksheet(3)



def update_time_to_first_response(link):
    # Fetch all rows as a list of lists
    all_rows = sheet.get_all_values()
    new_time = calc_time(link)
    # loop through each row, skipping the header row (index 0)
    for i, row in enumerate(all_rows[1:], start=2):  # Start at 2 to match the correct row in Google Sheets
        if row[5].strip() == link.strip():  # Index 5 is the "Link" column
            # Update "Time to first response" column (index 4) for the matching row
            sheet.update_cell(i, 5, new_time)  # Column index 5 is "Time to first response"
            print(f"Updated row {i} with new time: {new_time}")
            return new_time != 'N/A'
    print("Link not found.")
    return False
    


# slack_links = [
        
# ]

# for valid_link in slack_links:
#     timing = calc_time(valid_link)
#     time.sleep(1)
#     update_time_to_first_response(valid_link,timing)