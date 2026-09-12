# not really an important file, all further data management was made directly in processing_model.ipynb

import pandas as pd
from sklearn.impute import SimpleImputer
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.float_format', '{:.2f}'.format)

dataset = pd.read_csv('data/kyiv_apartments.csv')
print(dataset.head(20))


area_set = pd.DataFrame(dataset[['total_area', 'living_area', 'kitchen_area']])
area_set.dropna(inplace=True)
relationship = area_set['living_area']/area_set['total_area']

relationship2 = area_set['kitchen_area']/area_set['total_area']

print('\n\n')
print(np.median(relationship))
print(np.median(relationship2))

# for el in dataset['living_area']:
#     print(f"{el}: {type(el)}")

dataset['living_area'] = dataset['living_area'].fillna((dataset['total_area'] * np.median(relationship)).round(1))
dataset['kitchen_area'] = dataset['kitchen_area'].fillna((dataset['total_area'] * np.median(relationship2)).round(1))

print(dataset.head(20))

dataset.drop_duplicates(inplace=True)

dataset.to_csv('data/kyiv_apartments_copy.csv', index=False)
# imputer = SimpleImputer(missing_values=np.nan, fill_value=np.median(relationship))
# imputer.fit(dataset[['living_area', 'kitchen_area']])
# dataset[['living_area', 'kitchen_area']] = imputer.transform(dataset[['living_area', 'kitchen_area']])
# print("\n\n\n")
# print(dataset.head(20))