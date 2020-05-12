import numpy as np

class TwoRegionModel:
    """
    Simple class that implements the equations given above
    and uses the solution method of Brakman et al. 2009
    """
    def __init__(self, 
            delta = 0.4,
            eps = 5,
            L = 1,
            phi = 0.5,
            sigma = 1e-4, max_iter = 10_000, verbose=1):
        self.delta = delta 
        self.eps = eps 
        self.L = L 
        self.phi = phi 
        self.sigma = sigma
        
        self.max_iter = max_iter
        self.verbose = verbose > 0
        
    def converged(self, c, p):
        return (c-p)/c < self.sigma
                
    def Y(self, w1, w2, lam):
        y1 = self.delta * lam * w1 + (1-self.delta)*self.phi
        y2 = self.delta * (1-lam) * w2 + (1-self.delta)*(1-self.phi)
        
        return y1, y2
    
    def W(self, y1, y2, i1, i2, T):
        i1_weight = np.power(i1, self.eps-1)
        i2_weight = np.power(i2, self.eps-1)
        T_weight = np.power(T, 1-self.eps) 
        
        w1 = np.power(y1*i1_weight + y2*i2_weight*T_weight, 1/self.eps)
        w2 = np.power(y1*i1_weight*T_weight + y2*i2_weight, 1/self.eps)
        
        return w1, w2
    
    def I(self, w1, w2, lam, T):
        rho = 1/(1-self.eps)
        
        w1_weight = np.power(w1, 1-self.eps)
        w2_weight = np.power(w2, 1-self.eps)
        T_weight = np.power(T, 1-self.eps)
        
        i1 = np.power(lam*w1_weight + (1-lam)*T_weight*w2_weight, rho)
        i2 = np.power(lam*w1_weight*T_weight + (1-lam)*w2_weight, rho)
        
        return i1, i2
    
    
    def solve(self, lam, T):
        """
        Solve the model for a given lambda and transportation cost.
        
        Returns a list of
        [(Wage 1, Wage 2), (Output 1, Output 2), (Income 1, Income 2), (Real wage 1, Real wage 2)]
        """
        i = 1
        w1 = 1.
        w2 = 1.
        
        while i < self.max_iter:
            y1, y2 = self.Y(w1, w2, lam)
            i1, i2 = self.I(w1, w2, lam, T)
            nw1, nw2 = self.W(y1, y2, i1, i2, T)
            
            if self.converged(nw1, w1) and self.converged(nw2, w2):
                if self.verbose:
                    print(f'Converged at iteration {i}')
                    
                real1 = nw1/np.power(i1, self.delta)
                real2 = nw2/np.power(i2, self.delta)
                
                solution = [
                    (nw1, nw2), (y1, y2), (i1, i2), (real1, real2)
                ]
                return solution
            
            w1 = nw1
            w2 = nw2
            
            i += 1
            if self.verbose: 
                print(f'Iteration: {i}/{self.max_iter}', end='\r')
        else:
            if self.verbose:
                print(f'Solution did not converge with {self.max_iter} iterations')
                
