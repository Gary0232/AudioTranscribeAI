import pandas as pd

data_df = pd.read_csv("../data/news_summary/news_summary.csv", encoding="latin1")
# drop the row containing NaN
data_df = data_df.dropna()

# sample 50 from the dataset
data_df = data_df.sample(50)

# save the sampled data
data_df.to_csv("data/news_summary/news_summary_sampled.csv", index=False, encoding="utf-8")