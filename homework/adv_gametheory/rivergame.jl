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
