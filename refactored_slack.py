import time
import datetime
from datetime import datetime
import requests
from extract_from_link import calc_time

import os

SLACK_API_TOKEN = os.environ['SLACK_API_TOKEN']

# -----------------------------------------------------------------------------------------------------
# set the timestamp to search after (this timestamp should be updated after
# script execution is finished)




# grab all conversations after the timestamp

class Conversations:
    def __init__(self,timestamp:int,limit:int) -> None:
        self.timestamp = timestamp
        self.limit = limit
        self.issues_data = {}
        self.latest_timestamp = 000000000.0
        self.total_messages = 0


    def fetch_conversations_after_timestamp(self, timestamp) -> list:
        data = self.get_conversations(timestamp)
        if data.get("ok"):
            self.process_conversations(data.get("messages", []), timestamp)
        
        results = []
        for issue_id, issue_data in reversed(self.issues_data.items()):
            if issue_id.startswith("issue_"):
                issue_date, issue_time = self._format_timestamp(issue_data['issue_timestamp'])
                first_response_time = calc_time(issue_data['first_message_link'])
                results.append({
                    "date": f"{issue_date}",
                    "time": f"{issue_time}",
                    "link": issue_data['first_message_link'],
                    "first_response_time": first_response_time
                })
                # Updating the latest timestamp
                # self.latest_timestamp = max(self.latest_timestamp, issue_data['issue_timestamp'])

    # Print the latest and starting  timestamp in human-readable format
        latest_date, latest_time = self._format_timestamp(self.latest_timestamp)
        start_date,start_time = self._format_timestamp(self.timestamp)
        print(f"start timestamp : {start_date} {start_time}")
        print(f"Latest timestamp: {latest_date} {latest_time}")
        print("Number of issues:", len(results))
        print(f"total messages processed: {self.total_messages}")
        return results
        
        
    # getting all conversations 
    def get_conversations(self,timestamp):
        url = "https://slack.com/api/conversations.history"
        headers = {
             'Authorization': f'Bearer {SLACK_API_TOKEN}',
            'Content-Type': 'application/json'
        }
        payload = {
            "channel": "C02NH8VL28G",
            "limit": self.limit,
            "oldest": str(timestamp)
        }
        response = requests.get(url, headers=headers, params=payload)
        return response.json()
    
    
    # processing the conversations 
    def process_conversations(self, messages, timestamp):
        # Add bot IDs to filter out
        excluded_bot_ids = [
            "B065JRCUCQK",  
            "B065C9GPXQE",
            "B065C9GPL3Y",
            "B065G0YQMHT",
            "B065MC65TPE",
            "B065JREMKEX",
            
        ]
        
        specific_bot_id = "B065JRDU43V"
        
        first_message = None

        for message in messages:
            self.total_messages +=1
            message_ts = float(message["ts"])
            bot_id = message.get("bot_id")
            
            self.latest_timestamp = max(self.latest_timestamp,message_ts)
            
            # Check if the bot ID is in the excluded bot IDs
            if bot_id in excluded_bot_ids:
                print(f"Excluded Bot ID: '{bot_id}'")
                continue
            
            if bot_id == specific_bot_id:
                first_message = self.process_bot_message(first_message, message, message_ts)
            else:
                self.process_normal_message(message, message_ts)
    
    
    def process_bot_message(self, first_message, message, message_ts):
        if not first_message:
        
            first_message = self.create_message_data(message, message_ts)
            print("First message:", first_message)
            return first_message
        else:
            second_message = self.create_message_data(message, message_ts)
            issue_id = f"issue_{int(message_ts)}"
            self.issues_data[issue_id] = {
                "issue_timestamp": first_message['timestamp'],
                "issue_text": first_message['text'],
                "first_message_link": first_message['link'],
                "response_tracking_start": second_message['timestamp'],
                "second_message_link": second_message['link'],
                "relpy_count": first_message['reply_count']
            }
            print("Second message:", second_message)
            return None
            
    
    
    def process_normal_message(self,message,message_ts):
        message_id = f"message_{int(message_ts)}"
        normal_message = self.create_message_data(message, message_ts)
        self.issues_data[message_id] = {
            "message_timestamp": normal_message['timestamp'],
            "message_text": normal_message["text"],
            "message_link": normal_message["link"],
            "reply_count": message.get("reply_count", 0)
        }
        print("Normal message date:", self._format_timestamp(normal_message['timestamp']))
    
    def create_message_data(self, message, message_ts) -> dict:
        app_redirect_link = f"https://slack.com/app_redirect?channel=C02NH8VL28G&message_ts={message_ts}"
        archives_link = self.convert_link_format(app_redirect_link)
        return {
            "timestamp": message_ts,
            "text": message.get("text", "")[:30],
            "link": archives_link,
            "reply_count": message.get("reply_count", 0)
        }

        
    def _format_timestamp(self, timestamp) -> str:
        # date_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        # time_str = datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
        # date_str = datetime.fromtimestamp(timestamp).strftime('%m/%d/%Y')
        # time_str = datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
        date_str = datetime.fromtimestamp(timestamp).strftime('%d/%m/%Y')
        time_str = datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
        print(f"Formatted date: {date_str}, time: {time_str}")
        return date_str, time_str
    

    def convert_link_format(self, app_redirect_link):
        parts = app_redirect_link.split('?')[1].split('&')
        channel = next(p.split('=')[1] for p in parts if p.startswith('channel='))
        ts = next(p.split('=')[1] for p in parts if p.startswith('message_ts='))
        ts_parts = ts.split('.')
        timestamp = f"{ts_parts[0]}{ts_parts[1].zfill(6)}"
        return f"https://code-institute-room.slack.com/archives/{channel}/p{timestamp}"

    def calculate_first_response_time(self, issue_timestamp, response_timestamp):
        return  issue_timestamp -response_timestamp
        
            
    
    
    














































