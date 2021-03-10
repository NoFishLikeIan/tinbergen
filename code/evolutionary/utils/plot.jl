using Plots

function plotpayoffs(evolutions, computepayoffs)
    M, N, T = size(evolutions)
    pay = zeros(Float64, M, T)

    for t in 1:T
        pay[:, t] = mean(computepayoffs(evolutions[:, :, t]), dims=2)
    end

    ts = ["T$t" for t in 1:T]
    groups = ["G$m" for m in 1:M]
    heatmap(ts, groups, pay, title="Average payoffs")

    savefig("plots/payoff_heat.png")
    
end

function plotquantities(evolutions)
    M, N, T = size(evolutions)
    qs = reshape(mean(evolutions, dims=2), (M, T))

    ts = ["T$t" for t in 1:T]
    groups = ["G$m" for m in 1:M]

    heatmap(ts, groups, qs, title="Average quantities")

    savefig("plots/q_heat.png")

end

function plotgroupquantities(group)
    N, T = size(group)
    
    ts = ["T$t" for t in 1:T]
    firms = ["F$m" for m in 1:N]

    heatmap(ts, firms, group, title="Average quantities")

    savefig("plots/q_group_heat.png")
end