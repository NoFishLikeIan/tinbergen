using JuMP, GLPK
using LinearAlgebra

isconnected(S) = sort(S) == collect(minimum(S):maximum(S))

function getsubconnected(S::Array{Int})::Array{Array{Int,1},1}
    S′ = [[]]

    for (j, i) in enumerate(S)
        if j == 1 
            push!(S′[end], i) 
        else
            if (i != last(S′[end]) + 1) push!(S′, []) end
            push!(S′[end], i)
        end
    end
    
    return S′
end

function findoptx(c::Vector{Float64}, e::Vector{Float64})
    n = length(c)
    model = Model(GLPK.Optimizer)

    A = LowerTriangular(ones(n, n))

    @variable(model, x[1:n] ≥ 0)
    @objective(model, Max, c'x)
    @constraint(model, A * x .≤ A * e)

    optimize!(model)

    return value.(x)
end

function makeriver(c::Vector{Float64}, e::Vector{Float64})
    x̄ = findoptx(c, e)

    N = collect(1:length(c))
    L = [(i, i + 1) for i in 1:N[end - 1]]

    v(r::UnitRange{Int64}) = v(collect(r))
    v(n::Array{Any,1}) = isempty(n) ? 0 : v(S)
    v(n::Int) = v([n])

    function v(S::Array{Int})
        # Normalized via c'x - c'e?
        S = sort(S)
        if S == N return c'x̄ end
        if isempty(S) return 0. end

        if !isconnected(S)
            return sum(v(E) for E in getsubconnected(S))
        end

        x̄ₛ = findoptx(c[S], e[S])

        return c[S]'x̄ₛ
    end

    return Graph(N, v, L)
end

function marginalvector(R::Graph)
    n = last(R.N)

    mᵘ = [ R.v(1:i) - R.v(1:(i - 1)) for i in R.N ]

    mˡ = reverse([ R.v(i:n) - R.v((i + 1):n) for i in reverse(R.N) ])

    fᵉ = @. (mᵘ + mˡ) / 2

    return mᵘ, mˡ, fᵉ
end