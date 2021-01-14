using Combinatorics

# using LazySets, Polyhedra

subpowerset(a) = powerset(a, 1, length(a) - 1)

∑(coll) = isempty(coll) ? 0 : sum(coll)

struct Game
    N::Array{Int}
    v::Function
end

function valuemapping(G::Game)
    return ((S, G.v(S)) for S in powerset(G.N))
end

"""
Harsanyi dividends for S ⊂ N
"""
function Δ(G::Game, S::AbstractArray{Int})
    G.v(S) - ∑(Δ(G, T) for T in subpowerset(S))
end

"""
Shapey value using Harsanyi dividends
"""
function fₛⁱ(G::Game, i::Int)
    ∑(Δ(G, T) / length(T) for T in powerset(N) if i ∈ T)
end

"""
Shapey value using permutations
"""
function fₛ(G::Game)
    Π = permutations(G.N)
    f_shapey = zeros(Int, length(G.N))

    for perm in Π
        m_π = copy(perm)
        for (i, s) in enumerate(perm)
            m_π[s] = G.v(perm[1:i]) - G.v(perm[1:i - 1])
        end
        f_shapey += m_π
    end

    return [fᵢ // length(Π) for fᵢ in f_shapey]
end


function isconvex(G::Game; verbose=false)
    v = G.v
    for (T, S) in combinations(collect(powerset(G.N)), 2)
        print("S=$S, T=$T:", v(S ∪ T), "+", v(S ∩ T), " > ", v(S), "+", v(T), "\n")
        if v(S ∪ T) + v(S ∩ T) < v(S) + v(T)
            if verbose print("Failed for $S and $T\n") end
            return false
        end
    end

    return true
end

# Polyhedra A matrix
A = [
    1 0 0;
    0 1 0;
    0 0 1;
    1 1 0;
    1 0 1;
    0 1 1;
    1 1 1
]

"""
Use polyhedra representation of system of inequality to 
find core of the game  
"""
function getcore(G::Game)
    N, v = G.N, G.v
    if length(N) != 3 throw("Core implemented only for N = 3!") end

    b = [v(1), v(2), v(3), v([1, 2]), v([1, 3]), v([2, 3]), v(N)]
    p = polyhedron(Polyhedra.hrep(A, b))

end