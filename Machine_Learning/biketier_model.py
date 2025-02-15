# -*- coding: utf-8 -*-
"""BikeTier_Model

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1hcxKwQGDVNFan7InTmfQiMjfsKjz9bxF
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE

df=pd.read_csv('/content/Data_for_ML.csv')
df

df.drop(columns=['latest_brand_name', 'most_purchased_brand_name','customer_id'], inplace=True)
df.info()

tier_mapping = {'high': 3, 'mid': 2, 'low': 1}
df['latest_brand_tier'] = df['latest_brand_tier'].map(tier_mapping)
df['most_purchased_brand_tier'] = df['most_purchased_brand_tier'].map(tier_mapping)

df.info()

df.corr()

value_counts = df['latest_brand_tier'].value_counts()
value_counts

X = df.drop(columns=['latest_brand_tier'])
y = df['latest_brand_tier']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

smote = SMOTE(sampling_strategy={1: 1200}, random_state=42)
X_train, y_train = smote.fit_resample(X_train, y_train)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = LogisticRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
report = classification_report(y_test, y_pred)

print(report)