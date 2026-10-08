# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 11:26:57 2026

@author: Jelle J
"""

import pandas as pd
import seaborn as sns

df = pd.read_csv("out.csv")
data = pd.DataFrame()

for idx in df["index"].unique():
    Vrows = df[
        (df["index"] == idx) &
        (df["folder"] == "Heiko_Dachi_V")
        ]["vertCount"]
    
    Zrows = df[
        (df["index"] == idx) &
        (df["folder"] == "Heiko_Dachi_Z")
        ]["vertCount"]
    
    if Vrows.empty or Zrows.empty:
        print(f"Skipping index {idx}: missing V or Z value")
        continue

    Vnum = Vrows.iloc[0]
    Znum = Zrows.iloc[0]
    
    result = Vnum - Znum
    
    diff = pd.DataFrame({
        "label": ["Heiko"],
        "diff": [result]
        })
    data = pd.concat([data, diff])

for idx in df["index"].unique():
    Vrows = df[
        (df["index"] == idx) &
        (df["folder"] == "Kokutsu_Dachi_V")
        ]["vertCount"]
    
    Zrows = df[
        (df["index"] == idx) &
        (df["folder"] == "Kokutsu_Dachi_Z")
        ]["vertCount"]
    
    if Vrows.empty or Zrows.empty:
        print(f"Skipping index {idx}: missing V or Z value")
        continue

    Vnum = Vrows.iloc[0]
    Znum = Zrows.iloc[0]
    
    result = Vnum - Znum
    
    diff = pd.DataFrame({
        "label": ["Kokutsu"],
        "diff": [result]
        })
    data = pd.concat([data, diff])

for idx in df["index"].unique():
    Vrows = df[
        (df["index"] == idx) &
        (df["folder"] == "Kosa_V")
        ]["vertCount"]
    
    Zrows = df[
        (df["index"] == idx) &
        (df["folder"] == "Kosa_Z")
        ]["vertCount"]
    
    if Vrows.empty or Zrows.empty:
        print(f"Skipping index {idx}: missing V or Z value")
        continue

    Vnum = Vrows.iloc[0]
    Znum = Zrows.iloc[0]
    
    result = Vnum - Znum
    
    diff = pd.DataFrame({
        "label": ["Kosa"],
        "diff": [result]
        })
    data = pd.concat([data, diff])

for idx in df["index"].unique():
    Vrows = df[
        (df["index"] == idx) &
        (df["folder"] == "Neko_V")
        ]["vertCount"]
    
    Zrows = df[
        (df["index"] == idx) &
        (df["folder"] == "Neko_Z")
        ]["vertCount"]
    
    if Vrows.empty or Zrows.empty:
        print(f"Skipping index {idx}: missing V or Z value")
        continue

    Vnum = Vrows.iloc[0]
    Znum = Zrows.iloc[0]
    
    result = Vnum - Znum
    
    diff = pd.DataFrame({
        "label": ["Neko"],
        "diff": [result]
        })
    data = pd.concat([data, diff])

for idx in df["index"].unique():
    Vrows = df[
        (df["index"] == idx) &
        (df["folder"] == "Shiko_V")
        ]["vertCount"]
    
    Zrows = df[
        (df["index"] == idx) &
        (df["folder"] == "Shiko_Z")
        ]["vertCount"]
    
    if Vrows.empty or Zrows.empty:
        print(f"Skipping index {idx}: missing V or Z value")
        continue

    Vnum = Vrows.iloc[0]
    Znum = Zrows.iloc[0]
    
    result = Vnum - Znum
    
    diff = pd.DataFrame({
        "label": ["Shiko"],
        "diff": [result]
        })
    data = pd.concat([data, diff])

for idx in df["index"].unique():
    Vrows = df[
        (df["index"] == idx) &
        (df["folder"] == "Tsuru_V")
        ]["vertCount"]
    
    Zrows = df[
        (df["index"] == idx) &
        (df["folder"] == "Tsuru_Z")
        ]["vertCount"]
    
    if Vrows.empty or Zrows.empty:
        print(f"Skipping index {idx}: missing V or Z value")
        continue

    Vnum = Vrows.iloc[0]
    Znum = Zrows.iloc[0]
    
    result = Vnum - Znum
    
    diff = pd.DataFrame({
        "label": ["Tsuru"],
        "diff": [result]
        })
    data = pd.concat([data, diff])

for idx in df["index"].unique():
    Vrows = df[
        (df["index"] == idx) &
        (df["folder"] == "Zenkutsu_V")
        ]["vertCount"]
    
    Zrows = df[
        (df["index"] == idx) &
        (df["folder"] == "Zenkutsu_Z")
        ]["vertCount"]
    
    if Vrows.empty or Zrows.empty:
        print(f"Skipping index {idx}: missing V or Z value")
        continue

    Vnum = Vrows.iloc[0]
    Znum = Zrows.iloc[0]
    
    result = Vnum - Znum
    
    diff = pd.DataFrame({
        "label": ["Zenkutsu"],
        "diff": [result]
        })
    data = pd.concat([data, diff])

sns.violinplot(data=data, x="label", y="diff", inner="quart")