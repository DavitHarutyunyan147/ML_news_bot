# ML_bot
# Armenian News Classifier Bot 🇦🇲

A Telegram bot powered by Machine Learning that automatically classifies Armenian news articles into three categories: **Politics, Culture, and Sports**.

## About the Project

The Armenian News Classifier Bot uses a trained Machine Learning model to analyze news text and predict which category it belongs to. Users can send a news article directly to the Telegram bot and receive a predicted category along with confidence scores for each available category.

This project combines Natural Language Processing (NLP), Machine Learning, and Telegram Bot API integration.

## Features

- **News Classification:** Categorizes Armenian news into Politics, Culture, or Sports.
- **Probability Scores:** Displays the model's estimated probability for each category when supported by the model.
- **Telegram Integration:** Provides a simple and accessible chat interface.
- **Text Validation:** Requests longer text when the submitted message contains fewer than 50 characters.
- **Error Handling:** Handles prediction errors and logs technical details.
- **Secure Token Storage:** Reads the Telegram bot token from a separate `token.txt` file.

## Categories

| Category | Armenian Label |
|---|---|
| Politics | Քաղաքական |
| Culture | Մշակույթ |
| Sports | Սպորտ |

## Technologies Used

- **Python** — Core programming language
- **Scikit-learn** — Machine Learning model and predictions
- **TF-IDF** — Text feature extraction
- **Logistic Regression** — Classification algorithm
- **Joblib** — Saving and loading the trained model
- **PyTelegramBotAPI** — Telegram Bot API integration
- **NumPy and SciPy** — Scientific computing dependencies

## How It Works

1. The user sends a news article to the Telegram bot.
2. The bot checks whether the text is long enough for analysis.
3. The trained model processes the text and predicts its category.
4. If probability estimates are available, the bot calculates the scores for all three categories.
5. The bot returns the predicted category and the estimated probability scores.

**Note:** The displayed probability scores are model estimates, not guarantees of correctness.

## Project Structure

```text
armenian-news-classifier/
├── bot.py
├── model.pkl
├── token.txt
├── requirements.txt
└── README.md
```

- `bot.py` — Telegram bot implementation.
- `model.pkl` — Serialized, trained Machine Learning model.
- `token.txt` — Telegram bot token. Keep this file private.
- `requirements.txt` — Python dependencies.
- `README.md` — Project documentation.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/armenian-news-classifier.git
cd armenian-news-classifier
```

Replace `YOUR_USERNAME` and the repository name with your actual GitHub details.

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure the Telegram Bot Token

Create a file named `token.txt` in the project directory and place your Telegram bot token inside it.

Do not upload your real token to a public GitHub repository.

### 5. Run the Bot

```bash
python bot.py
```

Once started, the bot will load the trained model and begin receiving Telegram messages.

## Usage

1. Open the Telegram bot.
2. Send `/start` to see the instructions.
3. Send an Armenian news article containing at least 50 characters.
4. Receive the predicted category and available probability estimates.

## Model Performance

The model achieved approximately **92.6% accuracy** on the test set used during development.

However, the test set contained only 27 samples. Therefore, this result should be considered preliminary and does not guarantee the same performance on new articles.

A larger and more diverse test dataset would provide a more reliable evaluation.

## Future Improvements

- Expand the training dataset with more Armenian news articles.
- Add more news categories.
- Improve text preprocessing and model evaluation.
- Compare Logistic Regression with other classification algorithms.
- Deploy the bot on a reliable hosting platform for continuous availability.
- Add support for news links and automated article extraction.

## Security

- Never commit `token.txt` or expose your Telegram bot token.
- Add secret files to `.gitignore`.
- Use a compatible version of the libraries used to train and save the model.

## License

Choose a license before distributing or reusing this project publicly.

---

**Built with Python, Machine Learning, and the Telegram Bot API.**
