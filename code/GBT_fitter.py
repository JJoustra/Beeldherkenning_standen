# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 08:56:11 2026

@author: Jelle J
"""

from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
import pandas as pd

import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
 

df = pd.read_csv("out.csv")
X = X = df[[    #VERGEET DEZE KOLOM NAMEN NIET AAN TE PASSEN, SUKKEL
    "gem_afstand_V",
    "gem_afstand_Z",
    "langste_V",
    "langste_Z",
    "verschil_gem",
    "verschil_top"
    ]]
y = df["label"]

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Classifier parameters & init
clf = GradientBoostingClassifier(
    n_estimators=10,
    learning_rate=0.1,
    max_depth=3,
    random_state=42
)
clf.fit(X_train, y_train)

# Make predictions
y_pred = clf.predict(X_test)

predictions = clf.predict(X_test)
cm = confusion_matrix(y_test, y_pred, labels=clf.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                              display_labels=clf.classes_)
disp.plot()
plt.show()


