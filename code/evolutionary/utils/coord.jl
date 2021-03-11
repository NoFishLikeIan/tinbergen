function coordloop(i, N, c)
    base = minimum(c)
    l = cld(i, N) - 1 + base
    r = i % N == 0 ? N : i % N

    return l, r
end

function nonempty(coals)
    return [c for c in coals if !isempty(c)]
end