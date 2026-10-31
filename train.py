import pandas as pd
import joblib

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report


df = pd.read_csv("news.csv")

df = df.dropna(subset=["text", "section"])
df = df.drop_duplicates(subset=["text"])

X = df["text"]
y = df["section"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

tfidf = TfidfVectorizer()
model = RandomForestClassifier(random_state=42)

pipe = Pipeline([('tfidf', tfidf), ('model', model)])

params = {
    'model__max_depth': [None, 6, 8, 12]
}

final_model = GridSearchCV(pipe, params, cv=3, verbose=2)
final_model.fit(X_train, y_train)

y_pred = final_model.predict(X_test)
print(classification_report(y_test, y_pred))

joblib.dump(final_model, "model.pkl")
print("Մոդելը պահպանվեց model.pkl ֆայլում։")
