#NOTE: DROP THIS SCRIPT INTO THE DIRECTORY - LET MAGIC ENSUE

# ----------------------- SETUP ----------------------- #

# IMPORTS
import pandas as pd
import numpy as np
import os
import glob

# DIRECTORIES
here = os.getcwd()                                  # Root
decision_data = here + "/decisionTask"              # Decison Tasks
demo_data = here + "/demo"                          # Demographic information
survey_data = here + "/surveys"                     # Surveys
output = here + "/CLEAN_DATA"                       # Output directory

# CREATE OUTPUT DIRECTORY IF IT DOESN'T EXIST
try:
    os.mkdir(output)

except:
    print("\nOUTPUT DIRECTORY EXISTS\n")


# ----------------------- COMPILER ----------------------- #

# LIST ALL TASK FILES
all_files = os.listdir(decision_data)

# SEPARATE INTO TASK-SPECIFIC LISTS
race_data = []
eval_data = []

for file in all_files:

    # COMPLETE DATA
    if "final" in file:

        # RACE TASK
        if "num_faces" in file:

            race_data.append(file)

        # EVAL TASK
        elif "vote_trait" in file:

            eval_data.append(file)

        else:
            continue

    else:
        continue

# MOVE TO DECISION TASK DIRECTORY
os.chdir(decision_data)

# READ AND JOIN CSV FOR EACH TASK
race = pd.concat([pd.read_csv(f) for f in race_data])
threat = pd.concat([pd.read_csv(f) for f in eval_data])


# ----------------------- PARSER ----------------------- #

# MOVE TO OUTPUT DIRECTORY
os.chdir(output)

# CREATE FRAME-WISE INDICES
race.reset_index(inplace=True)
threat.reset_index(inplace=True)

# ----------- RACE ----------- #
for index, row in enumerate(race["Trial_Component"]):

    # SET RESPONSE RANGE FROM 0 - 12
    race["Response"][index] = (race["Response"][index]) - 1

    # EXPERIMENTAL TRIAL
    if "faceArray" in row:

        race.loc[index, "FACES"] = pd.to_numeric(row[9:11])
        race.loc[index, "Trial"] = "Trial"

    # ATTENTION CHECK
    elif "AC" in row:

        race.loc[index, "FACES"] = pd.to_numeric(row[12:14])
        race.loc[index, "Trial"] = "Check"

cd1 = pd.DataFrame()                            # Empty df to append into

# LOOP THROUGH PARTICIPANT IDs
for participant in race["subjID"].unique():

    # BASE DICTIONARY
    pData = {"ID": participant}

    # ISOLATE PARTICIPANT DATA
    temp = race[race["subjID"] == participant]
    temp.reset_index(inplace=True)

    for index, val in enumerate(temp["subjID"]):

        real = temp["FACES"][index]             # Actual number of faces displayed
        response = temp["Response"][index]      # Reported number of faces
        r_time = temp["RT"][index]              # Response time per trial
        block = temp["Trial"][index]            # Trial vs. Attention Check

        # EXPERIMENTAL BLOCK
        if block == "Trial":

            r = str(real) + "_NUM"              # Format Key: No. of faces
            rt = str(real) + "_TIME"            # Format Key: Response time

            # ADD TO DICTIONARY
            try:
                pData[r].append(response)
                pData[rt].append(r_time)

            except:
                pData[r] = []
                pData[rt] = []

                pData[r].append(response)
                pData[rt].append(r_time)

        # ATTENTION CHECK BLOCK
        elif block == "Check":

            comp = (response == real)           # Boolean check value

            # ADD TO DICTIONARY
            try:
                pData["Attention"].append(comp)

            except:
                pData["Attention"] = []
                pData["Attention"].append(comp)

    for key in pData.keys():

        if key == "ID":
            continue

        elif key == "Attention":

            # ACCURACY PERCENTAGE
            accuracy = (sum(pData["Attention"])) / (len(pData["Attention"]))
            pData["Attention"] = accuracy

        else:

            # CALCULATE MEAN
            pData[key] = np.mean(pData[key])

    # ADD TO DATAFRAME + CLEAR DICTIONARY
    cd1 = cd1.append(pData, ignore_index=True)
    pData.clear()

# REFORMAT COLUMN NAMES
newCol = []

for k in cd1.columns[:-1]:

    up = str(k) + "_race"
    newCol.append(up)

newCol.append("ID")

cd1.columns = newCol


# ----------- THREAT ----------- #
for index, row in enumerate(threat["Trial_Component"]):

    if "faceArray" in row:

        threat.loc[index, "FACES"] = pd.to_numeric(row[9:11])
        threat.loc[index, "Trial"] = "Trial"

    elif "RATING" in row:

        # Prompt: "Select Neutral"
        threat.loc[index, "FACES"] = 4
        threat.loc[index, "Trial"] = "Check"

    elif "NOT" in row:

        # Prompt: "Select Not Threatening"
        threat.loc[index, "FACES"] = 1
        threat.loc[index, "Trial"] = "Check"

    elif "VERY" in row:

        # Prompt: "Select Very Threatening"
        threat.loc[index, "FACES"] = 7
        threat.loc[index, "Trial"] = "Check"

cd2 = pd.DataFrame()                            # Empty df to append into

# LOOP THROUGH PARTICIPANT IDs
for participant in threat["subjID"].unique():

    # BASE DICTIONARY
    pData = {"ID": participant}

    # ISOLATE PARTICIPANT DATA
    temp = threat[threat["subjID"] == participant]
    temp.reset_index(inplace=True)

    for index, val in enumerate(temp["subjID"]):

        real = temp["FACES"][index]             # Actual number of faces displayed
        response = temp["Response"][index]      # Reported number of faces
        r_time = temp["RT"][index]              # Response time per trial
        block = temp["Trial"][index]            # Trial vs. Attention Check

        # EXPERIMENTAL BLOCK
        if block == "Trial":

            r = str(real) + "_NUM"              # Format Key: No. of faces
            rt = str(real) + "_TIME"            # Format Key: Response time

            # ADD TO DICTIONARY
            try:
                pData[r].append(response)
                pData[rt].append(r_time)

            except:
                pData[r] = []
                pData[rt] = []

                pData[r].append(response)
                pData[rt].append(r_time)

        # ATTENTION CHECK BLOCK
        elif block == "Check":

            comp = (response == real)           # Boolean check value

            # ADD TO DICTIONARY
            try:
                pData["Attention"].append(comp)

            except:
                pData["Attention"] = []
                pData["Attention"].append(comp)

    for key in pData.keys():

        if key == "ID":
            continue

        elif key == "Attention":

            # ACCURACY PERCENTAGE
            accuracy = (sum(pData["Attention"])) / (len(pData["Attention"]))
            pData["Attention"] = accuracy

        else:

            # CALCULATE MEAN
            pData[key] = np.mean(pData[key])

    # ADD TO DATAFRAME + CLEAR DICTIONARY
    cd2 = cd2.append(pData, ignore_index=True)
    pData.clear()

# REFORMAT COLUMN NAMES
newCol = []

for k in cd2.columns[:-1]:

    up = k + "_threat"
    newCol.append(up)

newCol.append("ID")

cd2.columns = newCol


# ----------------------- DEMO ----------------------- #

# MOVE TO DEMO DIRECTORY
os.chdir(demo_data)

# SPLIT INTO DISTINCT LISTS
primes = []
demo = []

for file in os.listdir(demo_data):

    # COMPLETED DATA ONLY
    if "final" in file:

        # PRIME CHECKS
        if "summary_demo" in file:

            primes.append(file)

        # DEMOGRAPHIC INFO
        elif "last_demo" in file:

            demo.append(file)

        else:
            continue

    else:
        continue

# READ AND MERGE
summary_d = pd.concat([pd.read_csv(f) for f in primes])
demo_d = pd.concat([pd.read_csv(f) for f in demo])

# COMBINE CSVs
all_demo = pd.merge(summary_d, demo_d, on="SubjID", how="outer")

# REMOVE EXTRANEOUS COLUMNS
badCols = ["IP_x", "Unnamed: 5", "Study_y", "IP_y", "Unnamed: 11"]
all_demo.drop(badCols, axis=1, inplace=True)

# REFORMAT COLUMN HEADERS
all_demo.rename(columns={"SubjID": "ID", "Study_x": "Study"}, inplace=True)

# ----------------------- SURVEYS ----------------------- #

os.chdir(survey_data)

surveys = []

for file in os.listdir():

    if "final" in file:

        surveys.append(file)

# EMPTY DF TO APPEND INTO
cleanSurveys = pd.DataFrame()

# SDO MEASURES TO BE REVERSE SCORED
reverseScores = ["It would be good if groups could be equal",
"Group equality should be our ideal",
"All groups should be given an equal chance in life",
"We should do what we can to equalize conditions for different groups",
"Increased social equality",
"We would have fewer problems if we treated people more equally",
"We should strive to make incomes as equal as possible",
"No one group should dominate in society"]

for participant in surveys:

    # READ PARTICIPANT DATA
    temp = pd.read_csv(participant)
    pData = {'ID': temp["subjID"][0]}

    # SPLIT INTO SURVEY-SPECIFIC DFs
    sdo = temp[temp["survey_name"] == "sdo"]
    sdo.reset_index(inplace=True)

    exposure = temp[temp["survey_name"] == "exposure"]
    exposure.reset_index(inplace=True)

    secs = temp[temp["survey_name"] == "secs"]
    secs.reset_index(inplace=True)

    # SDO
    sdo_score = 0

    for index, val in enumerate(sdo["response"]):

        # REVERSE SCORES
        if (sdo["survey_item"][index]) in reverseScores:

            rev_val = 8 - val
            sdo_score += rev_val

        # SCORES AS IS
        else:

            sdo_score += val

    pData["SDO_score"] = sdo_score

    # EXPOSURE
    white = 0
    latino = 0

    for index, val in enumerate(exposure["response"]):

        if "White" in exposure["survey_item"][index]:

            white += val

        elif "Hispanic" in exposure["survey_item"][index]:

            latino += val

    pData["Exposure_white"] = white
    pData["Exposure_latino"] = latino

    # SECS
    secs_score = 0

    for val in secs["response"]:

        # MOVE SCALE FROM 1-11 TO 0-10
        s_val = val - 1
        secs_score += s_val

    pData["SECS_score"] = secs_score
    cleanSurveys = cleanSurveys.append(pData, ignore_index=True)
    pData.clear()


# ----------------------- PUSH ----------------------- #

# COMBINE CLEAN DATA FROM BOTH TASKS
total = cd1.merge(cd2, on = "ID", how = "outer")
total = total.merge(all_demo, on="ID", how="outer")
total = total.merge(cleanSurveys, on="ID", how="outer")

# MOVE ID VARIABLE TO FRONT OF DF
NC = list(total.columns)
NC.remove("ID")
NC.insert(0, "ID")

# REARRANGE DF
NC = total[NC]

# MOVE TO OUTPUT DIRECTORY
if (os.getcwd() != output):

    os.chdir(output)

# PUSH TO CSV
NC.to_csv("CLEAN_bothTasks.csv", index=False)
print("\nAll Data Parsed!\n")
