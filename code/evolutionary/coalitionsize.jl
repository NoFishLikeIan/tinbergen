using Plots
using Printf

function makerecurisve(M, N, ρ)
    function EN(t)
        if t == 0 return N end

        C = N * M / (M - t)
        
        return (1 - ρ) * EN(t - 1) + ρ * C
    end

    return EN
end

M, N = 10, 5

ρs = [0.0, 0.1, 0.2, 0.5, 1.0]
aρ = 0.1

ts = M - 1

plot(
    title="Expected group size for a given ρ | M=$M, N=$N", 
    xaxis="t", yaxis="E[Nₜ]", legend=:topleft, dpi=200)

for ρ in ρs
    EN = makerecurisve(M, N, ρ)
    Nₜ = EN.(1:ts)

    plot!(1:ts, Nₜ, label="ρ=$(@sprintf("%.2f", ρ))", dpi=200)
end

savefig("plots/expected.png")


function makeanalytical(M, N, ρ)
    function EN(t)
        if t == 1 return N end

        first = N * (1 - ρ)^t

        Σ = sum(
            (1 - ρ)^i / (M - t + i)
            for i in 0:(t - 1)
        )

        second = ρ * N * M * Σ

        return first + second
    end

    return EN
end


ρ = .5
EN_an = makeanalytical(M, N, ρ)
EN_re = makerecurisve(M, N, ρ)

EN_re.(1:ts)
EN_an.(1:ts)