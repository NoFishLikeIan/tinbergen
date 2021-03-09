function X(xs::AbstractMatrix{Int64}...)::AbstractArray{Int64,3}
    k = length(xs)
    i, j = size(xs[1])

    A = zeros(Int64, k, i, j)

    for x in 1:k A[x,:,:] = xs[x] end
    return A
end