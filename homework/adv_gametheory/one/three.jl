one, two, three = [1], [2], [3] # Players
N = one ∪ two ∪ three

E = 20
dᵢ = [10, 15, 5]

function d(K::Array{Int})
    ∑(dᵢ[i] for i in K)
end

function v(S::Array{Int})
    if isempty(S) return 0 end
    S = sort(S)
    K = filter(i -> i ∉ S, N)

    return maximum((0, E - d(K)))
end

v(S::Int) = v([S])

G = Game(N, v)

# part a

for S in powerset(N)
    print("v($S) = $(v(S))\n")
end

# part b
print("Shapley value $(fₛ(G))")
