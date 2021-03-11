using Base.Threads, Random
using StatsBase
using IterTools

Random.seed!(1122)

include("utils/plot.jl")
include("utils/coord.jl")
include("stability.jl")

Σ = collect(1:10) 

b = 1
Σ′(N) = (N + 1) * mean(Σ) * maximum(Σ) # Maximum profits
p(Q, N) = (N + 1) * mean(Σ) - b * sum(Q)


function Π(Q)
    N = length(Q)
    price = p(Q, N)
    return Q .* price
end

function computepayoffs(groups)
    M, N = size(groups)
    pay = zeros(Float64, M, N)

    @threads for m in 1:M
        Q = groups[m, :]
        pay[m, :] =  Π(Q)
    end

    return pay
end

function evolvegroups(groups, pay, coalitions)
    M, N = size(groups)
    next = copy(groups)

    @threads for c in nonempty(coalitions)
        C = length(c)
        profit = pay[c, :]
        soft = @. exp(profit / Σ′(N))
        prob = vec(soft ./ sum(soft))

        i = sample(1:(N * C), pweights(prob)) # Weighted birth
        j = sample(filter(!=(i), 1:(N * C))) # Random death excluded i

        next[coordloop(j, N, c)...] = next[coordloop(i, N, c)...]
    end

    return next
end

function evolvegame(coalitions, pay)
    newcoal = copy(coalitions)
    C = length(coalitions)

    profit = mean(pay, dims=2)
    cprofit = [mean(profit[c]) for c in coalitions]
    
    c = sample(1:C)

    lower = c == 1 ? C : c - 1
    upper = c == C ? 1 : c + 1

    ctakeover =  cprofit[lower] > cprofit[upper] ? lower : upper # Join with lowest profitable market

    newcoal[c]  = vcat(coalitions[c], coalitions[ctakeover])
    newcoal[ctakeover] = []
    
    return newcoal

end

function evolve(M, N; T=100, swapgroup=0.0)    
    evolution = zeros(Int64, M, N, T)
    evolution[:, :, 1] = rand(Σ, (M, N))
        
    coalitions = [[i] for i in 1:M]

    allcoalitions = []

    for t in 2:T
        pay = computepayoffs(evolution[:, :, t - 1])
        next = evolvegroups(evolution[:, :, t - 1], pay, coalitions)

        if length(nonempty(coalitions)) > 1 && rand() < swapgroup
            coalitions = evolvegame(coalitions, pay)
            push!(allcoalitions, (t, nonempty(coalitions)))
        end

        evolution[:, :, t] = next
    end

    return evolution, allcoalitions

end



# localstability([5, 20], 100; iter=20)
# globaldynamics([3, 10], [5, 20], 100)

Ms, Ns = range(3, 103, step=1), range(3, 103, step=1)

convergence = globalstability(Ms, Ns; iter=150, swapgroup=0.01, filename="convergence_low")

convergence = globalstability(Ms, Ns; iter=150, swapgroup=.1, filename="convergence_high")