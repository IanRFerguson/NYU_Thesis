# RUN FIRST GEE TO GET SCALED VARIABLES
source("01_GEE.R")

# -------------------------------- GEOMODELING -------------------------------- #

# RECODE TYPOS
small.kahuna$state <- recode(small.kahuna$state, "MARKETING" = "MARYLAND")
small.kahuna$state <- recode(small.kahuna$state, "LLLINOIS" = "ILLINOIS")

# DROP BAD OBSERVATION
small.kahuna <- small.kahuna %>% filter(state != "UNITED STATES")

# CONVERT STATE VAR TO FACTOR
small.kahuna$state <- as.factor(small.kahuna$state)

# DROP VARS OF NO INTEREST
small.kahuna <- small.kahuna %>% 
        dplyr::select(!c(FACES, zip, BLOCK))

tar.vars <- small.kahuna %>% select(!state) %>% colnames()

for (var in tar.vars) {
        
        small.kahuna[var] <- as.numeric(unlist(small.kahuna[var]))
}

# RUN GEE
mod.statewse <- geeglm(Response ~ . + (Experimental.Condition * Trial.Block) -race, data = small.kahuna,
                       id = state, corstr = "exchangeable")

rip.city <- tidy(mod.statewse)
setwd("~/DOCUMENTS/ACADEMIA/02_NYU/THESIS/01_ANALYSIS/05_CLEAN/")

# PUSH TO CSV ... We'll need this to plot in Python
write.table(rip.city, "RIP_City.csv", sep = "\t")
