library(tidyverse)
library(geepack)
library(scales)
library(psych)
library(ez)
library(readxl)
library(reshape2)

here <- "~/DOCUMENTS/ACADEMIA/02_NYU/THESIS/01_ANALYSIS/05_CLEAN/"
setwd(here)
data <- read_excel("02_bigKahuna.xlsx")


# ----------------------- CONVERT DATA ---------------------- #

big.dog <- data %>% 
        dplyr::select(ID, Exposure_latino, Exposure_white, SDO_score, SECS_score, age, education, gender, income, poli, race, state, BLOCK, contains("CORR")) %>% 
        na.omit()

# SELECT KEY VARIABLES TO USE IN ANOVA ... MELT DATA BY ID AND BLOCK (TWO ROWS / PARTICIPANT == ONE ROW / TASK)
small.dog <- big.dog %>% 
                select(ID, CORR_num_race, CORR_num_threat, BLOCK) %>%
                mutate(FZ_num_race = fisherz(CORR_num_race), FZ_num_threat = fisherz(CORR_num_threat)) %>% 
                select(!contains("CORR")) %>% 
                melt(id.vars = c("ID", "BLOCK")) %>% 
                rename("Condition" = BLOCK,
                       "Block" = variable)


# ----------------------- ANOVA ---------------------- #

there <- paste0(here, "/49_PLOTS/")
setwd(there)

# TREAT ID AND CONDITION AS CATEGORICAL FACTORS
small.dog$ID <- as.factor(small.dog$ID)
small.dog$Condition <- as.factor(small.dog$Condition)

# RUN EZ ANOVA WITH BLOCK AS WITHIN VAR + CONDITION AS BETWEEN VAR
options(digits = 10)
ok.boomer <- ezANOVA(data = small.dog, 
                     dv = .(value), 
                     wid = .(ID), 
                     within = .(Block), 
                     between = .(Condition), 
                     return_aov = T, detailed = T)

# WRITE ANOVA RESULTS TO TABLE
apaTables::apa.ezANOVA.table(ok.boomer, table.title = "ANOVA Results", table.number = 1, filename = "ANOVA.doc")
       
# CONFIRM MAIN EFFECT WITH BONFERRONI POST-HOC
bonf.correction <- pairwise.t.test(x = clean.data$value, g = clean.data$Block, p.adjust.method = "bonf")    

# WRITE FORMATTED RESULTS TO MEAN / SD TABLE
pretty <- small.dog
pretty$Condition <- recode_factor(pretty$Condition, "EXPERIMENTAL" = "Experimental", "CONTROL" = "Control")
pretty$Block <- recode_factor(pretty$Block, "FZ_num_race" = "Race Task", "FZ_num_threat" = "Threat Task")
apaTables::apa.2way.table(data = pretty, iv1 = Block, iv2 = Condition, dv = value, show.conf.interval = T, filename = "TwoByTwo.doc")
        
