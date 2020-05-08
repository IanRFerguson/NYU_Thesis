library(tidyverse)
library(geepack)
library(scales)
library(psych)

here <- "~/DOCUMENTS/ACADEMIA/02_NYU/THESIS/01_ANALYSIS/05_CLEAN/01_SCRIPTS/"
setwd(here)

# READ IN TRIALWISE OBSERVATIONS ... GEE USES LONG-FORMAT DATA
target.dir <- ("~/DOCUMENTS/ACADEMIA/02_NYU/THESIS/01_ANALYSIS/05_CLEAN/00_SEP/GEE/")
target.dir.files <- list.files(target.dir)
setwd(target.dir)

# EMPTY DF TO APPEND INTO
all.data <- data.frame()

for (file in target.dir.files) {
        
        temp <- read_csv(file)
        
        all.data <- dplyr::bind_rows(all.data, temp)
}

# CLEANUP GLOBAL ENVIRONMENT ... buh bye!
rm(temp, file, target.dir.files)

# TOTAL DF ... ALL OBSERVATIONS
small.kahuna <- all.data %>% dplyr::select(!c("X1", "PCOne", "PCTwo")) %>% na.omit()

# -------------------------------- TASK SPECIFIC SCALING -------------------------------- #

race.only <- small.kahuna %>%  filter(TASK == -.5) 
threat.only <- small.kahuna %>% filter(TASK == .5)

between_scale <- c("Response", "RT")

# SCALE VARIABLES AROUND 0
ian_rescale <- function(object) {
        
        temp <- scales::rescale(object, to = c(-.5, .5))
        
        return(temp)
}

for (var in between_scale) {
        
        race.only[, var] <- ian_rescale(race.only[, var])
        threat.only[, var] <- ian_rescale(threat.only[, var])
}

# JOIN DFs
small.kahuna <- dplyr::bind_rows(race.only, threat.only)

# -------------------------------- OTHER VAR SCALING -------------------------------- #

within_scale <- c("Exposure_latino", "Exposure_white", "SDO_score", "SECS_score", "age", "income")

for (var in within_scale) {
        
        small.kahuna[, var] <- ian_rescale(small.kahuna[, var])
}

# BLOCK
small.kahuna <- small.kahuna %>% mutate(BLOCK_scaled = as.numeric(ifelse(BLOCK == "CONTROL", -.5, .5)))

# POLITICAL ORIENTATION
small.kahuna$poli <- plyr::mapvalues(small.kahuna$poli, 
                               from = c("EXTREMELY_LIBERAL", "MODERATELY_LIBERAL", "SLIGHTLY_LIBERAL","NEITHER", "SLIGHTLY_CONSERVATIVE", 
                                        "MODERATELY_CONSERVATIVE", "EXTREMELY_CONSERVATIVE"),
                               to = as.numeric(c(-3, -2, -1, 0, 1, 2, 3)))

# GENDER
small.kahuna$gender <- plyr::mapvalues(small.kahuna$gender, 
                                 from = c("MALE", "DECLINE", "FEMALE"), 
                                 to = as.numeric(c(-.5, 0, .5)))

# EDUCATION
small.kahuna$education <- plyr::mapvalues(small.kahuna$education, 
                                    from = c("LessThanHighSchool", "HighSchool", "SomeCollege", "Associate", "Bachelor",
                                             "SomeGraduate", "master", "doctoral"),
                                    to = as.numeric(c(-4, -3, -2, -1, 1, 2, 3, 4)))

# RACE
small.kahuna$race <- gsub("¬†", "", small.kahuna$race)
small.kahuna$race <- plyr::mapvalues(small.kahuna$race,
                               from = c("Other", "Black", "Asian White", "White"),
                               to = as.numeric(c(-5, -.25, .25, .5)))



# -------------------------------- CLEAN IT UP -------------------------------- #

# DROP VARIABLES OF NO INTEREST
small.kahuna.clean <- small.kahuna %>%
        select(!c(BLOCK, FACES, "state", "zip"))

for (var in colnames(small.kahuna.clean)) {
        
        small.kahuna.clean[var] <- as.numeric(unlist(small.kahuna.clean[var]))
}

# RENAME VARIABLES FOR CLARITY
small.kahuna.clean <- small.kahuna.clean %>% 
        rename(Experimental.Condition = TASK,
               Trial.Block = BLOCK_scaled)

# SIM
small.kahuna <- small.kahuna %>% 
        rename(Experimental.Condition = TASK,
               Trial.Block = BLOCK_scaled)

# CLEAN UP ENVIRONMENT
rm(between_scale, within_scale, var, threat.only, race.only)

# -------------------------------- MODELING -------------------------------- #

mod.2 <- geeglm(Response ~ . + (Experimental.Condition * Trial.Block) -race, data = small.kahuna.clean,
                id = subjID, corstr = "exchangeable")

