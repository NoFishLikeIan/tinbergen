N = collect(1:9)
L = [(i, i + 1) for i in N[1:end - 1]]

v(n::Int) = 0
v(r::UnitRange{Int64}) = v(collect(r))
function v(S::Array{Int})
    if isempty(S) || !isconnected(S) return 0 end
    return length(S) ≥ length(N) * 2 / 3 ? 1 : 0
end

E = Graph(N, v, L)

# Part a

mᵘ, mˡ, fᵉ = marginalvector(E)

print("
mᵘ = $mᵘ, 
mˡ = $mˡ,
fᵉ = $fᵉ
")

# Part b

M = graphtoMyerson(E)