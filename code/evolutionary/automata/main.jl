using LinearAlgebra
using Einsum, Tensors

Space = AbstractMatrix{Int64}
State = AbstractVector{Int64}
Play = AbstractArray{Int64,3}


include("utils/matrix.jl")
include("utils/automata.jl")

G = Strategy(
    [1 0; 0 1], # (C, D)
    X(
        [1 0; 0 1], # (C × y) -> y  
        [0 1; 0 1] # (D × y) -> D
    )
)

Y = Strategy(
    [0 1; 0 1; 1 0], # (D, D′, C)
    X(
        [0 1 0; 0 0 1], # (D × C) -> D′, (D × D) -> C
        [0 1 0; 0 1 0], # (D′ x y) -> D′
        [0 0 1; 0 0 1]  # (C × y) -> C 
    )
)

global α = [1, 0] # Start by cooperating 
global β = [1, 0, 0] # Start by defecting 

Γ = [2 0; 3 1] # Payoff matrix

step = evolve(G, Y)

for t in 1:20

    π_G = (G.Σ'α)' * Γ * (Y.Σ'β)
    π_X = (G.Σ'α)' * Γ' * (Y.Σ'β)

    print("
        G$(G.Σ'α)=$(π_G), X$(Y.Σ'β)=$(π_X)\n
    ")

    α, β = step(α, β)
end