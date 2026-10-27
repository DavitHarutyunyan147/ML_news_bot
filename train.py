
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report



df = pd.read_csv("news.csv")

df = df.dropna(subset=["text", "section"]).copy()

df["text"] = df["text"].astype(str).str.strip()
df["section"] = df["section"].astype(str).str.strip()

df = df[df["text"].str.len() >= 20]
df = df.drop_duplicates(subset=["text"])

print("Հոդվածների քանակը ըստ բաժինների՝")
print(df["section"].value_counts())

X = df["text"]
y = df["section"]


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)




pipeline = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            ngram_range=(1, 2),
            sublinear_tf=True
        )
    ),
    (
        "model",
        LogisticRegression(
            max_iter=2000,
            class_weight="balanced",
            random_state=42
        )
    )
])



params = {
    "model__C": [0.1, 1, 10]
}

grid = GridSearchCV(
    estimator=pipeline,
    param_grid=params,
    cv=3,
    scoring="f1_macro",
    verbose=2,
    n_jobs=-1
)



grid.fit(X_train, y_train)

model = grid.best_estimator_

print("\n--- Մոդելի գնահատում ---")
print("Լավագույն պարամետրեր:", grid.best_params_)

y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))

print("\nClassification report:")
print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)



joblib.dump(model, "model.pkl")

print("\nՄոդելը պահպանվեց model.pkl ֆայլում։")




test_texts = [
    "ԱԺ պատգամավորները խոսել են ՀՀ-ԵՄ հարաբերությունների մասին։",
    "Հայաստանի ֆուտբոլի հավաքականը հաղթել է մրցակցին։",
    "Թանգարանում բացվել է նոր ցուցահանդես։"
]

vectorizer = model.named_steps["tfidf"]

print("\n--- Թեստային կանխատեսումներ ---")

for text in test_texts:
    prediction = model.predict([text])[0]
    probabilities = model.predict_proba([text])[0]

    transformed_text = vectorizer.transform([text])
    recognized_words = vectorizer.inverse_transform(
        transformed_text
    )[0]

    print("\nՏեքստ:", text)
    print("Կանխատեսում:", prediction)
    print("Ճանաչված բառերի քանակը:", transformed_text.nnz)
    print("Ճանաչված բառերը:", recognized_words)

    print("Գնահատականներ:")

    for section, probability in sorted(
        zip(model.classes_, probabilities),
        key=lambda item: item[1],
        reverse=True
    ):
        print(f"  {section}: {probability * 100:.1f}%")



print("\n--- Բառապաշարի ստուգում ---")
print("Բառապաշարի չափը:", len(vectorizer.vocabulary_))

for word in ["պատգամավորները", "ֆուտբոլի", "թանգարանում"]:
    print(
        f"'{word}' բառը բառապաշարում կա՞:",
        word in vectorizer.vocabulary_
    )
