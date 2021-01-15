using Combinatorics

subpowerset(a) = powerset(a, 1, length(a) - 1)

∑(coll) = isempty(coll) ? 0 : sum(coll)