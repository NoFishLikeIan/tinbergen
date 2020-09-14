library(lpirfs)
library(ggplot2)
library(dplyr)

df <- read.csv("data/parsed_rz.csv", header=TRUE, row.names="t")

restr <- df %>% select("Y", "G", "NEWSY")

results <- lp_lin(restr,
                    lags_endog_lin = 4,
                    trend = 0,
                    shock_type = 1,
                    confint = 1.96,
                    hor = 20)



png(filename="plots/rz/irf.png",width = 465, height = 225, units='mm', res = 300)
plot(results)
dev.off()

high_un <- as.numeric(df["UN"] >= 6.5)
high_un[is.na(high_un)] <- 0.

results <- lp_nl(restr,
                    switching=high_un,
                    lags_endog_lin = 4,
                    lags_endog_nl = 1,
                    trend = 0,
                    shock_type = 1,
                    confint = 1.96,
                    use_logistic=FALSE,
                    lag_switching=FALSE,
                    hor = 20)

plot_regime <- function(results, i, file, title) {

    # Low regime
    s1_n_y <- results$irf_s1_mean[i, , 3]
    s1_n_y_lower <- results$irf_s1_low[i, , 3]
    s1_n_y_upper <- results$irf_s1_up[i, , 3]

    s2_n_y <- results$irf_s2_mean[i, , 3]
    s2_n_y_lower <- results$irf_s2_low[i, , 3]
    s2_n_y_upper <- results$irf_s2_up[i, , 3]

    upper = max(c(s1_n_y_upper, s2_n_y_upper)) + 0.2
    lower = min(c(s1_n_y_lower, s2_n_y_lower)) - 0.2

    png(filename=file, width = 465, height = 225, units='mm', res = 300)

    plot(s1_n_y, col="blue", type="l", ylim=c(lower, upper), xlim=c(1, 21), main = title, xlab="periods")   
    lines(s2_n_y, col="red")

    lines(s1_n_y_upper, col="blue", lty=2)
    lines(s1_n_y_lower, col="blue", lty=2)


    lines(s2_n_y_upper, col="red", lty=2)
    lines(s2_n_y_lower, col="red", lty=2)

    legend("topleft", legend=c("High Unemployment", "Low Unemployment"),
       col=c("red", "blue"), lty=1:1, cex=0.8)

    dev.off()
}

cum_resp <- function(results) {
    y_s1 <- results$irf_s1_mean[1, , 3]
    g_s1 <- results$irf_s1_mean[2, , 3]

    high_u <- mean(y_s1) / mean(g_s1)

    y_s2 <- results$irf_s2_mean[1, , 3]
    g_s2 <- results$irf_s2_mean[2, , 3]

    low_u <- mean(y_s2) / mean(g_s2)

    return(c(high_u, low_u))
}

plot_regime(results, 1, "plots/rz/NonY-regime.png", "IRF: NEWSY -> Y")
plot_regime(results, 2, "plots/rz/NonG-regime.png", "IRF: NEWSY -> G")

cum_resp_regi <- cum_resp(results)

print(cum_resp_regi)