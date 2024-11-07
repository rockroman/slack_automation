import requests
from datetime import datetime
import re
import os

SLACK_API_TOKEN = os.environ['SLACK_API_TOKEN']

def calc_time(link):
    print("Received link inside calc_time:", link)
    channel_id = link.split("/")[4]
    message_ts_raw = link.split("/")[5][1:]  # Removing the 'p' prefix from timestamp
    message_ts = f"{message_ts_raw[:10]}.{message_ts_raw[10:]}"

    # Prepare headers for Slack API
    headers = {
     'Authorization': f'Bearer {SLACK_API_TOKEN}',
    'Content-Type': 'application/json'
    }

    # Use conversations.replies to get message details and reply count
    url = "https://slack.com/api/conversations.replies"
    payload = {
        "channel": channel_id,
        "ts": message_ts
    }

    response = requests.get(url, headers=headers, params=payload)
    data = response.json()

    if data.get("ok"):
        # Get the timestamp and user ID of the original message
        original_message = data["messages"][0]
        # print("original message =",original_message)
        original_user_id = original_message.get("user")
        timestamp = float(original_message["ts"])
        date_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        print ("conv time = ", date_time)
        message_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        message_time = datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
        bot_id = original_message.get("bot_id")
        passed_time = None

        # Check if the bot's message has "Thank you for requesting support"
        if bot_id and "Thank you for requesting support" in original_message.get("text", ""):
            # Extract user ID from the support message text
            match = re.search(r'<@([A-Z0-9]+)>', original_message["text"])
            if match:
                original_user_id = match.group(1)
        
        # Output original message details
        print("Original User ID:", original_user_id)
        print("Bot ID:", bot_id)
        print(f"Conversation date: {message_date}")
        print(f"Conversation time: {message_time}")
        print(f"Number of replies: {original_message.get('reply_count', 0)}")
        
        # Find the first valid reply
        first_reply_time = None
        for reply in data["messages"][1:]:  # Skip the first item, as it's the original message
            reply_user_id = reply.get("user")
            print("reply user Id = ",reply_user_id)
            reply_bot_id = reply.get("bot_id")
            
            # Check if reply is not from the original user or a bot
            if reply_user_id != original_user_id and reply_bot_id is None:
                reply_timestamp = float(reply["ts"])
                first_reply_time = datetime.fromtimestamp(reply_timestamp).strftime('%Y-%m-%d %H:%M:%S')
                break  # Stop after finding the first valid reply

        if first_reply_time:
            print("First valid reply time:", first_reply_time)
            
            quest_time =datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
            response_time = datetime.strptime(first_reply_time, '%Y-%m-%d %H:%M:%S') 
            time_passed  = response_time - quest_time
            # print(time_passed)
            hours = time_passed.days * 24 + time_passed.seconds // 3600
            # print("hours =", hours)
            mins = (time_passed.seconds % 3600) //60
            # print( "minutes ", mins)
            if hours != 0:
                passed_time = str(hours) +" hours and "+ str(mins)+ " minutes"
            else:
                passed_time = str(mins) + " minutes"
            print( "passed time = ",passed_time)
            return passed_time     
        else:
            
            print("No valid replies found.")
            return "N/A"
    else:
        print("Error:", data.get("error"))
        return

















