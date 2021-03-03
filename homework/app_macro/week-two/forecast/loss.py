import numpy as np

from sklearn.metrics import make_scorer

def make_quad_loss(alpha: float, scorer = False):
    
    def p_quad_loss(y_hat: np.ndarray, y: np.ndarray) -> np.float:
        e = y_hat - y
        sqr = np.square(e)

        return -np.sum(np.where(e < 0, (1-alpha)*sqr, alpha*sqr))

    if scorer:
        return make_scorer(p_quad_loss)
    else:
        return p_quad_loss