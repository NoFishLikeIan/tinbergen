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
    ∑(Δ(G, T) / length(T) for T in powerset(G.N) if i ∈ T)
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
