N = collect(1:6)
L = [(1, 2), (1, 3), (2, 4), (3, 5), (4, 5), (5, 6)]

v(n::Int) = v([n])
v(S::Array{Int}) = (1 ∈ S && 6 ∈ S) ? 1 : 0

supply = Graph(N, v, L)

myers = graphtoMyerson(supply)

# Part a

for S in powerset(N)
    value = myers.v(S)
    if value > 0 print("v($S) = $(value)\n") end
end

# Part b

μ_s = μ(supply)
print("μ = ", μ_s)

L′ = filter(!=((1, 2)), L)

brokensupply = Graph(N, v, L′)
μ_b = μ(brokensupply)
print("μ′ = ", μ_b)
 
print(
    "Is fair? $(μ_s[1]) - $(μ_b[1]) = $(μ_s[2]) - $(μ_b[2]) -> ",
    μ_s[1] - μ_b[1] == μ_s[2] - μ_b[2])