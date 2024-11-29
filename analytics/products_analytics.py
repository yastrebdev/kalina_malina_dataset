import pandas as pd
import matplotlib.pyplot as plt

products = pd.read_csv('../data/28_11_2024_14_53_products.csv')
pc = products.copy(deep=True)

pc.drop_duplicates(ignore_index=True, inplace=True)

filtered_by_rating = pc[
    (pc['rating'] >= 4) & (pc['rating'] <= 5)]

sorted_by_review = filtered_by_rating.sort_values(by='review_count', ascending=False)
top_10 = sorted_by_review.head(15)

top_10.to_csv('top_10_products.csv', index=False, encoding='utf-8')



pc['calorie_category'] = (
    pd.cut(pc['nutritionKcal'], bins=[0, 150, 300, 450, 600, 1000],
    labels=['Очень низкая', 'Низкая', 'Средняя', 'Высокая', 'Очень высокая']))

pc['fat_to_protein_ratio'] = pc['fats'] / pc['proteins']

filtered_by_ftpr = pc[pc['fat_to_protein_ratio'] <= 0.400000]
sorted_ftpr = filtered_by_ftpr.sort_values(by='fat_to_protein_ratio', ascending=False)

ftpr_table = sorted_ftpr[['name', 'rating', 'price', 'proteins', 'fats', 'carbohydrates', 'calorie_category', 'fat_to_protein_ratio']]

ftpr_top_10 = ftpr_table.head(10).sort_values(by='fat_to_protein_ratio', ascending=True)

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)

ftpr_top_10.to_csv('ftpr_top_10_products.csv', index=False, encoding='utf-8')



pc['shelfLife_category'] = pd.cut(
    pc['shelfLife'],
    bins=[0, 3, 7, 14, 30],
    labels=['1-3 дня', '4-7 дней', '8-14 дней', '15+ дней'])

shelf_life_analysis = pc.groupby('shelfLife_category').agg(
    avg_price=('price', 'mean'),
    count=('id', 'count')
)


plt.figure(figsize=(14, 8))

shelf_life_analysis['avg_price'].plot(kind='bar', color='skyblue', alpha=0.7, label='Средняя цена')
shelf_life_analysis['count'].plot(kind='line', marker='o', secondary_y=True, label='Количество товаров')

plt.title('Анализ сроков годности')
plt.ylabel('Средняя цена')
plt.xlabel('Категории срока годности')
plt.legend()
plt.show()