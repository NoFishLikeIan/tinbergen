from typing import List
from .industry import Industry

class Circle:
    def __init__(self, cities: List[float], tau: float):
        self.cities = [c % 1 for c in cities]
        self.tau = tau
    

