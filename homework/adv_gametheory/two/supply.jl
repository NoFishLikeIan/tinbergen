supplyN = collect(1:6)
supplyL = [(1, 2), (1, 3), (2, 4), (3, 5), (4, 5), (5, 6)]

supplyv(n::Array{Any,1}) = isempty(n) ? 0 : supplyv(S)
supplyv(n::Int) = supplyv([n])
supplyv(S::Array{Int}) = (1 ∈ S && 6 ∈ S) ? 1 : 0

supply = Graph(supplyN, supplyv, supplyL)

myers = graphtoMyerson(supply)

# Part a

for S in powerset(supplyN)
    value = myers.v(S)
    if value != 0 print("v($S) = $(value)\n") end
end

# Part b

μ_s = μ(supply)
print("μ = ", μ_s, "\n")

supplyL′ = filter(!=((1, 2)), supplyL)

brokensupply = Graph(supplyN, supplyv, supplyL′)
μ_b = μ(brokensupply)
print("μ′ = ", μ_b, "\n")
 
print(
    "Is fair? $(μ_s[1]) - $(μ_b[1]) = $(μ_s[2]) - $(μ_b[2]) -> ",
    μ_s[1] - μ_b[1] == μ_s[2] - μ_b[2], "\n")


linkgame = graphtolink(brokensupply)
positionvalue = πˡ(brokensupply)

for S in powerset(linkgame.N)
    value = linkgame.v(S)
    if value != 0 print("v($S) = $(value)\n") end
end