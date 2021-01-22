using JuMP, GLPK
using LinearAlgebra

isconnected(S) = S == collect(minimum(S):maximum(S))

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
        if isempty(S) || !isconnected(S) return 0. end

        x̄ₛ = findoptx(c[S], e[S])

        return c[S]'x̄ₛ
    end

    return Graph(N, v, L)
end
