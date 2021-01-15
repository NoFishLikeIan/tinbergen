struct Graph
    N::Array{Int}
    v::Function
    L::Array{Tuple{Int,Int}}
end

function getneigh(G::Graph)
    neigh = [[] for i in G.N]

    for (from, to) in G.L
        push!(neigh[from], to)
        push!(neigh[to], from)
    end

    return neigh
end

function getneigh(G::Graph, S::Array{Int})
    neigh = [[] for i in G.N]

    for (from, to) in G.L
        if from ∈ S && to ∈ S 
            push!(neigh[from], to) 
            push!(neigh[to], from)
        end
    end

    return neigh
end


function isvalidpath(G::Graph, path::Array{Int})
    neigh = getneigh(G)

    for (j, from) in enumerate(path[1:end - 1])
        to = path[j + 1]
        if to ∉ neigh[from]
            return false
        end
    end      
    
    return true
end

function traversefrom!(search::Array{Int}, neighbours, node::Int)
    if node ∉ search push!(search, node) end

    notvisited = filter(n -> n ∉ search, neighbours[node])

    for neigh in notvisited
        traversefrom!(search, neighbours, neigh)
    end
end

function traversefrom(neighbours, node::Int)
    search = Int[]
    traversefrom!(search, neighbours, node)
    return search
end


function getcomponents(G::Graph, S::Array{Int})
    subneigh = getneigh(G, S)
    comps = []

    for (j, node) in enumerate(S)
        notincomp = isnothing(
            findfirst(comp -> node ∈ comp, comps))

        if notincomp 
            push!(comps, traversefrom(subneigh, node))
        end
    end

    return comps    
end

function graphtoMyerson(G::Graph)::Game
    vL(S::Array{Int}) = ∑(G.v(T) for T in getcomponents(G, S))
    return Game(G.N, vL)
end

μ(G::Graph) = fₛ(graphtoMyerson(G))