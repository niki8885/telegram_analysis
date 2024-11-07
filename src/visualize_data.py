import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os
from PIL import Image
import ast
import numpy as np
from collections import Counter
import matplotlib.font_manager as fm

# Set font for emoji support; fallback to 'DejaVu Sans' if NotoColorEmoji is not available
emoji_font_path = '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'  # Update path for your OS
if os.path.exists(emoji_font_path):
    plt.rcParams['font.family'] = fm.FontProperties(fname=emoji_font_path).get_name()
else:
    plt.rcParams['font.family'] = 'DejaVu Sans'

# Load the CSV data
df = pd.read_csv('../data/all_messages_data.csv')
df['Message'] = df['Message'].fillna('')  # Fill missing messages with an empty string
df['Message Length'] = df['Message'].apply(len)  # Calculate message length
df['Timestamp'] = pd.to_datetime(df['Timestamp'])  # Ensure the 'Timestamp' column is in datetime format

# Function to plot a histogram of message lengths (clipped at a specified value)
def histogram_message_len_clipped(data, clip_value=500):
    clipped_data = data[data['Message Length'] <= clip_value]
    plt.figure(figsize=(10, 6))
    sns.histplot(clipped_data['Message Length'], kde=True, bins=30, color='blue')
    plt.title(f'Distribution of Message Lengths (Clipped at {clip_value} characters)', fontsize=16)
    plt.xlabel('Message Length', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.tight_layout()
    plt.show()

# Function to plot a histogram of message lengths using a logarithmic scale
def histogram_message_len_log(data):
    plt.figure(figsize=(10, 6))
    sns.histplot(data['Message Length'], kde=True, bins=30, color='blue')
    plt.xscale('log')
    plt.title('Distribution of Message Lengths (Log Scale)', fontsize=16)
    plt.xlabel('Message Length (Log Scale)', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.tight_layout()
    plt.show()

# Function to generate a word cloud for all users or a specific user
def word_cloud(data, user=None):
    all_text = ' '.join(data[data['Sender'] == user]['Message']) if user else ' '.join(data['Message'])
    filtered_text = ' '.join([word for word in all_text.split() if len(word) > 3])
    wordcloud = WordCloud(width=1600, height=800, background_color='white').generate(filtered_text)
    plt.figure(figsize=(20, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(f'Word Cloud for {"All Users" if not user else user}', fontsize=20)
    plt.axis('off')
    plt.show()

# Function to plot a bar chart showing the number of messages per sender
def bar_message_per_sender(data):
    message_counts = data['Sender'].value_counts()
    plt.figure(figsize=(20, 10))
    sns.barplot(x=message_counts.index, y=message_counts.values, palette='viridis', hue=None, legend=False)
    plt.title('Number of Messages Sent by Each Sender', fontsize=20)
    plt.xlabel('Sender', fontsize=16)
    plt.ylabel('Number of Messages', fontsize=16)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.tight_layout()
    plt.show()

# Ensure the 'Sticker' column exists; exit if not found
if 'Sticker' not in df.columns:
    print("Column 'Sticker' not found in data.")
    exit()

# Count the usage of each sticker
sticker_usage = df['Sticker'].dropna().value_counts()

# Create a DataFrame to store sticker usage data
sticker_df = pd.DataFrame({
    'Sticker': sticker_usage.index,
    'Count': sticker_usage.values
})

# Save the sticker usage data to a CSV file
output_file = '../data/popular_stickers.csv'
sticker_df.to_csv(output_file, index=False)
print(f"Sticker usage data saved to {output_file}")

# Function to visualize the top 10 stickers
def visualize_top_stickers(stickers_csv, stickers_path):
    if not os.path.exists(stickers_csv):
        print(f"File not found: {stickers_csv}")
        return

    stickers_df = pd.read_csv(stickers_csv)
    top_stickers = stickers_df.head(10)

    fig, axes = plt.subplots(1, len(top_stickers), figsize=(20, 5))
    fig.suptitle('Top 10 Stickers', fontsize=16)

    for i, (sticker, count) in enumerate(zip(top_stickers['Sticker'], top_stickers['Count'])):
        sticker_path = os.path.join(stickers_path, sticker)
        if os.path.exists(sticker_path):
            img = Image.open(sticker_path)
            axes[i].imshow(img)
        else:
            axes[i].text(0.5, 0.5, 'No Image', ha='center', va='center', fontsize=12)
        axes[i].set_title(f"#{i + 1}\nUsed: {count}", fontsize=12)
        axes[i].axis('off')

    plt.tight_layout()
    plt.show()

# Function to generate a pie chart for message reactions
def pie_chart_messages_per_reaction(data):
    data['Reaction Count'] = data['Reactions'].apply(
        lambda x: sum(len(ast.literal_eval(x)) for r in ast.literal_eval(x)) if pd.notna(x) else 0)
    categories = pd.cut(data['Reaction Count'], bins=[-1, 0, 1, 5, 10, float('inf')],
                        labels=['0', '1', '1-5', '5-10', '>10'])
    reaction_counts = categories.value_counts().sort_index()
    plt.figure(figsize=(8, 8))
    plt.pie(reaction_counts, labels=None, autopct='%1.1f%%', startangle=140,
            colors=sns.color_palette('pastel'))
    plt.title('Messages per Reaction Distribution')
    plt.legend(reaction_counts.index, title="Reaction Ranges", loc="upper right")
    plt.tight_layout()
    plt.show()

# Function to generate a heatmap of average response time by day and hour
def heatmap_response_time(data):
    data['Hour'] = data['Timestamp'].dt.hour
    data['Day'] = data['Timestamp'].dt.day_name()
    data['Response Time'] = data['Timestamp'].diff().dt.total_seconds().div(60).fillna(0)
    avg_response = data.groupby(['Day', 'Hour'])['Response Time'].mean().unstack()
    plt.figure(figsize=(12, 8))
    sns.heatmap(avg_response, cmap='coolwarm', annot=True, fmt='.1f',
                cbar_kws={'label': 'Avg Response Time (min)'}, annot_kws={"size": 8})
    plt.title('Average Response Time Heatmap', fontsize=16)
    plt.xlabel('Hour of Day', fontsize=14)
    plt.ylabel('Day of Week', fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.show()

# Function to plot the number of inactive days for each user
def histogram_inactive_days(data):
    data['Date'] = data['Timestamp'].dt.date
    active_days = data.groupby('Sender')['Date'].nunique()
    total_days = (data['Date'].max() - data['Date'].min()).days + 1
    inactive_days = total_days - active_days
    plt.figure(figsize=(20, 15))
    sns.barplot(x=inactive_days.index, y=inactive_days.values, palette='coolwarm', hue=None, legend=False)
    plt.title('Number of Inactive Days per User')
    plt.xlabel('Sender')
    plt.ylabel('Inactive Days')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Function to plot average response time by day of the week
def bar_chart_avg_response_time(data):
    data['Response Time'] = data['Timestamp'].diff().dt.total_seconds().div(60).fillna(0)
    data['Day of Week'] = data['Timestamp'].dt.day_name()
    avg_response_time = data.groupby('Day of Week')['Response Time'].mean().sort_index()
    plt.figure(figsize=(20, 16))
    sns.barplot(x=avg_response_time.index, y=avg_response_time.values, palette='mako', hue=None, legend=False)
    plt.title('Average Response Time by Day of Week')
    plt.xlabel('Day of Week')
    plt.ylabel('Avg Response Time (min)')
    plt.tight_layout()
    plt.show()

# Function to visualize message activity by hour for each user
def message_activity_by_hour(data):
    data['Hour'] = data['Timestamp'].dt.hour
    user_hour_activity = data.groupby(['Sender', 'Hour']).size().unstack(fill_value=0)
    plt.figure(figsize=(12, 8))
    sns.heatmap(user_hour_activity, cmap='YlGnBu', annot=True, fmt='d', linewidths=0.5)
    plt.title('Message Activity by Hour for Each User')
    plt.xlabel('Hour of Day')
    plt.ylabel('User')
    plt.show()


# Call all functions
histogram_message_len_clipped(df)
word_cloud(df)
bar_message_per_sender(df)
visualize_top_stickers('../data/popular_stickers.csv', '../html_messages/')
pie_chart_messages_per_reaction(df)
heatmap_response_time(df)
histogram_inactive_days(df)
bar_chart_avg_response_time(df)
message_activity_by_hour(df)
histogram_message_len_log(df)
