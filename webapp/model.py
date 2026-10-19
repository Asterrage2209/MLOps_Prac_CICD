import pickle
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

x,y=load_iris(return_X_y=True)  
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

model=GaussianNB()
model.fit(x_train, y_train)
y_pred = model.predict(x_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model accuracy: {accuracy}")

with open('MLOps/P2/model.pkl', 'wb') as f:
    pickle.dump(model, f)