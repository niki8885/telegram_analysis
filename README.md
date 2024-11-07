

# Telegram Chat Analysis Project

## Project Description

This project analyzes messages from Telegram chats, providing comprehensive statistics, data visualizations, and reports. The goal is to automate the analysis of messages, including sticker usage, reactions, response times, and user activity visualizations.

## Project Structure


telegram_analysis/
│
├── data/                            # Project data
│   ├── all_messages_data.csv        # Main CSV with processed chat data
│   ├── message_length_stats.csv     # Message length statistics
│   ├── reaction_stats.csv           # Reaction statistics
│   ├── detailed_reactions.csv       # Detailed reaction data
│   ├── response_time_stats.csv      # Response time statistics
│   ├── popular_stickers.csv         # Sticker usage statistics
│
├── html_messages/                   # Raw Telegram HTML chat files
│   └── stickers/                    # Stickers extracted from messages
│
├── src/                             # Source code scripts
│   ├── parse_data.py                # Data parsing from HTML files
│   ├── analyze_data.py              # Data analysis and CSV generation
│   ├── visualize_data.py            # Data visualization (charts, plots)
│   ├── main.py                      # Main script to run all steps
│
├── LICENSE                          # Project license
├── README.md                        # Project description (this file)
├── requirements.txt                 # Python dependencies


## How to Use

### 1. Clone the Repository
```bash
git clone https://github.com/username/telegram_analysis.git
cd telegram_analysis
```

### 2. Install Dependencies
Make sure you have Python 3.8+ installed, then run:
```bash
pip install -r requirements.txt
```

### 3. Run the Project

#### Parse Data from HTML
To extract messages from Telegram's HTML files:
```bash
python src/parse_data.py
```

#### Analyze Data
Generate statistics:
```bash
python src/analyze_data.py
```

#### Visualize Data
Create visualizations:
```bash
python src/visualize_data.py
```


## Key Features

### 1. **Data Parsing (`parse_data.py`)**
Extracts messages, stickers, and reactions from Telegram HTML files and saves them in CSV format.

### 2. **Data Analysis (`analyze_data.py`)**
- General message statistics.
- Message length statistics.
- Reaction and response time statistics.

### 3. **Data Visualization (`visualize_data.py`)**
- Histograms of message lengths.
- Word clouds.
- Heatmaps of activity by day and hour.
- Top 10 stickers.


## License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Contact
Author: Nikita Manaenkov


