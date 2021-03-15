
M = 40
N = 5
ρs = [0.01, 0.1, 0.5]
iter = 30
Ts = 100

sim = zeros((length(ρs), Ts, iter))

for (j, ρ) in enumerate(ρs)
    for t in 1:Ts
        print("$t / $Ts\r")
        for i in 1:iter
            
            _, coalitions = evolve(M, N, T=t; swapgroup=ρ)

            if isempty(coalitions)
                coalsize = N
            else
                coalsize = mean(map(coal -> length(coal) * N, coalitions[end][2]))
            end

            sim[j, t, i] = coalsize
        end
    end
    print("\n")
end

average = reshape(mean(sim, dims=3), (length(ρs), Ts))