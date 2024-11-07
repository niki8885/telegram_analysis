import pandas as pd
import ast
from datetime import timedelta

# Load the CSV data
try:
    df = pd.read_csv('../data/all_messages_data.csv')
    df['Message'] = df['Message'].fillna('')  # Fill missing messages with an empty string
    df['Message Length'] = df['Message'].apply(len)  # Calculate message length
except FileNotFoundError:
    print("Error: The file '../data/all_messages_data.csv' was not found.")
    exit()

# Ensure the 'Reactions' column is parsed correctly
df['Reactions'] = df['Reactions'].apply(
    lambda x: ast.literal_eval(x) if isinstance(x, str) and x.startswith('[') else []
)


# Function to print total statistics
def total_stat(data):
    """Prints total statistics including the number of messages and the date range."""
    print(f"\nTotal messages: {len(data)}")
    print(f"First message: {data['Timestamp'].min()}")
    print(f"Last message: {data['Timestamp'].max()}")


# Function to calculate message length statistics
def message_length(data):
    """Calculates and saves message length statistics (mean, median, mode) for each sender."""
    message_stats = data.groupby('Sender')['Message Length'].agg(
        Mean='mean',
        Median='median',
        Mode=lambda x: x.mode().iloc[0] if not x.mode().empty else None
    )
    try:
        message_stats.to_csv('../data/message_length_stats.csv')
        print("\nMessage Length Statistics Saved to '../data/message_length_stats.csv'")
    except IOError as e:
        print(f"Error saving file: {e}")
    return message_stats


# Function to calculate total reactions received by each sender
def reaction_stats(data):
    """Calculates and saves reaction statistics including total reactions and detailed reactions."""
    reaction_counts = {}
    sender_reactions = {}

    for _, row in data.iterrows():
        sender = row['Sender']
        for reaction in row['Reactions']:
            for user in reaction['users']:
                reaction_counts[sender] = reaction_counts.get(sender, 0) + 1
                sender_reactions.setdefault(user, {}).setdefault(sender, 0)
                sender_reactions[user][sender] += 1

    reaction_stats_df = pd.DataFrame.from_dict(reaction_counts, orient='index', columns=['Total Reactions Received'])
    try:
        reaction_stats_df.to_csv('../data/reaction_stats.csv')
        print("\nReaction Statistics Saved to '../data/reaction_stats.csv'")
    except IOError as e:
        print(f"Error saving file: {e}")

    detailed_reactions_df = pd.DataFrame(sender_reactions).fillna(0).astype(int).T
    try:
        detailed_reactions_df.to_csv('../data/detailed_reactions.csv')
        print("\nDetailed Reaction Statistics Saved to '../data/detailed_reactions.csv'")
    except IOError as e:
        print(f"Error saving file: {e}")

    return reaction_stats_df


# Function to calculate response time statistics
def response_time_stats(data):
    """Calculates and saves response time statistics (mean, median, mode) for each sender."""
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])
    data['Previous Timestamp'] = data['Timestamp'].shift(1)
    data['Previous Sender'] = data['Sender'].shift(1)

    data['Response Time'] = data.apply(
        lambda row: (row['Timestamp'] - row['Previous Timestamp']).total_seconds() / 60
        if pd.notnull(row['Previous Timestamp']) and row['Sender'] != row['Previous Sender'] else None,
        axis=1
    )

    response_stats = data.groupby('Sender')['Response Time'].agg(
        Mean='mean',
        Median='median',
        Mode=lambda x: x.mode().iloc[0] if not x.mode().empty else None
    )

    try:
        response_stats.to_csv('../data/response_time_stats.csv')
        print("\nResponse Time Statistics Saved to '../data/response_time_stats.csv'")
    except IOError as e:
        print(f"Error saving file: {e}")

    return response_stats


# Run major analysis
total_stat(df)
message_stats = message_length(df)
reaction_stats_df = reaction_stats(df)
response_time_stats_df = response_time_stats(df)