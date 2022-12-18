import pandas as pd

data = pd.read_csv('../../data/data2.csv')

all_columns = data.columns.tolist()
columns_to_drop = [col for col in all_columns if col != "text"]
data = data.drop(columns=columns_to_drop)


nrEvaluationPrompts = 1000

sample = data.sample(n=nrEvaluationPrompts)

sample.to_csv("promptsSample.csv")
