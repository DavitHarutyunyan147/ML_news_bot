import logging
from pathlib import Path

import joblib
import telebot

from sentiment import get_sentiment


BASE_DIR = Path(__file__).resolve().parent
TOKEN_PATH = BASE_DIR / "token.txt"
MODEL_PATH = BASE_DIR / "model.pkl"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


if not TOKEN_PATH.is_file():
    raise FileNotFoundError(
        f"token.txt ֆայլը չի գտնվել։ Ուղի՝ {TOKEN_PATH}"
    )

TOKEN = TOKEN_PATH.read_text(encoding="utf-8").strip()

if not TOKEN:
    raise ValueError(
        "token.txt ֆայլը դատարկ է։ Տեղադրիր նոր Telegram token-ը։"
    )

print("Telegram token-ը հաջողությամբ կարդացվել է։")


if not MODEL_PATH.is_file():
    raise FileNotFoundError(
        f"model.pkl ֆայլը չի գտնվել։ Ուղի՝ {MODEL_PATH}"
    )

try:
    model = joblib.load(MODEL_PATH)
except Exception as error:
    raise RuntimeError(
        f"Մոդելը չհաջողվեց բեռնել։ Պատճառ՝ {error}"
    ) from error

if not hasattr(model, "predict"):
    raise TypeError(
        "model.pkl ֆայլում գտնվող օբյեկտը չունի predict() մեթոդ։"
    )

print("Մոդելը հաջողությամբ բեռնվել է։")
print("Մոդելի դասերը՝", list(model.classes_))


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def start(message):
    response = (
        "Բարև։ Ես հայկական նորությունների դասակարգման բոտ եմ։\n\n"
        "Ուղարկիր նորության տեքստը, և ես կփորձեմ որոշել դրա բաժինը "
        "և տոնայնությունը (դրական, բացասական կամ չեզոք)։\n\n"
        "Հասանելի բաժիններ՝\n"
        "• Քաղաքական\n"
        "• Մշակույթ\n"
        "• Սպորտ\n\n"
        "Լավ արդյունքի համար ուղարկիր ամբողջական նորությունը։"
    )

    bot.reply_to(message, response)


@bot.message_handler(content_types=["text"])
def predict(message):
    text = (message.text or "").strip()

    if not text:
        bot.reply_to(
            message,
            "Ուղարկիր նորության տեքստ։"
        )
        return

    if len(text) < 20:
        bot.reply_to(
            message,
            "Տեքստը շատ կարճ է։ Ուղարկիր առնվազն 20 նիշ "
            "կամ ամբողջական նորությունը։"
        )
        return

    try:
        prediction = model.predict([text])[0]

        response = f" Կանխատեսված բաժին՝ {prediction}"

        sentiment, positive_percent, negative_percent, neutral_percent = get_sentiment(text)

        response += f"\n\nՆորության տոնայնությունը՝ {sentiment}"
        response += f"\n• Դրական: {positive_percent:.1f}%"
        response += f"\n• Բացասական: {negative_percent:.1f}%"
        response += f"\n• Չեզոք: {neutral_percent:.1f}%"

        logger.info("Կանխատեսված բաժին՝ %s", prediction)

        bot.reply_to(message, response)

    except Exception:
        logger.exception("Նորության դասակարգման սխալ")

        bot.reply_to(
            message,
            "Չհաջողվեց վերլուծել նորությունը։ "
            "Ստուգիր տերմինալի սխալը։"
        )


if __name__ == "__main__":
    print("Բոտը գործարկվում է...")

    bot.infinity_polling(
        skip_pending=True,
        timeout=30,
        long_polling_timeout=30
    )
