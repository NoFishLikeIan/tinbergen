using DifferentialEquations
using Plots

function noncoop(p, n)
    sum(((1 - p)^(n - 1) * p^(i - 1) * binomial(n, n - i) * i / n for i in 1:(n - 1)))
end

ṗ(p, n) = p * (1 - p) * (p^(n - 1) - noncoop(p, n))

function solvecoop(n::Int, p0::Float64; tspan=(0.0, 1.0))
    
    function system!(dp, x, ρ, t)
        p = x[1]
        n = ρ[1]
        dp[1] = p * (1 - p) * (p^(n - 1) - noncoop(p, n))
    end
    
    prob = ODEProblem(system!, [p0], tspan, [n])

    sol = solve(prob, Tsit5(), reltol=1e-8, abstol=1e-8)

    return sol
end

# Plotting
ps = range(.001, 1., length=100)

plot(title="ṗ(p, n)", yaxis="ṗ", xaxis="p", dpi=300, legend=:topleft)
hline!([0.], linecolor=:black, linestyle=:dot, label=false)

for n in [3, 10, 30, 40, 50]
    plot!(ṗ.(ps, n), label="n = $n")
end

savefig("plots/pdot.png")

n = 20
plot(title="Reproduction dynamics in cooperation game, ṗ", xaxis="t", yaxis="p(t)")

for p0 in range(.2, .9; step=.1)
    sol = solvecoop(n, p0)
    plot!(sol, label="p0=$p0")
end

savefig("plots/sol.png")

