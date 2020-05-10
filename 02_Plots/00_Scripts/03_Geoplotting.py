import pandas as pd
import numpy as np
import os
import csv

# ----------------- READ IN DATA ----------------- #

# Current Directory + CSV to read
here = os.getcwd()
target = here + "/05_ripCity.csv"

outputList = []

# Open CSV and add lines to empty list
with open(target, mode="r", newline='') as target_file:

    # Read CSV
    reader = csv.reader(target_file, delimiter='\t')

    for line in reader:

        outputList.append(line)

# First list entry == column headers
columns = outputList[0]
columns.insert(0, "X")

# Push list to df
pdx = pd.DataFrame(data = outputList[1:], columns=columns)
pdx.drop("X", axis=1, inplace=True)

# Only keep states!
for index, val in enumerate(pdx["term"]):

    if "state" in val:                                      # I.e., Drop all non-geographic coefficients
        temp = val.replace("state", "")
        pdx["term"][index] = temp.title().strip()
        continue

    else:
        pdx.drop(index, axis=0, inplace=True)

pdx.reset_index(inplace=True)
pdx.drop("index", axis=1, inplace=True)

# ----------------- PLOTTING ----------------- #

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import us

# Convert all applicable columns to numeric data type
for var in (pdx.columns[1:]):

    pdx[var] = pd.to_numeric(pdx[var])

# Lookup FIPS values for coefficients (using "states" package)
for index, var in enumerate(pdx["term"]):

    try:
        temp = us.states.lookup(var)
        pdx.loc[index, "FV"] = temp.fips                    #  Assign to new columns
        pdx.loc[index, "ABR"] = temp.abbr

    except:
        print("Error at " + var)
        continue

# Fill in missing values ... inefficient, but effective!
fupdate = [53, 54, 55, 56]
supdate = ["WA", "WV", "WI", "WY"]

starter = 0
index = 31

for k in (fupdate):

    pdx.loc[index, "FV"] = fupdate[starter]
    pdx.loc[index, "ABR"] = supdate[starter]

    starter += 1
    index += 1

# ----------------- GEOPLOTTING! ----------------- #

import plotly.express as px

fig = px.choropleth(locations=pdx["ABR"], color=pdx["estimate"], width=1000, height=500,
                    color_continuous_scale="RdBu_r",
                    locationmode="USA-states", scope="usa",
                   labels={'color':'Beta'})
fig.update_layout(title_x=0.5)

fig.show()
