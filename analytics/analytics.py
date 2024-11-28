import pandas as pd

products = pd.read_csv('../data/28_11_2024_14_53_products.csv')
products_copy = products.copy(deep=True)

products_copy.drop_duplicates(ignore_index=True, inplace=True)

filtered_by_rating = products_copy[
    (products_copy['rating'] >= 4) & (products_copy['rating'] <= 5)]

sorted_by_review = filtered_by_rating.sort_values(by='review_count', ascending=False)
top_10 = sorted_by_review.head(10)

top_10.to_csv('top_10_products.csv', index=False, encoding='utf-8')