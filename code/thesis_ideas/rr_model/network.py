import networkx as nx
import numpy as np
from itertools import permutations

from typing import List, NoReturn, Tuple, Iterable

from .model import Industry


class Network:
    def __init__(self, nodes: List[Industry], d_matrix: np.array):

        self.n = len(nodes)
        self.nodes = nodes

        for supp, to in permutations(range(self.n), 2):
            dep = d_matrix[supp, to]

            if dep != 0:
                self.nodes[to].add_supplier(
                    self.nodes[supp],
                    dep
                )

        self.G = nx.from_numpy_array(
            d_matrix, create_using=nx.DiGraph)

    def __getitem__(self, item):
        return self.nodes[item]

    def __len__(self):
        return len(self.nodes)

    @property
    def sources_index(self) -> Iterable[int]:

        indices = (node for node, indegree in self.G.in_degree(
            self.G.nodes()) if indegree == 0)

        return indices

    @property
    def sources(self) -> Iterable[Industry]:
        return (self.nodes[i] for i in self.sources_index)

    def step(self) -> NoReturn:
        nodes = list(self.sources_index)

        while len(nodes) > 0:
            idx = nodes.pop(0)
            self.nodes[idx].step()

            nodes += [succ for succ in self.G.successors(idx)]

    def bring_to_steady(self, verbose=False, iters=150) -> NoReturn:
        for i in range(iters):
            if verbose:
                print(f'{i+1}/{iters}', end='\r')

            self.step()
