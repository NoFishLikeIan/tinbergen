include("shapley.jl")

one, two, three = [1], [2], [3] # Players
N = one ∪ two ∪ three

# Payoff function
function v(S::Array{Int})
    S = sort(S)
    if S == N 4
    elseif S == one 1
    elseif S == two 2
    elseif S == three 0
    elseif S == one ∪ two 3
    elseif S == one ∪ three 3
    elseif S == two ∪ three 2
    elseif isempty(S) 0
    end
end
v(S::Int) = v([S])

G = Game(N, v)

# Part a

for S in powerset(N, 1)
    dividend = Δ(G, S)
    print("Δ($S) = $(dividend)\n")
end

# Part b

shapey_div = (i -> fₛⁱ(G, i)).(G.N)
shapey = fₛ(G)

print("Shapey value, $(shapey)\n")

# Part c