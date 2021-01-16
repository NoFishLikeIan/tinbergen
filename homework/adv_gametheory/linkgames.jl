struct Link
    N::Array{Tuple{Int,Int}}
    v::Function
end

function graphtolink(G::Graph)
    N = G.L

    rˡ(S::Tuple{Int,Int}) = rˡ([S])
    function rˡ(S::Array{Tuple{Int,Int}})
        L′ = filter(edge -> edge ∈ S, G.L)
        myersonG = graphtoMyerson(Graph(G.N, G.v, L′))

        return myersonG.v(myersonG.N)
    end

    return Link(N, rˡ)
end

function πˡ(graph::Graph)
    link = graphtolink(graph)
    N = collect(1:length(link.N))

    v(S::Int) = v([S])
    function v(S::Array{Int})
        E = link.N[S]
        return link.v(E)
    end

    edgevalue = fₛ(Game(N, v))
    positionvalue = zeros(Rational, length(graph.N))

    for (l, edge) in enumerate(link.N)
        (i, j) = edge
        positionvalue[i] += edgevalue[l] // 2
        positionvalue[j] += edgevalue[l] // 2
    end

    return positionvalue
end