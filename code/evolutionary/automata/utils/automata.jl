struct Strategy
    Σ::Space
    X::Play
end

function evolve(A::Strategy, B::Strategy)
    Σₐ, Xₐ = A.Σ, A.X
    Σᵦ, Xᵦ = B.Σ, B.X

    function step(α::State, β::State)

        α′ = similar(α)
        β′ = similar(β)

        @einsum α′[k] = α[i] * Xₐ[i, j, k] * Σᵦ[l, j] * β[l]
        @einsum β′[k] = β[i] * Xᵦ[i, j, k] * Σₐ[l, j] * α[l]

        return (α′, β′)

    end
    return step

    function step(t::Tuple{State,State})
        return step(t...)
    end

end