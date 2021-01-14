struct Population
    f::Function
end

function getn(pop::Population) return length(pop.f(0)) end

function relatedeness(pop::Population, p::Float64)
    n = getn(pop)
    densities = pop.f(p)
    Pₐ = sum(i -> densities[i] * (i - 1) / n * (i - 2) / (n - 1), 1:n) / p

end

# Example
pop = Population(p -> [(1 - p)^2, 2p * (1 - p), p^2])