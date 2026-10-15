# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 13:17:51 2026

@author: Jelle J
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report
 
# Load the dataset
df = pd.read_csv("ASFDADSFASDFASDF")
X = df["COL1"],["COL2"] #etc etc
y = df["COL0"]

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Create and train the classifier
clf = GradientBoostingClassifier(
    n_estimators=10,
    learning_rate=0.1,
    max_depth=2,
    random_state=42
)
clf.fit(X_train, y_train)

# Make predictions
y_pred = clf.predict(X_test)

# Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Get class probabilities
print("Probabilities:", clf.predict_proba(X_test[:3]))