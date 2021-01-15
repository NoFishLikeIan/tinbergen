
function findpath!(
    path::Array{Int}, neighs, 
    from::Int, to::Int)

    push!(path, from)
    neighbours = neighs[from]

    if isempty(neighbours) return 
    elseif to ∈ neighbours
        push!(path, to)
        return path
    end

    for n in filter(n -> n ∉ path, neighbours)
        res = findpath!(path, neighs, n, to)
        if !isnothing(res) return res end
    end

    pop!(path) 
end

function findpath(G::Graph, from::Int, to::Int)
    neighs = getneigh(G)
    path = Int[]
    res = findpath!(path, neighs, from, to)
    if isnothing(res) return [] 
    else return path end
end

function finddipath(G::Graph, from::Int, to::Int)
    neighs = getdineigh(G)
    path = Int[]
    res = findpath!(path, neighs, from, to)
    if isnothing(res) return []
    else return path end
end

function Lⁱ(G, i)  
    subset = []
    for (j, h) in G.L
        if j ∈ findpath(G, i, h)
            push!(subset, (j, h))
        elseif h ∈ findpath(G, i, h)
            push!(subset, (h, j))
        end
    end
    
    return subset
end

"""
Assumes a cycle-free graph 
"""
function followers(G::Graph)
    F(j) = [h for (k, h) in G.L if k == j]
    return F
end

function subordinate(G::Graph)

    F(j) = [h for (_, h) in Lⁱ(G, i) if !isempty(finddipath(G, h, j))]
    
    return F
end

function hⁱ(mG::Graph, i::Int)
    G = Graph(mG.N, mG.v, Lⁱ(mG, i))

    F̂ = subordinate(G)
    F̅ = followers(G)

    return [G.v(F̂(j)) - ∑(G.v(F̂(h)) for h in F̅(j)) for j in G.N]
end 