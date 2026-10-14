# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 11:26:57 2026

@author: Jelle J
"""

import pandas as pd
import seaborn as sns

df = pd.read_csv("out.csv")
data = pd.DataFrame()

for label in df["label"].unique():
    print(label)

    for idx in df["index"].unique():
        Vrows = df[
            (df["index"] == idx) &
            (df["folder"] == "Voor") &
            (df["label"] == label)
            ]["vertCount"]
        
        Zrows = df[
            (df["index"] == idx) &
            (df["folder"] == "Zij") &
            (df["label"] == label)
            ]["vertCount"]
        
        if Vrows.empty or Zrows.empty:
            print(f"Skipping index {idx}")
            continue
    
        Vnum = Vrows.iloc[0]
        Znum = Zrows.iloc[0]
        
        result = Vnum - Znum
        
        diff = pd.DataFrame({
            "label": [label],
            "diff": [result]
            })
        data = pd.concat([data, diff])

sns.violinplot(data=data, x="label", y="diff", inner="quart")
