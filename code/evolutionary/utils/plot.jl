using Plots

function plotpayoffs(evolutions, computepayoffs, title; filename="payoff_heat")
    M, N, T = size(evolutions)
    pay = zeros(Float64, M, T)

    for t in 1:T
        pay[:, t] = mean(computepayoffs(evolutions[:, :, t]), dims=2)
    end

    groups = ["G$m" for m in 1:M]

    heatmap(1:T, groups, pay, title=title, xaxis="time", dpi=200, c=:thermal)

    savefig("plots/group/$filename.png")
    
end

function plotquantities(evolutions, coalitions, title; filename="q_heat")
    M, N, T = size(evolutions)
    qs = reshape(mean(evolutions, dims=2), (M, T))

    plot(title=title, xaxis="time", dpi=200)

    for m in 1:M
        plot!(1:T, qs[m, :], label="G$m")
    end
    
    allcoals = unique(x -> x[2], coalitions)

    for (t, coal) in allcoals

        vline!([t], c="red", alpha=0.3)
        txt = join(["{$(join(s, ", "))}" for s in coal], ", ")

        if length(allcoals) < 3
            annotate!(t + 2, minimum(qs),  text(txt, :red, 4))
        end

    end


    savefig("plots/group/$filename.png")

end

function plotgroupquantities(group, title; filename="q_group_heat")
    N, T = size(group)
    
    ts = ["T$t" for t in 1:T]
    firms = ["F$m" for m in 1:N]

    heatmap(1:T, firms, group, title=title, xaxis="time", dpi=200, c=:plasma)

    savefig("plots/local/$filename.png")
end

function plotgroupprices(groups, p, title; filename="p_group")
    N, T, I = size(groups)
    
    prices = zeros(Float64, I, T)

    plot(
        title=title, xaxis="t", yaxis="p(Q)", c="gray", alpha=0.5
    )

    for i in 1:I
        price = [p(sum(Q), N) for Q in eachcol(groups[:, :, i])]
        plot!(1:T, price, c="gray", alpha=0.5, label=false)
        prices[i, :] = price
    end

    plot!(1:T, mean(prices, dims=1)', c="red", label="mean(p(Q))")

    savefig("plots/local/$filename.png")
end