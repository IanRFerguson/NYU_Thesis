here <- "~/DOCUMENTS/ACADEMIA/02_NYU/THESIS/01_ANALYSIS/05_CLEAN/01_SCRIPTS/"
setwd(here)
source("00_SETUP.R") # SCRIPT LOCATED IN ../DATA_ANALYSIS DIRECTORY FYI

library(cowplot)

# PLOT LINEAR TRENDS FOR RESPONSES IN RACE TASK
plt.RACE <- big.kahuna.clean %>% 
                dplyr::select(contains(c("NUM_race", "BLOCK")) & !contains(c("CORR", "FISHER"))) %>%
                melt() %>% 
                mutate(faces = as.numeric(gsub("_NUM_race", "", variable))) %>% 
                ggplot(aes(x = faces, y = value, fill = BLOCK)) +
                geom_smooth(method = "lm", color = "black", size = 0.5, linetype = "dotted") +
                scale_fill_manual(values = bad.boys.only) +
                theme_minimal() +
                labs(x = "Number of Latinos in Ensemble",
                     y = "Average Number of Latino Faces Reported",
                     title = "Race Task",
                     fill = "Experimental Condition") +
                coord_cartesian(ylim = c(4, 7), xlim = c(0, 11.5)) +
                theme(plot.title = element_text(hjust = 0.5, face="bold"))
        

# PLOT LINEAR TRENDS FOR RESPONSES IN THREAT TASK
plt.THREAT <- big.kahuna.clean %>% 
                dplyr::select(contains(c("NUM_threat", "BLOCK")) & !contains(c("CORR", "FISHER"))) %>% 
                melt() %>% 
                mutate(faces = as.numeric(gsub("_NUM_threat", "", variable))) %>% 
                ggplot(aes(x = faces, y = value, fill = BLOCK)) +
                geom_smooth(method = "lm", color = "black", size = 0.5, linetype = "dotted") +
                scale_fill_manual(values = bad.boys.only) +
                theme_minimal() +
                labs(x = "Number of Latinos in Ensemble",
                     y = "Average Threat Response (4 = Neutral)",
                     title = "Threat Task",
                     fill = "Condition") +
                coord_cartesian(ylim = c(4, 5), xlim = c(0, 11.5)) +
                theme(plot.title = element_text(hjust = 0.5, face="bold"))

# MERGE PLOTS INTO ONE FIGURE (see: subplots in Python)
prow <- plot_grid(
        plt.RACE + theme(legend.position = "none"),
        plt.THREAT + theme(legend.position = "none"),
        hjust = -5,
        nrow = 1,
        align = "vh"
)

# ISOLATE LEGEND FROM EITHER PLOT
plegend <- get_legend(plt.RACE +
                              guides(guide_legend(nrow = 1)) +
                              theme(legend.position = "bottom"))

plot_grid(prow, plegend, ncol = 1, rel_heights = c(1, .1))





