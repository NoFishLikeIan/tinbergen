function plotpayoffs(evolutions, computepayoffs, title; filename="payoff_heat")
    M, N, T = size(evolutions)
    pay = zeros(Float64, M, T)

    for t in 1:T
        pay[:, t] = mean(computepayoffs(evolutions[:, :, t]), dims=2)
    end

    groups = ["G$m" for m in 1:M]

    limit = maximum(abs.(pay))

    heatmap(
        1:T, groups, pay, 
        clim=(-limit, limit),
        title=title, xaxis="time", dpi=200)

    savefig("plots/group/$filename.png")
    
end

function plotquantities(evolutions, coalitions, title; filename="q_heat")
    M, N, T = size(evolutions)

    uniquecoals = unique(x -> Set(x[2]), coalitions)
    windows = [
        ((1, uniquecoals[1][1]), [[m] for m in 1:M])
    ]

    for i in 1:(length(uniquecoals) - 1)
        l, coals = uniquecoals[i]
        r = uniquecoals[i + 1][1]

        push!(windows, ((l, r), coals))
    end

    push!(windows, ((uniquecoals[end][1], T), uniquecoals[end][2]))

    qs = reshape(mean(evolutions, dims=2), (M, T))

    plot(title=title, xaxis="time", dpi=200, yaxs="mean q within group")

    for (window, coal) in windows
        from, to = window

        for (i, c) in enumerate(coal)
            plot!(
                from:to, qs[c, from:to]', label=false,
                linewidth=2, 
                c=palette(:tab20)[((i * 2) % 20) + 1]
            )
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

    plot!(1:T, mean(prices, dims=1)', c="red", label="mean(p(Q))", dpi=200)

    savefig("plots/local/$filename.png")
end