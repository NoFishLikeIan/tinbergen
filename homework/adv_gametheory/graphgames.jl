struct Graph
    N::Array{Int}
    v::Function
    L::Array{Tuple{Int,Int}}
end

function getdineigh(G::Graph)
    neigh = [[] for i in G.N]

    for (from, to) in G.L
        push!(neigh[from], to)
    end

    return neigh
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

function degree(args...)
    length.(getneigh(args...))
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

function harsanyidegree(G::Graph)
    game = graphtoMyerson(G)
    ϕ = zeros(Rational, length(G.N))

    for S in powerset(G.N)
        ds = degree(G, S)
        dsum = sum(ds)
        if dsum == 0 continue end

        Δ_S = Δ(game, S)

        for i in S
            ϕ[i] += (Δ_S * ds[i]) // dsum
        end

    end


    return ϕ
end