import pandas as pd
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import nltk
import re
import matplotlib.pyplot as plt

nltk.download('stopwords')
russian_stopwords = set(stopwords.words("russian"))
stemmer = SnowballStemmer("russian")

reviews = pd.read_csv('../data/28_11_2024_14_53_reviews.csv')
reviews_copy = reviews.copy(deep=True)

five_star_reviews = reviews_copy[reviews_copy['rating'] == 5]['text']

all_text = " ".join(five_star_reviews)

words = re.findall(r'\b\w+\b', all_text.lower())

filtered_words = [word for word in words if len(word) >= 5 and word not in russian_stopwords]
lemmatized_words = [stemmer.stem(word) for word in filtered_words]

word_counts = Counter(lemmatized_words)

most_common_words = word_counts.most_common(3)

labels, values = zip(*most_common_words)
colors = ['#ff9999', '#66b3ff', '#99ff99']

plt.figure(figsize=(10, 10))
plt.pie(
    values,
    labels=labels,  # Оставляем лейблы без изменений
    colors=colors,
    autopct=lambda val: f'{int(val/100.*sum(values))}',  # Выводим количество вместо процентов
    startangle=140,
    textprops={'fontsize': 16}  # Увеличение шрифта подписей
)
plt.show()