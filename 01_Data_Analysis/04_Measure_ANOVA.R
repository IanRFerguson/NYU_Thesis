library(tidyverse)
library(ez)
library(apaTables)
library(readxl)
library(reshape2)

here <- "~/DOCUMENTS/ACADEMIA/02_NYU/THESIS/01_ANALYSIS/05_CLEAN/"
setwd(here)
data <- read_excel("02_bigKahuna.xlsx")

# SELECT TARGET VARIABLES
demographics <- data %>% select(ID, BLOCK, SDO_score, SECS_score)

# Z TRANSFORM CONSERVATISM MEASURES TO ACCOUNT FOR BETWEEN-MEASURE VARIANCE
demographics <- demographics %>% 
        mutate(CCS = (SDO_score + SECS_score) / 2)  %>%
        mutate(SDO_z = scale(SDO_score),
               SECS_z = scale(SECS_score),
               CCS_z = scale(CCS)) %>% 
        select(!c(SDO_score, SECS_score, CCS_z)) %>% 
        na.omit()

# GROUP BY PARTICIPANT AND BLOCK ... THREE ROWS PER PARTICIPANT
demo.melt <- demographics %>% melt(id.vars = c("ID", "BLOCK"))

# RUN RM ANOVA
demo.aov <- ezANOVA(demo.melt, dv = .(value), 
                    between = .(BLOCK), 
                    within = .(variable), 
                    wid = .(ID), detailed = T, return_aov = T)

# OUTPUT CLEAN ANOVA TABLE
setwd(paste0(here, "/49_PLOTS/"))
apaTables::apa.ezANOVA.table(ez.output = demo.aov, table.title = "Conservatism ANOVA", table.number = 1, filename = "CONS_ANVOA.doc")
