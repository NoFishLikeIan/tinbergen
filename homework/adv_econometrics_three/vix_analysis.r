library(ggplot2)
library(xts)
library(tseries)
library(dplyr)
library(fracdiff)
library(forecast)
library(boot)


set.seed(11148705)

csv_to_xts <- function(path) {
    
    returns <- read.zoo(filepath, sep = ",", format = "%Y%m%d")
    
    X <- log(as.xts(returns))
    
    return(X)
}

autocorr <- function(vector, h) {
  n <- length(vector)
  vec_dem <- vector-mean(vector)
  
  prev <- vec_dem[1:(n-abs(h))]
  subs <- vec_dem[(1+abs(h)):n]
  
  rho_hat <- t(prev)%*%subs / t(vec_dem)%*%vec_dem
  
  
  return(rho_hat) 
} 

sample_acf <- function(series, hs) {
  vec <- as.vector(series)
  
  compute_autocorr <- function(h) autocorr(vec, h) 
  
  ac <- sapply(hs, compute_autocorr)
  
  return(ac)
}

ols <- function(y, X) {
  coeff <- solve(t(X)%*%X, t(X)%*%y)
  
  res <- y - X%*%coeff
  sigma_squared <- t(res)%*%res / (nrow(X) - ncol(X))
  
  varcov <- sigma_squared[1] * solve(t(X)%*%X)
  
  result <- list(coeff=coeff, res=res, sigma_squared=sigma_squared, varcov=varcov)
  
  return(result)
}

df_test <- function(series, orders=1:20) {
  
  n <- length(series)
  diffSeries <- diff(series)
  
  taus <- vector("list", length(orders))
  bics <- vector("list", length(orders))

  for (p in orders) {
    nregs <- 2+p
    y <- series[(nregs+1):n]
      
    ncol<-nregs
    nrow<-n-nregs
    
    X <- matrix(ncol=ncol,nrow=nrow)
    X[, 1] <- 1 # Add intercept
    X[, 2] <- series[nregs:(n-1)] # Add the X_{t-1} regressor
    
    for (j in 1:p) {
      X[, 2+j] <- diffSeries[(nregs-j):(n-1-j)] # Add the Delta X_{t-1} regressors
    }
    
    result <- ols(y, X)
    
    coeff <- result$coeff
    
    # Find the BIC value
    
    sigma_squared <- result$sigma_squared
    bic <- log(sigma_squared) + log(n)*nregs/n
    
    # Compute the t-statistic
    
    varcov <- result$varcov
    se <- sqrt(diag(varcov))[2]
    
    phi <- coeff[2]
    tau <- (phi-1)/se
    
    taus[[p]] <- tau
    bics[[p]] <- bic
  }
  
  min_bic <- which.min(bics)
  
  statistic = taus[[min_bic]]
  
  return(statistic)
}
  


spectral_dens <- function(X, l=NULL) {
  n <- length(X)
  hs <- as.vector((1-n):(n-1))
  
  corrs <- sample_acf(X, hs)
  
  w_bar_filter <- function (h) if (abs(h) < l) 1 - abs(h)/(l+1) else 0
  
  weights <- if (!is.null(l)) sapply(hs, w_bar_filter) else rep(1, length(hs))
  
  dens <- function(lambda) {
    cosines <- cos(lambda*hs)
    f_hat <- sum(weights*corrs*cosines)
    return (f_hat / (2*pi))
  }
  
  return (dens)
}

GPH <- function(vec, skip_first=3, test=FALSE) {
  
  m <- trunc(sqrt(n))
  density_space <- sapply((skip_first+1:m), function(j) (2*pi*j)/n)
  
  dens_fn <- spectral_dens(dX, l=NULL)
  
  estimated_dens <- sapply(density_space, dens_fn)
  
  y <- log(estimated_dens)
  
  X <- matrix(nrow=length(y), ncol=2)
  X[, 1] <- 1
  X[, 2] <- log(2*sin(0.5*density_space))
  
  result <- ols(y, X)
  
  b <- result$coeff[2]
  d <- -0.5*b
  
  if (test) {
    varcov <- result$varcov
    b_var <- diag(varcov)[2]
    d_se <- sqrt(b_var*0.5^2)
    
    t_stat = d/d_se
    
    print(paste("The t-statistic of the parameter d is", t_stat, sep=": "))
  }
  
  return(d)
}

evaluate_arfima <- function(dX) {
  vec <- as.vector(dX)
  
  fitted <- arfima(vec, drange=c(-0.5, 0), estim="mle")
  d <- fitted$d
  

  frac_dX <- diffseries(vec, d)

  results = list(series=frac_dX, d=d, fit=fitted)

  return(results)
}

bootstrap_std_arfima <- function(dX) {
  vec_dx <- dX
  
  estimate <- function(formula, data, indices) {
    
    d <- data[indices] 
    fit <- arfima(d, drange=c(-0.5, 0), estim="mle")
    return(coef(fit))
    
  }
  
  results <- boot(data=vec_dx, statistic=estimate, R=1000)
  
  return(results)
}

plot_density <- function(dens_fn) {
  
  density_space <- seq(0, 2*pi, length.out=n)
  estimated_dens <- sapply(density_space, dens_fn)
   
  df <- data.frame(lambda=density_space, f_estimated_density=estimated_dens)
  
  p <- ggplot(data=df, aes(lambda, f_estimated_density)) + geom_line()
  
  return(p)
} 



main <- function() {
  
  script_dir <- dirname(sys.frame(1)$ofile)
  filepath <- file.path(script_dir, "data", "vix_data.csv")
  X <- csv_to_xts(filepath)
  dX <- na.trim(diff(X))
  
  # --- Exercise 2
  
  tau <- df_test(X)
  
  outcome <- if (tau < -2.86) "reject" else "do not reject"
  
  print(paste("Results of DF test on X: we", outcome, "with a t-statistic of", tau))
  
  # --- Exercise 4
  
  l <- 33
  
  dens_fn <- spectral_dens(dX, l)
  
  p <- plot_density(dens_fn)
  
  print(p)
  
  # --- Exercise 4
  
  d_hat <- GPH(dX, test=TRUE)
  
  print(paste("The estimated fractional difference parameter (of dX) is d", d_hat, sep=": "))
  
  # # --- Exercise 5
   
  results <- evaluate_arfima(dX)
  
  frac_dX <- results$series
  d_hat <- results$d
  
  dens_fn <- spectral_dens(frac_dX, l)
  p <- plot_density(dens_fn)
  print(p)
  
  bootstrap_results <- bootstrap_std_arfima(dX)

  
  # # --- Exercise 6
  
  fit <- results$fit

  res <- residuals(fit)
  
  print(paste("Estimated d: ", results$d))
  
  jb <- jarque.bera.test(res)
  
  outcome <- if (jb$p.value < 0.05) "rejects" else "does not reject"
  
  print(paste("The test", outcome, "the null hypothesis that the residuals are normally distributed"))


}



# if __name__ == "__main__":
    # main()
  