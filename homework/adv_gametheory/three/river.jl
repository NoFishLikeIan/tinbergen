c = [2., 4., 7.]
e = [1., 0., 0.]

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

# Part d

h1 = hⁱ(R, 1)
h2 = hⁱ(R, 2)
h3 = hⁱ(R, 3)

print("
h1 = $h1, 
h2 = $h2,
h3 = $h3
")

hs = [h1, h2, h3]

# Part e

for S in powerset(R.N)
    value = R.v(S)
    hstring = join([trunc.(Int, h[S]) for h in hs], ", ")
    
    print("$(S) -> $(hstring) ≥ $(value)\n")
end