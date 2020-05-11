def logit(lam):
    return lambda x: lam*x*(1-x)
