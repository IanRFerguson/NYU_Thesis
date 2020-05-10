here <- "~/DOCUMENTS/ACADEMIA/02_NYU/THESIS/01_ANALYSIS/05_CLEAN/01_SCRIPTS/"
setwd(here)
source("02_SETUP.R")

library(psych)
library(ggridges)
library(praise)

# -------------------------- COVARIATES -------------------------- #

covar <- big.kahuna %>% 
        dplyr::select(BLOCK, SDO_score, SECS_score) %>% 
        mutate(SC_us = (SDO_score + SECS_score) / 2)

covar$SDO_score <- scale(covar$SDO_score)
covar$SECS_score <- scale(covar$SECS_score)
covar$SC_us <- scale(covar$SC_us)

covar %>% 
        melt() %>% 
        na.omit() %>% 
        ggplot(aes(x = value, y = variable, fill = BLOCK)) +
        geom_density_ridges(scale = 1.75, alpha = 0.5) +
        scale_y_discrete(expand = c(0, 0), labels = c("SDO Score", "SECS Score", "Conservatism Score")) +     
        scale_x_continuous(expand = c(0, 0), labels = ) +   
        coord_cartesian(clip = "off") +
        theme_ridges() +
        scale_fill_manual(labels = c("Control", "Experimental"), values = bad.boys.only) +
        labs(x = "", y = "", 
             title = "", fill = "Experimental Condition") +
        theme(plot.title = element_text(hjust = 0.5, vjust = 1))




