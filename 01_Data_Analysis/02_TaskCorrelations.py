# GOAL: For each participant we want to calculate four correlations: Num/Race, Time/Race, Num/Threat, & Time/Threat

# IMPORTS
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.getcwd()
os.chdir("..")

# Sorry for the naming conventions ... but at least I'm consistent
kahuna = pd.read_excel("02_bigKahuna.xlsx")

# Vector represents possible number of Latino faces / ensemble
compare_me = list(range(0, 13))

# Loop through participant responses
for index, participant in enumerate(kahuna["ID"]):

    # Isolate participant data
    temp = (kahuna.iloc[index, ]).to_frame().T

    temp_race_n = (temp.loc[:, numRace]).to_numpy().tolist()
    temp_race_t = (temp.loc[:, timeRace]).to_numpy().tolist()
    temp_threat_n = (temp.loc[:, numThreat]).to_numpy().tolist()
    temp_threat_t = (temp.loc[:, timeThreat]).to_numpy().tolist()

    try:
        kahuna.loc[index, "CORR_num_race"] = round(np.corrcoef(temp_race_n, compare_me)[0,1], 3)

    except:
        print("Error in num race")
        continue

    try:
        kahuna.loc[index, "CORR_time_race"] = round(np.corrcoef(temp_race_t, compare_me)[0,1], 3)

    except:
        print("Error in time race")
        continue

    try:
        kahuna.loc[index, "CORR_num_threat"] = round(np.corrcoef(temp_threat_n, compare_me)[0,1], 3)

    except:
        print("Error in num threat")
        continue

    try:
        kahuna.loc[index, "CORR_time_threat"] = round(np.corrcoef(temp_threat_t, compare_me)[0,1], 3)

    except:
        print("Error in time threat")
        continue

# Push to Excel
kahuna.to_excel("02_bigKahuna.xlsx")
