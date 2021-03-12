
function localstability(Ns, T; iter=20)
    for N in Ns
        groups = zeros(Int64, N, T, iter)
            
        for i in 1:iter
            print("Iteration $i / $iter \r")
            evolutions, coalitions = evolve(1, N, T=T)
            group = evolutions[1, :, :]
            groups[:, :, i] = evolutions[1, :, :]

        end
        print("\n")

        plotgroupquantities(
            groups[:, :, end], 
            "Quantities with N=$N"; filename="q_group_heat_$N")
        
        plotgroupprices(
            groups, p, 
            "Prices with N=$N"; filename="p_group_$N")
        
    end
end

function globaldynamics(Ms, Ns, T)
    
    for M in Ms

        for N in Ns
            print("Global dynamics for M=$M and N=$N \n")
            evolutions, coalitions = evolve(M, N, T=T; swapgroup=0.1)
        
            plotpayoffs(
                evolutions, computepayoffs, "Mean π, M=$M, N=$N, ρ = 0.1"; filename="pi_group_$M-$N")

            plotquantities(
                evolutions, coalitions,  "Mean q, M=$M, N=$N, ρ = 0.1"; filename="q_group_$M-$N")
        end
    end

end

function globalstability(
    Ns; T=100, iter=20, M=20,
    ρs=range(0., 1., length=50),
    filename="convergence")

    X, Y = length(ρs), length(Ns)
    
    convergence = zeros(Float64, X, Y)
    tup = collect(product(ρs, Ns))

    for (i, j) in product(1:X, 1:Y)
        print("Tuple ($i, $j) / ($X, $Y) \r")

        ρ, N = tup[i, j]

        mnvar = 0.

        for i in iter
            history, _ = evolve(M, N, T=T; swapgroup=ρ)
            mnvar += mean(var(history[:, :, end], dims=2))
        end

        convergence[i, j] = mnvar

    end
    print("\n")

    heatmap(
        convergence, 
        title="Divergence of tacit collusion with M = $M", 
        xticks=false, yticks=false,
        xaxis="N", yaxis="ρ")

    savefig("plots/global/$filename.png")

    return convergence
end