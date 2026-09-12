import pandas as pd
import numpy as np
import os

route = "data/kyiv_apartments.csv"
if not os.path.exists(route):
    print(f"File {route} not found.")
    exit(1)

dataset = pd.read_csv(route)
dataset.info()
# print(dataset.notna().sum())
print("\n\n")
print(dataset.drop_duplicates(inplace=True))
dataset.info()