c = [2., 4., 7.]
e = [1., 0., 2.]

R = makeriver(c, e)
myers = graphtoMyerson(R)

# Part a
for S in powerset(R.N)
    value = R.v(S)
    print("v($S) = $(value)\n")
end

# Part b

mᵘ, mˡ, fᵉ = marginalvector(R)

print("
μ = $(collect(Float64, μ(R)))
mᵘ = $mᵘ, 
mˡ = $mˡ,
fᵉ = $fᵉ
")