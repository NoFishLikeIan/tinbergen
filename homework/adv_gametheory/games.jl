struct Game
    N::Array{Int}
    v::Function
end

function valuemapping(G::Game)
    return ((S, G.v(S)) for S in powerset(G.N))
end

"""
Tests the convexity of the game
"""
function isconvex(G::Game)
    v = G.v
    for (T, S) in combinations(collect(powerset(G.N)), 2)
        if v(S ∪ T) + v(S ∩ T) < v(S) + v(T)
            return false
        end
    end

    return true
end

"""
Use polyhedra representation of system of inequality to 
find core of the game  
"""
function getcore(G::Game)
    N, v = G.N, G.v
    if length(N) != 3 throw("Core implemented only for N = 3!") end

end