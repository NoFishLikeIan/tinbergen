import numpy as np

np.random.seed(11148705)


n = 2000
k = 6
sigma = 0.25
l = 1

X = np.random.randn(n, k)
betas = np.random.randint(-10, 10, k)
