import pandas as pd
from bs4 import BeautifulSoup
import os
from datetime import datetime

# Path to the folder containing HTML files
folder_path = '../html_messages/'

# List to store parsed data
all_data = []

# Loop through all HTML files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.html'):  # Check for HTML files
        file_path = os.path.join(folder_path, filename)

        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

        # Extracting messages from the HTML file
        messages = soup.find_all('div', class_='message default clearfix')

        for msg in messages:
            sender = msg.find('div', class_='from_name').text.strip() if msg.find('div', class_='from_name') else "Unknown"
            timestamp = msg.find('div', class_='pull_right date details')
            if timestamp:
                timestamp = timestamp['title']
                message_time = datetime.strptime(timestamp, '%d.%m.%Y %H:%M:%S UTC%z')
            else:
                message_time = None

            text = msg.find('div', class_='text').text.strip() if msg.find('div', class_='text') else ''
            sticker = msg.find('a', class_='sticker_wrap clearfix pull_left')
            sticker_link = sticker['href'] if sticker else None

            reactions = []
            reaction_elements = msg.find_all('div', class_='reaction')
            for reaction in reaction_elements:
                emoji = reaction.find('div', class_='emoji').text.strip() if reaction.find('div', class_='emoji') else None
                userpics = [user['title'] for user in reaction.find_all('div', class_='initials')]
                reactions.append({'emoji': emoji, 'users': userpics})

            if sender:
                all_data.append({
                    'Sender': sender,
                    'Timestamp': message_time,
                    'Message': text,
                    'Sticker': sticker_link,
                    'Reactions': reactions
                })

# Save DataFrame as CSV
df = pd.DataFrame(all_data)
df.to_csv('../data/all_messages_data.csv', index=False)
