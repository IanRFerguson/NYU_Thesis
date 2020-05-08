# IMPORTS
library(tidyverse)
library(readxl)
library(reshape2)

# LINE UP WORKING DIRECTORY
here <- "~/DOCUMENTS/ACADEMIA/02_NYU/THESIS/01_ANALYSIS/05_CLEAN/"
setwd(here)

# COLOR SCHEME FOR PLOTS ... excuse my naming conventions
bad.boys.only <- c("dodgerblue2", "lightcoral")

# READ IN DATA FROM PYTHON
big.kahuna <- read_excel("02_bigKahuna.xlsx")

# REMOVE NULL OBSERVATIONS
big.kahuna.clean <- big.kahuna %>% 
        na.omit()

# CONVERT TO FACTORS
ideo.inOrder <- c("EXTREMELY_LIBERAL", "MODERATELY_LIBERAL","SLIGHTLY_LIBERAL", "NEITHER",
                  "SLIGHTLY_CONSERVATIVE", "MODERATELY_CONSERVATIVE", "EXTREMELY_CONSERVATIVE")

big.kahuna.clean$poli <- factor(big.kahuna.clean$poli, levels = ideo.inOrder)

big.kahuna.clean$BLOCK <- as.factor(big.kahuna.clean$BLOCK)
big.kahuna.clean$gender <- as.factor(big.kahuna.clean$gender)

# NEW CONSERVATIVE VARIABLE
big.kahuna.clean <- big.kahuna.clean %>% 
        mutate("SDO_z" = scale(SDO_score)) %>% 
        mutate("SECS_z" = scale(SECS_score)) %>%
        mutate("SC_us" = (SDO_score + SECS_score) / 2) %>% 
        mutate("SC_z" = (SDO_z + SECS_z) / 2)

# PUSH TO CSV
write_csv(x = big.kahuna.clean, path = paste0(here, "03_compiledData_clean.csv"))
