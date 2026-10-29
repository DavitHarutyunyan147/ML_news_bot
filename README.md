# Armenian News Classification & Sentiment Analysis Bot

A Python-based project designed to collect, classify, and analyze Armenian-language news articles using web scraping, Machine Learning, and Natural Language Processing (NLP).

The project collects news articles from Aravot.am, organizes them into three categories — Political, Culture, and Sport — and provides a Telegram bot that predicts the category of a news article and estimates its sentiment.

## Features

- **Automated News Scraping:** Collects Armenian news articles from Aravot.am.
- **News Classification:** Uses a Machine Learning model to classify articles into Political, Culture, and Sport categories.
- **Sentiment Analysis:** Analyzes Armenian text and estimates whether its sentiment is positive, negative, or neutral.
- **Dataset Generation:** Automatically extracts article titles, text, URLs, and category labels into a CSV file.
- **Telegram Integration:** Allows users to submit news articles and receive analysis directly through Telegram.
- **Duplicate Prevention:** Avoids collecting the same article URL multiple times during scraping.
- **Error Handling:** Handles request failures, missing article content, and model prediction errors.
- **Logging:** Records important bot events and errors to help with debugging.

## Technologies Used

- **Python** — Main programming language.
- **Requests** — Downloads web pages.
- **BeautifulSoup4** — Parses HTML and extracts article information.
- **Pandas and CSV** — Support dataset preparation and data handling.
- **Scikit-learn** — Supports Machine Learning model development.
- **Joblib** — Loads the trained classification model.
- **PyTelegramBotAPI** — Connects the project to Telegram.
- **Regular Expressions (Regex)** — Identifies article URLs and processes text patterns.

## Project Structure

```text
project/
├── train.py          # Collects news articles and generates news.csv
├── parser.py         # Additional news parsing script, if used
├── sentiment.py      # Armenian keyword-based sentiment analysis
├── bot.py            # Telegram bot and prediction logic
├── news.csv          # Generated news dataset
├── model.pkl         # Trained Machine Learning model
├── token.txt         # Telegram Bot API token
├── requirements.txt  # Python dependencies
└── README.md         # Project documentation
```

## News Data Collection

The `train.py` script collects articles from three sections of Aravot.am:

| Category | Armenian label | Target articles |
|---|---|---:|
| Political | Քաղաքական | 334 |
| Culture | Մշակույթ | 333 |
| Sport | Սպորտ | 333 |
| **Total** | | **1,000** |

The scraper is designed to collect a dataset with approximately 1,000 articles distributed across the three categories.

### Scraping Process

1. Opens the selected news category pages.
2. Identifies article links using URL patterns.
3. Navigates through listing pages to discover additional articles.
4. Removes duplicate URLs and tracks visited pages.
5. Downloads article pages using HTTP requests.
6. Extracts article titles and text paragraphs from HTML.
7. Skips articles whose extracted content is missing or too short.
8. Assigns the appropriate category to each successfully extracted article.
9. Saves the resulting dataset in `news.csv`.

The scraper includes request timeouts and a delay between requests to reduce unnecessary repeated requests to the website.

The final number of articles may be lower than the target if some pages are inaccessible or the article content cannot be extracted.

## Dataset Format

The generated `news.csv` file contains four columns:

| Column | Description |
|---|---|
| `title` | Title of the news article |
| `text` | Extracted article content |
| `url` | Original article URL |
| `section` | News category label |

Example:

```csv
title,text,url,section
"Example news title","Example Armenian news article text...","https://www.aravot.am/...","Քաղաքական"
```

The `text` column provides the input for text classification, while `section` contains the target category used during model training.

## Machine Learning Classification

The project uses a trained Machine Learning model to predict the category of an Armenian news article.

The classification categories are:

- **Քաղաքական (Political)** — Political events, government activities, public policy, and related topics.
- **Մշակույթ (Culture)** — Cultural events, arts, entertainment, and related topics.
- **Սպորտ (Sport)** — Sports competitions, athletes, teams, and sporting events.

The model is stored in `model.pkl` and loaded by the Telegram bot using Joblib.

When a user submits an article, the bot passes the text to the model's `predict()` method and returns the predicted category.

**Note:** `train.py` is the data collection script. Model training is a separate step and must be performed using a training script that prepares the data, trains the classifier, and saves the resulting model as `model.pkl`.

## Armenian Sentiment Analysis

The `sentiment.py` module implements a rule-based sentiment analysis system using predefined Armenian positive and negative keywords.

### Sentiment Categories

- **Positive (Դրական)** — Positive keywords appear more frequently.
- **Negative (Բացասական)** — Negative keywords appear more frequently.
- **Neutral (Չեզոք)** — Positive and negative keyword counts are equal.

The module calculates estimated positive, negative, and neutral percentages based on keyword matches. A neutral baseline is included in the calculation.

For example, words associated with victories, achievements, awards, and success may contribute to a positive result. Words associated with accidents, conflict, injuries, crime, and losses may contribute to a negative result.

This approach is lightweight and does not require a separately trained sentiment model.

However, keyword-based analysis has limitations: it may not understand context, sarcasm, negation, or cases where a normally positive or negative word is used differently.

## Telegram Bot

The `bot.py` script connects the classification model and sentiment analysis module to Telegram.

### Available Commands

- `/start` — Starts the bot and displays a welcome message.
- `/help` — Displays instructions for using the bot.

### How the Bot Works

1. The user sends a news article as a text message.
2. The bot checks whether the message contains enough text for analysis.
3. The Machine Learning model predicts the news category.
4. The sentiment module calculates the estimated sentiment.
5. The bot returns the predicted category and sentiment percentages.

The response includes the predicted category and the estimated positive, negative, and neutral sentiment percentages.

The bot uses continuous polling to receive incoming messages and includes basic error handling and logging.

## Installation

### Requirements

- Python 3.10 or newer recommended.
- Internet connection.
- A Telegram account.
- A Telegram bot token obtained through [BotFather](https://t.me/BotFather).

### 1. Clone the Repository

```bash
git clone YOUR_REPOSITORY_URL
cd YOUR_PROJECT_FOLDER
```

Replace the placeholders with your actual repository URL and project directory.

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows using PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

If `requirements.txt` is available:

```bash
python -m pip install -r requirements.txt
```

Otherwise, install the main dependencies:

```bash
python -m pip install requests beautifulsoup4 pandas scikit-learn joblib pyTelegramBotAPI
```

Additional packages may be needed by your separate model-training script.

## Running the Project

### Step 1: Collect News Articles

Run the scraper:

```bash
python train.py
```

After execution, the script generates `news.csv` containing the articles it successfully collected.

### Step 2: Train the Model

Use your Machine Learning training script to train a classifier on `news.csv`.

The training process should:

1. Load the CSV dataset.
2. Use `text` as the input feature.
3. Use `section` as the target label.
4. Train and evaluate a suitable text classification model.
5. Save the trained model as `model.pkl`.

The saved model must be compatible with the environment in which the Telegram bot runs.

### Step 3: Configure the Telegram Token

Create a file named `token.txt` in the project directory.

Paste your Telegram bot token into the file and save it.

Keep this token private. Do not publish it in your GitHub repository.

### Step 4: Start the Telegram Bot

Run:

```bash
python bot.py
```

Once started, the bot loads the saved model and waits for incoming messages.

Open your bot in Telegram, send `/start`, and then submit a news article for analysis.

## Configuration

The scraping settings can be adjusted in `train.py`:

- `TOTAL_COUNT` — Target total number of articles.
- `EXTRA_LINKS` — Number of article links to collect relative to the target.
- `LINES_COUNT` — Maximum number of paragraphs extracted per article.
- `MAX_LISTING_PAGES` — Maximum number of listing pages to visit per category.
- `REQUEST_DELAY` — Delay between scraping requests.
- `OUTPUT_FILE` — Name of the generated dataset file.

These settings can be modified depending on dataset requirements and website availability.

## Limitations

- The scraper depends on Aravot.am's website structure and availability.
- Some articles may fail to download or may not contain extractable text.
- The dataset may not reach the target of 1,000 articles.
- Classification quality depends on the training data, preprocessing, and model evaluation.
- The sentiment module uses keyword matching rather than contextual language understanding.
- Predictions should be treated as automated estimates, not verified conclusions about an article.

## Future Improvements

Potential improvements include:

- Improving HTML extraction and pagination handling.
- Increasing dataset size and maintaining balanced categories.
- Evaluating classification performance using accuracy, precision, recall, and F1-score.
- Improving Armenian text preprocessing and tokenization.
- Replacing or supplementing keyword-based sentiment analysis with a trained NLP model.
- Adding confidence scores to category predictions.
- Improving input validation and handling unrelated messages.
- Deploying the bot to a hosting service for continuous operation.
- Adding automated dataset updates and model retraining.

## Purpose

This project demonstrates the practical application of Python, web scraping, Machine Learning, and Natural Language Processing to Armenian-language news.

It combines automated data collection, text classification, rule-based sentiment analysis, and Telegram integration in one project.

## Author

Developed as a Python and Machine Learning project focused on Armenian-language news analysis.
