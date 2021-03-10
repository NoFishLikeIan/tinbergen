using Base.Threads
using StatsBase

include("utils/plot.jl")

Σ = collect(1:10) 

b = 1

p(Q, N) = (N + 1) * mean(Σ) - b * sum(Q)

function Π(Q, N)
    price = p(Q, N)
    return Q .* price
end

function computepayoffs(groups)
    M, N = size(groups)
    pay = similar(groups)

    for m in 1:M
        Q = groups[m, :]
        pay[m, :] =  Π(Q, N)
    end

    return pay
end

function evolvegroups(groups, pay)
    M, N = size(groups)
    next = copy(groups)

    for m in 1:M
        profit = pay[m, :]
        soft = profit .- minimum(profit)
        prob = soft ./ sum(soft)

        i = sample(1:N, pweights(prob)) # Weighted birth
        j = sample(1:N) # Random death

        next[m, j] = next[m, i]
    end

    return next
end

function evolvegame(groups, pay)
    M, N = size(groups)
    p̄ = mean(pay, dims=2)

    death = sample(1:M)

    lower = death == 1 ? M : death - 1
    upper = death == M ? 1 : death + 1

    groups[death, :] = p̄[lower] > p̄[upper] ? groups[lower, :] : groups[upper, :]

    return groups

end

function evolve(M, N; T=100, swapgroup=0.0)    
    evolution = zeros(M, N, T)
    evolution[:, :, 1] = rand(Σ, (M, N))

    for t in 2:T
        pay = computepayoffs(evolution[:, :, t - 1])
        next = evolvegroups(evolution[:, :, t - 1], pay)

        if rand() < swapgroup
            next = evolvegame(next, pay)
        end

        evolution[:, :, t] = next
    end

    return evolution

end

M, N, T = 5, 10, 30
evolutions = evolve(M, N, T=T, swapgroup=1.)

plotpayoffs(evolutions, computepayoffs)
plotquantities(evolutions)
plotgroupquantities(evolutions[1, :, :])