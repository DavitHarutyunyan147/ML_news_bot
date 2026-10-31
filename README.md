# ML News Bot

**ML News Bot** is a Python-based Telegram bot for analyzing Armenian news articles. It combines web scraping, text classification with Machine Learning, and a lightweight keyword-based sentiment analysis component.

The project collects articles from [Aravot.am](https://www.aravot.am/), prepares a CSV dataset, trains a text-classification model, and makes the trained model available through a Telegram bot.

## Features

- **News scraping:** Collects articles from the Politics, Culture, and Sport sections of Aravot.am.
- **Dataset generation:** Saves article titles, text, URLs, and section labels to `news.csv`.
- **News classification:** Uses a TF-IDF text representation and a Random Forest classifier to predict an article's section.
- **Model selection:** Uses `GridSearchCV` to compare configured `max_depth` values.
- **Sentiment analysis:** Estimates positive, negative, or neutral tone using predefined Armenian keywords.
- **Telegram integration:** Lets users submit text and receive classification and sentiment results.
- **Basic reliability measures:** Includes request timeouts, duplicate URL handling, logging, and exception handling.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| pandas | Reading and processing the dataset |
| Scikit-learn | TF-IDF, Random Forest, model selection, and evaluation |
| NumPy / SciPy | Scientific computing dependencies |
| Joblib | Saving and loading the trained model |
| Requests | Sending HTTP requests |
| BeautifulSoup4 | Parsing HTML during web scraping |
| PyTelegramBotAPI | Telegram bot integration |
| CSV | Dataset storage |

## Project Structure

```text
ML_news_bot/
│
├── bot.py
├── parser.py
├── train.py
├── sentiment.py
├── requirements.txt
├── .gitignore
└── README.md
```

### Main Files

- **`parser.py`** — Scrapes article links and article content from Aravot.am, then writes the collected records to `news.csv`.
- **`train.py`** — Reads `news.csv`, prepares the text and labels, trains and evaluates a TF-IDF + Random Forest pipeline using `GridSearchCV`, and saves the selected model as `model.pkl`.
- **`bot.py`** — Loads the Telegram token and trained model, handles incoming text messages, predicts the news category, and returns sentiment analysis results.
- **`sentiment.py`** — Contains the Armenian positive and negative keyword lists and the `get_sentiment()` function.
- **`requirements.txt`** — Lists the Python packages required by the project.
- **`.gitignore`** — Excludes local files and generated artifacts that should not be committed.

## How It Works

The project has three main stages.

### 1. Collecting News

The scraper in `parser.py` visits the following Aravot.am sections:

- Politics
- Culture
- Sport

It collects article titles, text, URLs, and category labels. The resulting dataset is saved to `news.csv` with these columns:

| Column | Description |
|---|---|
| `title` | Article title |
| `text` | Extracted article text |
| `url` | Original article URL |
| `section` | News category |

The scraper includes URL normalization, duplicate prevention, pagination handling, request timeouts, and a delay between requests. It targets approximately 1,000 articles across the three sections; the actual number may be lower if articles cannot be retrieved or parsed.

### 2. Training the Classification Model

The training script in `train.py`:

1. Reads `news.csv` using pandas.
2. Removes rows with missing text or section labels.
3. Removes duplicate article text.
4. Splits the data into training and test sets.
5. Builds a Scikit-learn pipeline with `TfidfVectorizer` and `RandomForestClassifier`.
6. Uses `GridSearchCV` to search the configured maximum tree-depth values.
7. Prints a classification report for the test set.
8. Saves the fitted model to `model.pkl` using Joblib.

The trained model is required by the Telegram bot.

### 3. Telegram Bot and Sentiment Analysis

The bot in `bot.py` loads `model.pkl` and uses its `predict()` method to classify submitted text. It also calls `get_sentiment()` from `sentiment.py` to estimate the text's tone.

The sentiment component counts occurrences of predefined positive and negative Armenian keywords. It is a simple rule-based heuristic, not a context-aware language model. Its percentage values are based on the detected keyword counts and a small neutral baseline; they should not be interpreted as a human-level understanding of sentiment.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/DavitHarutyunyan147/ML_news_bot.git
cd ML_news_bot
```

### 2. Create and Activate a Virtual Environment

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

On Linux or macOS:

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

## Configuration

### Telegram Bot Token

Create a file named `token.txt` in the project directory and put your Telegram Bot API token inside it:

```text
YOUR_TELEGRAM_BOT_TOKEN
```

You can create a Telegram bot and obtain its token through [BotFather](https://t.me/BotFather).

Do not publish your real token or commit `token.txt` to GitHub.

## Usage

Run the commands in the following order.

### 1. Scrape the News Dataset

```bash
python parser.py
```

This creates `news.csv` in the project directory.

### 2. Train the Machine Learning Model

After the dataset has been generated:

```bash
python train.py
```

This evaluates the model on the test split and saves the fitted model as `model.pkl`.

### 3. Start the Telegram Bot

Make sure `token.txt` and `model.pkl` are present, then run:

```bash
python bot.py
```

Send the bot a text message containing at least 20 characters. It will return a predicted news category and the sentiment estimate.

## Local Files

The following files are generated or supplied locally and are not included in the repository:

- `token.txt` — your private Telegram bot token.
- `news.csv` — the scraped dataset.
- `model.pkl` — the trained Machine Learning model.

You can regenerate `news.csv` and `model.pkl` by following the Usage instructions.

## Current Limitations

- The scraper depends on Aravot.am's website structure and availability. Changes to the website may require parser updates.
- The requested dataset size is a target, not a guarantee; some articles may fail to download or parse.
- Model quality depends on the size, balance, and quality of the collected dataset.
- The current training script uses a single train/test split and does not include a separate final validation dataset.
- The sentiment component relies on keyword matching and does not reliably understand context, negation, or sarcasm.
- The sentiment percentages are heuristic scores, not calibrated probabilities.
- The bot requires a compatible local `model.pkl` file and a valid Telegram token.

## Future Improvements

- Add more Armenian news sources and expand the dataset.
- Improve article extraction and make scraping more resilient to website changes.
- Evaluate the classifier with additional metrics and more robust validation.
- Experiment with other text-classification algorithms and Armenian NLP methods.
- Improve sentiment analysis with a trained Armenian-language model.
- Add automated tests and more detailed logging.
- Improve bot commands and user interaction.

## Project Purpose

This project is a practical exploration of Python development, web scraping, text classification, and Telegram bot integration. It demonstrates a workflow from collecting textual data to training a model and making predictions through a messaging interface.

---

**Author:** [Davit Harutyunyan](https://github.com/DavitHarutyunyan147)

**Repository:** [ML_news_bot](https://github.com/DavitHarutyunyan147/ML_news_bot)
