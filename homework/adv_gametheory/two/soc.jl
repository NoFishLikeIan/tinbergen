H = Set([1, 2])
M = Set([1, 2, 3])

E = Set(M ∪ E for E in P(H))
F = P(H) ∪ P(M) ∪ E
∅ = Set{Int64}()

function unionstable(F)
    for A ∈ F
        for B ∈ F
            if A ∪ B ∉ F && A ∩ B != ∅
                return A, B
            end
        end
    end

    return true
end

setminus(A, i) = filter(j -> i != j, A)

function twoacc(F)
    for A ∈ filter(E -> length(E) > 2, F)
        combs = collect(combinations(collect(A), 2))

        acc = findfirst(
            t -> setminus(A, t[1]) ∈ F && setminus(A, t[2]) ∈ F, combs)
        
        if isnothing(acc) return A end

    end

    return true
end

function vandenBrink(F)
    if !(∅ ∈ F) throw("No empty set") end

    res = unionstable(F)
    if res != true
        throw("Not union stable for $A and $B")
    end

    res = twoacc(F)
    if res != true
        throw("Not 2-accessible via $A")
    end
end
