import pandas as pd

df = pd.read_csv("similarity.csv")
sorted_df = df.sort_values(by='similarity', ascending=False)
sorted_df.to_csv("sorted_data.csv")
