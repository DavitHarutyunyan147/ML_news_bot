# ML News Bot

**ML News Bot** is a Python-based Telegram bot that combines Machine Learning, Web Scraping, and Natural Language Processing techniques to analyze Armenian news articles.

The project collects news articles from [Aravot.am](https://www.aravot.am/), organizes them into categories, and uses a Machine Learning model to classify news. It also includes a keyword-based sentiment analysis component that identifies positive and negative language in submitted text.

The main goal of this project is to explore how Python, Machine Learning, and automation can be combined to build a practical news analysis application.

## Features

- **News Scraping:** Automatically collects articles from Aravot.am.
- **News Classification:** Uses a Machine Learning model to predict the category of a news article.
- **Sentiment Analysis:** Analyzes text and identifies positive, negative, or neutral sentiment using predefined Armenian keywords.
- **Telegram Integration:** Provides an accessible interface for interacting with the analysis system.
- **Dataset Generation:** Collects and stores news articles in CSV format.
- **Error Handling:** Includes basic exception handling and logging to improve reliability.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Scikit-learn | Machine Learning |
| NumPy | Numerical operations |
| SciPy | Scientific computing dependency |
| Joblib | Loading the trained model |
| Requests | Sending HTTP requests |
| BeautifulSoup4 | HTML parsing and web scraping |
| PyTelegramBotAPI | Telegram bot integration |
| CSV | Dataset storage |

## Project Structure

```text
ML_news_bot/
│
├── bot.py
├── train.py
├── parser.py
├── sentiment.py
├── requirements.txt
└── README.md
```

### File Description

- **bot.py** — Main Telegram bot application. Handles user interactions, receives messages, loads the Machine Learning model, and provides analysis results.
- **train.py** — Scrapes news articles from Aravot.am and generates a dataset in CSV format.
- **parser.py** — Contains additional news parsing functionality.
- **sentiment.py** — Implements keyword-based sentiment analysis for Armenian text.
- **requirements.txt** — Contains the Python dependencies required by the project.

## How It Works

The project consists of several components that work together:

### 1. News Scraping

The scraper collects articles from three main sections of Aravot.am:

- Politics
- Culture
- Sport

It extracts article information, including titles and text, and stores the collected data in a CSV file.

The scraper also includes URL normalization, duplicate prevention, pagination handling, request timeouts, and delays between requests.

### 2. Machine Learning Classification

The project uses a trained Machine Learning model to classify news articles into predefined categories.

The model receives text as input and predicts the corresponding news category.

The expected model file is:

```text
model.pkl
```

The model must be available locally for the Telegram bot to load and use it.

### 3. Sentiment Analysis

The sentiment analysis component is implemented in `sentiment.py`.

It uses predefined lists of positive and negative Armenian words to analyze submitted text.

Based on the detected keywords, the system calculates sentiment scores and determines whether the text is:

- Positive
- Negative
- Neutral

This is a rule-based approach rather than a trained Deep Learning model.

### 4. Telegram Bot

The Telegram bot connects the different components into one application.

Users can send text messages and receive analysis results directly through Telegram.

The bot uses the Machine Learning model for news classification and the sentiment analysis module for evaluating text sentiment.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/DavitHarutyunyan147/ML_news_bot.git
```

### 2. Navigate to the Project Directory

```bash
cd ML_news_bot
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Activate it on Linux or macOS:

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

## Configuration

Before running the Telegram bot, prepare the required configuration files.

### Telegram Bot Token

Create a file named `token.txt` in the project directory and place your Telegram Bot API token inside it.

```text
YOUR_TELEGRAM_BOT_TOKEN
```

You can obtain a bot token through [BotFather](https://t.me/BotFather).

### Machine Learning Model

Place your trained Machine Learning model in the project directory and name it:

```text
model.pkl
```

The bot uses Joblib to load the model.

**Important:** The model file and Telegram token are required locally but are not included in the public repository.

## Usage

### Run the News Scraper

To collect news articles and generate the dataset:

```bash
python train.py
```

The collected articles are saved in:

```text
news.csv
```

### Run the Telegram Bot

After configuring `token.txt` and placing `model.pkl` in the project directory, start the bot:

```bash
python bot.py
```

The bot will connect to Telegram and start listening for incoming messages.

## Current Limitations

Although the project combines several useful technologies, it has some limitations:

- Sentiment analysis relies on predefined keywords and does not fully understand context, sarcasm, or negation.
- Machine Learning predictions depend on the quality and diversity of the training dataset.
- The classification component requires an existing compatible model file.
- Web scraping depends on the structure and availability of the source website.
- The project currently focuses on a limited number of Armenian news categories.

## Future Improvements

Possible improvements include:

- Developing a dedicated Machine Learning training pipeline.
- Improving classification accuracy through dataset expansion and model evaluation.
- Implementing more advanced Natural Language Processing techniques for Armenian.
- Replacing keyword-based sentiment analysis with a trained sentiment classification model.
- Adding more Armenian news sources.
- Introducing automated model retraining.
- Improving Telegram bot functionality and user experience.
- Adding unit tests and more comprehensive error handling.

## Project Purpose

This project was developed as a practical exploration of Python programming, Web Scraping, Machine Learning, and Telegram Bot development.

It demonstrates how different Python technologies can be integrated into a single application to collect, process, and analyze real-world textual data.

---

**Author:** [Davit Harutyunyan](https://github.com/DavitHarutyunyan147)

**GitHub Repository:** [ML_news_bot](https://github.com/DavitHarutyunyan147/ML_news_bot)
